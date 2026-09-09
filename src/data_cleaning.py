from pathlib import Path

import pandas as pd


# ----------------------------
# File Paths
# ----------------------------

RAW_DATA = Path("dataset/raw/clipboard_dataset.csv")
PROCESSED_DIR = Path("dataset/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_DIR / "cleaned_clipboard_dataset.csv"


# ----------------------------
# Load Dataset
# ----------------------------

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

df = pd.read_csv(RAW_DATA)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nColumn Information")
print(df.info())


# ----------------------------
# Missing Values
# ----------------------------

print("\n" + "=" * 60)
print("Missing Values")
print("=" * 60)

print(df.isnull().sum())


# ----------------------------
# Remove Missing Values
# ----------------------------

before = len(df)

df.dropna(inplace=True)

after = len(df)

print(f"\nRemoved {before-after} rows containing missing values.")


# ----------------------------
# Remove Duplicate Rows
# ----------------------------

before = len(df)

duplicates = df.duplicated().sum()

df.drop_duplicates(inplace=True)

after = len(df)

print(f"Duplicate Rows Found : {duplicates}")
print(f"Removed              : {before-after}")


# ----------------------------
# Remove Leading & Trailing Spaces
# ----------------------------

df["text"] = df["text"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip()


# ----------------------------
# Remove Empty Strings
# ----------------------------

before = len(df)

df = df[df["text"] != ""]

after = len(df)

print(f"\nRemoved Empty Text Rows : {before-after}")


# ----------------------------
# Convert Datatypes
# ----------------------------

df["text"] = df["text"].astype("string")
df["label"] = df["label"].astype("category")


print("\nFinal Data Types\n")
print(df.dtypes)


# ----------------------------
# Final Summary
# ----------------------------

print("\n" + "=" * 60)
print("Cleaning Summary")
print("=" * 60)

print(f"Final Shape : {df.shape}")

print("\nLabel Distribution\n")
print(df["label"].value_counts())


# ----------------------------
# Save Clean Dataset
# ----------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\nSaved Clean Dataset To:")
print(OUTPUT_FILE)

print("\nData Cleaning Completed Successfully!")