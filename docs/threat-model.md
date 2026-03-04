# Threat Model — Adversarial Primitives for OFIF

## Why this exists
OFIF operates in contested, noisy, and failure-prone environments. A credible field system must model adversarial influence explicitly so confidence, decision cards, and audit trails remain defensible.

We represent adversarial influence as **events**, not anecdotes.

## Adversarial primitive families

### 1) Sensor deception (observation integrity)
- Spoofing / decoys (false signatures across modalities)
- Occlusion / blinding
- Calibration drift
- Time manipulation (clock drift, reorderings)

### 2) Physical compromise (custody)
- Tamper (movement, enclosure opening, media replacement)
- Theft / swap
- Power sabotage and repeated cycling

### 3) RF / comms interference (availability + freshness)
- Jamming / interference (degraded QoS)
- Rogue gateway / network impersonation (identity mismatch)
- Partition / outage

### 4) Cyber compromise (confidentiality + integrity)
- Credential compromise
- Firmware compromise
- Supply chain compromise (update channel)

### 5) Data poisoning (model + knowledge integrity)
- Annotation poisoning
- Training set injection
- Knowledge graph poisoning

### 6) Social/operational manipulation (human-in-loop)
- Insider misuse
- Coercion to override guardrails

## Defensive controls (modeled)
- Event signing + optional attestation
- Replay detection + dedup
- Custody chain events (maintenance/tamper/swap)
- Anomaly detection on link/sensor state
- Lineage governance for datasets and models (approval, diff, rollback)
- Access control policies + data classification

## Minimal invariants
1. Every event carries provenance + integrity fields (even if empty).
2. Every decision card cites evidence IDs and model/version IDs.
3. Every enrichment step emits a DerivationEvent (inputs → outputs).
4. Every custody-changing action emits a CustodyEvent.
