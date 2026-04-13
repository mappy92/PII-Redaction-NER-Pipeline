---
title: Canadian Banking PII Redactor
emoji: 🏦
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
---

# 🏦 Canadian Banking Document PII Redactor

> **Live Demo:** [PII Redaction for banking](https://pii-redaction-ner-pipeline.streamlit.app/)

Production-style NLP pipeline that detects and redacts PII from Canadian
banking documents using fine-tuned spaCy NER + regex fallback.

Mirrors real-world financial institution redaction workflows for KYC, AML,
wire transfers, and loan applications.

---

## Entity Types

| Label         | Example                          | Layer         |
|---------------|----------------------------------|---------------|
| PERSON        | Sarah Kowalski                   | spaCy NER     |
| ORG           | TD Bank, Royal Bank of Canada    | spaCy NER     |
| EMAIL         | sarah.k@gmail.com                | spaCy + regex |
| PHONE         | 416-555-0192                     | spaCy + regex |
| ACCOUNT_NO    | 00152-004-7823941                | Regex         |
| TRANSIT_NO    | 00152-004                        | Regex         |
| CREDIT_CARD   | 4532-1234-5678-9012              | Regex         |
| SIN           | 482-716-930                      | Regex         |
| POSTAL_CODE   | M5V 2H1                          | Regex         |
| ADDRESS       | 47 Lakeshore Blvd W, Toronto ON  | spaCy NER     |
| DOB           | 1984-07-22                       | Regex         |
| AMOUNT        | $42,500.00                       | Regex         |
| SWIFT         | TDOMCATTTOR                      | Regex         |

---

## Document Types

1. KYC Form :  Customer onboarding
2. Wire Transfer Request :  SWIFT / domestic
3. Personal Loan Application
4. Account Statement Header
5. SAR Memo :  Suspicious Activity Report (AML)
6. Customer Complaint Letter

---

## Data Sources

| Source | Used For | Licence |
|--------|----------|---------|
| [Ontario Top Baby Names](https://data.ontario.ca/dataset/eb4c585c-6ada-4de7-8ff1-e876fb1a6b0b) | Real Canadian first names | Open Government Licence Ontario |
| Faker (en_CA) | Addresses, phones, emails | MIT |
| Custom generator | Banking document templates | N/A |

**All training data is 100% synthetic. No real PII used.**

---

## Run Locally

```bash
git clone https://github.com/your-username/pii-redaction-ner-pipeline
cd pii-redaction-ner-pipeline
conda env create -f environment.yml
conda activate pii-ner-pipeline
streamlit run app.py
```

---

## Author

**Manpreet Singh** :  Data Scientist
[LinkedIn](https://linkedin.com/in/manpreet-singh-ds) · [Portfolio](https://mappy92.github.io)
