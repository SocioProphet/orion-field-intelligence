#!/usr/bin/env python3
"""Convert an OrionObservationEvent fixture into a UI-safe OrionMapMarker.

This adapter is the safe seam between governed field-intelligence events and
presentation-layer map markers. It does not consume raw OSIRIS route data and
it does not enable any scanner/sweep/recon action.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

LAYER_BY_EVENT_TYPE = {
    "natural_hazard.fire_weather_alert": "natural_hazard",
    "natural_hazard.seismic_event": "natural_hazard",
    "asset.facility": "facility_asset",
    "cyber.cve_exposure": "cyber_exposure",
    "field_report.operator_observation": "field_report",
    "incident.fused_facility_risk": "fused_incident",
    "recon.policy_required": "gated_disabled",
}

ACTION_GATED_STATES = {
    "action_gated",
    "scope_required",
    "authorization_required",
    "expired",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError:
        fail(f"missing input: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"expected top-level object in {path}")
    return value


def event_to_marker(event: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "schema_version",
        "event_id",
        "event_type",
        "location",
        "severity",
        "confidence",
        "source_record_refs",
        "evidence_grade",
        "policy_state",
    ]
    missing = [field for field in required if field not in event]
    if missing:
        fail(f"event missing required fields: {', '.join(missing)}")

    location = event.get("location") or {}
    if location.get("type") != "Point" or not isinstance(location.get("coordinates"), list):
        fail("event location must be GeoJSON Point with coordinates")

    source_refs = event.get("source_record_refs")
    if not isinstance(source_refs, list) or not source_refs:
        fail("event must include at least one source_record_ref")

    event_type = event["event_type"]
    policy_state = event["policy_state"]
    action_enabled = policy_state not in ACTION_GATED_STATES

    marker = {
        "schema_version": "0.1.0",
        "marker_id": event["event_id"].replace("orion-evt-", "orion-marker-", 1),
        "event_ref": event["event_id"],
        "layer_group": LAYER_BY_EVENT_TYPE.get(event_type, "unknown"),
        "coordinates": location["coordinates"],
        "title": event.get("title") or event_type,
        "severity": event["severity"],
        "confidence": event["confidence"],
        "evidence_grade": event["evidence_grade"],
        "policy_state": policy_state,
        "source_count": len(source_refs),
        "asset_refs": event.get("asset_refs", []),
        "selectable": True,
        "action_enabled": action_enabled,
    }

    if event.get("decision_card_ref"):
        marker["decision_card_ref"] = event["decision_card_ref"]
    if event.get("receipt_ref"):
        marker["receipt_ref"] = event["receipt_ref"]
    if not action_enabled:
        marker["action_disabled_reason"] = f"policy_state={policy_state}"

    return marker


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        fail("usage: scripts/orion_event_to_marker.py <event.json> <marker-output.json>")
    event_path = Path(argv[1])
    output_path = Path(argv[2])
    marker = event_to_marker(load_json(event_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(marker, handle, indent=2)
        handle.write("\n")
    print(f"wrote marker {marker['marker_id']} -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
