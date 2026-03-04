# Start Here — Orion Field Intelligence Framework (OFIF)

This patch adds **adversarial primitives** and **defensive governance** to the OFIF event-first sensor fusion framework.

## Reading order
1. `docs/threat-model.md`
2. `contracts/envelope/event-envelope.v1.json`
3. `contracts/schemas/observation-event.v1.json`
4. `ontology/adversary.ttl` (+ `assets.ttl`, `comms.ttl`, `operations.ttl`, `environment.ttl`)
5. `docs/diagrams/` (Mermaid diagrams)

## Scope
- Defensive modeling only: attacks are represented as events + indicators + controls.
- No operational guidance for wrongdoing is included.
