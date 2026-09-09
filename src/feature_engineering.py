from pathlib import Path
import re

import pandas as pd

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

INPUT_FILE = Path("dataset/processed/cleaned_clipboard_dataset.csv")

OUTPUT_DIR = Path("dataset/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "featured_clipboard_dataset.csv"

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

print("=" * 70)
print("Feature Engineering")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"\nLoaded Dataset: {df.shape}")

# ---------------------------------------------------
# Basic Features
# ---------------------------------------------------

df["text"] = df["text"].astype(str)

df["text_length"] = df["text"].str.len()

df["word_count"] = df["text"].str.split().str.len()

df["digit_count"] = df["text"].str.count(r"\d")

df["uppercase_count"] = df["text"].str.count(r"[A-Z]")

df["lowercase_count"] = df["text"].str.count(r"[a-z]")

df["special_char_count"] = df["text"].str.count(r"[^A-Za-z0-9\s]")

df["whitespace_count"] = df["text"].str.count(r"\s")

# ---------------------------------------------------
# Pattern Features
# ---------------------------------------------------

EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

URL_REGEX = r"(http|https)://"

IP_REGEX = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

HEX_REGEX = r"\b[a-fA-F0-9]{32,}\b"

df["contains_email"] = (
    df["text"]
    .str.contains(EMAIL_REGEX, regex=True)
    .astype(int)
)

df["contains_url"] = (
    df["text"]
    .str.contains(URL_REGEX, regex=True)
    .astype(int)
)

df["contains_ip"] = (
    df["text"]
    .str.contains(IP_REGEX, regex=True)
    .astype(int)
)

df["contains_hex"] = (
    df["text"]
    .str.contains(HEX_REGEX, regex=True)
    .astype(int)
)

# ---------------------------------------------------
# Keyword Features
# ---------------------------------------------------

KEYWORDS = [
    "password",
    "token",
    "secret",
    "apikey",
    "api_key",
    "bearer",
    "jwt",
    "ssh",
    "private",
    "mysql",
    "mongodb",
    "postgres",
    "redis",
    "otp",
    "visa",
    "mastercard",
    "upi",
]

def keyword_count(text):
    text = text.lower()
    return sum(word in text for word in KEYWORDS)

df["keyword_count"] = df["text"].apply(keyword_count)

# ---------------------------------------------------
# Save
# ---------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\nFeatures Created")

print(df.columns.tolist())

print("\nDataset Shape")

print(df.shape)

print("\nSaved")

print(OUTPUT_FILE)

print("\nFeature Engineering Completed Successfully!")