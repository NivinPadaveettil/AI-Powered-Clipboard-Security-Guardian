from pathlib import Path
import pandas as pd

from generators.safe_generator import generate_safe_samples
from generators.password_generator import generate_password_samples
from generators.secret_generator import generate_secret_samples
from generators.payment_generator import generate_payment_samples
from generators.otp_generator import generate_otp_samples
from generators.db_generator import generate_db_samples

# ----------------------------------------
# Configuration
# ----------------------------------------

SAFE_SAMPLES = 30000
PASSWORD_SAMPLES = 10000
SECRET_SAMPLES = 15000
PAYMENT_SAMPLES = 10000
OTP_SAMPLES = 10000
DB_SAMPLES = 10000

OUTPUT_DIR = Path("dataset/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "clipboard_dataset.csv"

# ----------------------------------------
# Generate Dataset
# ----------------------------------------

print("=" * 70)
print("Generating Synthetic Clipboard Dataset")
print("=" * 70)

rows = []

print("Generating Safe Samples...")
rows.extend(generate_safe_samples(SAFE_SAMPLES))

print("Generating Password Samples...")
rows.extend(generate_password_samples(PASSWORD_SAMPLES))

print("Generating Secret Samples...")
rows.extend(generate_secret_samples(SECRET_SAMPLES))

print("Generating Payment Samples...")
rows.extend(generate_payment_samples(PAYMENT_SAMPLES))

print("Generating OTP Samples...")
rows.extend(generate_otp_samples(OTP_SAMPLES))

print("Generating Database Samples...")
rows.extend(generate_db_samples(DB_SAMPLES))

# ----------------------------------------
# Create DataFrame
# ----------------------------------------

df = pd.DataFrame(rows)

print(f"\nTotal Generated Samples: {len(df):,}")

# Remove duplicates
before = len(df)
df.drop_duplicates(inplace=True)
after = len(df)

print(f"Removed Duplicates: {before - after:,}")

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
df.to_csv(OUTPUT_FILE, index=False)

print("\nDataset saved to:")
print(OUTPUT_FILE)

print("\nDataset Shape:")
print(df.shape)

print("\nLabel Distribution:")
print(df["label"].value_counts())

print("\nDone!")