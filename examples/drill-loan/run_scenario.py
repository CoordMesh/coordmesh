"""Run the two independent applications and compare their conformance reports."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "drill-loan"
ALICE_PROJECT = EXAMPLE / "alice" / "Alice.csproj"
BOB_APP = EXAMPLE / "bob" / "bob.py"
EXPECTED = ROOT / "tests" / "conformance" / "drill-loan" / "expected-state.json"


def run(command, description):
    print(f"\n== {description} ==", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def execute(temp_path):
    artifacts = {"DOTNET_NOLOGO": "1", "DOTNET_CLI_TELEMETRY_OPTOUT": "1"}
    exchange = temp_path / "mailbox"
    exchange.mkdir()
    build_dir = temp_path / "dotnet-artifacts"
    run(["dotnet", "build", str(ALICE_PROJECT), "--artifacts-path", str(build_dir), "--nologo", "--verbosity", "quiet"], "Build independent Alice C# application")
    alice_dll = next(path for path in build_dir.rglob("Alice.dll") if "bin" in path.parts)

    def alice(action):
        env = os.environ.copy()
        env.update(artifacts)
        print(f"\n== Alice: {action} ==", flush=True)
        subprocess.run(["dotnet", str(alice_dll), action, str(exchange)], cwd=ROOT, check=True, env=env)

    def bob(action):
        run([sys.executable, str(BOB_APP), action, str(exchange)], f"Bob: {action}")

    alice("publish")
    bob("request")
    alice("accept")
    bob("observe-and-return")
    alice("finalize")
    bob("finalize")

    alice_state = json.loads((exchange / "alice-state.json").read_text(encoding="utf-8"))
    bob_state = json.loads((exchange / "bob-state.json").read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    if alice_state != bob_state:
        raise SystemExit("FAIL: Alice and Bob derived different final states")
    if alice_state != expected:
        raise SystemExit("FAIL: both applications agreed, but the result differs from the conformance vector")
    documents = sorted(p.name for p in exchange.glob("*.jsonld"))
    if documents != ["01-offer.jsonld", "02-request.jsonld", "03-acceptance.jsonld", "04-handover.jsonld", "05-return.jsonld"]:
        raise SystemExit(f"FAIL: unexpected exchanged artifacts: {documents}")
    print("\nPASS: independent C# and Python applications derived the same expected final state.")
    print(f"Inspectable ValueFlows JSON-LD artifacts: {len(documents)}")


def main():
    keep = sys.argv[1:] == ["--keep"]
    if sys.argv[1:] not in ([], ["--keep"]):
        raise SystemExit("Usage: python run_scenario.py [--keep]")
    if keep:
        directory = Path(tempfile.mkdtemp(prefix="coordmesh-drill-loan-"))
        execute(directory)
        print(f"\nArtifacts retained at: {directory / 'mailbox'}")
    else:
        with tempfile.TemporaryDirectory(prefix="coordmesh-drill-loan-") as temp:
            execute(Path(temp))


if __name__ == "__main__":
    main()
