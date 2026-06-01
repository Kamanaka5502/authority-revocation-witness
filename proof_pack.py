import json
import subprocess
import sys
from pathlib import Path

RECEIPT_FILE = Path("authority_receipt.json")

EXPECTED = {
    "total_cases": 5,
    "authority_valid": 1,
    "revocation_warning": 1,
    "revalidation_required": 0,
    "revoked_authority_refused": 2,
    "operational_divergence": 1,
    "arw_p4": 1
}


def fail(message):
    print(f"FAIL: {message}")
    sys.exit(1)


def main():
    result = subprocess.run(
        [sys.executable, "authority_witness.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        fail("authority_witness.py did not complete successfully")

    if not RECEIPT_FILE.exists():
        fail("authority_receipt.json was not generated")

    receipt = json.loads(RECEIPT_FILE.read_text())

    if receipt.get("artifact") != "Authority Revocation Witness":
        fail("receipt artifact name mismatch")

    if receipt.get("policy_id") != "ARW-AUTHORITY-POLICY-v1":
        fail("policy_id missing or incorrect")

    if not receipt.get("policy_hash"):
        fail("policy_hash missing")

    summary = receipt.get("decision_summary", {})

    for key, expected_value in EXPECTED.items():
        actual_value = summary.get(key)
        if actual_value != expected_value:
            fail(f"{key} expected {expected_value}, got {actual_value}")

    results = receipt.get("results", [])
    if len(results) != EXPECTED["total_cases"]:
        fail("result count mismatch")

    required = [
        "case_id",
        "decision",
        "severity",
        "required_response",
        "prior_authority",
        "authority_revoked",
        "protected_consequence_attempted",
        "revalidated",
        "decision_matches_expected",
        "severity_matches_expected",
        "case_hash"
    ]

    for item in results:
        for key in required:
            if key not in item:
                fail(f"{item.get('case_id', 'UNKNOWN')} missing {key}")

        if not item["decision_matches_expected"]:
            fail(f"{item['case_id']} decision did not match expected")

        if not item["severity_matches_expected"]:
            fail(f"{item['case_id']} severity did not match expected")

    print("PASS: Authority Revocation Witness proof pack verified")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
