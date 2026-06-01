# Changelog

## v0.1.0

Initial proof release of Authority Revocation Witness.

### Added

- Canonical authority-revocation proof cases.
- Authority revocation policy file: `authority_policy.json`.
- Executable witness verifier: `authority_witness.py`.
- Deterministic receipt generation: `authority_receipt.json`.
- Proof pack runner: `proof_pack.py`.
- CLI interface: `arw_cli.py`.
- Discrimination tests for valid authority, pending revocation, revoked authority refusal, operational divergence, and ARW_P4 refusal/rollback.
- GitHub Actions proof-pack workflow.
- Install and replay instructions.
- Buyer-facing proof summary.
- Security and boundary notes.
- Architecture overview.

### Proof Surface

The v0.1.0 proof pack validates five cases:

- ARW-001: revoked authority with protected consequence attempted, `REVOKED_AUTHORITY_REFUSED / ARW_P3`.
- ARW-002: revoked authority with valid revalidation, `AUTHORITY_VALID / ARW_NONE`.
- ARW-003: pending revocation, `REVOCATION_WARNING / ARW_P1`.
- ARW-004: operational divergence, `OPERATIONAL_DIVERGENCE / NOT_APPLICABLE`.
- ARW-005: revoked authority plus invalid custody/standing basis, `REVOKED_AUTHORITY_REFUSED / ARW_P4`.

### Verification

Expected local verification:

```bash
python proof_pack.py
python -m pytest -q
```

Expected result:

- proof pack PASS
- 6 tests passed
- deterministic replay leaves the repo clean
