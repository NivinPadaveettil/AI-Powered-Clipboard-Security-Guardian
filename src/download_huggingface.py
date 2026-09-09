from datasets import load_dataset
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("dataset/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Downloading AI4Privacy PII dataset...")

dataset = load_dataset("ai4privacy/pii-masking-200k")

train = dataset["train"].to_pandas()

print(train.head())
print(train.columns)

train.to_csv(
    OUTPUT_DIR / "huggingface_pii.csv",
    index=False
)

print("Saved dataset/raw/huggingface_pii.csv")