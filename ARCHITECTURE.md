# Architecture

## Execution Surface

Authority Revocation Witness is organized as a deterministic proof artifact.

The architecture separates case data, governing policy, witness logic, generated receipts, proof-pack validation, CLI access, tests, and CI replay.

## Flow

1. `authority_cases.json` supplies continuation attempts and expected classifications.
2. `authority_policy.json` defines the decision and severity model.
3. `authority_witness.py` evaluates revocation state, revalidation, custody, standing, and protected consequence attempts.
4. `authority_receipt.json` records the deterministic witness result.
5. `proof_pack.py` verifies expected proof counts and receipt structure.
6. `arw_cli.py` provides an operator command surface.
7. `tests/` validates discrimination behavior.
8. `.github/workflows/proof-pack.yml` runs proof replay in CI.

## Core Separation

Operational dimensions:

- actor
- action
- output
- replay trace

Authority dimensions:

- prior authority
- revocation status
- revocation pending state
- protected consequence attempted
- revalidation state
- custody validity
- standing validity

The witness only refuses stale continuation when authority has been revoked and a protected consequence attempts to bind without valid revalidation.

## Decision Surface

- `AUTHORITY_VALID`: authority remains valid or valid revalidation is present.
- `REVOCATION_WARNING`: authority revocation is pending but not yet active.
- `REVALIDATION_REQUIRED`: authority has been revoked but no protected consequence has attempted to bind yet.
- `REVOKED_AUTHORITY_REFUSED`: authority has been revoked and protected consequence binding is attempted without revalidation.
- `OPERATIONAL_DIVERGENCE`: operational continuity failed, so authority-revocation continuity cannot be isolated.

## Enforcement Interpretation

The repository does not enforce production decisions directly.

It produces a receipt indicating what enforcement response would be required if the witness were integrated into a production authority, identity, standing, and custody system.

## Replay Invariant

Running the proof pack must not mutate the repository state.

Expected replay check:

```bash
python proof_pack.py
python -m pytest -q
git status
```

Expected result:

```text
nothing to commit, working tree clean
```
