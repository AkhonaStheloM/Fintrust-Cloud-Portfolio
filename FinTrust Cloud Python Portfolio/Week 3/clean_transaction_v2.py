import csv
import json
import logging
from datetime import datetime
from pathlib import Path

# ── Logging setup ──────────────────────────────────────────────────

LOG_DIR = Path("logs")
DATA_DIR = Path("data")

LOG_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fintrust.pipeline")

# ── Config ─────────────────────────────────────────────────────────

RAW_INPUT = DATA_DIR / "raw_transactions.csv"
CLEAN_CSV = DATA_DIR / "clean_transactions.csv"
SUMMARY_JSON = DATA_DIR / "daily_summary.json"


def normalise_date(date_str):
    for fmt in ("%Y-%m-%d", "%d/%m/%y", "%d/%m/%Y"):
        try:
            return datetime.strptime(
                date_str.strip(),
                fmt
            ).strftime("%Y-%m-%d")
        except ValueError:
            continue

    logger.warning(
        "Unrecognised date format: '%s' - returning as-is",
        date_str
    )

    return date_str.strip()


def clean_transaction(row, row_num):
    """Return cleaned transaction dictionary."""

    try:
        return {
            "transaction_id": int(row["TxID"].strip()),
            "account_id": int(row["AcctID"].strip()),
            "type": row["TYPE"].strip().lower(),
            "amount": float(row["Amount"].strip()),
            "date": normalise_date(row["Date"]),
            "description": row["Desc"].strip() or "No description"
        }

    except (KeyError, ValueError) as e:
        raise ValueError(
            f"Row {row_num}: {e}"
        ) from e


def main():

    logger.info(
        "=== FinTrust Transaction Pipeline starting ==="
    )

    logger.info("Input: %s", RAW_INPUT)

    if not RAW_INPUT.exists():
        logger.critical(
            "Input file not found: %s - aborting",
            RAW_INPUT
        )
        return

    transactions = []
    skipped = 0

    try:
        with open(
            RAW_INPUT,
            "r",
            newline="",
            encoding="utf-8"
        ) as fin:

            reader = csv.DictReader(fin)

            for row_num, row in enumerate(reader, start=2):

                try:
                    tx = clean_transaction(
                        row,
                        row_num
                    )

                    transactions.append(tx)

                except ValueError as e:
                    logger.warning(
                        "Skipped: %s",
                        e
                    )
                    skipped += 1

    except PermissionError:
        logger.error(
            "Permission denied reading %s",
            RAW_INPUT
        )
     