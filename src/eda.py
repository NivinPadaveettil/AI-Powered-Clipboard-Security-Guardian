from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
# ---------------------------------------------------
# Paths
# ---------------------------------------------------

DATASET = Path("dataset/processed/featured_clipboard_dataset.csv")

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

FIGURE_DIR = REPORT_DIR / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

print("=" * 70)
print("AI Security Clipboard Guardian")
print("Exploratory Data Analysis")
print("=" * 70)

df = pd.read_csv(DATASET)

print("\nDataset Loaded Successfully\n")

print(f"Shape : {df.shape}")

print("\nColumns\n")

print(df.columns.tolist())

print("\nData Types\n")

print(df.dtypes)

# ---------------------------------------------------
# Missing Values
# ---------------------------------------------------

print("\n" + "=" * 70)
print("Missing Values")
print("=" * 70)

print(df.isnull().sum())

# ---------------------------------------------------
# Duplicate Rows
# ---------------------------------------------------

duplicates = df.duplicated().sum()

print("\nDuplicate Rows :", duplicates)

# ---------------------------------------------------
# Label Distribution
# ---------------------------------------------------

print("\n" + "=" * 70)
print("Label Distribution")
print("=" * 70)

print(df["label"].value_counts())

print("\nPercentage Distribution\n")

print(
    (
        df["label"]
        .value_counts(normalize=True)
        * 100
    ).round(2)
)

# ---------------------------------------------------
# Text Statistics
# ---------------------------------------------------

df["text_length"] = df["text"].astype(str).str.len()

df["word_count"] = (
    df["text"]
    .astype(str)
    .str.split()
    .str.len()
)

print("\n" + "=" * 70)
print("Text Statistics")
print("=" * 70)

print(df[["text_length", "word_count"]].describe())


# ---------------------------------------------------
# Correlation Heatmap
# ---------------------------------------------------

numeric_cols = [
    "text_length",
    "word_count",
    "digit_count",
    "uppercase_count",
    "lowercase_count",
    "special_char_count",
    "whitespace_count",
    "contains_email",
    "contains_url",
    "contains_ip",
    "contains_hex",
    "keyword_count",
]

plt.figure(figsize=(12, 8))

corr = df[numeric_cols].corr(numeric_only=True)

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Feature Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "correlation_heatmap.png",
    dpi=300
)

plt.close()
# ---------------------------------------------------
# Visualization
# ---------------------------------------------------

print("\nGenerating Visualizations...")


# -----------------------------
# Label Distribution
# -----------------------------

plt.figure(figsize=(10,6))

sns.countplot(
    data=df,
    x="label",
    order=df["label"].value_counts().index
)

plt.xticks(rotation=45)

plt.title(
    "Clipboard Dataset Class Distribution"
)

plt.xlabel("Category")

plt.ylabel("Number of Samples")


plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "label_distribution.png",
    dpi=300
)

plt.close()



# -----------------------------
# Class Percentage Pie Chart
# -----------------------------


plt.figure(figsize=(8,8))


df["label"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)


plt.title(
    "Class Distribution Percentage"
)

plt.ylabel("")


plt.savefig(
    FIGURE_DIR / "class_distribution_pie.png",
    dpi=300
)


plt.close()



# -----------------------------
# Text Length Histogram
# -----------------------------


plt.figure(figsize=(10,6))


sns.histplot(
    df["text_length"],
    bins=50,
    kde=True
)


plt.title(
    "Clipboard Text Length Distribution"
)

plt.xlabel(
    "Characters"
)

plt.ylabel(
    "Frequency"
)


plt.tight_layout()


plt.savefig(
    FIGURE_DIR / "text_length_distribution.png",
    dpi=300
)


plt.close()



# -----------------------------
# Text Length Boxplot
# -----------------------------


plt.figure(figsize=(10,5))


sns.boxplot(
    x=df["text_length"]
)


plt.title(
    "Text Length Outlier Detection"
)


plt.savefig(
    FIGURE_DIR / "text_length_boxplot.png",
    dpi=300
)


plt.close()



print("Visualization Completed")

# ---------------------------------------------------
# Save Statistics
# ---------------------------------------------------

stats = []

stats.append("# AI Security Clipboard Guardian")
stats.append("")
stats.append("## Dataset Overview")
stats.append("")
stats.append(f"Shape : {df.shape}")
stats.append("")
stats.append("### Label Distribution")
stats.append("")
stats.append(df["label"].value_counts().to_string())
stats.append("")
stats.append("### Missing Values")
stats.append("")
stats.append(df.isnull().sum().to_string())
stats.append("")
stats.append("### Text Statistics")
stats.append("")
stats.append(
    df[["text_length", "word_count"]]
    .describe()
    .to_string()
)

with open(
    REPORT_DIR / "eda_report.md",
    "w",
    encoding="utf-8"
) as f:

    f.write("\n".join(stats))

print("\nSaved")

print(REPORT_DIR / "eda_report.md")

print("\nPhase 1 Completed Successfully!")

features = [
    "digit_count",
    "uppercase_count",
    "special_char_count",
    "keyword_count",
]

for feature in features:

    plt.figure(figsize=(8,5))

    sns.histplot(
        df[feature],
        bins=30,
        kde=True
    )

    plt.title(feature.replace("_"," ").title())

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / f"{feature}.png",
        dpi=300
    )

    plt.close()

features = [
    "text_length",
    "digit_count",
    "special_char_count",
]

for feature in features:

    plt.figure(figsize=(12,6))

    sns.boxplot(
        data=df,
        x="label",
        y=feature
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / f"{feature}_boxplot.png",
        dpi=300
    )

    plt.close()

Q1 = df["text_length"].quantile(0.25)
Q3 = df["text_length"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[
    (df["text_length"] < lower) |
    (df["text_length"] > upper)
]

print("\nOutlier Analysis")
print("=" * 40)

print("Lower Bound :", lower)
print("Upper Bound :", upper)
print("Outliers    :", len(outliers))

# ---------------------------------------------------
# Overall Word Cloud
# ---------------------------------------------------

print("\nGenerating Word Cloud...")

text = " ".join(df["text"].astype(str))

wc = WordCloud(
    width=1600,
    height=800,
    background_color="white",
    max_words=300
).generate(text)

plt.figure(figsize=(16,8))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title("Overall Word Cloud")

plt.savefig(
    FIGURE_DIR / "wordcloud_overall.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

for label in sorted(df["label"].unique()):

    label_text = " ".join(
        df[df["label"] == label]["text"].astype(str)
    )

    wc = WordCloud(
        width=1400,
        height=700,
        background_color="white",
        max_words=200
    ).generate(label_text)

    plt.figure(figsize=(14,7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(label)

    plt.savefig(
        FIGURE_DIR / f"wordcloud_{label}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    vectorizer = CountVectorizer(
    stop_words="english",
    max_features=20
)

X = vectorizer.fit_transform(df["text"])

counts = X.toarray().sum(axis=0)

words = vectorizer.get_feature_names_out()

freq = (
    pd.DataFrame({
        "word": words,
        "count": counts
    })
    .sort_values("count", ascending=False)
)

plt.figure(figsize=(12,6))

sns.barplot(
    data=freq,
    x="count",
    y="word"
)

plt.title("Top 20 Words")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "top_words.png",
    dpi=300
)

plt.close()

vocabulary = set()

for text in df["text"]:
    vocabulary.update(text.lower().split())

print("\nVocabulary Size")
print("=" * 40)
print(len(vocabulary))