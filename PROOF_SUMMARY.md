# Authority Revocation Witness — Proof Summary

## Core Claim

Previously valid authority does not survive revocation.

A system can preserve an executable action path while the authority basis that originally admitted the action has been revoked.

When that happens, continuation may remain operationally possible but no longer admissible.

## What This Repository Proves

This repository demonstrates a narrow but important failure class:

> A consequence can attempt to bind after the authority that originally made it admissible has been revoked.

The witness separates five conditions:

1. **AUTHORITY_VALID**  
   Authority remains valid or continuation has been validly revalidated.

2. **REVOCATION_WARNING**  
   Authority revocation is pending but not yet active.

3. **REVALIDATION_REQUIRED**  
   Authority has been revoked, but no protected consequence has attempted to bind yet.

4. **REVOKED_AUTHORITY_REFUSED**  
   Authority has been revoked and a protected consequence is attempted without revalidation.

5. **OPERATIONAL_DIVERGENCE**  
   The operational trace changed, so authority-revocation continuity cannot be isolated.

## Current Proof Surface

The proof pack currently validates five cases:

| Case | Condition | Decision | Severity | Required Response |
|---|---|---|---|---|
| ARW-001 | Revoked authority with protected consequence | REVOKED_AUTHORITY_REFUSED | ARW_P3 | REFUSE_CONTINUATION |
| ARW-002 | Revoked authority with valid revalidation | AUTHORITY_VALID | ARW_NONE | ALLOW_CONTINUATION |
| ARW-003 | Pending revocation | REVOCATION_WARNING | ARW_P1 | LOG_AND_NOTIFY |
| ARW-004 | Operational divergence | OPERATIONAL_DIVERGENCE | NOT_APPLICABLE | CHECK_OPERATIONAL_DIVERGENCE |
| ARW-005 | Revoked authority plus custody/standing failure | REVOKED_AUTHORITY_REFUSED | ARW_P4 | REFUSE_OR_ROLLBACK |

## Why Prior Authority Alone Is Insufficient

An audit trail can prove that authority once existed.

A replay trace can prove that the same action path can be reproduced.

A runtime can prove that the actor and action remained executable.

None of those prove that the authority was still valid when consequence attempted to bind.

This repo demonstrates that prior authority and current authority are not the same proof class.

## Severity Model

The witness classifies authority revocation using an external policy file:

```text
authority_policy.json
```

Severity classes:

| Severity | Meaning | Required Response |
|---|---|---|
| ARW_NONE | No authority revocation issue | ALLOW_CONTINUATION |
| ARW_P1 | Revocation pending | LOG_AND_NOTIFY |
| ARW_P2 | Authority revoked, no protected consequence yet | REVALIDATION_REQUIRED |
| ARW_P3 | Revoked authority with protected consequence attempted | REFUSE_CONTINUATION |
| ARW_P4 | Revoked authority plus custody or standing failure | REFUSE_OR_ROLLBACK |

## Verification Commands

Run the full proof pack:

```bash
python proof_pack.py
```

Run tests:

```bash
python -m pytest -q
```

Run CLI summary:

```bash
python arw_cli.py summary
```

Expected proof-pack result:

```text
PASS: Authority Revocation Witness proof pack verified
```

Expected test result:

```text
6 passed
```

## Interpretation

This is not a generic access-control demo.

This is not an audit-log wrapper.

This is a proof artifact for revoked authority at the continuation boundary.

The proof surface is:

```text
prior authority existed
authority revoked
protected consequence attempted
no valid revalidation
therefore continuation refused
```

The system did not fail because execution was impossible.

It failed because authority was no longer admissible.
