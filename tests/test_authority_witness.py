import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from authority_witness import evaluate_case

POLICY = json.loads(Path("authority_policy.json").read_text())
CASES = json.loads(Path("authority_cases.json").read_text())["cases"]


def case_by_id(case_id):
    for case in CASES:
        if case["case_id"] == case_id:
            return case
    raise AssertionError(f"Missing case {case_id}")


def test_revoked_authority_refused_p3():
    result = evaluate_case(case_by_id("ARW-001"), POLICY)

    assert result["decision"] == "REVOKED_AUTHORITY_REFUSED"
    assert result["severity"] == "ARW_P3"
    assert result["required_response"] == "REFUSE_CONTINUATION"
    assert result["prior_authority"] is True
    assert result["authority_revoked"] is True
    assert result["protected_consequence_attempted"] is True
    assert result["revalidated"] is False


def test_revalidated_authority_valid():
    result = evaluate_case(case_by_id("ARW-002"), POLICY)

    assert result["decision"] == "AUTHORITY_VALID"
    assert result["severity"] == "ARW_NONE"
    assert result["required_response"] == "ALLOW_CONTINUATION"
    assert result["authority_revoked"] is True
    assert result["revalidated"] is True


def test_revocation_warning():
    result = evaluate_case(case_by_id("ARW-003"), POLICY)

    assert result["decision"] == "REVOCATION_WARNING"
    assert result["severity"] == "ARW_P1"
    assert result["required_response"] == "LOG_AND_NOTIFY"
    assert result["revocation_pending"] is True
    assert result["authority_revoked"] is False


def test_operational_divergence_not_applicable():
    result = evaluate_case(case_by_id("ARW-004"), POLICY)

    assert result["decision"] == "OPERATIONAL_DIVERGENCE"
    assert result["severity"] == "NOT_APPLICABLE"
    assert result["required_response"] == "CHECK_OPERATIONAL_DIVERGENCE"


def test_revoked_authority_refused_p4():
    result = evaluate_case(case_by_id("ARW-005"), POLICY)

    assert result["decision"] == "REVOKED_AUTHORITY_REFUSED"
    assert result["severity"] == "ARW_P4"
    assert result["required_response"] == "REFUSE_OR_ROLLBACK"
    assert result["custody_valid"] is False
    assert result["standing_valid"] is False


def test_all_cases_match_expected_outputs():
    for case in CASES:
        result = evaluate_case(case, POLICY)
        assert result["decision"] == case["expected_decision"]
        assert result["severity"] == case["expected_severity"]
