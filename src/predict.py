from pathlib import Path
import json
import torch

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
)

MODEL_DIR = Path("models/distilbert_clipboard")

# Load model only once
print("Loading AI model...")

tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)

model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)

model.eval()

# Load labels
with open("dataset/processed/label_mapping.json") as f:
    label_map = json.load(f)

id2label = {v: k for k, v in label_map.items()}


def predict(text: str):
    """
    Predict clipboard text category.

    Returns:
        (label, confidence)
    """

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=1)

    confidence, prediction = torch.max(probabilities, dim=1)

    return (
        id2label[prediction.item()],
        confidence.item(),
    )