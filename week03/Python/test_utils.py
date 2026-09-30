import unittest

from fintrust_utils import (
    calculate_monthly_fee,
    calculate_simple_interest,
    categorise_transaction,
    format_rand,
    generate_report_header,
    mask_id_number,
    summarise_transactions,
    validate_account_type,
    validate_id_number,
)


class FinTrustUtilsTests(unittest.TestCase):
    def test_format_rand(self):
        self.assertEqual(format_rand(45230.75), "R 45,230.75")

    def test_mask_id_number(self):
        self.assertEqual(
            mask_id_number("8501015009084"),
            "850101******4",
        )
        self.assertEqual(mask_id_number("123"), "123")

    def test_validate_id_number(self):
        self.assertTrue(validate_id_number("8501015009084"))
        self.assertFalse(validate_id_number("123"))
        self.assertFalse(validate_id_number("85010150090AB"))

    def test_validate_account_type(self):
        self.assertTrue(validate_account_type("savings"))
        self.assertTrue(validate_account_type("cheque"))
        self.assertTrue(validate_account_type("credit"))
        self.assertFalse(validate_account_type("investment"))

    def test_simple_interest(self):
        self.assertEqual(calculate_simple_interest(10000, 0.12, 6), 600.0)

    def test_monthly_fees(self):
        self.assertEqual(calculate_monthly_fee("savings"), 0.0)
        self.assertEqual(calculate_monthly_fee("cheque"), 65.0)
        self.assertEqual(calculate_monthly_fee("credit"), 120.0)
        self.assertEqual(calculate_monthly_fee("unknown"), 0.0)

    def test_transaction_categories(self):
        self.assertEqual(categorise_transaction(499), "small")
        self.assertEqual(categorise_transaction(500), "medium")
        self.assertEqual(categorise_transaction(4999), "medium")
        self.assertEqual(categorise_transaction(5000), "large")
        self.assertEqual(categorise_transaction(-5000), "large")

    def test_transaction_summary(self):
        amounts = [5000, -250, 1200, -800, 3500, -1500]
        self.assertEqual(
            summarise_transactions(amounts),
            (9700, -2550, 7150),
        )

    def test_report_header_contains_account_details(self):
        header = generate_report_header("Thabo Nkosi", "ACC-10042")
        self.assertIn("FinTrust Bank", header)
        self.assertIn("Thabo Nkosi", header)
        self.assertIn("ACC-10042", header)


if __name__ == "__main__":
    unittest.main()
