import json
import hashlib
import os
from pathlib import Path

CASE_FILE = Path("authority_cases.json")
POLICY_FILE = Path("authority_policy.json")
RECEIPT_FILE = Path("authority_receipt.json")


def stable_hash(obj):
    encoded = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def classify_case(case, policy):
    if case.get("operational_divergence", False):
        cls = policy["severity_classes"]["NOT_APPLICABLE"]
        return {
            "decision": "OPERATIONAL_DIVERGENCE",
            "severity": "NOT_APPLICABLE",
            "required_response": cls["required_response"],
            "reason": cls["condition"]
        }

    authority = case.get("authority_status", {})
    revoked = bool(authority.get("revoked", False))
    revocation_pending = bool(authority.get("revocation_pending", False))
    protected = bool(case.get("protected_consequence_attempted", False))
    revalidated = bool(case.get("revalidated", False))
    custody_valid = bool(case.get("custody", {}).get("valid", False))
    standing_valid = bool(case.get("standing", {}).get("valid", False))

    if revalidated:
        cls = policy["severity_classes"]["ARW_NONE"]
        return {
            "decision": "AUTHORITY_VALID",
            "severity": "ARW_NONE",
            "required_response": cls["required_response"],
            "reason": "Continuation allowed because fresh revalidation is present."
        }

    if revocation_pending and not revoked:
        cls = policy["severity_classes"]["ARW_P1"]
        return {
            "decision": "REVOCATION_WARNING",
            "severity": "ARW_P1",
            "required_response": cls["required_response"],
            "reason": cls["condition"]
        }

    if not revoked:
        cls = policy["severity_classes"]["ARW_NONE"]
        return {
            "decision": "AUTHORITY_VALID",
            "severity": "ARW_NONE",
            "required_response": cls["required_response"],
            "reason": "Authority remains valid."
        }

    if revoked and not protected:
        cls = policy["severity_classes"]["ARW_P2"]
        return {
            "decision": "REVALIDATION_REQUIRED",
            "severity": "ARW_P2",
            "required_response": cls["required_response"],
            "reason": cls["condition"]
        }

    if revoked and protected and (not custody_valid or not standing_valid):
        cls = policy["severity_classes"]["ARW_P4"]
        return {
            "decision": "REVOKED_AUTHORITY_REFUSED",
            "severity": "ARW_P4",
            "required_response": cls["required_response"],
            "reason": cls["condition"]
        }

    if revoked and protected:
        cls = policy["severity_classes"]["ARW_P3"]
        return {
            "decision": "REVOKED_AUTHORITY_REFUSED",
            "severity": "ARW_P3",
            "required_response": cls["required_response"],
            "reason": cls["condition"]
        }

    cls = policy["severity_classes"]["NOT_APPLICABLE"]
    return {
        "decision": "OPERATIONAL_DIVERGENCE",
        "severity": "NOT_APPLICABLE",
        "required_response": cls["required_response"],
        "reason": "Case did not match a defined authority-revocation class."
    }


def evaluate_case(case, policy):
    classification = classify_case(case, policy)
    authority = case.get("authority_status", {})

    result = {
        "case_id": case["case_id"],
        "description": case["description"],
        "decision": classification["decision"],
        "severity": classification["severity"],
        "required_response": classification["required_response"],
        "reason": classification["reason"],
        "prior_authority": bool(case.get("prior_authority", False)),
        "authority_revoked": bool(authority.get("revoked", False)),
        "revocation_pending": bool(authority.get("revocation_pending", False)),
        "protected_consequence_attempted": bool(case.get("protected_consequence_attempted", False)),
        "revalidated": bool(case.get("revalidated", False)),
        "custody_valid": bool(case.get("custody", {}).get("valid", False)),
        "standing_valid": bool(case.get("standing", {}).get("valid", False)),
        "expected_decision": case.get("expected_decision"),
        "expected_severity": case.get("expected_severity"),
        "decision_matches_expected": classification["decision"] == case.get("expected_decision"),
        "severity_matches_expected": classification["severity"] == case.get("expected_severity"),
        "case_hash": stable_hash(case)
    }
    return result


def main():
    with CASE_FILE.open("r", encoding="utf-8") as f:
        case_payload = json.load(f)

    with POLICY_FILE.open("r", encoding="utf-8") as f:
        policy = json.load(f)

    cases = case_payload.get("cases", [case_payload])
    results = [evaluate_case(case, policy) for case in cases]

    receipt = {
        "artifact": "Authority Revocation Witness",
        "policy_id": policy["policy_id"],
        "policy_hash": stable_hash(policy),
        "decision_summary": {
            "total_cases": len(results),
            "authority_valid": sum(1 for r in results if r["decision"] == "AUTHORITY_VALID"),
            "revocation_warning": sum(1 for r in results if r["decision"] == "REVOCATION_WARNING"),
            "revalidation_required": sum(1 for r in results if r["decision"] == "REVALIDATION_REQUIRED"),
            "revoked_authority_refused": sum(1 for r in results if r["decision"] == "REVOKED_AUTHORITY_REFUSED"),
            "operational_divergence": sum(1 for r in results if r["decision"] == "OPERATIONAL_DIVERGENCE"),
            "arw_p4": sum(1 for r in results if r["severity"] == "ARW_P4")
        },
        "results": results,
        "issued_at": os.environ.get("ARW_ISSUED_AT", "DETERMINISTIC_RECEIPT"),
        "witness_rule": "Previously valid authority does not authorize protected consequence binding after revocation without revalidation."
    }

    receipt["receipt_hash"] = stable_hash(receipt)

    with RECEIPT_FILE.open("w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
