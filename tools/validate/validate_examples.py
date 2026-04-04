#!/usr/bin/env python3
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except Exception:
    print("[FAIL] Missing dependency: jsonschema")
    print("       Install with: python3 -m pip install -r requirements-dev.txt")
    raise

try:
    from rdflib import Graph
except Exception:
    print("[FAIL] Missing dependency: rdflib")
    print("       Install with: python3 -m pip install -r requirements-dev.txt")
    raise

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIRS = [ROOT / "contracts" / "schemas", ROOT / "contracts" / "envelope"]
EXAMPLE_ROOT = ROOT / "examples"
ONTOLOGY_ROOT = ROOT / "ontology"

failures = 0

def ok(msg: str) -> None:
    print(f"[OK] {msg}")

def fail(msg: str) -> None:
    global failures
    failures += 1
    print(f"[FAIL] {msg}")

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def find_schema_for_example(example_path: Path):
    base = example_path.name.replace(".example.json", "")
    matches = []
    for schema_dir in SCHEMA_DIRS:
        if schema_dir.exists():
            matches.extend(sorted(schema_dir.glob(f"{base}.v*.json")))

    if len(matches) == 1:
        return matches[0]

    rel = example_path.relative_to(ROOT)
    if len(matches) == 0:
        fail(f"No schema found for example: {rel}")
    else:
        fail(
            f"Multiple candidate schemas for {rel}: "
            + ", ".join(str(m.relative_to(ROOT)) for m in matches)
        )
    return None

def main() -> int:
    contract_json = sorted(
        {p for schema_dir in SCHEMA_DIRS if schema_dir.exists() for p in schema_dir.rglob("*.json")}
    )
    example_json = sorted(EXAMPLE_ROOT.rglob("*.example.json")) if EXAMPLE_ROOT.exists() else []
    ttl_files = sorted(ONTOLOGY_ROOT.rglob("*.ttl")) if ONTOLOGY_ROOT.exists() else []

    parsed_schemas = {}
    for path in contract_json:
        try:
            schema = load_json(path)
            Draft202012Validator.check_schema(schema)
            parsed_schemas[path] = schema
        except Exception as e:
            fail(f"Schema check failed: {path.relative_to(ROOT)} :: {e}")

    if failures == 0:
        ok(f"Checked {len(parsed_schemas)} contract/envelope schema files")

    parsed_examples = {}
    for path in example_json:
        try:
            parsed_examples[path] = load_json(path)
        except Exception as e:
            fail(f"Example JSON parse failed: {path.relative_to(ROOT)} :: {e}")

    if failures == 0:
        ok(f"Parsed {len(parsed_examples)} example JSON files")

    for example_path, instance in parsed_examples.items():
        schema_path = find_schema_for_example(example_path)
        if schema_path is None:
            continue

        schema = parsed_schemas.get(schema_path)
        if schema is None:
            fail(f"Schema unavailable for validation: {schema_path.relative_to(ROOT)}")
            continue

        try:
            validator = Draft202012Validator(schema, format_checker=FormatChecker())
            validator.validate(instance)
            ok(
                f"Validated {example_path.relative_to(ROOT)} "
                f"against {schema_path.relative_to(ROOT)}"
            )
        except Exception as e:
            fail(
                f"Validation failed: {example_path.relative_to(ROOT)} "
                f"against {schema_path.relative_to(ROOT)} :: {e}"
            )

    for path in ttl_files:
        try:
            g = Graph()
            g.parse(path, format="turtle")
            ok(f"Parsed Turtle: {path.relative_to(ROOT)} ({len(g)} triples)")
        except Exception as e:
            fail(f"Turtle parse failed: {path.relative_to(ROOT)} :: {e}")

    if failures:
        print(f"[SUMMARY] validation finished with {failures} failure(s)")
        return 1

    print("[SUMMARY] all validation checks passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
