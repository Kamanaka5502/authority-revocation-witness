# Security and Boundary Notes

## Scope

Authority Revocation Witness is a local proof artifact for demonstrating revoked authority refusal at a continuation boundary.

It is not a production authorization engine.

It is not a live access-control system.

It is not connected to external authority, custody, identity, financial, healthcare, legal, or infrastructure systems.

## Local Execution

The repository requires no secrets, tokens, credentials, API keys, network calls, or external services to run the proof pack.

The witness is designed for deterministic local replay:

```bash
python proof_pack.py
python -m pytest -q
```

## Boundary

The proof surface shows that previously valid authority does not authorize continuation after revocation.

Production use would require integration with real systems of record for:

- authority
- identity
- custody
- standing
- revocation status
- policy version
- revalidation
- consequence binding

## No Production Enforcement Claim

This repository does not claim to enforce real-world refusal, rollback, denial, or authorization decisions by itself.

It demonstrates the classification logic and receipt structure needed to witness when such enforcement should occur.

## Safe Use

Use this repository to inspect, replay, test, and reason about authority revocation and stale authority.

Do not use it as the sole basis for real-world healthcare, financial, legal, employment, infrastructure, or access-control decisions without a validated production integration layer.
