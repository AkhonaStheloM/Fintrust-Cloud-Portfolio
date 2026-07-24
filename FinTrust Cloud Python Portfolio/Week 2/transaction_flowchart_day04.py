# FinTrust Bank - Automated Transaction Decision Engine

BLOCKED_COUNTRIES = ["KP", "IR", "CU", "SY", "SD"]
DAILY_LIMIT = 50000
ATM_LIMIT = 5000
LARGE_THRESHOLD = 10000
REVIEW_THRESHOLD = 5000


def assess_transaction(tx_id, customer, amount, destination, is_trusted_device):

    if destination.upper() in BLOCKED_COUNTRIES:
        status = "BLOCKED"
        reason = f"Transfer to {destination} is not permitted"

    elif amount > DAILY_LIMIT:
        status = "BLOCKED"
        reason = "Amount exceeds daily limit of R50 000"

    elif amount <= 0:
        status = "BLOCKED"
        reason = "Invalid amount"

    elif amount > LARGE_THRESHOLD:
        if is_trusted_device:
            status = "PENDING"
            reason = "Large transfer - OTP verification required"
        else:
            status = "REVIEW"
            reason = "Large transfer from unrecognised device"

    elif amount > REVIEW_THRESHOLD and not is_trusted_device:
        status = "REVIEW"
        reason = "Moderate amount from unrecognised device"

    else:
        status = "APPROVED"
        reason = "All checks passed"

    return {
        "tx_id": tx_id,
        "customer": customer,
        "status": status,
        "reason": reason
    }


test_cases = [
    ("TX001", "Thabo Nkosi", 500.00, "ZA", True),
    ("TX002", "Amahle Dlamini", 15000.00, "ZA", True),
    ("TX003", "Sipho Mokoena", 8000.00, "ZA", False),
    ("TX004", "Lerato Sithole", 200.00, "IR", True),
    ("TX005", "Nomvula Dube", 75000.00, "ZA", True),
]

print("=" * 65)
print(f"{'TX ID':<8} {'Customer':<18} {'Status':<10} Reason")
print("=" * 65)

for tc in test_cases:
    result = assess_transaction(*tc)
    print(
        f"{result['tx_id']:<8} "
        f"{result['customer']:<18} "
        f"{result['status']:<10} "
        f"{result['reason']}"
    )