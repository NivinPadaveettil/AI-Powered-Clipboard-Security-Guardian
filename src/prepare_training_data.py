from pathlib import Path
import json

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

INPUT_FILE = Path("dataset/processed/cleaned_clipboard_dataset.csv")

OUTPUT_DIR = Path("dataset/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_FILE = OUTPUT_DIR / "train.csv"
VAL_FILE = OUTPUT_DIR / "validation.csv"
TEST_FILE = OUTPUT_DIR / "test.csv"

LABEL_MAP = OUTPUT_DIR / "label_mapping.json"

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

print("=" * 70)
print("Preparing Training Dataset")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"\nLoaded Dataset: {df.shape}")

# ---------------------------------------------------
# Encode Labels
# ---------------------------------------------------

encoder = LabelEncoder()

df["label_id"] = encoder.fit_transform(df["label"])

label_mapping = {
    label: int(idx)
    for idx, label in enumerate(encoder.classes_)
}

with open(LABEL_MAP, "w") as f:
    json.dump(label_mapping, f, indent=4)

print("\nLabel Mapping")

for label, idx in label_mapping.items():
    print(f"{label:20} -> {idx}")

# ---------------------------------------------------
# Train / Validation / Test Split
# ---------------------------------------------------

train_df, temp_df = train_test_split(
    df,
    test_size=0.20,
    stratify=df["label"],
    random_state=42
)

val_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    stratify=temp_df["label"],
    random_state=42
)

print("\nDataset Split")
print(f"Train      : {train_df.shape}")
print(f"Validation : {val_df.shape}")
print(f"Test        : {test_df.shape}")

# ---------------------------------------------------
# Save
# ---------------------------------------------------

train_df.to_csv(TRAIN_FILE, index=False)
val_df.to_csv(VAL_FILE, index=False)
test_df.to_csv(TEST_FILE, index=False)

print("\nSaved Files")
print(TRAIN_FILE)
print(VAL_FILE)
print(TEST_FILE)
print(LABEL_MAP)

print("\nPreparation Completed Successfully!")