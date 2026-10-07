using System.Globalization;
using System.Text.Json;
using System.Text.Json.Nodes;

internal static class Program
{
    private const string Vf = "https://w3id.org/valueflows/ont/vf#";
    private const string Root = "https://example.org/coordmesh/drill-loan/";
    private const string Alice = Root + "participant/alice";
    private const string Bob = Root + "participant/bob";
    private const string Drill = Root + "resource/drill-x";
    private const string Offer = Root + "intent/offer-1";
    private const string Request = Root + "intent/request-1";
    private const string Agreement = Root + "agreement/loan-1";
    private const string Commitment = Root + "commitment/use-1";
    private const string Handover = Root + "event/handover-1";
    private const string Return = Root + "event/return-1";
    private const string Start = "2026-10-10T14:00:00Z";
    private const string End = "2026-10-10T16:00:00Z";
    private static readonly JsonSerializerOptions JsonOptions = new() { WriteIndented = true };

    private static int Main(string[] args)
    {
        try
        {
            if (args.Length != 2) throw new ArgumentException("Usage: Alice <publish|accept|finalize> <exchange-directory>");
            var exchange = Path.GetFullPath(args[1]);
            Directory.CreateDirectory(exchange);
            switch (args[0])
            {
                case "publish": Publish(exchange); break;
                case "accept": AcceptAndHandOver(exchange); break;
                case "finalize": FinalizeState(exchange); break;
                default: throw new ArgumentException($"Unknown Alice operation: {args[0]}");
            }
            return 0;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Alice failed: {ex.Message}");
            return 1;
        }
    }

    private static void Publish(string exchange)
    {
        WriteGraph(exchange, "01-offer.jsonld",
            Node(Alice, "Agent"),
            Node(Bob, "Agent"),
            Node(Drill, "EconomicResource",
                ("trackingIdentifier", Root + "resource/drill-x"),
                ("primaryAccountable", Ref(Alice))),
            Node(Offer, "Intent",
                ("action", Ref(Vf + "use")),
                ("provider", Ref(Alice)),
                ("resourceInventoriedAs", Ref(Drill)),
                ("hasBeginning", Start),
                ("hasEnd", End)));
    }

    private static void AcceptAndHandOver(string exchange)
    {
        var offer = ReadNode(exchange, "01-offer.jsonld", Offer, "Intent");
        ReadNode(exchange, "01-offer.jsonld", Alice, "Agent");
        ReadNode(exchange, "01-offer.jsonld", Bob, "Agent");
        var resource = ReadNode(exchange, "01-offer.jsonld", Drill, "EconomicResource");
        var request = ReadNode(exchange, "02-request.jsonld", Request, "Intent");
        Require(Id(offer["action"]) == Vf + "use", "offer action is not ValueFlows use");
        Require(Id(request["action"]) == Vf + "use", "request action is not ValueFlows use");
        Require(Id(offer["provider"]) == Alice && Id(request["provider"]) == Alice, "provider identity mismatch");
        Require(Id(request["receiver"]) == Bob, "request receiver mismatch");
        Require(Id(offer["resourceInventoriedAs"]) == Drill && Id(request["resourceInventoriedAs"]) == Drill, "resource mismatch");
        Require(Text(resource["trackingIdentifier"]) == Drill && Id(resource["primaryAccountable"]) == Alice, "drill identity/accountability mismatch");
        Require(Text(offer["hasBeginning"]) == Start && Text(offer["hasEnd"]) == End, "offer interval mismatch");
        Require(Text(request["hasBeginning"]) == Start && Text(request["hasEnd"]) == End, "request interval mismatch");

        WriteGraph(exchange, "03-acceptance.jsonld",
            Node(Agreement, "Agreement"),
            Node(Commitment, "Commitment",
                ("action", Ref(Vf + "use")),
                ("provider", Ref(Alice)),
                ("receiver", Ref(Bob)),
                ("resourceInventoriedAs", Ref(Drill)),
                ("hasBeginning", Start),
                ("hasEnd", End),
                ("satisfies", Ref(Request)),
                ("clauseOf", Ref(Agreement))));

        WriteGraph(exchange, "04-handover.jsonld", Node(Handover, "EconomicEvent",
            ("action", Ref(Vf + "transfer-custody")),
            ("provider", Ref(Alice)),
            ("receiver", Ref(Bob)),
            ("resourceInventoriedAs", Ref(Drill)),
            ("hasPointInTime", "2026-10-10T14:00:00Z")));
    }

    private static void FinalizeState(string exchange)
    {
        var offer = ReadNode(exchange, "01-offer.jsonld", Offer, "Intent");
        ReadNode(exchange, "01-offer.jsonld", Alice, "Agent");
        ReadNode(exchange, "01-offer.jsonld", Bob, "Agent");
        var resource = ReadNode(exchange, "01-offer.jsonld", Drill, "EconomicResource");
        var request = ReadNode(exchange, "02-request.jsonld", Request, "Intent");
        var agreement = ReadNode(exchange, "03-acceptance.jsonld", Agreement, "Agreement");
        var commitment = ReadNode(exchange, "03-acceptance.jsonld", Commitment, "Commitment");
        var handover = ReadNode(exchange, "04-handover.jsonld", Handover, "EconomicEvent");
        var returned = ReadNode(exchange, "05-return.jsonld", Return, "EconomicEvent");

        Require(Id(offer["action"]) == Vf + "use" && Id(request["action"]) == Vf + "use", "offer/request do not use ValueFlows use");
        Require(Id(offer["provider"]) == Alice && Id(request["provider"]) == Alice && Id(request["receiver"]) == Bob, "participant references mismatch");
        Require(Id(offer["resourceInventoriedAs"]) == Drill && Id(request["resourceInventoriedAs"]) == Drill, "offer/request resource mismatch");
        Require(Text(resource["trackingIdentifier"]) == Drill && Id(resource["primaryAccountable"]) == Alice, "drill identity/accountability mismatch");
        Require(Id(commitment["action"]) == Vf + "use" && Id(commitment["provider"]) == Alice && Id(commitment["receiver"]) == Bob, "commitment semantic mismatch");
        Require(Id(commitment["resourceInventoriedAs"]) == Drill, "commitment resource mismatch");
        Require(Text(commitment["hasBeginning"]) == Start && Text(commitment["hasEnd"]) == End, "commitment interval mismatch");
        Require(Id(commitment["satisfies"]) == Request && Id(commitment["clauseOf"]) == Agreement, "commitment relationship mismatch");

        var events = new[] { handover, returned }.OrderBy(e => DateTimeOffset.Parse(Text(e["hasPointInTime"]), CultureInfo.InvariantCulture)).ToArray();
        ValidateTransfer(events[0], Handover, Alice, Bob, "2026-10-10T14:00:00Z");
        ValidateTransfer(events[1], Return, Bob, Alice, "2026-10-10T16:00:00Z");
        var state = State(events);
        File.WriteAllText(Path.Combine(exchange, "alice-state.json"), JsonSerializer.Serialize(state, JsonOptions));
        Console.WriteLine("Alice interpreted the drill as returned to Alice.");
    }

    private static object State(JsonNode[] events) => new
    {
        provider = Alice,
        receiver = Bob,
        resource = Drill,
        action = Vf + "use",
        interval = new { start = Start, end = End },
        agreement = Agreement,
        commitment = Commitment,
        commitmentSatisfies = Request,
        commitmentClauseOf = Agreement,
        custodyEvents = events.Select(e => new
        {
            id = Text(e["@id"]),
            action = Id(e["action"]),
            provider = Id(e["provider"]),
            receiver = Id(e["receiver"]),
            resource = Id(e["resourceInventoriedAs"]),
            at = Text(e["hasPointInTime"])
        }).ToArray(),
        finalCustodian = Id(events[^1]["receiver"]),
        result = "returned"
    };

    private static void ValidateTransfer(JsonNode e, string id, string provider, string receiver, string at)
    {
        Require(Text(e["@id"]) == id, "custody event identity mismatch");
        Require(Id(e["action"]) == Vf + "transfer-custody", "custody event action mismatch");
        Require(Id(e["provider"]) == provider && Id(e["receiver"]) == receiver, "custody event participant mismatch");
        Require(Id(e["resourceInventoriedAs"]) == Drill, "custody event resource mismatch");
        Require(Text(e["hasPointInTime"]) == at, "custody event time mismatch");
    }

    private static JsonNode ReadNode(string dir, string file, string id, string type)
    {
        var document = JsonNode.Parse(File.ReadAllText(Path.Combine(dir, file)))!;
        ValidateContext(document["@context"]);
        var graph = document["@graph"]?.AsArray() ?? throw new InvalidDataException($"{file} has no @graph");
        var node = graph.FirstOrDefault(n => Text(n?["@id"]) == id)
            ?? throw new InvalidDataException($"{file} does not contain {id}");
        Require(Text(node["@type"]) == Vf + type, $"{id} is not ValueFlows {type}");
        return node;
    }

    private static void WriteGraph(string dir, string file, params JsonObject[] nodes)
    {
        var graph = new JsonObject
        {
            ["@context"] = new JsonObject
            {
                ["vf"] = "https://w3id.org/valueflows/ont/vf#",
                ["xsd"] = "http://www.w3.org/2001/XMLSchema#",
                ["action"] = new JsonObject { ["@id"] = "vf:action", ["@type"] = "@id" },
                ["provider"] = new JsonObject { ["@id"] = "vf:provider", ["@type"] = "@id" },
                ["receiver"] = new JsonObject { ["@id"] = "vf:receiver", ["@type"] = "@id" },
                ["resourceInventoriedAs"] = new JsonObject { ["@id"] = "vf:resourceInventoriedAs", ["@type"] = "@id" },
                ["primaryAccountable"] = new JsonObject { ["@id"] = "vf:primaryAccountable", ["@type"] = "@id" },
                ["trackingIdentifier"] = "vf:trackingIdentifier",
                ["satisfies"] = new JsonObject { ["@id"] = "vf:satisfies", ["@type"] = "@id" },
                ["clauseOf"] = new JsonObject { ["@id"] = "vf:clauseOf", ["@type"] = "@id" },
                ["hasBeginning"] = new JsonObject { ["@id"] = "vf:hasBeginning", ["@type"] = "xsd:dateTime" },
                ["hasEnd"] = new JsonObject { ["@id"] = "vf:hasEnd", ["@type"] = "xsd:dateTime" },
                ["hasPointInTime"] = new JsonObject { ["@id"] = "vf:hasPointInTime", ["@type"] = "xsd:dateTime" }
            },
            ["@graph"] = new JsonArray(nodes.Select(n => (JsonNode)n).ToArray())
        };
        File.WriteAllText(Path.Combine(dir, file), graph.ToJsonString(JsonOptions));
    }

    private static JsonObject Node(string id, string type, params (string Key, JsonNode? Value)[] fields)
    {
        var node = new JsonObject { ["@id"] = id, ["@type"] = Vf + type };
        foreach (var (key, value) in fields) node[key] = value?.DeepClone();
        return node;
    }

    private static JsonObject Ref(string id) => new() { ["@id"] = id };
    private static void ValidateContext(JsonNode? context)
    {
        Require(Text(context?["vf"]) == Vf, "document does not use the ValueFlows vocabulary prefix");
        Require(Text(context?["xsd"]) == "http://www.w3.org/2001/XMLSchema#", "document has an unexpected XML Schema prefix");
        foreach (var term in new[] { "action", "provider", "receiver", "resourceInventoriedAs", "primaryAccountable", "satisfies", "clauseOf" })
        {
            Require(Text(context?[term]?["@id"]) == "vf:" + term && Text(context?[term]?["@type"]) == "@id", $"unexpected JSON-LD mapping for {term}");
        }
        Require(Text(context?["trackingIdentifier"]) == "vf:trackingIdentifier", "unexpected JSON-LD mapping for trackingIdentifier");
        foreach (var term in new[] { "hasBeginning", "hasEnd", "hasPointInTime" })
        {
            Require(Text(context?[term]?["@id"]) == "vf:" + term && Text(context?[term]?["@type"]) == "xsd:dateTime", $"unexpected JSON-LD mapping for {term}");
        }
    }
    private static string Id(JsonNode? node) => Text(node?["@id"]);
    private static string Text(JsonNode? node) => node?.GetValue<string>() ?? throw new InvalidDataException("Expected a string value");
    private static void Require(bool condition, string message) { if (!condition) throw new InvalidDataException(message); }
}
