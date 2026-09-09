import random
import string

SPECIAL = "!@#$%^&*()_-+=<>?"

COMMON_WORDS = [
    "admin",
    "password",
    "welcome",
    "login",
    "computer",
    "cyber",
    "security",
    "student",
    "college",
    "engineer",
    "guardian",
    "clipboard",
    "python",
    "database"
]


def random_password(length=None):
    """Generate a realistic strong password."""

    if length is None:
        length = random.randint(8, 20)

    chars = (
        string.ascii_letters
        + string.digits
        + SPECIAL
    )

    password = "".join(random.choice(chars) for _ in range(length))

    return password


def dictionary_password():
    """Generate human-style passwords."""

    word = random.choice(COMMON_WORDS)

    return (
        word.capitalize()
        + str(random.randint(100, 9999))
        + random.choice(SPECIAL)
    )


def company_password():
    """Generate company-style passwords."""

    return (
        "Company@"
        + str(random.randint(2024, 2035))
    )


PASSWORD_GENERATORS = [
    random_password,
    dictionary_password,
    company_password,
]


def generate_password_samples(n=10000):

    rows = []

    for _ in range(n):

        generator = random.choice(PASSWORD_GENERATORS)

        rows.append({
            "text": generator(),
            "label": "password"
        })

    return rows


if __name__ == "__main__":

    samples = generate_password_samples(20)

    print("=" * 60)
    print("Generated Password Samples")
    print("=" * 60)

    for sample in samples:
        print(sample)