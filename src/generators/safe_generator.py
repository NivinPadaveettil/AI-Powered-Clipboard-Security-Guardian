import random
import uuid

FIRST_NAMES = [
    "Alice","Bob","Charlie","David","Emma","Sophia",
    "Liam","Noah","Olivia","Ava","Nivin","Rahul",
    "Anjali","Arjun","Sara","John","Jane","Alex"
]

DOMAINS = [
    "gmail.com",
    "outlook.com",
    "yahoo.com",
    "company.com",
    "college.edu"
]

LANGUAGES = [
    "Python",
    "C",
    "C++",
    "Java",
    "JavaScript",
    "Go",
    "Rust"
]

COMMANDS = [
    "git status",
    "git pull",
    "git push",
    "docker ps",
    "docker compose up",
    "sudo apt update",
    "sudo apt install python3",
    "pip install transformers",
    "npm install",
    "python main.py",
    "ls -la",
    "pwd"
]

URLS = [
    "https://github.com",
    "https://huggingface.co",
    "https://kaggle.com",
    "https://stackoverflow.com",
    "https://docs.python.org"
]

NOTES = [
    "Meeting starts at 10 AM",
    "Submit assignment before Friday",
    "Buy milk and bread",
    "Complete AI project",
    "Call the project supervisor",
    "Prepare presentation slides",
    "Review cybersecurity notes"
]

HTML = [
    "<html><body>Hello World</body></html>",
    "<h1>Clipboard Guardian</h1>",
    "<div class='container'></div>"
]

SQL = [
    "SELECT * FROM users;",
    "UPDATE employee SET salary=50000;",
    "DELETE FROM logs WHERE id=5;",
    "INSERT INTO users VALUES(1,'Alice');"
]

JSON = [
    '{"name":"Alice","age":22}',
    '{"project":"Clipboard Guardian"}',
    '{"status":"success"}'
]

PYTHON = [
    'print("Hello World")',
    'for i in range(10): print(i)',
    'import pandas as pd'
]

SAFE_GENERATORS = []

def email():
    return f"{random.choice(FIRST_NAMES).lower()}{random.randint(1,999)}@{random.choice(DOMAINS)}"

SAFE_GENERATORS.append(email)

def url():
    return random.choice(URLS)

SAFE_GENERATORS.append(url)

def command():
    return random.choice(COMMANDS)

SAFE_GENERATORS.append(command)

def notes():
    return random.choice(NOTES)

SAFE_GENERATORS.append(notes)

def html():
    return random.choice(HTML)

SAFE_GENERATORS.append(html)

def sql():
    return random.choice(SQL)

SAFE_GENERATORS.append(sql)

def json_data():
    return random.choice(JSON)

SAFE_GENERATORS.append(json_data)

def python_code():
    return random.choice(PYTHON)

SAFE_GENERATORS.append(python_code)

def paragraph():

    name=random.choice(FIRST_NAMES)
    language=random.choice(LANGUAGES)

    return f"{name} is learning {language} programming for cybersecurity."

SAFE_GENERATORS.append(paragraph)

def uuid_text():
    return str(uuid.uuid4())

SAFE_GENERATORS.append(uuid_text)

def generate_safe_samples(n=30000):

    rows=[]

    for _ in range(n):

        func=random.choice(SAFE_GENERATORS)

        rows.append({
            "text":func(),
            "label":"safe"
        })

    return rows
if __name__ == "__main__":
    samples = generate_safe_samples(20)

    print("=" * 60)
    print("Generated Safe Clipboard Samples")
    print("=" * 60)

    for sample in samples:
        print(sample)