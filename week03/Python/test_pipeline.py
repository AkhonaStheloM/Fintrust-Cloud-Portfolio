import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from clean_transactions import build_summary, clean_transaction, normalise_date


class TransactionHelperTests(unittest.TestCase):
    def test_normalise_date_and_clean_transaction(self):
        self.assertEqual(normalise_date("26/07/21"), "2021-07-26")
        row = {
            "TxID": "1001",
            "AcctID": "101",
            "TYPE": " DEPOSIT ",
            "Amount": "5000.00",
            "Date": "2026-07-21",
            "Desc": " Salary ",
        }
        self.assertEqual(
            clean_transaction(row),
            {
                "transaction_id": 1001,
                "account_id": 101,
                "type": "deposit",
                "amount": 5000.0,
                "date": "2026-07-21",
                "description": "Salary",
            },
        )

    def test_build_summary(self):
        transactions = [
            {"type": "deposit", "amount": 5000.0},
            {"type": "withdrawal", "amount": -250.0},
            {"type": "deposit", "amount": 12000.0},
        ]
        self.assertEqual(
            build_summary(transactions),
            {
                "total_transactions": 3,
                "total_deposits": 2,
                "total_withdrawals": 1,
                "sum_deposits": 17000.0,
                "sum_withdrawals": -250.0,
            },
        )


class TransactionPipelineIntegrationTests(unittest.TestCase):
    source_dir = Path(__file__).parent

    def run_pipeline(self, raw_csv):
        with tempfile.TemporaryDirectory() as temp_dir:
            work_dir = Path(temp_dir)
            data_dir = work_dir / "data"
            data_dir.mkdir()
            (data_dir / "raw_transactions.csv").write_text(
                raw_csv,
                encoding="utf-8",
            )
            shutil.copy2(
                self.source_dir / "clean_transaction_v2.py",
                work_dir / "clean_transaction_v2.py",
            )

            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            result = subprocess.run(
                [sys.executable, "clean_transaction_v2.py"],
                cwd=work_dir,
                capture_output=True,
                text=True,
                env=env,
            )

            summary = json.loads(
                (data_dir / "daily_summary.json").read_text(
                    encoding="utf-8",
                )
            )
            log = (work_dir / "logs" / "pipeline.log").read_text(
                encoding="utf-8",
            )
            clean_csv_exists = (data_dir / "clean_transactions.csv").exists()
            return result, summary, log, clean_csv_exists

    def test_pipeline_creates_outputs(self):
        raw_csv = (
            "TxID,AcctID,TYPE,Amount,Date,Desc\n"
            "1001,101,DEPOSIT,5000,2026-07-21,Salary\n"
            "1002,101,WITHDRAWAL,-250,2026-07-21,ATM\n"
        )
        result, summary, log, clean_csv_exists = self.run_pipeline(raw_csv)

        self.assertEqual(result.returncode, 0)
        self.assertTrue(clean_csv_exists)
        self.assertEqual(summary["total_transactions"], 2)
        self.assertEqual(summary["total_deposits"], 1)
        self.assertEqual(summary["total_withdrawals"], 1)
        self.assertIn("Processed 2 valid transactions", log)

    def test_pipeline_skips_invalid_rows_and_continues(self):
        raw_csv = (
            "TxID,AcctID,TYPE,Amount,Date,Desc\n"
            "1001,101,DEPOSIT,5000,2026-07-21,Salary\n"
            "BAD,102,DEPOSIT,not-a-number,2026-07-21,Broken row\n"
        )
        result, summary, log, clean_csv_exists = self.run_pipeline(raw_csv)

        self.assertEqual(result.returncode, 0)
        self.assertTrue(clean_csv_exists)
        self.assertEqual(summary["total_transactions"], 1)
        self.assertIn("Skipped:", log)
        self.assertIn("skipped 1 rows", log)


if __name__ == "__main__":
    unittest.main()
