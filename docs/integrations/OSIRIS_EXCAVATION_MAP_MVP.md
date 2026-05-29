# OSIRIS Excavation Map MVP

Status: initial OFIF-owned implementation plan
Related issue: `SocioProphet/orion-field-intelligence#2`
Source quarantine repo: `mdheller/osiris`
Gaia source issue: `SocioProphet/gaia-world-model#29`

## 1. Purpose

This document moves the product-facing map lesson from OSIRIS excavation into Orion Field Intelligence Framework ownership.

`mdheller/osiris` is a quarantine/excavation carcass. It may inform map-first UX, layer grouping, and inspection-panel grammar. It is not a trusted runtime dependency and is not an Orion product source.

OFIF owns the field-intelligence event surface:

```text
GaiaSourceRecord refs -> OrionObservationEvent -> OrionFusionLink -> OrionPolicyEnvelope -> OrionDecisionCard -> OrionMapReceipt
```

Gaia owns source/provenance records. SCOPE-D owns scanner, sweep, recon, and active target behavior.

## 2. Controlling rule

Do not copy OSIRIS dashboard shell, route handlers, scanner UI behavior, or stealth/evasion code into Orion.

Do not wire live OSIRIS feeds into Orion in this tranche.

Do not expose scanner/sweep/recon as Orion UI action.

Orion consumes fixture-backed events and source-record references first. Live source data must come through Gaia-owned source adapters after source-ledger review.

## 3. MVP surface

The first map MVP should present one governed facility-risk scenario:

- natural hazard / fire-weather event,
- facility asset event,
- passive cyber exposure event,
- field report event,
- fused facility-risk incident,
- policy envelope,
- decision card,
- receipt.

Required UI concepts:

- map shell / operational theater,
- layer rail with Orion-owned groups,
- selected-event drawer,
- provenance/source-ref drawer,
- policy badge,
- decision-card panel,
- receipt-state indicator.

## 4. Orion layer groups

Initial Orion-owned layer groups:

| Group | Event types |
|---|---|
| Natural hazard | `natural_hazard.fire_weather_alert`, `natural_hazard.seismic_event` |
| Facility / asset | `asset.facility` |
| Cyber exposure | `cyber.cve_exposure` |
| Field reports | `field_report.operator_observation` |
| Fused incidents | `incident.fused_facility_risk` |
| Gated / disabled | `recon.policy_required` and any future unauthorized action surfaces |

These groups replace inherited OSIRIS groups. OSIRIS groups such as aviation, maritime, surveillance, and recon may return later only after Gaia/SCOPE-D source and policy gates exist.

## 5. Required selected-event fields

A selected Orion event must expose:

- event id,
- event type,
- title,
- summary,
- observed time,
- valid-until time where present,
- location,
- severity,
- confidence,
- source record refs,
- evidence grade,
- policy state,
- asset refs,
- related event refs,
- decision card ref,
- receipt ref.

## 6. Policy states

Initial policy states:

- `public_view_allowed`
- `internal_view_allowed`
- `unverified_source`
- `attribution_required`
- `action_gated`
- `scope_required`
- `authorization_required`
- `expired`

The fused facility-risk incident must remain `action_gated` in the MVP.

## 7. Receipt states

Initial receipt states:

- `none`
- `render_receipt_ready`
- `decision_receipt_ready`
- `emitted.synthetic`
- `emitted.live`

The MVP may use `emitted.synthetic` only.

## 8. SCOPE-D boundary

The following are not Orion-owned product actions:

- live scan,
- port sweep,
- host enumeration,
- service fingerprinting,
- banner grabbing,
- vulnerability probing,
- user-supplied target network action,
- stealth/evasion fetch behavior.

Orion may show a passive cyber exposure event if it is represented as source-backed field intelligence. Orion must mark any action path as gated and unavailable unless SCOPE-D supplies an authorized evidence object.

## 9. Acceptance criteria for this Orion tranche

- Orion owns event/policy/decision/receipt contracts or explicitly aligns to them.
- Fixture-backed event records exist under Orion ownership.
- A validator checks cross references across event, policy envelope, decision card, fusion link, and receipt.
- A map adapter can be added later that consumes OrionObservationEvent records rather than raw OSIRIS route data.
- Docs explicitly state that OSIRIS is not the product repo.
- Scanner/sweep/recon are disabled/gated by design.

## 10. Cross-repo links

- `SocioProphet/gaia-world-model#29` owns source/provenance records.
- `SocioProphet/SCOPE-D:docs/osiris-scanner-sweep-quarantine.md` owns scanner/sweep quarantine.
- `SocioProphet/sociosphere#406` coordinates the lane.
