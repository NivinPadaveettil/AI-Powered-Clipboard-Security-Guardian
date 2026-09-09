# AI-Powered Clipboard Security Guardian
## Individual Micro Project – Final Presentation (PPT) (`ppt.md`)

**Submission Deadline:** 10/09/2026  
**Submission Email:** farbeena4517.cs@jawaharlalcolleges.com  

---

## Slide 1: Title Slide

### AI-Powered Clipboard Security Guardian
**Real-Time Sensitive Data Exposure Protection via Transformer-Based NLP & Flask Web Interface**

- **Project Title:** AI-Powered Clipboard Security Guardian
- **Student Name:** [Your Name]
- **Register No.:** [Your Register Number]
- **Course & Branch:** Computer Science & Engineering
- **Institution:** Jawaharlal College of Engineering and Technology

---
> 🎤 **Speaker Notes:**  
> "Good morning/afternoon respected faculty and evaluators. I am presenting my Individual Micro Project titled 'AI-Powered Clipboard Security Guardian'. This project develops a real-time cybersecurity tool using a fine-tuned DistilBERT transformer model and a Flask web interface to detect and prevent confidential data leakage from system clipboards."

---

## Slide 2: Introduction

### Background & Context

- **System Clipboard Role:** The operating system clipboard is a temporary storage buffer used constantly by users to copy and paste text.
- **Unprotected Buffer:** Default operating systems (Windows, macOS, Linux) store clipboard data in unencrypted plain text until manually overwritten or cleared upon system reboot.
- **Common Clipboard Content:** Users routinely copy passwords, API tokens, credit card numbers, OTPs, SSH private keys, and database connection strings.
- **Security Gap:** Traditional security software monitors files and network traffic but ignores memory-resident clipboard content, leaving a critical attack surface open to unauthorized access, clipboard hijacker malware, and accidental pasting into untrusted platforms.

---
> 🎤 **Speaker Notes:**  
> "To introduce the topic: while firewalls and antivirus tools protect files and network traffic, the system clipboard remains completely unmonitored. Users frequently copy sensitive secrets that remain in plain text memory, exposing organizations and individuals to severe data leakage risks."

---

## Slide 3: Problem Statement

### The Danger of Accidental Sensitive Data Exposure

- **Accidental Leakage Vector:** Sensitive credentials pasted into public AI chatbots, shared code repositories (Git), messaging apps, or video-sharing screens.
- **Clipboard Sniffer Malware:** Malicious background applications that silently extract clipboard text to hijack crypto wallets and steal user login credentials.
- **Lack of Real-Time Remediation:** Standard security frameworks offer no automated mechanism to identify data sensitivity level or auto-purge dangerous content after temporary usage.

### Key Research Question
> **How can we build an intelligent, real-time AI guardian that automatically intercepts clipboard content, classifies sensitive data categories, calculates exposure risk, and sanitizes dangerous text before confidentiality is compromised?**

---
> 🎤 **Speaker Notes:**  
> "Our problem statement addresses the lack of real-time monitoring and dynamic sanitization for clipboard data. The key challenge is detecting sensitive data instantly (<10ms) without interfering with user productivity, and purging high-risk secrets before they can be compromised."

---

## Slide 4: Objectives

### Core Goals & System Deliverables

1. **Real-time Clipboard Polling:** Build a background listener thread to intercept clipboard text updates instantly.
2. **Transformer NLP Classification:** Fine-tune a lightweight **DistilBERT** model to categorize text into 8 distinct sensitivity classes.
3. **Exploratory Data Analysis & Preprocessing:** Process a dataset of 56,359 records with statistical feature extraction and tokenization.
4. **Dynamic Risk Engine:** Map model predictions to a granular Risk Scoring Engine (Risk Scores 0–100, Levels: Low, Medium, High, Critical).
5. **Automated Sanitization:** Implement a thread-safe auto-clear timer to purge sensitive data (10s – 30s timeouts).
6. **Flask Web Application:** Develop a web interface for real-time security dashboard monitoring, event logging, and analytical reporting.
7. **SQLite Security Logging:** Store detection metadata (excluding raw text) in an audit database.

---
> 🎤 **Speaker Notes:**  
> "The objectives of this micro project are to create an end-to-end pipeline: from data generation and DistilBERT fine-tuning to building a dynamic risk engine, automated clipboard sanitization, an SQLite audit log, and a Flask web application interface."

---

## Slide 5: Dataset Description

### Dataset Overview & Metadata

- **Dataset Source:** Custom synthetic security dataset generation pipeline (`src/generators/`) merged with curated security corpora (API keys, JWTs, SSH keys, DB strings, passwords, OTPs, payment data, safe text).
- **Number of Records/Samples:** **56,359 samples**
- **Number of Features:** **14 features** (1 text feature, 1 target label, 12 engineered numerical/boolean features)
- **Target Variable:** `label` (Categorical, 8 distinct classes)
- **Brief Description:** A comprehensive NLP cybersecurity dataset representing real-world clipboard text snippets with varied sequence lengths, entropy levels, digit ratios, and keyword patterns.

#### Feature Name & Description Table

| Feature Name | Type | Description |
| :--- | :--- | :--- |
| **`text`** | String | Raw clipboard text snippet sample |
| **`label`** | Categorical | **Target Variable** (8 categories) |
| **`text_length`** | Integer | Total character count in the string |
| **`word_count`** | Integer | Total count of whitespace-delimited words |
| **`digit_count`** | Integer | Number of numerical digits (0-9) |
| **`uppercase_count`** | Integer | Number of uppercase alphabetical letters |
| **`lowercase_count`** | Integer | Number of lowercase alphabetical letters |
| **`special_char_count`**| Integer | Count of non-alphanumeric special characters |
| **`whitespace_count`** | Integer | Count of space, tab, and newline characters |
| **`contains_email`** | Boolean (0/1)| Indicator flag if an email address is detected |
| **`contains_url`** | Boolean (0/1)| Indicator flag if a Web URL/URI is detected |
| **`contains_ip`** | Boolean (0/1)| Indicator flag if an IPv4/IPv6 address is present |
| **`contains_hex`** | Boolean (0/1)| Indicator flag if a hexadecimal token is present |
| **`keyword_count`** | Integer | Count of security-relevant keywords detected |

#### Target Class Distribution

| Class Name (`label`) | Record Count | Percentage | Class Description |
| :--- | :---: | :---: | :--- |
| **`payment`** | 10,000 | 17.74% | Credit card numbers, CVVs, expiry dates |
| **`otp`** | 9,999 | 17.74% | One-Time Passwords, 2FA auth codes |
| **`api_key`** | 9,926 | 17.61% | AWS, Stripe, GitHub, Google API tokens |
| **`db_credentials`** | 8,571 | 15.21% | Connection URIs, MySQL/Postgres credentials |
| **`password`** | 6,685 | 11.86% | Complex user passwords & credential hashes |
| **`safe`** | 6,104 | 10.83% | Standard plain text, public code, URLs |
| **`ssh_key`** | 3,335 | 5.92% | OpenSSH / RSA / ED25519 private keys |
| **`jwt`** | 1,739 | 3.09% | JSON Web Tokens (`eyJ...`) |
| **Total** | **56,359** | **100.00%** | **Full Multi-Class Dataset** |

---
> 🎤 **Speaker Notes:**  
> "The dataset contains 56,359 samples across 14 attributes. The target variable 'label' spans 8 security classes: payment details, OTPs, API keys, database credentials, passwords, safe text, SSH keys, and JWT tokens."

---

## Slide 6: Data Preprocessing & Exploratory Data Analysis (EDA)

### Data Preparation & Exploratory Data Analysis Pipeline

- **Handling Missing Values:** Inspected all 56,359 rows across all 14 features; confirmed **0 missing (null/NaN) values** present.
- **Removing Duplicates & Outliers:** Deduplicated identical text samples to prevent data leakage between splits; removed anomalous text fragments exceeding sequence boundaries (>1,361 chars).
- **Data Cleaning:** Lowercasing, whitespace trimming, label mapping serialization to `label_mapping.json` (mapping text labels to integer class IDs `0` through `7`).
- **Encoding Categorical Data:** Target label `label` mapped to numerical tensor representation `label_id`.
- **Feature Scaling & Normalization:** Statistical text features (length, word count, character densities) scaled using standard scaling for EDA visualizations.
- **Train-Test-Validation Split:** Stratified 80 / 10 / 10 split ratio:
  - **Train Set:** 45,087 samples (80%)
  - **Validation Set:** 5,636 samples (10%)
  - **Test Set:** 5,636 samples (10%)

#### EDA Key Statistical Summary & Observations

| Metric / Attribute | Text Length (`text_length`) | Word Count (`word_count`) |
| :--- | :---: | :---: |
| **Mean** | 89.37 characters | 4.26 words |
| **Standard Deviation** | 225.14 characters | 5.83 words |
| **Minimum** | 3.00 characters | 1.00 word |
| **25th Percentile (Q1)** | 20.00 characters | 1.00 word |
| **50th Percentile (Median)** | 40.00 characters | 1.00 word |
| **75th Percentile (Q3)** | 60.00 characters | 5.00 words |
| **Maximum** | 1,361.00 characters | 28.00 words |

#### EDA Visual Key Observations:
1. **High Character Density in Secrets:** Categories like `api_key`, `jwt`, and `ssh_key` exhibit high special character and uppercase density compared to `safe` text.
2. **Short Word Count:** Over 50% of sensitive clipboard instances contain $\le 5$ words, reflecting key-value pairs, tokens, and single-string credentials.

---
> 🎤 **Speaker Notes:**  
> "For preprocessing and EDA: we verified zero missing values, performed data cleaning, mapped categorical labels to numerical IDs, and split the data into 80% training, 10% validation, and 10% test sets. Key EDA observations showed high special character density and low word counts for sensitive tokens."

---

## Slide 7: Machine Learning Algorithm

### Transformer Backbone: Fine-Tuned DistilBERT (`distilbert-base-uncased`)

- **Model Choice:** `DistilBertForSequenceClassification`
- **Why DistilBERT?**
  - **Speed & Efficiency:** 40% smaller and 60% faster than BERT-base while retaining 95% of language comprehension capabilities.
  - **Low Latency:** Inference runs in `<10ms` on CPU/GPU, ensuring real-time clipboard monitoring without system lag.
  - **Deep Contextual Awareness:** Attention mechanisms capture complex key-value structures, SSH headers, and token patterns that regex alone fails to catch.

#### Model Specifications & Architecture

```
Input Clipboard Text Snippet
         │
         ▼
DistilBertTokenizerFast (max_length=128 tokens, truncation=True)
         │
         ▼
DistilBERT Base Architecture (6 Transformer Layers, 768 Hidden Dim, 12 Attention Heads, 66M Params)
         │
         ▼
Pooled Output Dropout Layer (p = 0.2)
         │
         ▼
Linear Sequence Classification Head (768 Dim ──> 8 Output Class Logits)
         │
         ▼
Softmax Probability Activation ──> Predicted Class Label & Confidence Score
```

---
> 🎤 **Speaker Notes:**  
> "We chose DistilBERT as our machine learning backbone. DistilBERT is a lightweight transformer model with 66 million parameters. It provides deep contextual language understanding with sub-10 millisecond inference speed, perfectly suited for real-time clipboard monitoring."

---

## Slide 8: Model Training & Testing

### Fine-Tuning Setup & Hyperparameter Configuration

- **Framework:** PyTorch & Hugging Face `Trainer` API
- **Tokenization Strategy:** Tokenized with `DistilBertTokenizerFast`, capped at `max_length=128` tokens. Dynamic batch padding via `DataCollatorWithPadding`.
- **Handling Class Imbalance:** Computed balanced class loss weights using Scikit-Learn `compute_class_weight`:
  $$\text{weight}_j = \frac{N_{\text{samples}}}{N_{\text{classes}} \times N_j}$$
- **Hardware Acceleration:** PyTorch FP16 Mixed Precision training enabled on NVIDIA CUDA GPU.

#### Training Hyperparameters Summary

| Hyperparameter | Value / Setting | Description |
| :--- | :--- | :--- |
| **Base Model** | `distilbert-base-uncased` | Pre-trained Transformer Backbone |
| **Number of Epochs** | `4 Epochs` | Full training passes over 45,087 train samples |
| **Learning Rate** | `2e-5` ($2 \times 10^{-5}$) | AdamW Optimizer initial learning rate |
| **Weight Decay** | `0.01` | L2 Regularization parameter |
| **Batch Size** | `16 per device` | Training and Evaluation batch size |
| **Evaluation Strategy** | `per epoch` | Evaluates validation metrics after each epoch |
| **Best Model Metric** | `F1-Score` | Saves checkpoint with highest Validation F1 |

---
> 🎤 **Speaker Notes:**  
> "The model was fine-tuned for 4 epochs using the Hugging Face Trainer API, an AdamW optimizer with learning rate 2e-5, FP16 mixed precision, and balanced class loss weighting to handle class support differences."

---

## Slide 9: Model Evaluation

### Outstanding Test Performance Across 5,636 Test Samples

- **Evaluation Metrics:** Evaluated on the unseen test dataset using standard classification metrics:
  - **Accuracy:** **1.00 (100.00%)**
  - **Weighted Precision:** **1.00 (100.00%)**
  - **Weighted Recall:** **1.00 (100.00%)**
  - **Weighted F1-Score:** **1.00 (100.00%)**

#### Class-Wise Classification Performance Table

| Class Label (`label`) | Precision | Recall | F1-Score | Test Support | Evaluation Result |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`api_key`** | 1.00 | 1.00 | 1.00 | 993 | Perfect |
| **`db_credentials`** | 1.00 | 1.00 | 1.00 | 857 | Perfect |
| **`jwt`** | 1.00 | 1.00 | 1.00 | 174 | Perfect |
| **`otp`** | 1.00 | 1.00 | 1.00 | 1,000 | Perfect |
| **`password`** | 1.00 | 1.00 | 1.00 | 668 | Perfect |
| **`payment`** | 1.00 | 1.00 | 1.00 | 1,000 | Perfect |
| **`safe`** | 1.00 | 1.00 | 1.00 | 611 | Perfect |
| **`ssh_key`** | 1.00 | 1.00 | 1.00 | 333 | Perfect |
| **Overall Summary** | **1.00** | **1.00** | **1.00** | **5,636** | **Optimal Performance** |

#### Metric Formula Definitions
$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}, \quad \text{Precision} = \frac{TP}{TP + FP}$$
$$\text{Recall} = \frac{TP}{TP + FN}, \quad \text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

---
> 🎤 **Speaker Notes:**  
> "Model evaluation on 5,636 test samples yielded 100% Accuracy, Precision, Recall, and F1-score across all 8 classes. The distinct structure of API keys, SSH keys, JWT tokens, and passwords allows our DistilBERT model to classify sensitive content with zero errors."

---

## Slide 10: Flask Web Application

### Web Workflow, Architecture & Interface Overview

- **Framework:** Flask (Python Web Framework) + Jinja2 HTML Templates + Bootstrap CSS
- **System Role:** Provides a browser-based dashboard for real-time monitoring, visual alert inspection, and historical reporting.

#### Flask Web Architecture Workflow

```
+------------------------+      HTTP Requests      +------------------------+
|  User Web Browser      |  <------------------->  |   Flask Web Server     |
|  (Live Dashboard GUI)  |    GET / , GET /api     |   (Python / WSGI App)  |
+------------------------+                         +------------------------+
                                                               │
                                                               ▼
                                                   +------------------------+
                                                   | SQLite Logger Backend  |
                                                   | (clipboard_guardian.db)|
                                                   +------------------------+
```

#### Key Web Application Features:
1. **Live System Dashboard (`/`):** Real-time monitoring status, total detection counter, risk severity breakdown cards (Critical, High, Medium, Safe).
2. **Detection Event Feed:** Displays recent clipboard detections with class label badges, confidence scores, and assigned risk levels.
3. **Audit History Viewer (`/history`):** Complete table of all logged security events with category filters and search bar.
4. **Analytics Summary (`/analytics`):** Interactive visualization of category frequencies and confidence averages.

---
> 🎤 **Speaker Notes:**  
> "Slide 10 presents our Flask Web Application. Built with Flask and Bootstrap, the web application exposes a browser dashboard that allows security administrators to view live clipboard events, inspect risk scores, filter historical logs, and track threat trends."

---

## Slide 11: Results & Output

### Real-Time Detection, Risk Scoring & Sanitization Results

- **Risk Engine Matrix (`src/core/risk_scoring.py`):** Automatically maps predicted classes to risk scores (0–100) and auto-clear sanitization timers.

#### Risk Scoring & Action Results Matrix

| Detected Category | Assigned Risk Level | Risk Score | Prescribed Action | Auto-Clear Timeout |
| :--- | :---: | :---: | :--- | :---: |
| **`password`** | **Critical** | **100** | Clear clipboard immediately | **15 seconds** |
| **`ssh_key`** | **Critical** | **100** | Clear clipboard immediately | **10 seconds** |
| **`api_key`** | **Critical** | **95** | Clipboard will be cleared | **15 seconds** |
| **`jwt`** | **Critical** | **95** | Clipboard will be cleared | **20 seconds** |
| **`db_credentials`**| **High** | **90** | Clipboard will be cleared | **20 seconds** |
| **`payment`** | **High** | **90** | Clipboard will be cleared | **20 seconds** |
| **`otp`** | **Medium** | **70** | Clear after temporary use | **30 seconds** |
| **`safe`** | **Low** | **0** | No action required | **None (0s)** |

#### Output Execution Walkthrough:
1. **User copies SSH Key:** `-----BEGIN OPENSSH PRIVATE KEY-----...`
2. **Model Prediction:** Category: `ssh_key`, Confidence: `0.9998`
3. **Risk Scoring Result:** Level: **Critical**, Score: **100**
4. **Action Output:** System triggers 10-second auto-clear timer; thread purges clipboard; SQLite logs event metadata.
5. **Dashboard Output:** Flask web UI and PyQt6 desktop UI display updated Critical alert counter.

---
> 🎤 **Speaker Notes:**  
> "The outputs demonstrate how classification triggers real-time protection: when an SSH key or password is copied, the risk engine assigns a Critical score of 100, displays an alert, and purges the text within 10 to 15 seconds."

---

## Slide 12: Conclusion

### Summary of Project Achievements

- **Successful Real-Time Security Tool:** Successfully engineered an AI-powered clipboard guardian that eliminates the silent threat of clipboard data exposure.
- **High-Accuracy AI Detection:** Fine-tuned DistilBERT model achieved **100% Accuracy, Precision, Recall, and F1-score** across 8 security categories.
- **Automated Protection:** Implemented thread-safe, dynamic sanitization that automatically purges sensitive credentials (passwords, SSH keys, API keys, OTPs) after designated timeouts.
- **User-Friendly Monitoring Interface:** Developed a Flask Web Interface and PyQt6 Desktop GUI alongside an privacy-centric SQLite audit database (zero raw text stored).

---
> 🎤 **Speaker Notes:**  
> "To conclude: this micro project successfully proves that lightweight transformer NLP models can be deployed locally for real-time cybersecurity defense, providing automated protection against accidental sensitive data leaks."

---

## Slide 13: Future Scope

### Potential Enhancements & Next Steps

1. **OCR Image Clipboard Scanning:** Extend detection from plain text to screenshots and image buffers containing visible credentials using Tesseract OCR.
2. **Context-Aware Whitelisting:** Implement application-specific rules (e.g., allow copying passwords into password manager applications, but block pasting into browsers).
3. **Native OS System Tray & Push Alerts:** Build native desktop tray icons with OS-level toast notifications for Windows, macOS, and Linux.
4. **Enterprise Central Telemetry:** Integrate Flask backend with SIEM security platforms (Splunk, Elastic Stack, Microsoft Sentinel) for centralized enterprise monitoring.

---
> 🎤 **Speaker Notes:**  
> "Future scope includes expanding detection to image screenshots via OCR, adding application whitelisting rules, providing native OS tray popups, and integrating telemetry into enterprise SIEM systems."

---

## Slide 14: References

### Academic Papers, Technical Documentation & Frameworks

1. Sanh, V., Debut, L., Chaumond, J., & Wolf, T. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter*. arXiv preprint arXiv:1910.01108.
2. Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). *BERT: Pre-training of deep bidirectional transformers for language understanding*. arXiv preprint arXiv:1810.04805.
3. Hugging Face Documentation. (2024). *Transformers: State-of-the-art Natural Language Processing*. https://huggingface.co/docs/transformers
4. Flask Documentation. (2024). *Flask Web Development Framework (v3.x)*. Pallets Projects. https://flask.palletsprojects.com/
5. PyTorch Documentation. (2024). *PyTorch Ecosystem for Machine Learning*. Meta AI. https://pytorch.org/
6. Scikit-learn Developers. (2024). *Scikit-learn: Machine Learning in Python*. https://scikit-learn.org/
7. OWASP Foundation. (2023). *OWASP Top 10 Sensitive Data Exposure & API Security Top 10*. https://owasp.org/

---
> 🎤 **Speaker Notes:**  
> "Slide 14 lists the primary academic and technical references used in this project, including the DistilBERT paper by Sanh et al., Hugging Face Transformers, PyTorch, Flask, and OWASP security guidelines. Thank you for your time, and I am now open to your questions."
