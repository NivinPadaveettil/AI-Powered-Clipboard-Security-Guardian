
import random
import secrets
import string


DB_NAMES = [
    "employees",
    "inventory",
    "sales",
    "production",
    "finance",
    "student_db",
    "clipboard_ai",
    "analytics"
]

HOSTS = [
    "localhost",
    "127.0.0.1",
    "db.company.internal",
    "mysql-server",
    "postgres-server",
    "mongodb.local"
]

USERS = [
    "root",
    "admin",
    "developer",
    "test",
    "postgres",
    "mysql",
    "readonly"
]


def rand(length):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def mysql_uri():

    return (
        f"mysql://{random.choice(USERS)}:"
        f"{rand(12)}@"
        f"{random.choice(HOSTS)}:3306/"
        f"{random.choice(DB_NAMES)}"
    )


def postgres_uri():

    return (
        f"postgresql://{random.choice(USERS)}:"
        f"{rand(12)}@"
        f"{random.choice(HOSTS)}:5432/"
        f"{random.choice(DB_NAMES)}"
    )


def mongodb_uri():

    return (
        f"mongodb://{random.choice(USERS)}:"
        f"{rand(12)}@"
        f"{random.choice(HOSTS)}:27017/"
        f"{random.choice(DB_NAMES)}"
    )


def redis_uri():

    return (
        f"redis://:{rand(10)}@"
        f"{random.choice(HOSTS)}:6379"
    )


def sqlite_path():

    return (
        f"C:/Users/Admin/Documents/"
        f"{random.choice(DB_NAMES)}.db"
    )


def env_file():

    return f"""
DB_HOST={random.choice(HOSTS)}
DB_NAME={random.choice(DB_NAMES)}
DB_USER={random.choice(USERS)}
DB_PASSWORD={rand(16)}
"""


def docker_compose():

    return f"""
environment:
  MYSQL_ROOT_PASSWORD: {rand(16)}
  MYSQL_DATABASE: {random.choice(DB_NAMES)}
  MYSQL_USER: developer
  MYSQL_PASSWORD: {rand(16)}
"""


GENERATORS = [

    mysql_uri,
    postgres_uri,
    mongodb_uri,
    redis_uri,
    sqlite_path,
    env_file,
    docker_compose

]


def generate_db_samples(n=10000):

    rows = []

    for _ in range(n):

        func = random.choice(GENERATORS)

        rows.append({

            "text": func(),

            "label": "db_credentials"

        })

    return rows


if __name__ == "__main__":

    samples = generate_db_samples(20)

    print("=" * 60)
    print("Generated Database Samples")
    print("=" * 60)

    for sample in samples:
        print(sample)