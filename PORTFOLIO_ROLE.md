# Portfolio Role — Authority Revocation Witness

## Control Dimension: Revocation Interrupts Continuation

This repository is a supporting proof surface within the **Elyria Systems Pre-Execution Governance** portfolio.

It establishes that authority which once existed is not automatically continuing authority:

> **A technically executable action must still refuse when the authority basis that admitted it has been revoked and fresh revalidation is absent.**

## How to Navigate the Portfolio

1. **Start with the flagship runnable proof surface:** [Elyria Admission Runtime](https://github.com/Kamanaka5502/elyria-admission-runtime)
2. **Review the full portfolio hierarchy:** [Elyria Systems — Portfolio Start Here](https://github.com/Kamanaka5502/Samantha-Revita-Elyria-Systems/blob/main/PORTFOLIO_START_HERE.md)
3. **Then return here** to inspect the revocation failure class, refusal outcome, receipt posture, and test corridor.

## Relationship to the Flagship Runtime

```text
Elyria Admission Runtime
    → evaluates whether movement may bind now

Authority Revocation Witness
    → proves that prior approval cannot carry forward after revocation
      without an explicit revalidation basis
```

## Reviewer Question

```text
Can the system distinguish “the action can still execute”
from “the action is still authorized to bind consequence”?
```

This repository exists to make that distinction inspectable.

> **Pre-Execution Governance category:** Prior authority is not continuing authority after revocation.
