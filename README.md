# Orion Field Intelligence Framework (OFIF)

Event-driven sensor fusion + reasoning for field operations.

## OSIRIS excavation migration

This repository owns the Orion/OFIF side of the OSIRIS excavation migration. `mdheller/osiris` is a quarantine/excavation carcass only; it is not a runtime dependency and is not the product home.

Orion owns the field-intelligence event surface:

```text
GaiaSourceRecord refs -> OrionObservationEvent -> OrionFusionLink -> OrionPolicyEnvelope -> OrionDecisionCard -> OrionMapReceipt -> OrionMapMarker
```

Gaia owns source/provenance records. SCOPE-D owns scanner, sweep, recon, and active target behavior. Prophet Platform is only a later downstream runtime/workbench consumer after the Gaia/Orion seam stabilizes.

### Current MVP artifacts

- `docs/integrations/OSIRIS_EXCAVATION_MAP_MVP.md`
- `schemas/orion-observation-event.v0_1.schema.json`
- `schemas/orion-policy-envelope.v0_1.schema.json`
- `schemas/orion-decision-card.v0_1.schema.json`
- `schemas/orion-fusion-link.v0_1.schema.json`
- `schemas/orion-map-receipt.v0_1.schema.json`
- `schemas/orion-map-marker.v0_1.schema.json`
- `fixtures/facility-risk/**`
- `scripts/orion_event_to_marker.py`
- `scripts/validate_facility_risk_fixtures.py`

### Validation

Run:

```bash
python3 scripts/validate_facility_risk_fixtures.py
```

The validator checks the facility-risk chain, the Gaia source-record references, the policy envelope, decision card, receipt, committed map marker, and the generated marker output from `scripts/orion_event_to_marker.py`.

### Boundaries

Do not copy OSIRIS dashboard shell, route handlers, scanner UI behavior, or stealth/evasion code into Orion.

Do not wire live OSIRIS feeds into Orion in this tranche.

Do not expose scanner/sweep/recon as Orion UI action.
