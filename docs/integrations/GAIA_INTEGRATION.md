# OFIF ↔ GAIA Integration

Status: v0 integration contract

## Purpose

This document defines how the Orion Field Intelligence Framework (OFIF) integrates with GAIA World Model.

OFIF owns field intelligence: event envelopes, observation schemas, sensor fusion primitives, field custody, communications state, adversarial indicators, and decision-card evidence discipline.

GAIA owns the world model: geospatial substrate, ontology integration, evidence graph, data cube, simulation, map surfaces, and policy-constrained actions.

The integration rule is:

**OFIF tells GAIA what happened in the field. GAIA tells OFIF what that means in the world.**

## Scope

OFIF emits validated, signed, classified, and provenance-aware events. GAIA consumes those events and maps them into world-state features, evidence nodes, spatial/temporal layers, model context, and decision support outputs.

GAIA may also return contextual information to OFIF consumers, including weather, terrain, soil, infrastructure, asset, communications, threat, model-forecast, and policy context.

## Authority boundaries

| Domain | System of record |
| --- | --- |
| Event envelope | OFIF |
| Observation payload schemas | OFIF |
| Field asset/comms/custody/adversary vocabularies | OFIF |
| Canonical world entity IDs | GAIA |
| Satellite/remote-sensing context | GAIA |
| Spatiotemporal data cube | GAIA |
| Forecast/simulation products | GAIA |
| Map and tile products | GAIA |
| Decision evidence links | Shared, with source event IDs preserved |

## Required guarantees

OFIF producers and bridge adapters must:

1. Preserve original event IDs.
2. Preserve `observed_at` and `ingested_at` separately.
3. Preserve provenance, integrity, classification, and adversarial fields.
4. Never coerce GAIA enrichment back into raw OFIF observations.
5. Emit derivation events when field events are enriched, aggregated, inferred, or fused.
6. Keep defensive/adversarial primitives defensive: indicators, controls, confidence impacts, and evidence records only.

## GAIA context returned to OFIF

GAIA may provide context packets for OFIF decision support. Context packets must include provenance references and distinguish observation, forecast, and scenario data.

Initial context families:

- weather context;
- soil context;
- terrain context;
- land-cover context;
- infrastructure context;
- jurisdiction context;
- asset context;
- communications context;
- threat context;
- model forecast context;
- policy context.

## Spatial key

H3 is the first shared spatial index between OFIF and GAIA. OFIF observations may also include lat/lon, zone IDs, property IDs, or other local identifiers. GAIA binds these to additional world-model objects such as OSM features, parcels, watersheds, facilities, raster cells, or simulation meshes.

## Flagship use case

The first integrated product is soil intelligence:

- OFIF supplies local field observations, custody state, link state, calibration state, and adversarial context.
- GAIA supplies satellite/reanalysis/terrain/soil context and model estimates.
- The bridge emits a decision card with source event IDs, model version IDs, confidence, uncertainty, and provenance.

## Implementation references

Companion GAIA artifacts:

- `docs/integrations/OFIF_INTEGRATION.md`
- `contracts/mappings/ofif-to-gaia.v1.json`
- `contracts/mappings/gaia-to-ofif-context.v1.json`
- `gaia/ontology/imports/ofif.yaml`
- `docs/GAIA_ORION_SOIL_INTELLIGENCE_USE_CASE.md`

OFIF companion artifacts:

- `ontology/gaia-bindings.ttl`
- bridge fixtures and validation tests to be added after schema freeze.

## Non-goals

- OFIF does not become a general Earth observation platform.
- GAIA does not replace OFIF event envelopes.
- GAIA enrichments must not mutate OFIF raw events.
- The integration must not include operational guidance for wrongdoing.
