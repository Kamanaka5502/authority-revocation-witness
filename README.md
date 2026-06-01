# Authority Revocation Witness

Authority Revocation Witness is a deterministic proof artifact showing that previously valid authority does not survive revocation.

A system may preserve the same actor, action, output, and replay trace while the authority basis that originally admitted the action has been revoked.

> Proof class: executable continuation after authority revocation  
> Decision surface: AUTHORITY_VALID / REVOCATION_WARNING / REVALIDATION_REQUIRED / REVOKED_AUTHORITY_REFUSED / OPERATIONAL_DIVERGENCE  
> Core claim: prior authority is not continuing authority after revocation

## Core Failure Class

A continuation can remain executable after the authority that authorized it has been revoked.

This witness compares an attempted continuation against its authority status, revocation state, consequence class, and operational trace. If a protected consequence is attempted after authority revocation, the witness refuses continuation unless fresh revalidation is present.

## Proof Claim

Given an execution attempt `a`:

- ActorValid(a) = true
- ActionExecutable(a) = true
- PriorAuthority(a) = true
- AuthorityRevoked(a) = true
- ProtectedConsequenceAttempted(a) = true
- Revalidated(a) = false

Therefore:

AuthorityContinuationAdmissible(a) = false

The system did not fail because it could not execute.

It failed because its authority basis had been revoked.

## Run

`python3 authority_witness.py`

Expected decision:

`REVOKED_AUTHORITY_REFUSED`

## Repo Structure

AUTHORITY_REVOCATION_WITNESS/
- README.md
- authority_cases.json
- authority_policy.json
- authority_witness.py
- authority_receipt.json
- proof_pack.py
- arw_cli.py
- tests/

## Why It Matters

Most systems can prove that authority once existed.

Fewer can prove that the authority was still valid when consequence attempted to bind.
