"""
PII Redaction NER Pipeline — BANKING DOMAIN
Project Setup Script

Usage:
    python setup_project.py

What it creates:
    pii-redaction-ner-pipeline/
    ├── All folders
    ├── 4 Jupyter notebooks (banking domain)
    ├── src/regex_patterns.py   (Canadian banking patterns)
    ├── src/redactor.py
    ├── src/document_generator.py  ← 6 banking document types
    ├── app.py                  (Streamlit UI)
    ├── requirements.txt
    ├── environment.yml
    ├── README.md               (HF Spaces ready)
    ├── .gitignore
    └── docs/model_card.md + audit_trail.md
"""

import os

ROOT = "pii-redaction-ner-pipeline"

FOLDERS = [
    "data/raw",
    "data/synthetic",
    "data/annotated",
    "notebooks",
    "src",
    "model",
    "docs",
]

GITIGNORE = """\
data/raw/
data/synthetic/
data/annotated/
model/
__pycache__/
*.pyc
.env
.venv/
venv/
*.egg-info/
.ipynb_checkpoints/
.DS_Store
Thumbs.db
"""

README = """\
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

> **Live Demo:** [your-username-pii-redaction-ner-pipeline.hf.space](https://huggingface.co/spaces)

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

1. KYC Form — Customer onboarding
2. Wire Transfer Request — SWIFT / domestic
3. Personal Loan Application
4. Account Statement Header
5. SAR Memo — Suspicious Activity Report (AML)
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

**Manpreet Singh** — Data Scientist
[LinkedIn](https://linkedin.com/in/manpreet-singh-ds) · [Portfolio](https://mappy92.github.io)
"""

REQUIREMENTS = """\
spacy>=3.7.0
https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.7.3/en_core_web_trf-3.7.3-py3-none-any.whl
faker>=24.0.0
pandas>=2.0.0
numpy>=1.26.0
requests>=2.31.0
streamlit>=1.32.0
scikit-learn>=1.4.0
matplotlib>=3.8.0
seaborn>=0.13.0
huggingface_hub>=0.21.0
"""

ENVIRONMENT_YML = """\
name: pii-ner-pipeline
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - ipykernel
  - jupyter
  - notebook
  - pip:
    - spacy>=3.7.0
    - https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.7.3/en_core_web_trf-3.7.3-py3-none-any.whl
    - faker>=24.0.0
    - pandas>=2.0.0
    - numpy>=1.26.0
    - requests>=2.31.0
    - streamlit>=1.32.0
    - scikit-learn>=1.4.0
    - matplotlib>=3.8.0
    - seaborn>=0.13.0
    - huggingface_hub>=0.21.0
"""

REGEX_PATTERNS = r'''"""
src/regex_patterns.py
Regex fallback layer for Canadian banking PII.
Catches structured formats that NER handles poorly (account numbers, SINs, cards).
"""

import re
from typing import List, Tuple

PATTERNS: List[Tuple[str, re.Pattern]] = [

    # Canadian bank account number: transit(5)-institution(3)-account(7+)
    ("ACCOUNT_NO", re.compile(
        r"\b\d{5}-\d{3}-\d{6,12}\b"
    )),

    # Transit / routing: 5-digit-dash-3-digit or 9-digit MICR
    ("TRANSIT_NO", re.compile(
        r"\b\d{5}-(?:002|003|004|006|010|016|030|039)\b"
        r"|\b0\d{8}\b"
    )),

    # Credit/debit card: 16 digits with spaces or dashes
    ("CREDIT_CARD", re.compile(
        r"\b(?:\d{4}[\s\-]?){3}\d{4}\b"
    )),

    # SIN: 3-3-3 with space or dash
    ("SIN", re.compile(
        r"\b[1-9]\d{2}[\s\-]\d{3}[\s\-]\d{3}\b"
    )),

    # Canadian phone
    ("PHONE", re.compile(
        r"\b(\+?1[\s\-\.])?\(?\d{3}\)?[\s\-\.]\d{3}[\s\-\.]\d{4}\b"
    )),

    # Email
    ("EMAIL", re.compile(
        r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"
    )),

    # Canadian postal code: A1A 1A1
    ("POSTAL_CODE", re.compile(
        r"\b[A-Z]\d[A-Z][\s]?\d[A-Z]\d\b"
    )),

    # Date of birth (ISO, slashed, or written)
    ("DOB", re.compile(
        r"\b\d{4}[\-/]\d{2}[\-/]\d{2}\b"
        r"|\b\d{1,2}[/\-]\d{1,2}[/\-]\d{4}\b"
        r"|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b"
    )),

    # Dollar amounts
    ("AMOUNT", re.compile(
        r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
        r"|\bCAD\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
    )),

    # SWIFT/BIC (Canadian — contains CA)
    ("SWIFT", re.compile(
        r"\b[A-Z]{4}CA[A-Z0-9]{2}(?:[A-Z0-9]{3})?\b"
    )),
]


def regex_find(text: str) -> List[Tuple[int, int, str]]:
    """Return list of (start, end, label) for all regex matches."""
    found = []
    for label, pattern in PATTERNS:
        for m in pattern.finditer(text):
            found.append((m.start(), m.end(), label))
    return found


def _overlaps(a, b) -> bool:
    return a[0] < b[1] and b[0] < a[1]


def deduplicate(entities):
    """Remove overlapping spans, keep the longer one."""
    sorted_ents = sorted(entities, key=lambda x: (x[0], -(x[1] - x[0])))
    kept = []
    for ent in sorted_ents:
        if not any(_overlaps(ent, k) for k in kept):
            kept.append(ent)
    return kept
'''

DOCUMENT_GENERATOR = r'''"""
src/document_generator.py

6 Canadian banking document templates with auto-extracted PII spans.
All data is 100% synthetic — seeded with real Ontario name data.

Document types:
  1. KYC Form
  2. Wire Transfer Request
  3. Personal Loan Application
  4. Account Statement Header
  5. SAR Memo (AML)
  6. Customer Complaint Letter
"""

import random
import string
from datetime import date, timedelta
from faker import Faker

fake = Faker("en_CA")

CANADIAN_BANKS = [
    "Royal Bank of Canada", "TD Bank", "Bank of Nova Scotia",
    "Bank of Montreal", "CIBC", "National Bank of Canada",
    "Desjardins Group", "HSBC Canada", "Laurentian Bank",
    "Canadian Western Bank",
]

CANADIAN_CITIES_PROV = {
    "Toronto": "ON", "Ottawa": "ON", "Mississauga": "ON",
    "Brampton": "ON", "Hamilton": "ON", "London": "ON",
    "Markham": "ON", "Kitchener": "ON", "Windsor": "ON",
    "Calgary": "AB", "Edmonton": "AB",
    "Vancouver": "BC",
    "Montreal": "QC",
    "Halifax": "NS",
}
CITIES = list(CANADIAN_CITIES_PROV.keys())

INST_CODES = ["002", "003", "004", "006", "010", "016"]


# ── Helpers ────────────────────────────────────────────────────────────────────

def ca_phone():
    ac = random.choice(["416","647","437","905","519","613","604","403","780","514"])
    return f"{ac}-{random.randint(200,999)}-{random.randint(1000,9999)}"

def account_no():
    return f"{random.randint(10000,99999)}-{random.choice(INST_CODES)}-{random.randint(1000000,9999999)}"

def transit_no():
    return f"{random.randint(10000,99999)}-{random.choice(INST_CODES)}"

def ca_sin():
    return f"{random.randint(100,899)}-{random.randint(100,999)}-{random.randint(100,999)}"

def ca_card():
    g = [str(random.randint(4000,4999))] + [str(random.randint(1000,9999)) for _ in range(3)]
    return "-".join(g)

def ca_dob():
    s = date(1955,1,1)
    return (s + timedelta(days=random.randint(0,(date(2000,12,31)-s).days))).isoformat()

def ca_postal(prov="ON"):
    prefix = {"ON": random.choice(["M","L","K","N","P"]),
               "BC": "V", "AB": "T", "QC": "H", "NS": "B"}
    safe = "ABCEGHJKLMNPRSTVWXYZ"
    p = prefix.get(prov, "M")
    return f"{p}{random.randint(0,9)}{random.choice(safe)} {random.randint(0,9)}{random.choice(safe)}{random.randint(0,9)}"

def dollars(lo, hi):
    return f"${random.randint(lo,hi):,}.00"

def find_span(text, value):
    idx = text.find(str(value))
    return None if idx == -1 else (idx, idx + len(str(value)))

def collect(text, pairs):
    ents = []
    for value, label in pairs:
        span = find_span(text, str(value))
        if span:
            ents.append((span[0], span[1], label))
    return ents


# ── Document generators ────────────────────────────────────────────────────────

def gen_kyc_form(names=None):
    name  = random.choice(names) if names else fake.name()
    email = fake.email()
    phone = ca_phone()
    city  = random.choice(CITIES)
    prov  = CANADIAN_CITIES_PROV[city]
    pc    = ca_postal(prov)
    addr  = f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    s     = ca_sin()
    dob   = ca_dob()
    bank  = random.choice(CANADIAN_BANKS)
    acct  = account_no()
    tr    = transit_no()

    text = f"""CUSTOMER IDENTIFICATION FORM (KYC)
{bank}
─────────────────────────────────────
Full Legal Name:    {name}
Date of Birth:      {dob}
Social Insurance:   {s}
Primary Address:    {addr}
Phone Number:       {phone}
Email Address:      {email}

Account Number:     {acct}
Transit Number:     {tr}
Institution:        {bank}

I certify the above information is accurate.
Signature: ________________    Date: {date.today().isoformat()}
"""
    return {"text": text, "doc_type": "KYC",
            "entities": collect(text, [
                (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
                (addr,"ADDRESS"),(s,"SIN"),(dob,"DOB"),
                (bank,"ORG"),(acct,"ACCOUNT_NO"),(tr,"TRANSIT_NO"),(pc,"POSTAL_CODE"),
            ])}


def gen_wire_transfer(names=None):
    sender   = random.choice(names) if names else fake.name()
    receiver = random.choice(names) if names else fake.name()
    s_email  = fake.email()
    s_phone  = ca_phone()
    s_acct   = account_no()
    r_acct   = account_no()
    amount   = dollars(500, 250000)
    bank_from = random.choice(CANADIAN_BANKS)
    bank_to   = random.choice(CANADIAN_BANKS)
    swift     = f"{''.join(random.choices(string.ascii_uppercase,k=4))}CA{''.join(random.choices('ABCDEFGHJKLMNPRSTUVWXYZ23456789',k=2))}"
    ref       = f"WR-{''.join(random.choices(string.digits,k=8))}"
    city      = random.choice(CITIES)
    prov      = CANADIAN_CITIES_PROV[city]
    pc        = ca_postal(prov)

    text = f"""WIRE TRANSFER REQUEST — {bank_from}
Reference: {ref}
─────────────────────────────────────
SENDER
Name:               {sender}
Email:              {s_email}
Phone:              {s_phone}
Account Number:     {s_acct}
Bank:               {bank_from}

RECIPIENT
Beneficiary Name:   {receiver}
Account Number:     {r_acct}
Bank:               {bank_to}
SWIFT / BIC:        {swift}
Postal Code:        {pc}

TRANSFER DETAILS
Amount:             {amount} CAD
Authorization Date: {date.today().isoformat()}

Subject to FINTRAC reporting requirements.
"""
    return {"text": text, "doc_type": "WIRE_TRANSFER",
            "entities": collect(text, [
                (sender,"PERSON"),(receiver,"PERSON"),
                (s_email,"EMAIL"),(s_phone,"PHONE"),
                (s_acct,"ACCOUNT_NO"),(r_acct,"ACCOUNT_NO"),
                (bank_from,"ORG"),(bank_to,"ORG"),
                (swift,"SWIFT"),(amount,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


def gen_loan_application(names=None):
    name     = random.choice(names) if names else fake.name()
    email    = fake.email()
    phone    = ca_phone()
    city     = random.choice(CITIES)
    prov     = CANADIAN_CITIES_PROV[city]
    pc       = ca_postal(prov)
    addr     = f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    s        = ca_sin()
    dob      = ca_dob()
    bank     = random.choice(CANADIAN_BANKS)
    acct     = account_no()
    req_amt  = dollars(5000, 500000)
    income   = dollars(40000, 250000)
    employer = fake.company()

    text = f"""PERSONAL LOAN APPLICATION
{bank}
─────────────────────────────────────
APPLICANT INFORMATION
Full Name:          {name}
Date of Birth:      {dob}
SIN:                {s}
Address:            {addr}
Phone:              {phone}
Email:              {email}

EMPLOYMENT
Employer:           {employer}
Annual Income:      {income}

LOAN REQUEST
Requested Amount:   {req_amt}
Purpose:            Personal / home improvement
Existing Account:   {acct}

By submitting, the applicant authorizes {bank} to verify all information.
"""
    return {"text": text, "doc_type": "LOAN_APPLICATION",
            "entities": collect(text, [
                (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
                (addr,"ADDRESS"),(s,"SIN"),(dob,"DOB"),
                (bank,"ORG"),(employer,"ORG"),
                (acct,"ACCOUNT_NO"),(req_amt,"AMOUNT"),(income,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


def gen_account_statement(names=None):
    name    = random.choice(names) if names else fake.name()
    email   = fake.email()
    city    = random.choice(CITIES)
    prov    = CANADIAN_CITIES_PROV[city]
    pc      = ca_postal(prov)
    addr    = f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    bank    = random.choice(CANADIAN_BANKS)
    acct    = account_no()
    card    = ca_card()
    balance = dollars(0, 150000)
    avail   = dollars(0, 50000)

    text = f"""{bank}
MONTHLY ACCOUNT STATEMENT
─────────────────────────────────────
Account Holder:     {name}
Mailing Address:    {addr}
Email on File:      {email}

Account Number:     {acct}
Linked Card:        {card}

Period: {date.today().replace(day=1).isoformat()} to {date.today().isoformat()}
Closing Balance:    {balance}
Available Credit:   {avail}

For questions contact {bank} customer service.
"""
    return {"text": text, "doc_type": "ACCOUNT_STATEMENT",
            "entities": collect(text, [
                (name,"PERSON"),(email,"EMAIL"),
                (addr,"ADDRESS"),(bank,"ORG"),
                (acct,"ACCOUNT_NO"),(card,"CREDIT_CARD"),
                (balance,"AMOUNT"),(avail,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


def gen_sar_memo(names=None):
    subject  = random.choice(names) if names else fake.name()
    analyst  = random.choice(names) if names else fake.name()
    phone    = ca_phone()
    email    = fake.email()
    city     = random.choice(CITIES)
    prov     = CANADIAN_CITIES_PROV[city]
    pc       = ca_postal(prov)
    addr     = f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    bank     = random.choice(CANADIAN_BANKS)
    acct     = account_no()
    amount   = dollars(10000, 500000)
    s        = ca_sin()
    ref      = f"SAR-{date.today().year}-{''.join(random.choices(string.digits,k=6))}"

    text = f"""SUSPICIOUS ACTIVITY REPORT (SAR)
CONFIDENTIAL — AML COMPLIANCE
{bank}
─────────────────────────────────────
Report Reference:   {ref}
Date Filed:         {date.today().isoformat()}
Prepared By:        {analyst}

SUBJECT INFORMATION
Subject Name:       {subject}
Known Address:      {addr}
Phone:              {phone}
Email:              {email}
SIN on File:        {s}

ACCOUNT DETAILS
Account Number:     {acct}
Institution:        {bank}

SUSPICIOUS ACTIVITY
Transaction Amount: {amount}
Narrative: Multiple large cash deposits inconsistent with
           customer profile. Flagged for FINTRAC review.

Tipping off the subject is prohibited under PCMLTFA.
"""
    return {"text": text, "doc_type": "SAR_MEMO",
            "entities": collect(text, [
                (subject,"PERSON"),(analyst,"PERSON"),
                (email,"EMAIL"),(phone,"PHONE"),
                (addr,"ADDRESS"),(s,"SIN"),
                (bank,"ORG"),(acct,"ACCOUNT_NO"),
                (amount,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


def gen_complaint_letter(names=None):
    name  = random.choice(names) if names else fake.name()
    email = fake.email()
    phone = ca_phone()
    city  = random.choice(CITIES)
    prov  = CANADIAN_CITIES_PROV[city]
    pc    = ca_postal(prov)
    addr  = f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    bank  = random.choice(CANADIAN_BANKS)
    acct  = account_no()
    card  = ca_card()
    amount = dollars(50, 5000)

    text = f"""To: Customer Relations, {bank}
From: {name}
Date: {date.today().isoformat()}
─────────────────────────────────────
RE: Unauthorized Transaction — Account {acct}

Dear {bank} Customer Relations,

I am writing to dispute an unauthorized transaction on my account.
My name is {name}. I can be reached at {phone} or {email}.
My mailing address is {addr}.

A charge of {amount} appeared on card {card} which I did not authorize.
Please investigate and reverse this transaction immediately.

Sincerely,
{name}
"""
    return {"text": text, "doc_type": "COMPLAINT_LETTER",
            "entities": collect(text, [
                (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
                (addr,"ADDRESS"),(bank,"ORG"),
                (acct,"ACCOUNT_NO"),(card,"CREDIT_CARD"),
                (amount,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


GENERATORS = [
    gen_kyc_form, gen_wire_transfer, gen_loan_application,
    gen_account_statement, gen_sar_memo, gen_complaint_letter,
]


def generate_dataset(n: int = 5000, names=None) -> list:
    """Generate n synthetic banking documents, balanced across all 6 types."""
    docs = [GENERATORS[i % len(GENERATORS)](names=names) for i in range(n)]
    random.shuffle(docs)
    return docs
'''

REDACTOR = r'''"""
src/redactor.py
Two-layer PII redactor: spaCy NER + regex fallback.
"""

import spacy
from typing import List, Tuple
from src.regex_patterns import regex_find, deduplicate

REDACTION_MAP = {
    "PERSON":      "[NAME REDACTED]",
    "ORG":         "[ORG REDACTED]",
    "EMAIL":       "[EMAIL REDACTED]",
    "PHONE":       "[PHONE REDACTED]",
    "ACCOUNT_NO":  "[ACCOUNT REDACTED]",
    "TRANSIT_NO":  "[TRANSIT REDACTED]",
    "CREDIT_CARD": "[CARD REDACTED]",
    "SIN":         "[SIN REDACTED]",
    "POSTAL_CODE": "[POSTAL REDACTED]",
    "ADDRESS":     "[ADDRESS REDACTED]",
    "DOB":         "[DOB REDACTED]",
    "AMOUNT":      "[AMOUNT REDACTED]",
    "SWIFT":       "[SWIFT REDACTED]",
    "DEFAULT":     "[REDACTED]",
}


class PIIRedactor:
    def __init__(self, model_path: str = "./model/model-best"):
        self.nlp = spacy.load(model_path)

    def detect(self, text: str) -> List[Tuple[int, int, str]]:
        doc = self.nlp(text)
        spacy_ents = [(e.start_char, e.end_char, e.label_) for e in doc.ents]
        regex_ents = regex_find(text)
        return sorted(deduplicate(spacy_ents + regex_ents), key=lambda x: x[0])

    def redact(self, text: str) -> Tuple[str, List[Tuple[int, int, str]]]:
        entities = self.detect(text)
        chars = list(text)
        for start, end, label in sorted(entities, key=lambda x: -x[0]):
            token = REDACTION_MAP.get(label, REDACTION_MAP["DEFAULT"])
            chars[start:end] = list(token)
        return "".join(chars), entities
'''

APP = r'''"""
app.py — Streamlit: Canadian Banking PII Redactor
Deploy to Hugging Face Spaces (SDK: streamlit)
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Canadian Banking PII Redactor",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 Canadian Banking Document PII Redactor")
st.caption(
    "Detects and masks PII in banking documents using spaCy NER + regex · "
    "Built by [Manpreet Singh](https://linkedin.com/in/manpreet-singh-ds)"
)
st.divider()

@st.cache_resource(show_spinner="Loading NER model...")
def load_redactor():
    # Uncomment after training:
    # from src.redactor import PIIRedactor
    # return PIIRedactor("./model/model-best")
    return None

redactor = load_redactor()

SAMPLES = {
    "KYC Form": """\
CUSTOMER IDENTIFICATION FORM (KYC)
TD Bank
─────────────────────────────────────
Full Legal Name:    Sarah Kowalski
Date of Birth:      1984-07-22
Social Insurance:   482-716-930
Primary Address:    47 Lakeshore Blvd W, Toronto, ON M6K 1C3
Phone Number:       416-555-0192
Email Address:      sarah.kowalski@outlook.com
Account Number:     00152-004-7823941
Transit Number:     00152-004
""",
    "Wire Transfer": """\
WIRE TRANSFER REQUEST — Royal Bank of Canada
Reference: WR-20240387
─────────────────────────────────────
SENDER
Name:           Omar Farouq
Email:          o.farouq@gmail.com
Phone:          613-555-0847
Account Number: 00342-003-9182736

RECIPIENT
Beneficiary:    Global Trade Corp
Account Number: 00891-006-4421198
SWIFT / BIC:    ROYCCAT2
Amount:         $42,500.00 CAD
""",
    "SAR Memo": """\
SUSPICIOUS ACTIVITY REPORT (SAR)
Bank of Nova Scotia
─────────────────────────────────────
Subject Name:   Jing-Wei Huang
Address:        891 Rideau St, Ottawa, ON K1N 5Y3
Phone:          613-555-2291
Email:          j.huang@hotmail.com
SIN on File:    312-445-788
Account Number: 00671-010-2234891
Amount:         $185,000.00
""",
    "Complaint Letter": """\
To: Customer Relations, CIBC
From: Maria Santos
Date: 2025-03-15
─────────────────────────────────────
RE: Unauthorized Transaction — Account 00234-004-5512389

Dear CIBC Customer Relations,

I am writing to dispute an unauthorized charge.
I can be reached at 905-555-0334 or m.santos@gmail.com.
My address is 22 King St W, Hamilton, ON L8P 1A1.

A charge of $312.00 appeared on card 4532-1122-3344-5566.

Sincerely,
Maria Santos
""",
}

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📄 Input Document")
    doc_type = st.selectbox("Load a sample", ["— paste your own —"] + list(SAMPLES.keys()))
    default  = SAMPLES.get(doc_type, "") if doc_type != "— paste your own —" else ""
    text     = st.text_area("Document text", value=default, height=420, label_visibility="collapsed")
    run      = st.button("🔍 Detect & Redact PII", type="primary", use_container_width=True)

with col2:
    st.subheader("🛡️ Redacted Output")
    placeholder = st.empty()
    placeholder.text_area("Redacted", value="← Click Detect & Redact",
                           height=420, label_visibility="collapsed", disabled=True)

if run:
    if redactor is None:
        st.warning("⚠️ Model not trained yet — run notebooks 01–03 first.")
    else:
        with st.spinner("Scanning for PII..."):
            redacted_text, entities = redactor.redact(text)
        placeholder.text_area("Redacted", value=redacted_text,
                               height=420, label_visibility="collapsed")
        st.divider()
        st.subheader("📊 Detected Entities")
        if entities:
            df = pd.DataFrame([
                {"Original": text[s:e], "Label": lbl, "Start": s, "End": e}
                for s, e, lbl in entities
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
            c = st.columns(3)
            c[0].metric("PII detected", len(entities))
            c[1].metric("Unique types", df["Label"].nunique())
        else:
            st.info("No PII detected.")

with st.sidebar:
    st.header("📈 Model Metrics")
    st.caption("Populate after 04_evaluation.ipynb")
    st.metric("Recall",    "—")
    st.metric("Precision", "—")
    st.metric("F1",        "—")
    st.divider()
    st.header("🏷️ Entity Labels")
    for l in ["PERSON","ORG","EMAIL","PHONE","ACCOUNT_NO","TRANSIT_NO",
              "CREDIT_CARD","SIN","POSTAL_CODE","ADDRESS","DOB","AMOUNT","SWIFT"]:
        st.markdown(f"- `{l}`")
'''

NB_01 = r"""{
 "cells": [
  {"cell_type":"markdown","metadata":{},
   "source":["# Notebook 01 — Synthetic Banking Data Generation\n",
             "**Data sources:**\n",
             "1. Ontario Top Baby Names CSV (data.ontario.ca) — auto-downloaded\n",
             "2. Faker en_CA — addresses, phones, emails\n",
             "3. src/document_generator.py — 6 banking document types\n\n",
             "**Output:** `data/synthetic/documents.json` — 5,000 annotated docs"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["import os, json, random, requests\n",
             "import pandas as pd\n",
             "from faker import Faker\n",
             "import sys; sys.path.append('..')\n",
             "from src.document_generator import generate_dataset\n",
             "\n",
             "fake = Faker('en_CA')\n",
             "Faker.seed(42)\n",
             "random.seed(42)"]},

  {"cell_type":"markdown","metadata":{},"source":["## Step 1 — Download Ontario Baby Names (real open data)"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["MALE_URL   = 'https://data.ontario.ca/dataset/eb4c585c-6ada-4de7-8ff1-e876fb1a6b0b/resource/9571139d-e505-4a35-82fa-192af66c5714/download/ontario_top_baby_names_male.csv'\n",
             "FEMALE_URL = 'https://data.ontario.ca/dataset/f6de42e9-9ca4-4f06-b7db-e59cec7def7c/resource/d27df1b3-f0f8-4a1c-ba6b-71c18cbcc4c0/download/ontario_top_baby_names_female.csv'\n",
             "\n",
             "os.makedirs('../data/raw', exist_ok=True)\n",
             "for url, fname in [(MALE_URL,'ontario_names_male.csv'),(FEMALE_URL,'ontario_names_female.csv')]:\n",
             "    p = f'../data/raw/{fname}'\n",
             "    if not os.path.exists(p):\n",
             "        r = requests.get(url, timeout=30)\n",
             "        open(p,'wb').write(r.content)\n",
             "        print(f'Downloaded {fname}')\n",
             "    else:\n",
             "        print(f'Already exists: {fname}')"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["male_df   = pd.read_csv('../data/raw/ontario_names_male.csv')\n",
             "female_df = pd.read_csv('../data/raw/ontario_names_female.csv')\n",
             "print('Columns:', male_df.columns.tolist())\n",
             "print(male_df.head(3))"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["# Adapt column name if needed\n",
             "col = 'First Name' if 'First Name' in male_df.columns else male_df.columns[0]\n",
             "first_names = list(set(\n",
             "    male_df[col].dropna().str.title().tolist() +\n",
             "    female_df[col].dropna().str.title().tolist()\n",
             "))\n",
             "# Combine with Faker last names\n",
             "CANADIAN_NAMES = [f\"{fn} {fake.last_name()}\" for fn in first_names[:2000]]\n",
             "print(f'Total names: {len(CANADIAN_NAMES)}')\n",
             "print('Sample:', CANADIAN_NAMES[:5])"]},

  {"cell_type":"markdown","metadata":{},"source":["## Step 2 — Generate 5,000 Documents"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["documents = generate_dataset(n=5000, names=CANADIAN_NAMES)\n",
             "\n",
             "from collections import Counter\n",
             "print('By type:', Counter(d['doc_type'] for d in documents))"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["# Preview\n",
             "s = documents[0]\n",
             "print('=== TYPE:', s['doc_type'], '===')\n",
             "print(s['text'])\n",
             "print('ENTITIES:')\n",
             "for st,en,lbl in s['entities']:\n",
             "    print(f'  [{lbl}] {s[\"text\"][st:en]!r}')"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["# Entity distribution\n",
             "all_labels = [lbl for d in documents for _,_,lbl in d['entities']]\n",
             "print('Entity counts:')\n",
             "for lbl,cnt in Counter(all_labels).most_common():\n",
             "    print(f'  {lbl:<20} {cnt}')"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["os.makedirs('../data/synthetic', exist_ok=True)\n",
             "with open('../data/synthetic/documents.json','w') as f:\n",
             "    json.dump(documents, f, indent=2)\n",
             "print(f'Saved {len(documents)} documents')"]},

  {"cell_type":"markdown","metadata":{},"source":["## Done — Next: 02_annotation_prep.ipynb"]}
 ],
 "metadata": {
  "kernelspec": {"display_name": "PII NER Pipeline", "language": "python", "name": "pii-ner-pipeline"},
  "language_info": {"name": "python", "version": "3.11.0"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}"""

NB_02 = r"""{
 "cells": [
  {"cell_type":"markdown","metadata":{},
   "source":["# Notebook 02 — Annotation Preparation\n",
             "Converts documents.json → spaCy DocBin (train/dev/test 80/10/10)"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["import json, random, os\n",
             "import spacy\n",
             "from spacy.tokens import DocBin\n",
             "\n",
             "with open('../data/synthetic/documents.json') as f:\n",
             "    documents = json.load(f)\n",
             "\n",
             "random.seed(42)\n",
             "random.shuffle(documents)\n",
             "n = len(documents)\n",
             "train = documents[:int(n*0.8)]\n",
             "dev   = documents[int(n*0.8):int(n*0.9)]\n",
             "test  = documents[int(n*0.9):]\n",
             "print(f'Train: {len(train)} | Dev: {len(dev)} | Test: {len(test)}')"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["nlp = spacy.blank('en')\n",
             "\n",
             "def to_docbin(data, name):\n",
             "    db, skipped = DocBin(), 0\n",
             "    for item in data:\n",
             "        doc = nlp.make_doc(item['text'])\n",
             "        ents = []\n",
             "        for s,e,lbl in item['entities']:\n",
             "            span = doc.char_span(s, e, label=lbl, alignment_mode='contract')\n",
             "            if span: ents.append(span)\n",
             "            else:    skipped += 1\n",
             "        doc.ents = ents\n",
             "        db.add(doc)\n",
             "    print(f'{name}: {len(data)} docs, {skipped} spans skipped')\n",
             "    return db\n",
             "\n",
             "os.makedirs('../data/annotated', exist_ok=True)\n",
             "to_docbin(train,'train').to_disk('../data/annotated/train.spacy')\n",
             "to_docbin(dev,  'dev'  ).to_disk('../data/annotated/dev.spacy')\n",
             "to_docbin(test, 'test' ).to_disk('../data/annotated/test.spacy')\n",
             "print('Done')"]},

  {"cell_type":"markdown","metadata":{},"source":["## Done — Next: 03_model_training.ipynb"]}
 ],
 "metadata": {
  "kernelspec": {"display_name": "PII NER Pipeline", "language": "python", "name": "pii-ner-pipeline"},
  "language_info": {"name": "python", "version": "3.11.0"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}"""

NB_03 = r"""{
 "cells": [
  {"cell_type":"markdown","metadata":{},"source":["# Notebook 03 — Model Training\n",
   "Fine-tunes spaCy en_core_web_trf on 4,000 annotated banking documents\n",
   "Expected time: ~30-60 min CPU | ~5-10 min GPU"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["import subprocess\n",
             "\n",
             "# Generate config.cfg (run once)\n",
             "r = subprocess.run(['python','-m','spacy','init','config','../config.cfg',\n",
             "                    '--lang','en','--pipeline','ner','--optimize','accuracy'],\n",
             "                   capture_output=True, text=True)\n",
             "print(r.stdout or r.stderr)"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["r = subprocess.run([\n",
             "    'python','-m','spacy','train','../config.cfg',\n",
             "    '--output','../model',\n",
             "    '--paths.train','../data/annotated/train.spacy',\n",
             "    '--paths.dev','../data/annotated/dev.spacy',\n",
             "    '--gpu-id','-1'\n",
             "], capture_output=True, text=True)\n",
             "print(r.stdout[-3000:])\n",
             "if r.returncode != 0: print('ERR:', r.stderr[-1000:])"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["# Sanity check\n",
             "import spacy\n",
             "nlp = spacy.load('../model/model-best')\n",
             "\n",
             "test_text = '''\n",
             "Full Name: Priya Sharma\n",
             "SIN: 482-716-930  Phone: 416-555-0192\n",
             "Email: priya.s@gmail.com\n",
             "Account: 00152-004-7823941\n",
             "Address: 47 Lakeshore Blvd W, Toronto, ON M6K 1C3\n",
             "Amount: $42,500.00\n",
             "'''\n",
             "for ent in nlp(test_text).ents:\n",
             "    print(f'{ent.label_:<20} {ent.text}')"]},

  {"cell_type":"markdown","metadata":{},"source":["## Done — Next: 04_evaluation.ipynb"]}
 ],
 "metadata": {
  "kernelspec": {"display_name": "PII NER Pipeline", "language": "python", "name": "pii-ner-pipeline"},
  "language_info": {"name": "python", "version": "3.11.0"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}"""

NB_04 = r"""{
 "cells": [
  {"cell_type":"markdown","metadata":{},"source":["# Notebook 04 — Evaluation\n",
   "Per-entity precision/recall/F1 + confusion matrix\n",
   "Copy results into README.md and docs/model_card.md"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["import spacy, pandas as pd\n",
             "from spacy.scorer import Scorer\n",
             "from spacy.training import Example\n",
             "from spacy.tokens import DocBin\n",
             "\n",
             "nlp      = spacy.load('../model/model-best')\n",
             "db       = DocBin().from_disk('../data/annotated/test.spacy')\n",
             "examples = [Example(nlp(d.text), d) for d in db.get_docs(nlp.vocab)]\n",
             "results  = Scorer().score(examples)\n",
             "\n",
             "rows = [{'Entity':lbl,'Precision':f\"{s['p']:.1%}\",\n",
             "         'Recall':f\"{s['r']:.1%}\",'F1':f\"{s['f']:.1%}\"}\n",
             "        for lbl,s in results['ents_per_type'].items()]\n",
             "df = pd.DataFrame(rows).sort_values('F1',ascending=False)\n",
             "print(df.to_string(index=False))\n",
             "df.to_csv('../docs/evaluation_results.csv',index=False)"]},

  {"cell_type":"code","execution_count":null,"metadata":{},"outputs":[],
   "source":["import matplotlib.pyplot as plt, seaborn as sns\n",
             "from sklearn.metrics import confusion_matrix\n",
             "\n",
             "true_l, pred_l = [], []\n",
             "for ex in examples:\n",
             "    true_l += [e.label_ for e in ex.reference.ents]\n",
             "    pred_l += [e.label_ for e in ex.predicted.ents]\n",
             "\n",
             "labels = sorted(set(true_l))\n",
             "mn = min(len(true_l), len(pred_l))\n",
             "cm = confusion_matrix(true_l[:mn], pred_l[:mn], labels=labels)\n",
             "\n",
             "plt.figure(figsize=(13,10))\n",
             "sns.heatmap(cm, xticklabels=labels, yticklabels=labels,\n",
             "            annot=True, fmt='d', cmap='Blues')\n",
             "plt.title('NER Confusion Matrix — Canadian Banking PII')\n",
             "plt.ylabel('True'); plt.xlabel('Predicted')\n",
             "plt.tight_layout()\n",
             "plt.savefig('../docs/confusion_matrix.png', dpi=150)\n",
             "plt.show()"]},

  {"cell_type":"markdown","metadata":{},"source":["## Done\n",
   "- Paste the table above into README.md\n",
   "- confusion_matrix.png saved to docs/\n",
   "- Next: deploy with `streamlit run app.py`"]}
 ],
 "metadata": {
  "kernelspec": {"display_name": "PII NER Pipeline", "language": "python", "name": "pii-ner-pipeline"},
  "language_info": {"name": "python", "version": "3.11.0"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}"""

MODEL_CARD = """\
# Model Card — Canadian Banking PII NER

## Summary
Fine-tuned spaCy transformer NER for detecting PII in Canadian banking
documents (KYC, wire transfers, loan applications, SAR memos,
account statements, complaint letters).

## Entity Types
| Label        | Description               | Layer         |
|--------------|---------------------------|---------------|
| PERSON       | Full names                | spaCy NER     |
| ORG          | Bank and company names    | spaCy NER     |
| ADDRESS      | Street addresses          | spaCy NER     |
| EMAIL        | Email addresses           | spaCy + regex |
| PHONE        | Canadian phone numbers    | spaCy + regex |
| ACCOUNT_NO   | Bank account numbers      | Regex         |
| TRANSIT_NO   | Transit/routing numbers   | Regex         |
| CREDIT_CARD  | 16-digit card numbers     | Regex         |
| SIN          | Social Insurance Numbers  | Regex         |
| POSTAL_CODE  | Canadian postal codes     | Regex         |
| DOB          | Dates of birth            | Regex         |
| AMOUNT       | Dollar amounts            | Regex         |
| SWIFT        | SWIFT/BIC codes           | Regex         |

## Training Data
- 5,000 synthetic Canadian banking documents
- First names from Ontario Top Baby Names (data.ontario.ca)
- 80/10/10 train/dev/test split

## Ethical Note
All training data is 100% synthetic. No real PII used.
"""

AUDIT_TRAIL = """\
# Audit Trail

## Data Provenance
| Asset         | Source                               | Licence                          |
|---------------|--------------------------------------|----------------------------------|
| First names   | Ontario Top Baby Names (data.ontario.ca) | Open Government Licence Ontario |
| Last names    | Faker (en_CA)                        | MIT                              |
| Addresses     | Faker (en_CA)                        | MIT                              |
| Account nos   | Algorithmically generated            | N/A                              |
| SINs          | Format-valid only, not real          | N/A                              |

## No Real PII Used
All documents are synthetic. Values do not correspond to real individuals.

## Known Limitations
- English only (no French)
- Canadian bank account formats only
- Hyphenated names may be partially missed
"""

FILES = {
    ".gitignore":                          GITIGNORE,
    "README.md":                           README,
    "requirements.txt":                    REQUIREMENTS,
    "environment.yml":                     ENVIRONMENT_YML,
    "app.py":                              APP,
    "src/__init__.py":                     "# src package\n",
    "src/regex_patterns.py":               REGEX_PATTERNS,
    "src/redactor.py":                     REDACTOR,
    "src/document_generator.py":           DOCUMENT_GENERATOR,
    "docs/model_card.md":                  MODEL_CARD,
    "docs/audit_trail.md":                 AUDIT_TRAIL,
    "notebooks/01_data_generation.ipynb":  NB_01,
    "notebooks/02_annotation_prep.ipynb":  NB_02,
    "notebooks/03_model_training.ipynb":   NB_03,
    "notebooks/04_evaluation.ipynb":       NB_04,
    "data/raw/.gitkeep":                   "",
    "data/synthetic/.gitkeep":             "",
    "data/annotated/.gitkeep":             "",
    "model/.gitkeep":                      "",
}


def create_project():
    print(f"\n🏦 Setting up {ROOT}/ — Banking Domain\n")

    for folder in FOLDERS:
        path = os.path.join(ROOT, folder)
        os.makedirs(path, exist_ok=True)
        print(f"  📁 {path}/")

    print()
    for rel_path, content in FILES.items():
        full_path = os.path.join(ROOT, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  📄 {full_path}")

    print(f"""
✅  Done — ./{ROOT}/ is ready

──────────────────────────────────────────────────────
  NEXT STEPS
──────────────────────────────────────────────────────
  1. cd {ROOT}
  2. conda env create -f environment.yml
  3. conda activate pii-ner-pipeline
  4. python -m ipykernel install --user \\
       --name pii-ner-pipeline \\
       --display-name "PII NER Pipeline"
  5. python -m spacy download en_core_web_trf
  6. jupyter notebook
  7. Open notebooks/01_data_generation.ipynb
     → auto-downloads Ontario names CSV, no manual step needed

──────────────────────────────────────────────────────
  6 Document Types:
    KYC · Wire Transfer · Loan Application
    Account Statement · SAR Memo · Complaint Letter

  13 Entity Labels:
    PERSON · ORG · EMAIL · PHONE
    ACCOUNT_NO · TRANSIT_NO · CREDIT_CARD
    SIN · POSTAL_CODE · ADDRESS · DOB · AMOUNT · SWIFT
──────────────────────────────────────────────────────
""")


if __name__ == "__main__":
    create_project()