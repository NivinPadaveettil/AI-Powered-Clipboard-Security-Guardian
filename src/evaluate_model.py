from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from datasets import Dataset
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_recall_fscore_support,
)

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    DataCollatorWithPadding,
)

# -----------------------------------------------------
# Paths
# -----------------------------------------------------

MODEL_DIR = Path("models/distilbert_clipboard")
DATA_DIR = Path("dataset/processed")

TEST_FILE = DATA_DIR / "test.csv"
LABEL_FILE = DATA_DIR / "label_mapping.json"

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

# -----------------------------------------------------
# Load label mapping
# -----------------------------------------------------

with open(LABEL_FILE) as f:
    label_map = json.load(f)

id2label = {v: k for k, v in label_map.items()}
labels = [id2label[i] for i in range(len(id2label))]

# -----------------------------------------------------
# Load test data
# -----------------------------------------------------

df = pd.read_csv(TEST_FILE)

test_ds = Dataset.from_pandas(
    df[["text", "label_id"]]
)

# -----------------------------------------------------
# Tokenizer
# -----------------------------------------------------

tokenizer = DistilBertTokenizerFast.from_pretrained(
    MODEL_DIR
)

def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=128,
    )

test_ds = test_ds.map(tokenize, batched=True)

test_ds = test_ds.rename_column(
    "label_id",
    "labels",
)

test_ds.set_format("torch")

# -----------------------------------------------------
# Load model
# -----------------------------------------------------

model = DistilBertForSequenceClassification.from_pretrained(
    MODEL_DIR
)

trainer = Trainer(
    model=model,
    data_collator=DataCollatorWithPadding(tokenizer),
)

# -----------------------------------------------------
# Predict
# -----------------------------------------------------

predictions = trainer.predict(test_ds)

preds = np.argmax(predictions.predictions, axis=1)

truth = predictions.label_ids

# -----------------------------------------------------
# Metrics
# -----------------------------------------------------

acc = accuracy_score(truth, preds)

precision, recall, f1, _ = precision_recall_fscore_support(
    truth,
    preds,
    average="weighted",
)

print("\nAccuracy :", acc)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)

# -----------------------------------------------------
# Classification Report
# -----------------------------------------------------

report = classification_report(
    truth,
    preds,
    target_names=labels,
)

print("\n")
print(report)

with open(REPORT_DIR / "classification_report.txt", "w") as f:
    f.write(report)

# -----------------------------------------------------
# Confusion Matrix
# -----------------------------------------------------

cm = confusion_matrix(truth, preds)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels,
)

fig, ax = plt.subplots(figsize=(10, 8))

disp.plot(ax=ax, xticks_rotation=45)

plt.tight_layout()

plt.savefig(
    REPORT_DIR / "confusion_matrix.png",
    dpi=300,
)

plt.close()

print("\nSaved:")
print(REPORT_DIR / "classification_report.txt")
print(REPORT_DIR / "confusion_matrix.png")