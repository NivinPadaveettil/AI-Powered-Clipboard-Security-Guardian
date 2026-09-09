import random

SERVICES = [
    "Google",
    "Microsoft",
    "Amazon",
    "GitHub",
    "PayPal",
    "HDFC Bank",
    "ICICI Bank",
    "SBI",
    "Instagram",
    "Facebook",
    "X",
    "WhatsApp",
    "Telegram",
    "Dropbox",
    "AWS",
    "OpenAI"
]

TEMPLATES = [

    "Your OTP is {otp}. Do not share it with anyone.",

    "Verification code: {otp}",

    "Use {otp} to complete your login.",

    "{otp} is your one-time password.",

    "Your verification code is {otp}.",

    "{service}: Your OTP is {otp}. It expires in 5 minutes.",

    "{service}: Enter {otp} to continue.",

    "{service}: Security code {otp}.",

    "{service}: Use code {otp} for verification.",

    "{service}: Authentication code {otp}.",

    "One-Time Password: {otp}",

    "Login Code: {otp}",

    "Password Reset Code: {otp}",

    "Secure Login Code: {otp}",

    "{service}: Your login verification code is {otp}.",

    "{service}: Please verify using {otp}.",

    "{service}: Code {otp} will expire shortly."
]


def generate_otp():

    return random.randint(100000, 999999)


def generate_otp_samples(n=10000):

    rows = []

    for _ in range(n):

        otp = generate_otp()

        template = random.choice(TEMPLATES)

        service = random.choice(SERVICES)

        text = template.format(
            otp=otp,
            service=service
        )

        rows.append({

            "text": text,

            "label": "otp"

        })

    return rows


if __name__ == "__main__":

    samples = generate_otp_samples(20)

    print("=" * 60)
    print("Generated OTP Samples")
    print("=" * 60)

    for sample in samples:
        print(sample)