import random
import secrets
import string


CARD_TYPES = [
    "Visa",
    "Mastercard",
    "American Express"
]

BANKS = [
    "HDFC Bank",
    "ICICI Bank",
    "SBI",
    "Axis Bank",
    "Canara Bank"
]

UPI_PROVIDERS = [
    "okhdfcbank",
    "oksbi",
    "okaxis",
    "ybl",
    "ibl",
    "paytm"
]


def random_digits(n):
    return ''.join(secrets.choice(string.digits) for _ in range(n))


def fake_card_number():
    """
    Generates a synthetic training sample.
    Not guaranteed to be a valid payment card.
    """

    prefix = random.choice(["4111", "5555", "3782"])

    remaining = random_digits(12)

    return f"{prefix} {remaining[:4]} {remaining[4:8]} {remaining[8:]}"


def fake_cvv():
    return random_digits(3)


def expiry():
    month = random.randint(1, 12)
    year = random.randint(26, 35)

    return f"{month:02d}/{year}"


def upi_id():

    user = ''.join(
        secrets.choice(string.ascii_lowercase)
        for _ in range(random.randint(6, 12))
    )

    return f"{user}@{random.choice(UPI_PROVIDERS)}"


def payment_record():

    return (
        f"Card Type: {random.choice(CARD_TYPES)} | "
        f"Card Number: {fake_card_number()} | "
        f"Expiry: {expiry()} | "
        f"CVV: {fake_cvv()}"
    )


def bank_account():

    return (
        f"Bank: {random.choice(BANKS)} | "
        f"Account: {random_digits(12)} | "
        f"IFSC: HDFC{random_digits(7)}"
    )


PAYMENT_GENERATORS = [
    payment_record,
    upi_id,
    bank_account
]


def generate_payment_samples(n=10000):

    rows = []

    for _ in range(n):

        generator = random.choice(PAYMENT_GENERATORS)

        rows.append({

            "text": generator(),

            "label": "payment"

        })

    return rows


if __name__ == "__main__":

    samples = generate_payment_samples(20)

    print("=" * 60)
    print("Generated Payment Samples")
    print("=" * 60)

    for sample in samples:
        print(sample)