import argparse
import json
import subprocess
import sys
from pathlib import Path

RECEIPT_FILE = Path("authority_receipt.json")


def run_verify():
    result = subprocess.run(
        [sys.executable, "authority_witness.py"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        sys.exit(result.returncode)

    print(result.stdout)


def show_receipt():
    if not RECEIPT_FILE.exists():
        print("No authority_receipt.json found. Run: python arw_cli.py verify")
        sys.exit(1)

    print(RECEIPT_FILE.read_text())


def show_summary():
    if not RECEIPT_FILE.exists():
        print("No authority_receipt.json found. Run: python arw_cli.py verify")
        sys.exit(1)

    receipt = json.loads(RECEIPT_FILE.read_text())
    summary = receipt.get("decision_summary", {})

    print("Authority Revocation Witness Summary")
    print("------------------------------------")
    print(f"Policy: {receipt.get('policy_id', 'UNKNOWN')}")
    print(f"Receipt Hash: {receipt.get('receipt_hash', 'UNKNOWN')}")
    print(f"Total Cases: {summary.get('total_cases', 0)}")
    print(f"Authority Valid: {summary.get('authority_valid', 0)}")
    print(f"Revocation Warning: {summary.get('revocation_warning', 0)}")
    print(f"Revalidation Required: {summary.get('revalidation_required', 0)}")
    print(f"Revoked Authority Refused: {summary.get('revoked_authority_refused', 0)}")
    print(f"Operational Divergence: {summary.get('operational_divergence', 0)}")
    print(f"ARW_P4: {summary.get('arw_p4', 0)}")


def main():
    parser = argparse.ArgumentParser(
        description="Authority Revocation Witness CLI"
    )

    parser.add_argument(
        "command",
        choices=["verify", "receipt", "summary"],
        help="Command to run"
    )

    args = parser.parse_args()

    if args.command == "verify":
        run_verify()
    elif args.command == "receipt":
        show_receipt()
    elif args.command == "summary":
        show_summary()


if __name__ == "__main__":
    main()
