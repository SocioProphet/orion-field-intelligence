#!/usr/bin/env python3
"""Validate Orion facility-risk fixture chain.

Dependency-light structural validator for the OSIRIS excavation map MVP.
Does not import or run code from mdheller/osiris.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "fixtures" / "facility-risk"

REQUIRED_FILES = [
    "observation-events/fire-weather-alert.event.v0_1.json",
    "observation-events/facility-asset.event.v0_1.json",
    "observation-events/cve-exposure.event.v0_1.json",
    "observation-events/field-report.event.v0_1.json",
    "observation-events/fused-facility-risk.event.v0_1.json",
    "policy-envelopes/facility-risk-demo.policy.v0_1.json",
    "fusion-links/facility-risk-demo.fusion.v0_1.json",
    "decision-cards/facility-risk-demo.card.v0_1.json",
    "receipts/facility-risk-demo.receipt.v0_1.json",
]


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError:
        fail(f"missing fixture: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected top-level object in {path}")
    return value


def check_required(path: Path, doc: Dict[str, Any], required: Iterable[str]) -> None:
    missing = [field for field in required if field not in doc]
    if missing:
        fail(f"{path} missing required fields: {', '.join(missing)}")


def load_group(subdir: str, id_field: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    folder = FIXTURE_ROOT / subdir
    if not folder.exists():
        fail(f"missing fixture directory: {folder}")
    for path in sorted(folder.glob("*.json")):
        doc = load_json(path)
        check_required(path, doc, ["schema_version", id_field])
        if doc["schema_version"] != "0.1.0":
            fail(f"{path} has unsupported schema_version")
        key = doc[id_field]
        if key in out:
            fail(f"duplicate {id_field}: {key}")
        out[key] = doc
    return out


def assert_refs(path_label: str, refs: Iterable[str], table: Dict[str, Dict[str, Any]], kind: str) -> None:
    for ref in refs:
        if ref not in table:
            fail(f"{path_label} references missing {kind}: {ref}")


def main() -> int:
    for rel in REQUIRED_FILES:
        if not (FIXTURE_ROOT / rel).exists():
            fail(f"missing required fixture: {rel}")

    events = load_group("observation-events", "event_id")
    policies = load_group("policy-envelopes", "policy_envelope_id")
    fusions = load_group("fusion-links", "fusion_link_id")
    cards = load_group("decision-cards", "decision_card_id")
    receipts = load_group("receipts", "receipt_id")

    source_refs_seen = set()

    for event_id, event in events.items():
        check_required(
            Path(event_id),
            event,
            ["event_type", "observed_at", "location", "severity", "confidence", "source_record_refs", "evidence_grade", "policy_state"],
        )
        if not event["source_record_refs"]:
            fail(f"{event_id} must include at least one Gaia source_record_ref")
        source_refs_seen.update(event["source_record_refs"])
        if "related_event_refs" in event:
            assert_refs(event_id, event["related_event_refs"], events, "event")
        if "policy_envelope_ref" in event:
            assert_refs(event_id, [event["policy_envelope_ref"]], policies, "policy envelope")
        if "decision_card_ref" in event:
            assert_refs(event_id, [event["decision_card_ref"]], cards, "decision card")
        if "receipt_ref" in event:
            assert_refs(event_id, [event["receipt_ref"]], receipts, "receipt")

    for policy_id, policy in policies.items():
        check_required(policy_id, policy, ["policy_state", "permissions", "scope", "receipt_required"])
        permissions = policy["permissions"]
        for field in ["view", "enrich", "export", "scan", "notify", "act"]:
            if field not in permissions:
                fail(f"{policy_id} permissions missing {field}")
        if policy_id == "orion-pol-facility-risk-demo":
            if permissions["scan"] is not False or permissions["act"] is not False:
                fail("facility-risk demo policy must keep scan=false and act=false")

    for fusion_id, fusion in fusions.items():
        check_required(fusion_id, fusion, ["fused_event_ref", "input_event_refs", "source_record_refs", "fusion_method", "confidence", "rationale"])
        assert_refs(fusion_id, [fusion["fused_event_ref"]], events, "event")
        assert_refs(fusion_id, fusion["input_event_refs"], events, "event")
        if len(fusion["input_event_refs"]) < 2:
            fail(f"{fusion_id} must fuse at least two input events")
        source_refs_seen.update(fusion["source_record_refs"])

    for card_id, card in cards.items():
        check_required(card_id, card, ["event_ref", "title", "what_happened", "why_we_believe_it", "source_record_refs", "policy_envelope_ref", "receipt_state"])
        assert_refs(card_id, [card["event_ref"]], events, "event")
        assert_refs(card_id, [card["policy_envelope_ref"]], policies, "policy envelope")
        source_refs_seen.update(card["source_record_refs"])

    for receipt_id, receipt in receipts.items():
        check_required(receipt_id, receipt, ["receipt_type", "created_at", "event_ref", "source_record_refs", "policy_envelope_ref", "decision_card_ref", "mode"])
        assert_refs(receipt_id, [receipt["event_ref"]], events, "event")
        assert_refs(receipt_id, [receipt["policy_envelope_ref"]], policies, "policy envelope")
        assert_refs(receipt_id, [receipt["decision_card_ref"]], cards, "decision card")
        source_refs_seen.update(receipt["source_record_refs"])

    fused = events.get("orion-evt-facility-risk-fused-incident")
    if not fused:
        fail("missing fused facility-risk incident")
    if fused["policy_state"] != "action_gated":
        fail("fused facility-risk incident must remain action_gated")
    if fused.get("evidence_grade") != "fused.inferred":
        fail("fused facility-risk incident must remain fused.inferred")

    required_gaia_refs = {
        "gaia-src-facility-risk-fire-weather-alert",
        "gaia-src-facility-risk-facility-asset",
        "gaia-src-facility-risk-cve-exposure",
        "gaia-src-facility-risk-field-report",
    }
    missing_gaia_refs = sorted(required_gaia_refs - source_refs_seen)
    if missing_gaia_refs:
        fail(f"facility-risk chain missing Gaia source refs: {', '.join(missing_gaia_refs)}")

    print(
        "validated Orion facility-risk fixtures: "
        f"events={len(events)} policies={len(policies)} fusions={len(fusions)} "
        f"cards={len(cards)} receipts={len(receipts)} source_refs={len(source_refs_seen)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
