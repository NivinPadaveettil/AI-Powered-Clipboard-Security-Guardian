from pathlib import Path
import subprocess
import zipfile
import os
from datasets import load_dataset

# -------------------------------------------------
# Directories
# -------------------------------------------------

RAW_DIR = Path("dataset/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Hugging Face
# -------------------------------------------------

print("=" * 70)
print("Downloading Hugging Face Dataset")
print("=" * 70)

try:
    dataset = load_dataset("ai4privacy/pii-masking-200k")

    dataset["train"].to_pandas().to_csv(
        RAW_DIR / "huggingface_pii.csv",
        index=False
    )

    print("✓ Hugging Face dataset downloaded.")

except Exception as e:
    print(e)

# -------------------------------------------------
# Kaggle Dataset IDs
# -------------------------------------------------

KAGGLE_DATASETS = [
    "shivamb/10000-most-common-passwords",
    "rauf111/top-200-commonly-used-passwords-dataset"
]

print("\n")

print("=" * 70)
print("Downloading Kaggle Datasets")
print("=" * 70)

for dataset in KAGGLE_DATASETS:

    print(f"\nDownloading {dataset}")

    subprocess.run([
        "kaggle",
        "datasets",
        "download",
        "-d",
        dataset,
        "-p",
        str(RAW_DIR)
    ])

# -------------------------------------------------
# Extract ZIP Files
# -------------------------------------------------

print("\n")

print("=" * 70)
print("Extracting ZIP Files")
print("=" * 70)

for zip_file in RAW_DIR.glob("*.zip"):

    extract_dir = RAW_DIR / zip_file.stem

    extract_dir.mkdir(exist_ok=True)

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    print(f"✓ {zip_file.name}")

print("\n")

print("=" * 70)
print("Finished Downloading Datasets")
print("=" * 70)
