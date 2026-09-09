import random
import string
import base64
import secrets

# -----------------------------
# Helper Functions
# -----------------------------

def random_alnum(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def random_hex(length):
    alphabet = "0123456789abcdef"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# -----------------------------
# API Key Generators
# -----------------------------

def aws_access_key():
    return "AKIA" + random_alnum(16)


def github_pat():
    return "ghp_" + random_alnum(36)


def gitlab_pat():
    return "glpat-" + random_alnum(20)


def stripe_key():
    return "sk_live_" + random_alnum(32)


def openai_key():
    return "sk-proj-" + random_alnum(48)


def slack_token():
    return "xoxb-" + \
           str(random.randint(1000000000,9999999999)) + "-" + \
           str(random.randint(1000000000,9999999999)) + "-" + \
           random_alnum(24)


def bearer_token():
    return "Bearer " + random_alnum(80)


# -----------------------------
# JWT
# -----------------------------

def jwt_token():

    header = base64.urlsafe_b64encode(
        b'{"alg":"HS256","typ":"JWT"}'
    ).decode().rstrip("=")

    payload = base64.urlsafe_b64encode(
        random_alnum(40).encode()
    ).decode().rstrip("=")

    signature = random_alnum(43)

    return f"{header}.{payload}.{signature}"


# -----------------------------
# SSH Public Key
# -----------------------------

def ssh_public_key():

    return (
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ"
        + random_alnum(220)
        + " user@pc"
    )


# -----------------------------
# RSA Private Key
# -----------------------------

def rsa_private_key():

    body = "\n".join(
        random_alnum(64)
        for _ in range(20)
    )

    return (
        "-----BEGIN RSA PRIVATE KEY-----\n"
        + body +
        "\n-----END RSA PRIVATE KEY-----"
    )


# -----------------------------
# Kubernetes Secret
# -----------------------------

def kubernetes_secret():

    return f"""
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  password: {base64.b64encode(random_alnum(12).encode()).decode()}
"""


# -----------------------------
# Firebase Config
# -----------------------------

def firebase_config():

    return f"""{{
"apiKey":"AIza{random_alnum(35)}",
"authDomain":"project.firebaseapp.com",
"projectId":"clipboard-ai"
}}"""


# -----------------------------
# Secret Types
# -----------------------------

SECRET_GENERATORS = [

    ("api_key", aws_access_key),
    ("api_key", github_pat),
    ("api_key", gitlab_pat),
    ("api_key", stripe_key),
    ("api_key", openai_key),
    ("api_key", slack_token),

    ("jwt", jwt_token),

    ("ssh_key", ssh_public_key),
    ("ssh_key", rsa_private_key),

]


def generate_secret_samples(n=15000):

    rows = []

    for _ in range(n):

        label, func = random.choice(SECRET_GENERATORS)

        rows.append({

            "text": func(),

            "label": label

        })

    return rows


if __name__ == "__main__":

    samples = generate_secret_samples(20)

    print("=" * 60)
    print("Generated Secret Samples")
    print("=" * 60)

    for sample in samples:
        print(sample)
        print()