"""Independent Python participant for the non-normative drill-loan example."""

import json
import sys
from datetime import datetime
from pathlib import Path

VF = "https://w3id.org/valueflows/ont/vf#"
ROOT = "https://example.org/coordmesh/drill-loan/"
ALICE = ROOT + "participant/alice"
BOB = ROOT + "participant/bob"
DRILL = ROOT + "resource/drill-x"
OFFER = ROOT + "intent/offer-1"
REQUEST = ROOT + "intent/request-1"
AGREEMENT = ROOT + "agreement/loan-1"
COMMITMENT = ROOT + "commitment/use-1"
HANDOVER = ROOT + "event/handover-1"
RETURN = ROOT + "event/return-1"
START = "2026-10-10T14:00:00Z"
END = "2026-10-10T16:00:00Z"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_node(directory, filename, identifier, expected_type):
    document = json.loads((directory / filename).read_text(encoding="utf-8"))
    context = document.get("@context", {})
    require(context.get("vf") == VF, f"{filename} has an unexpected ValueFlows context")
    require(context.get("xsd") == "http://www.w3.org/2001/XMLSchema#", f"{filename} has an unexpected XML Schema context")
    for term in ("action", "provider", "receiver", "resourceInventoriedAs", "primaryAccountable", "satisfies", "clauseOf"):
        require(context.get(term) == {"@id": "vf:" + term, "@type": "@id"}, f"{filename} has an unexpected mapping for {term}")
    require(context.get("trackingIdentifier") == "vf:trackingIdentifier", f"{filename} has an unexpected trackingIdentifier mapping")
    for term in ("hasBeginning", "hasEnd", "hasPointInTime"):
        require(context.get(term) == {"@id": "vf:" + term, "@type": "xsd:dateTime"}, f"{filename} has an unexpected mapping for {term}")
    graph = document.get("@graph")
    require(isinstance(graph, list), f"{filename} has no @graph")
    node = next((item for item in graph if item.get("@id") == identifier), None)
    require(node is not None, f"{filename} does not contain {identifier}")
    require(node.get("@type") == VF + expected_type, f"{identifier} is not ValueFlows {expected_type}")
    return node


def reference(node, key):
    value = node.get(key)
    require(isinstance(value, dict) and isinstance(value.get("@id"), str), f"missing reference {key}")
    return value["@id"]


def write_graph(directory, filename, *nodes):
    document = {
        "@context": {
            "vf": VF,
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "action": {"@id": "vf:action", "@type": "@id"},
            "provider": {"@id": "vf:provider", "@type": "@id"},
            "receiver": {"@id": "vf:receiver", "@type": "@id"},
            "resourceInventoriedAs": {"@id": "vf:resourceInventoriedAs", "@type": "@id"},
            "primaryAccountable": {"@id": "vf:primaryAccountable", "@type": "@id"},
            "trackingIdentifier": "vf:trackingIdentifier",
            "satisfies": {"@id": "vf:satisfies", "@type": "@id"},
            "clauseOf": {"@id": "vf:clauseOf", "@type": "@id"},
            "hasBeginning": {"@id": "vf:hasBeginning", "@type": "xsd:dateTime"},
            "hasEnd": {"@id": "vf:hasEnd", "@type": "xsd:dateTime"},
            "hasPointInTime": {"@id": "vf:hasPointInTime", "@type": "xsd:dateTime"},
        },
        "@graph": list(nodes),
    }
    (directory / filename).write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def make_node(identifier, kind, **fields):
    node = {"@id": identifier, "@type": VF + kind}
    node.update(fields)
    return node


def request(directory):
    offer = read_node(directory, "01-offer.jsonld", OFFER, "Intent")
    read_node(directory, "01-offer.jsonld", ALICE, "Agent")
    read_node(directory, "01-offer.jsonld", BOB, "Agent")
    resource = read_node(directory, "01-offer.jsonld", DRILL, "EconomicResource")
    require(reference(offer, "action") == VF + "use", "offer does not describe ValueFlows use")
    require(reference(offer, "provider") == ALICE, "offer provider mismatch")
    require(reference(offer, "resourceInventoriedAs") == DRILL, "offer resource mismatch")
    require(resource.get("trackingIdentifier") == DRILL and reference(resource, "primaryAccountable") == ALICE, "drill identity/accountability mismatch")
    require(offer.get("hasBeginning") == START and offer.get("hasEnd") == END, "offer time window mismatch")
    write_graph(directory, "02-request.jsonld", make_node(
        REQUEST, "Intent",
        action={"@id": VF + "use"},
        provider={"@id": ALICE},
        receiver={"@id": BOB},
        resourceInventoriedAs={"@id": DRILL},
        hasBeginning=START,
        hasEnd=END,
    ))
    print("Bob discovered Alice's offer and requested the 14:00-16:00 use window.")


def observe_and_return(directory):
    agreement = read_node(directory, "03-acceptance.jsonld", AGREEMENT, "Agreement")
    commitment = read_node(directory, "03-acceptance.jsonld", COMMITMENT, "Commitment")
    request_node = read_node(directory, "02-request.jsonld", REQUEST, "Intent")
    require(reference(commitment, "clauseOf") == agreement["@id"], "commitment is not a clause of the agreement")
    require(reference(commitment, "satisfies") == request_node["@id"], "commitment does not satisfy Bob's request")
    require(reference(commitment, "action") == VF + "use", "commitment action mismatch")
    require(reference(commitment, "provider") == ALICE and reference(commitment, "receiver") == BOB, "commitment participants mismatch")
    require(reference(commitment, "resourceInventoriedAs") == DRILL, "commitment resource mismatch")
    require(commitment.get("hasBeginning") == START and commitment.get("hasEnd") == END, "accepted time window mismatch")
    handover = read_node(directory, "04-handover.jsonld", HANDOVER, "EconomicEvent")
    check_transfer(handover, HANDOVER, ALICE, BOB, "2026-10-10T14:00:00Z")
    write_graph(directory, "05-return.jsonld", make_node(
        RETURN, "EconomicEvent",
        action={"@id": VF + "transfer-custody"},
        provider={"@id": BOB},
        receiver={"@id": ALICE},
        resourceInventoriedAs={"@id": DRILL},
        hasPointInTime="2026-10-10T16:00:00Z",
    ))
    print("Bob interpreted Alice's acceptance and recorded the return.")


def check_transfer(event, identifier, provider, receiver, instant):
    require(event["@id"] == identifier, "custody event identity mismatch")
    require(reference(event, "action") == VF + "transfer-custody", "custody event action mismatch")
    require(reference(event, "provider") == provider and reference(event, "receiver") == receiver, "custody event participant mismatch")
    require(reference(event, "resourceInventoriedAs") == DRILL, "custody event resource mismatch")
    require(event.get("hasPointInTime") == instant, "custody event time mismatch")


def finalize(directory):
    offer = read_node(directory, "01-offer.jsonld", OFFER, "Intent")
    read_node(directory, "01-offer.jsonld", ALICE, "Agent")
    read_node(directory, "01-offer.jsonld", BOB, "Agent")
    resource = read_node(directory, "01-offer.jsonld", DRILL, "EconomicResource")
    request_node = read_node(directory, "02-request.jsonld", REQUEST, "Intent")
    agreement = read_node(directory, "03-acceptance.jsonld", AGREEMENT, "Agreement")
    commitment = read_node(directory, "03-acceptance.jsonld", COMMITMENT, "Commitment")
    handover = read_node(directory, "04-handover.jsonld", HANDOVER, "EconomicEvent")
    returned = read_node(directory, "05-return.jsonld", RETURN, "EconomicEvent")
    require(reference(offer, "action") == VF + "use" and reference(request_node, "action") == VF + "use", "offer/request action mismatch")
    require(reference(offer, "resourceInventoriedAs") == DRILL and reference(request_node, "resourceInventoriedAs") == DRILL, "offer/request resource mismatch")
    require(resource.get("trackingIdentifier") == DRILL and reference(resource, "primaryAccountable") == ALICE, "drill identity/accountability mismatch")
    require(reference(request_node, "provider") == ALICE and reference(request_node, "receiver") == BOB, "request participants mismatch")
    require(reference(commitment, "clauseOf") == agreement["@id"] and reference(commitment, "satisfies") == request_node["@id"], "commitment relationships mismatch")
    events = sorted((handover, returned), key=lambda e: datetime.fromisoformat(e["hasPointInTime"].replace("Z", "+00:00")))
    check_transfer(events[0], HANDOVER, ALICE, BOB, "2026-10-10T14:00:00Z")
    check_transfer(events[1], RETURN, BOB, ALICE, "2026-10-10T16:00:00Z")
    state = {
        "provider": ALICE,
        "receiver": BOB,
        "resource": DRILL,
        "action": VF + "use",
        "interval": {"start": START, "end": END},
        "agreement": AGREEMENT,
        "commitment": COMMITMENT,
        "commitmentSatisfies": REQUEST,
        "commitmentClauseOf": AGREEMENT,
        "custodyEvents": [
            {"id": event["@id"], "action": reference(event, "action"), "provider": reference(event, "provider"),
             "receiver": reference(event, "receiver"), "resource": reference(event, "resourceInventoriedAs"),
             "at": event["hasPointInTime"]}
            for event in events
        ],
        "finalCustodian": reference(events[-1], "receiver"),
        "result": "returned",
    }
    (directory / "bob-state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print("Bob independently interpreted the drill as returned to Alice.")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: bob.py <request|observe-and-return|finalize> <exchange-directory>")
    operation, folder = sys.argv[1], Path(sys.argv[2]).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    if operation == "request":
        request(folder)
    elif operation == "observe-and-return":
        observe_and_return(folder)
    elif operation == "finalize":
        finalize(folder)
    else:
        raise SystemExit(f"Unknown Bob operation: {operation}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # Report an explicit failing experiment to the harness.
        print(f"Bob failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
