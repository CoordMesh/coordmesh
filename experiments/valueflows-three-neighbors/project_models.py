#!/usr/bin/env python3
"""Non-normative field projection for the pinned ValueFlows model experiment."""

import json
import re
from datetime import datetime
from pathlib import Path

BASE = "https://example.invalid/three-neighbors/"
VF = "https://w3id.org/valueflows/ont/vf#"
FIXTURE = Path(__file__).with_name("fixture.jsonld")


def check(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    nodes = doc["@graph"]
    by_id = {node["@id"]: node for node in nodes}
    check(len(by_id) == len(nodes), "fixture IDs must be unique")
    for node in nodes:
        for field in ("provider", "receiver", "resourceInventoriedAs", "satisfies"):
            if field in node:
                check(node[field] in by_id, f"unresolved {field} reference in {node['@id']}")
        for ref in node.get("fulfills", []):
            check(ref in by_id, f"unresolved fulfills reference in {node['@id']}")
        for field in ("hasBeginning", "hasEnd", "hasPointInTime"):
            if field in node:
                datetime.fromisoformat(node[field].replace("Z", "+00:00"))

    intent = by_id[BASE + "use-intent"]
    commitment = by_id[BASE + "use-commitment"]
    use_event = by_id[BASE + "use-event"]
    check(intent["action"] == VF + "use", "intent action must be VF use")
    check(commitment["satisfies"] == intent["@id"], "commitment must satisfy intent")
    check(commitment["hasBeginning"] == intent["hasBeginning"] and commitment["hasEnd"] == intent["hasEnd"], "commitment interval must match intent")
    check(use_event["fulfills"] == [commitment["@id"]], "use event must fulfill commitment")

    # These labels stand in for implementation-generated local IDs. They are
    # deliberately not valid hREA ActionHashes or Bonfire ULIDs.
    ids = {name: f"{name}" for name in ("alice", "bob", "drill", "use-intent", "use-commitment", "use-event", "handover-event", "return-event")}
    def local(ref):
        return ids[ref.removeprefix(BASE)]
    def time_fields(node):
        return {key: node[key] for key in ("hasBeginning", "hasEnd", "hasPointInTime") if key in node}
    def bonfire_time_fields(node):
        return {re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", key).lower(): node[key] for key in ("hasBeginning", "hasEnd", "hasPointInTime") if key in node}
    def common(node):
        return {
            "action": node["action"].removeprefix(VF),
            "provider": local(node["provider"]),
            "receiver": local(node["receiver"]),
            "resource": local(node["resourceInventoriedAs"]),
            **time_fields(node),
        }

    hrea = {
        "resource": {"id": ids["drill"], "trackingIdentifier": by_id[BASE + "drill"]["trackingIdentifier"], "primaryAccountable": ids["alice"]},
        "intent": {"id": ids["use-intent"], **common(intent)},
        "commitment": {"id": ids["use-commitment"], **common(commitment), "satisfies": ids["use-intent"]},
        "economicEvents": [
            {"id": ids[node["@id"].removeprefix(BASE)], **common(node), **({"fulfills": [ids["use-commitment"]]} if "fulfills" in node else {})}
            for node in nodes if node.get("@type") == "EconomicEvent"
        ],
    }
    bonfire = {
        "resource": {"id": ids["drill"], "tracking_identifier": by_id[BASE + "drill"]["trackingIdentifier"], "primary_accountable_id": ids["alice"]},
        "intent": {"id": ids["use-intent"], "action_id": "use", "provider_id": ids["alice"], "receiver_id": ids["bob"], "resource_inventoried_as_id": ids["drill"], **bonfire_time_fields(intent)},
        "commitment": {"id": ids["use-commitment"], "action_id": "use", "provider_id": ids["alice"], "receiver_id": ids["bob"], "resource_inventoried_as_id": ids["drill"], **bonfire_time_fields(commitment)},
        "satisfaction_relation": {"satisfies_id": ids["use-intent"], "satisfied_by_id": ids["use-commitment"]},
        "economic_events": [
            {"id": ids[node["@id"].removeprefix(BASE)], "action_id": node["action"].removeprefix(VF), "provider_id": local(node["provider"]), "receiver_id": local(node["receiver"]), "resource_inventoried_as_id": local(node["resourceInventoriedAs"]), **bonfire_time_fields(node)}
            for node in nodes if node.get("@type") == "EconomicEvent"
        ],
        "unsupported_event_commitment_link": "Bonfire EconomicEvent model has no fulfills field in the pinned source model",
    }
    print(json.dumps({"validation": "PASS", "hrea_model_projection": hrea, "bonfire_model_projection": bonfire}, indent=2))


if __name__ == "__main__":
    main()
