from pathlib import Path
import json
import numpy as np

import evaluate
import pandas as pd

from datasets import Dataset

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
)

from sklearn.utils.class_weight import compute_class_weight

import torch

# --------------------------------------------------
# Paths
# --------------------------------------------------

DATA_DIR = Path("dataset/processed")

TRAIN_FILE = DATA_DIR / "train.csv"
VAL_FILE = DATA_DIR / "validation.csv"

LABEL_FILE = DATA_DIR / "label_mapping.json"

MODEL_DIR = Path("models/distilbert_clipboard")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

train_df = pd.read_csv(TRAIN_FILE)

val_df = pd.read_csv(VAL_FILE)

with open(LABEL_FILE) as f:
    label_mapping = json.load(f)

num_labels = len(label_mapping)

print("Labels:", label_mapping)

# --------------------------------------------------
# HuggingFace Dataset
# --------------------------------------------------

train_ds = Dataset.from_pandas(
    train_df[["text", "label_id"]]
)

val_ds = Dataset.from_pandas(
    val_df[["text", "label_id"]]
)

# --------------------------------------------------
# Tokenizer
# --------------------------------------------------

MODEL_NAME = "distilbert-base-uncased"

tokenizer = DistilBertTokenizerFast.from_pretrained(
    MODEL_NAME
)

def tokenize(batch):

    return tokenizer(
        batch["text"],
        truncation=True,
        padding=False,
        max_length=128,
    )

train_ds = train_ds.map(tokenize, batched=True)

val_ds = val_ds.map(tokenize, batched=True)

train_ds = train_ds.rename_column(
    "label_id",
    "labels"
)

val_ds = val_ds.rename_column(
    "label_id",
    "labels"
)

train_ds.set_format("torch")

val_ds.set_format("torch")

# --------------------------------------------------
# Model
# --------------------------------------------------

model = DistilBertForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=num_labels,
)

# --------------------------------------------------
# Class Weights
# --------------------------------------------------

weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(train_df["label_id"]),
    y=train_df["label_id"],
)

class_weights = torch.tensor(
    weights,
    dtype=torch.float
)

# --------------------------------------------------
# Metrics
# --------------------------------------------------

accuracy = evaluate.load("accuracy")

precision = evaluate.load("precision")

recall = evaluate.load("recall")

f1 = evaluate.load("f1")

def compute_metrics(eval_pred):

    logits, labels = eval_pred

    predictions = np.argmax(
        logits,
        axis=1
    )

    return {
        "accuracy": accuracy.compute(
            predictions=predictions,
            references=labels,
        )["accuracy"],

        "precision": precision.compute(
            predictions=predictions,
            references=labels,
            average="weighted",
        )["precision"],

        "recall": recall.compute(
            predictions=predictions,
            references=labels,
            average="weighted",
        )["recall"],

        "f1": f1.compute(
            predictions=predictions,
            references=labels,
            average="weighted",
        )["f1"],
    }

# --------------------------------------------------
# Training Arguments
# --------------------------------------------------

training_args = TrainingArguments(

    output_dir=str(MODEL_DIR),

    eval_strategy="epoch",

    save_strategy="epoch",

    logging_strategy="steps",

    logging_steps=100,

    learning_rate=2e-5,

    per_device_train_batch_size=16,

    per_device_eval_batch_size=16,

    num_train_epochs=4,

    weight_decay=0.01,

    load_best_model_at_end=True,

    metric_for_best_model="f1",

    greater_is_better=True,

    fp16=torch.cuda.is_available(),
)

# --------------------------------------------------
# Trainer
# --------------------------------------------------

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=train_ds,

    eval_dataset=val_ds,


    data_collator=DataCollatorWithPadding(
        tokenizer
    ),

    compute_metrics=compute_metrics,
)

# --------------------------------------------------
# Train
# --------------------------------------------------

trainer.train()

# --------------------------------------------------
# Save
# --------------------------------------------------

trainer.save_model(MODEL_DIR)

tokenizer.save_pretrained(MODEL_DIR)

print("\nTraining Completed Successfully!")

print(MODEL_DIR)