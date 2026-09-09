from pathlib import Path
import pandas as pd

RAW_DIR = Path("dataset/raw")
MERGED_DIR = Path("dataset/merged")
MERGED_DIR.mkdir(parents=True, exist_ok=True)

dfs = []

# -------------------------------------------------------
# Synthetic Dataset
# -------------------------------------------------------

print("Loading synthetic dataset...")

synthetic = pd.read_csv(RAW_DIR / "clipboard_dataset.csv")

dfs.append(synthetic)

# -------------------------------------------------------
# Kaggle Password Dataset 1
# -------------------------------------------------------

print("Loading common_passwords.csv...")

password_file = RAW_DIR / "10000-most-common-passwords" / "common_passwords.csv"

if password_file.exists():

    pw = pd.read_csv(password_file)

    print("Columns:", pw.columns.tolist())

    # Assume first column contains passwords
    col = pw.columns[0]

    pw = pw[[col]]

    pw.columns = ["text"]

    pw["label"] = "password"

    dfs.append(pw)

# -------------------------------------------------------
# Kaggle Password Dataset 2
# -------------------------------------------------------

print("Loading top_200_passwords.csv...")

password_file = RAW_DIR / "top-200-commonly-used-passwords-dataset" / "top_200_passwords.csv"

if password_file.exists():

    pw = pd.read_csv(password_file)

    print("Columns:", pw.columns.tolist())

    col = pw.columns[0]

    pw = pw[[col]]

    pw.columns = ["text"]

    pw["label"] = "password"

    dfs.append(pw)

# -------------------------------------------------------
# Merge
# -------------------------------------------------------

print("\nMerging datasets...")

df = pd.concat(dfs, ignore_index=True)

print("Before duplicate removal:", len(df))

df.drop_duplicates(inplace=True)

print("After duplicate removal :", len(df))

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

output = MERGED_DIR / "clipboard_dataset.csv"

df.to_csv(output, index=False)

print("\nSaved merged dataset to:")

print(output)

print("\nLabel Distribution")

print(df["label"].value_counts())