# Install and Replay

## Clone

```bash
git clone https://github.com/Kamanaka5502/authority-revocation-witness.git
cd authority-revocation-witness
```

## Create Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest
```

## Run Proof Pack

```bash
python proof_pack.py
```

Expected result:

```text
PASS: Authority Revocation Witness proof pack verified
```

## Run Tests

```bash
python -m pytest -q
```

Expected result:

```text
6 passed
```

## Run CLI

```bash
python arw_cli.py verify
python arw_cli.py summary
python arw_cli.py receipt
```

Expected summary:

```text
Total Cases: 5
Authority Valid: 1
Revocation Warning: 1
Revalidation Required: 0
Revoked Authority Refused: 2
Operational Divergence: 1
ARW_P4: 1
```

## Deterministic Replay Check

After running the proof pack and tests, the repository should remain clean:

```bash
git status
```

Expected result:

```text
nothing to commit, working tree clean
```

## What This Confirms

The replay confirms that the witness can distinguish valid authority, pending revocation, revoked authority refusal, valid revalidation, and operational divergence.
