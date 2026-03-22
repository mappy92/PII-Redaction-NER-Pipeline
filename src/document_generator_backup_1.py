"""
src/document_generator.py

7 Canadian banking document templates with:
  - Randomised field labels (50+ label variants per entity type)
  - Randomised field ORDER within each document
  - random_case() — Title / lower / UPPER case variation
  - Random filler sentences injected between sections
  - PII embedded in prose paragraphs
  - Pure freeform internal note (no structure at all)

This prevents positional overfitting — model must learn entity
patterns from context, not fixed template positions.
"""

import random
import string
from datetime import date, timedelta
from faker import Faker

fake = Faker("en_CA")

# ── Canadian reference data ────────────────────────────────────────────────────
CANADIAN_BANKS = [
    "Royal Bank of Canada", "TD Bank", "Bank of Nova Scotia",
    "Bank of Montreal", "CIBC", "National Bank of Canada",
    "Desjardins Group", "HSBC Canada", "Laurentian Bank",
    "Canadian Western Bank", "BMO", "RBC", "TD", "Scotiabank",
]

CANADIAN_CITIES_PROV = {
    "Toronto": "ON", "Ottawa": "ON", "Mississauga": "ON",
    "Brampton": "ON", "Hamilton": "ON", "London": "ON",
    "Markham": "ON", "Kitchener": "ON", "Windsor": "ON",
    "Calgary": "AB", "Edmonton": "AB",
    "Vancouver": "BC", "Montreal": "QC", "Halifax": "NS",
}
CITIES     = list(CANADIAN_CITIES_PROV.keys())
INST_CODES = ["002", "003", "004", "006", "010", "016"]

# ── Field label pools ──────────────────────────────────────────────────────────
# Empty string "" = no label, PII appears in pure prose

NAME_LABELS = [
    "Full Legal Name:", "Customer Name:", "Name:", "Client:",
    "Account Holder:", "Applicant:", "Subject:", "Individual:",
    "Primary Contact:", "Registered Name:", "Legal Name:",
    "Customer:", "Holder:", "Member Name:", "Beneficiary:", "",
]

PHONE_LABELS = [
    "Phone Number:", "Phone:", "Tel:", "Mobile:", "Cell:",
    "Contact Number:", "Telephone:", "Reach at:", "Call:",
    "Direct Line:", "Contact Phone:", "Primary Phone:",
    "Cellular:", "Home Phone:", "Work Phone:", "",
]

EMAIL_LABELS = [
    "Email Address:", "Email:", "E-mail:", "Contact Email:",
    "Electronic Mail:", "Email on File:", "Send to:",
    "Digital Contact:", "Online Contact:", "Email ID:",
    "Preferred Email:", "Correspondence Email:", "",
]

ADDR_LABELS = [
    "Primary Address:", "Address:", "Mailing Address:",
    "Residence:", "Located at:", "Home Address:",
    "Registered Address:", "Civic Address:", "Street Address:",
    "Current Address:", "Permanent Address:", "Postal Address:", "",
]

SIN_LABELS = [
    "Social Insurance:", "SIN:", "S.I.N.:", "Gov ID:",
    "Social Insurance Number:", "Government ID:", "Tax ID:",
    "National ID:", "ID Number:", "SIN Number:", "",
]

DOB_LABELS = [
    "Date of Birth:", "DOB:", "Born:", "Birth Date:",
    "Birthdate:", "Birth:", "D.O.B.:", "Date Born:", "Birthday:", "",
]

ACCT_LABELS = [
    "Account Number:", "Account:", "Acct:", "Account No:",
    "Bank Account:", "Account #:", "Account Reference:",
    "Chequing Account:", "Savings Account:", "Account ID:", "",
]

TRANSIT_LABELS = [
    "Transit Number:", "Transit:", "Routing:", "Branch Transit:",
    "Transit No:", "Routing Number:", "Branch Code:", "",
]

ORG_LABELS = [
    "Institution:", "Bank:", "Financial Institution:",
    "Issuing Bank:", "Organization:", "Company:", "Employer:",
    "Branch:", "Bank Name:", "",
]

AMT_LABELS = [
    "Amount:", "Total:", "Balance:", "Value:", "Sum:",
    "Transfer Amount:", "Loan Amount:", "Requested Amount:",
    "Outstanding Balance:", "Transaction Amount:", "CAD Amount:", "",
]

CARD_LABELS = [
    "Card Number:", "Credit Card:", "Debit Card:", "Card No:",
    "Card #:", "Linked Card:", "Payment Card:", "Card on File:", "",
]

SWIFT_LABELS = [
    "SWIFT Code:", "SWIFT / BIC:", "BIC:", "SWIFT:",
    "Bank Identifier:", "International Code:", "SWIFT/BIC Code:", "",
]

# ── Filler sentence pools ──────────────────────────────────────────────────────
FILLER_GENERAL = [
    "Please ensure all fields are completed accurately before submission.",
    "This document is confidential and intended solely for the named recipient.",
    "For any questions regarding this form, contact your branch representative.",
    "All information provided is subject to verification.",
    "Processing may take 3 to 5 business days.",
    "Retain a copy of this document for your records.",
    "This communication is protected under Canadian privacy legislation.",
    "Subject to standard terms and conditions.",
    "Branch use only — do not forward without authorization.",
    "This form must be signed and dated to be considered valid.",
    "Standard service fees may apply.",
    "Customer verified via two-factor authentication.",
    "Document submitted through online portal.",
    "Original signature on file at branch.",
    "Manager approval obtained prior to processing.",
    "Supporting documentation attached and verified.",
]

FILLER_LEGAL = [
    "This document is issued pursuant to the Bank Act (R.S.C., 1991, c. 46).",
    "Personal information is collected under the authority of PIPEDA.",
    "Subject to FINTRAC reporting requirements under the PCMLTFA.",
    "Governed by the laws of the Province of Ontario and applicable federal law.",
    "This report is filed in compliance with AML/ATF program requirements.",
    "Disclosure to unauthorized parties is strictly prohibited.",
    "Retention period: 7 years from date of issue per regulatory requirements.",
]


def pick_fillers(pool, n=1):
    if n == 0:
        return ""
    return "\n".join(random.sample(pool, min(n, len(pool))))


# ── Case variation ─────────────────────────────────────────────────────────────
def random_case(text):
    """60% Title, 25% lower, 10% UPPER, 5% unchanged."""
    r = random.random()
    if r < 0.60:    return text
    elif r < 0.85:  return text.lower()
    elif r < 0.95:  return text.upper()
    else:           return text


# ── Banking helpers ────────────────────────────────────────────────────────────
def ca_phone():
    ac = random.choice([
        "416","647","437","905","519","613",
        "604","403","780","514","289","365"
    ])
    return f"{ac}-{random.randint(200,999)}-{random.randint(1000,9999)}"

def account_no():
    return (f"{random.randint(10000,99999)}-"
            f"{random.choice(INST_CODES)}-"
            f"{random.randint(1000000,9999999)}")

def transit_no():
    return f"{random.randint(10000,99999)}-{random.choice(INST_CODES)}"

def ca_sin():
    return (f"{random.randint(100,899)}-"
            f"{random.randint(100,999)}-"
            f"{random.randint(100,999)}")

def ca_card():
    g = ([str(random.randint(4000,4999))] +
         [str(random.randint(1000,9999)) for _ in range(3)])
    return "-".join(g)

def ca_dob():
    s = date(1955, 1, 1)
    return (s + timedelta(
        days=random.randint(0, (date(2000,12,31)-s).days)
    )).isoformat()

def ca_postal(prov="ON"):
    prefix = {
        "ON": random.choice(["M","L","K","N","P"]),
        "BC": "V", "AB": "T", "QC": "H", "NS": "B"
    }
    safe = "ABCEGHJKLMNPRSTVWXYZ"
    p = prefix.get(prov, "M")
    return (f"{p}{random.randint(0,9)}{random.choice(safe)} "
            f"{random.randint(0,9)}{random.choice(safe)}{random.randint(0,9)}")

def dollars(lo, hi):
    return f"${random.randint(lo, hi):,}.00"

def find_all_spans(text, value):
    """Find ALL occurrences of value in text with word boundary check."""
    spans = []
    value = str(value)
    start = 0
    while True:
        idx = text.find(value, start)
        if idx == -1:
            break
        before = text[idx-1] if idx > 0 else " "
        after  = text[idx+len(value)] if idx+len(value) < len(text) else " "
        if before.isalnum() or after.isalnum():
            start = idx + 1
            continue
        spans.append((idx, idx + len(value)))
        start = idx + len(value)
    return spans

def collect(text, pairs):
    """Find ALL occurrences of each (value, label) pair."""
    ents = []
    for value, label in pairs:
        for start, end in find_all_spans(text, str(value)):
            ents.append((start, end, label))
    return ents

def build_field(label, value):
    """Build form field line. Empty label = value only (pure prose)."""
    if label:
        return f"{label:<26} {value}"
    return str(value)


# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENT GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def gen_kyc_form(names=None):
    """KYC — randomised field order, labels, case."""
    name  = random_case(random.choice(names) if names else fake.name())
    email = fake.email()
    phone = ca_phone()
    city  = random.choice(CITIES)
    prov  = CANADIAN_CITIES_PROV[city]
    pc    = ca_postal(prov)
    addr  = random_case(
        f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    )
    s     = ca_sin()
    dob   = ca_dob()
    bank  = random_case(random.choice(CANADIAN_BANKS))
    acct  = account_no()
    tr    = transit_no()

    field_defs = [
        (random.choice(NAME_LABELS),    name,  "PERSON"),
        (random.choice(DOB_LABELS),     dob,   "DOB"),
        (random.choice(SIN_LABELS),     s,     "SIN"),
        (random.choice(ADDR_LABELS),    addr,  "ADDRESS"),
        (random.choice(PHONE_LABELS),   phone, "PHONE"),
        (random.choice(EMAIL_LABELS),   email, "EMAIL"),
        (random.choice(ACCT_LABELS),    acct,  "ACCOUNT_NO"),
        (random.choice(TRANSIT_LABELS), tr,    "TRANSIT_NO"),
        (random.choice(ORG_LABELS),     bank,  "ORG"),
    ]
    random.shuffle(field_defs)

    header = random.choice([
        f"CUSTOMER IDENTIFICATION FORM (KYC)\n{bank}",
        f"KYC VERIFICATION — {bank}",
        f"KNOW YOUR CUSTOMER FORM\nInstitution: {bank}",
        f"{bank}\nCustomer Verification Document",
        f"CLIENT ONBOARDING — KYC\n{bank}",
    ])

    body    = "\n".join(build_field(lbl,val) for lbl,val,_ in field_defs)
    filler1 = pick_fillers(FILLER_GENERAL, random.randint(0,2))
    filler2 = pick_fillers(FILLER_LEGAL,   random.randint(0,1))

    text = f"""{header}
{"─"*40}
{filler1}
{body}
{"─"*40}
{filler2}
Signature: ________________    Date: {date.today().isoformat()}
"""
    return {
        "text": text, "doc_type": "KYC",
        "entities": collect(text, [(val,lbl) for _,val,lbl in field_defs])
    }


def gen_wire_transfer(names=None):
    """Wire transfer — randomised blocks + narrative."""
    sender    = random_case(random.choice(names) if names else fake.name())
    receiver  = random_case(random.choice(names) if names else fake.name())
    s_email   = fake.email()
    r_email   = fake.email()
    s_phone   = ca_phone()
    s_acct    = account_no()
    r_acct    = account_no()
    amount    = dollars(500, 250000)
    bank_from = random_case(random.choice(CANADIAN_BANKS))
    bank_to   = random_case(random.choice(CANADIAN_BANKS))
    swift     = (
        f"{''.join(random.choices(string.ascii_uppercase,k=4))}"
        f"CA{''.join(random.choices('ABCDEFGHJKLMNPRSTUVWXYZ23456789',k=2))}"
    )
    ref  = f"WR-{''.join(random.choices(string.digits,k=8))}"
    city = random.choice(CITIES)
    prov = CANADIAN_CITIES_PROV[city]
    pc   = ca_postal(prov)

    narratives = [
        f"This transfer was initiated by {sender} via online banking "
        f"on {date.today().isoformat()}. Amount of {amount} approved.",
        f"The sender {sender} contacted {bank_from} at {s_phone} "
        f"to authorize this wire of {amount} to {receiver}.",
        f"Branch staff verified identity of {sender} at {s_email}. "
        f"Transfer of {amount} to {receiver} at {bank_to} confirmed.",
        f"Wire requested by {sender}. Sending {amount} "
        f"from {bank_from} to {bank_to}.",
    ]

    sender_fields = [
        (random.choice(NAME_LABELS),  sender,   "PERSON"),
        (random.choice(EMAIL_LABELS), s_email,  "EMAIL"),
        (random.choice(PHONE_LABELS), s_phone,  "PHONE"),
        (random.choice(ACCT_LABELS),  s_acct,   "ACCOUNT_NO"),
        (random.choice(ORG_LABELS),   bank_from,"ORG"),
    ]
    random.shuffle(sender_fields)

    receiver_fields = [
        (random.choice(NAME_LABELS),  receiver, "PERSON"),
        (random.choice(EMAIL_LABELS), r_email,  "EMAIL"),
        (random.choice(ACCT_LABELS),  r_acct,   "ACCOUNT_NO"),
        (random.choice(ORG_LABELS),   bank_to,  "ORG"),
        (random.choice(SWIFT_LABELS), swift,    "SWIFT"),
    ]
    random.shuffle(receiver_fields)

    header = random.choice([
        f"WIRE TRANSFER REQUEST — {bank_from}",
        f"INTERNATIONAL TRANSFER FORM\n{bank_from}",
        f"FUNDS TRANSFER AUTHORIZATION\nRef: {ref}",
        f"{bank_from}\nWire Transfer — Ref: {ref}",
    ])

    s_block = "\n".join(build_field(l,v) for l,v,_ in sender_fields)
    r_block = "\n".join(build_field(l,v) for l,v,_ in receiver_fields)
    filler  = pick_fillers(FILLER_LEGAL, random.randint(0,1))

    text = f"""{header}
{"─"*40}
SENDER
{s_block}

RECIPIENT
{r_block}

{random.choice(AMT_LABELS):<26} {amount}
Authorization Date:        {date.today().isoformat()}
Postal Code:               {pc}
{"─"*40}
{random.choice(narratives)}
{filler}
"""
    all_pairs = (
        [(val,lbl) for _,val,lbl in sender_fields] +
        [(val,lbl) for _,val,lbl in receiver_fields] +
        [(amount,"AMOUNT"), (pc,"POSTAL_CODE")]
    )
    return {"text":text, "doc_type":"WIRE_TRANSFER",
            "entities":collect(text, all_pairs)}


def gen_loan_application(names=None):
    """Loan application — shuffled fields + officer prose note."""
    name     = random_case(random.choice(names) if names else fake.name())
    email    = fake.email()
    phone    = ca_phone()
    city     = random.choice(CITIES)
    prov     = CANADIAN_CITIES_PROV[city]
    pc       = ca_postal(prov)
    addr     = random_case(
        f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    )
    s        = ca_sin()
    dob      = ca_dob()
    bank     = random_case(random.choice(CANADIAN_BANKS))
    acct     = account_no()
    req_amt  = dollars(5000, 500000)
    income   = dollars(40000, 250000)
    employer = random_case(fake.company())

    app_fields = [
        (random.choice(NAME_LABELS),  name,  "PERSON"),
        (random.choice(DOB_LABELS),   dob,   "DOB"),
        (random.choice(SIN_LABELS),   s,     "SIN"),
        (random.choice(ADDR_LABELS),  addr,  "ADDRESS"),
        (random.choice(PHONE_LABELS), phone, "PHONE"),
        (random.choice(EMAIL_LABELS), email, "EMAIL"),
    ]
    random.shuffle(app_fields)

    loan_fields = [
        (random.choice(ORG_LABELS), employer, "ORG"),
        (random.choice(AMT_LABELS), income,   "AMOUNT"),
        (random.choice(AMT_LABELS), req_amt,  "AMOUNT"),
        (random.choice(ACCT_LABELS),acct,     "ACCOUNT_NO"),
    ]
    random.shuffle(loan_fields)

    officer_notes = random.choice([
        f"Spoke with {name} by phone at {phone}. "
        f"Confirmed employment at {employer}. Credible applicant.",
        f"Customer {name} visited branch {date.today().isoformat()}. "
        f"Email: {email}. Documents verified. SIN confirmed.",
        f"Application submitted online by {name}. "
        f"Follow-up to {phone} required. Address confirmed: {addr}.",
        f"Branch note: {name} provided all docs. "
        f"Contact via {email}. Income {income} verified with {employer}.",
    ])

    header = random.choice([
        f"PERSONAL LOAN APPLICATION\n{bank}",
        f"LOAN REQUEST FORM\nInstitution: {bank}",
        f"{bank}\nCredit Application",
        f"CREDIT APPLICATION FORM\n{bank}",
    ])

    app_block  = "\n".join(build_field(l,v) for l,v,_ in app_fields)
    loan_block = "\n".join(build_field(l,v) for l,v,_ in loan_fields)
    filler     = pick_fillers(FILLER_GENERAL, random.randint(0,2))

    text = f"""{header}
{"─"*40}
APPLICANT INFORMATION
{app_block}

EMPLOYMENT & LOAN DETAILS
{loan_block}
{"─"*40}
{filler}
OFFICER NOTES: {officer_notes}

By submitting, applicant authorizes {bank} to verify all information.
"""
    all_pairs = (
        [(val,lbl) for _,val,lbl in app_fields] +
        [(val,lbl) for _,val,lbl in loan_fields] +
        [(bank,"ORG"), (pc,"POSTAL_CODE")]
    )
    return {"text":text, "doc_type":"LOAN_APPLICATION",
            "entities":collect(text, all_pairs)}


def gen_account_statement(names=None):
    """Account statement — shuffled header fields."""
    name    = random_case(random.choice(names) if names else fake.name())
    email   = fake.email()
    phone   = ca_phone()
    city    = random.choice(CITIES)
    prov    = CANADIAN_CITIES_PROV[city]
    pc      = ca_postal(prov)
    addr    = random_case(
        f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    )
    bank    = random_case(random.choice(CANADIAN_BANKS))
    acct    = account_no()
    card    = ca_card()
    balance = dollars(0, 150000)
    avail   = dollars(0, 50000)

    header_fields = [
        (random.choice(NAME_LABELS),  name,  "PERSON"),
        (random.choice(ADDR_LABELS),  addr,  "ADDRESS"),
        (random.choice(EMAIL_LABELS), email, "EMAIL"),
        (random.choice(PHONE_LABELS), phone, "PHONE"),
        (random.choice(ACCT_LABELS),  acct,  "ACCOUNT_NO"),
        (random.choice(CARD_LABELS),  card,  "CREDIT_CARD"),
        (random.choice(ORG_LABELS),   bank,  "ORG"),
    ]
    random.shuffle(header_fields)

    bal_fields = [
        (random.choice(AMT_LABELS), balance, "AMOUNT"),
        (random.choice(AMT_LABELS), avail,   "AMOUNT"),
    ]

    header = random.choice([
        f"{bank}\nMONTHLY ACCOUNT STATEMENT",
        f"ACCOUNT STATEMENT\n{bank}",
        f"{bank} — STATEMENT OF ACCOUNT",
        f"MONTHLY STATEMENT\nIssued by: {bank}",
    ])

    hdr_block = "\n".join(build_field(l,v) for l,v,_ in header_fields)
    bal_block = "\n".join(build_field(l,v) for l,v,_ in bal_fields)
    filler    = pick_fillers(FILLER_GENERAL, random.randint(0,2))

    text = f"""{header}
{"─"*40}
{hdr_block}

Period: {date.today().replace(day=1).isoformat()} to {date.today().isoformat()}
{bal_block}
{"─"*40}
{filler}
Paperless statements available at {email}.
For questions contact {bank} customer service.
"""
    all_pairs = (
        [(val,lbl) for _,val,lbl in header_fields] +
        [(val,lbl) for _,val,lbl in bal_fields] +
        [(pc,"POSTAL_CODE")]
    )
    return {"text":text, "doc_type":"ACCOUNT_STATEMENT",
            "entities":collect(text, all_pairs)}


def gen_sar_memo(names=None):
    """SAR — structured header + unstructured narrative."""
    subject  = random_case(random.choice(names) if names else fake.name())
    analyst  = random_case(random.choice(names) if names else fake.name())
    phone    = ca_phone()
    email    = fake.email()
    city     = random.choice(CITIES)
    prov     = CANADIAN_CITIES_PROV[city]
    pc       = ca_postal(prov)
    addr     = random_case(
        f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    )
    bank     = random_case(random.choice(CANADIAN_BANKS))
    acct     = account_no()
    amount   = dollars(10000, 500000)
    s        = ca_sin()
    ref      = f"SAR-{date.today().year}-{''.join(random.choices(string.digits,k=6))}"

    subject_fields = [
        (random.choice(NAME_LABELS),  subject, "PERSON"),
        (random.choice(ADDR_LABELS),  addr,    "ADDRESS"),
        (random.choice(PHONE_LABELS), phone,   "PHONE"),
        (random.choice(EMAIL_LABELS), email,   "EMAIL"),
        (random.choice(SIN_LABELS),   s,       "SIN"),
        (random.choice(ACCT_LABELS),  acct,    "ACCOUNT_NO"),
        (random.choice(ORG_LABELS),   bank,    "ORG"),
        (random.choice(AMT_LABELS),   amount,  "AMOUNT"),
    ]
    random.shuffle(subject_fields)

    narratives = [
        f"On {date.today().isoformat()}, analyst {analyst} identified "
        f"unusual activity on the account held by {subject} at {addr}. "
        f"The account {acct} received deposits totalling {amount}. "
        f"Customer contacted at {phone} and {email} but provided no "
        f"satisfactory explanation. Filed for FINTRAC review.",

        f"Subject {subject} at {addr} was flagged by automated monitoring. "
        f"Account {acct} used for transfers deviating from normal behaviour. "
        f"Total flagged: {amount}. Email {email} and phone {phone} on file. "
        f"SIN verified as {s}. Escalating to compliance.",

        f"Report initiated by {analyst}. Subject {subject} at {addr} "
        f"conducted transactions of {amount}. Contact: {phone}, {email}. "
        f"Account: {acct}. SIN: {s}. No contact pending investigation.",

        f"{analyst} flagged {subject} following routine review. "
        f"Multiple cash deposits of {amount} detected on {acct}. "
        f"Subject at {addr}. Reachable at {email} or {phone}. "
        f"SIN {s} verified. Forwarded to fraud unit.",
    ]

    header = random.choice([
        f"SUSPICIOUS ACTIVITY REPORT (SAR)\nCONFIDENTIAL — AML COMPLIANCE\n{bank}",
        f"AML COMPLIANCE REPORT\n{bank}\nRef: {ref}",
        f"FINTRAC SUSPICIOUS ACTIVITY FILING\n{bank}",
        f"{bank}\nINTERNAL SAR — CONFIDENTIAL\nRef: {ref}",
    ])

    subj_block = "\n".join(build_field(l,v) for l,v,_ in subject_fields)
    filler     = pick_fillers(FILLER_LEGAL, 2)

    text = f"""{header}
{"─"*40}
Report Reference:          {ref}
Date Filed:                {date.today().isoformat()}
Prepared By:               {analyst}
{"─"*40}
SUBJECT INFORMATION
{subj_block}
{"─"*40}
NARRATIVE:
{random.choice(narratives)}
{"─"*40}
{filler}
Tipping off the subject is prohibited under PCMLTFA.
"""
    all_pairs = (
        [(val,lbl) for _,val,lbl in subject_fields] +
        [(analyst,"PERSON"), (pc,"POSTAL_CODE")]
    )
    return {"text":text, "doc_type":"SAR_MEMO",
            "entities":collect(text, all_pairs)}


def gen_complaint_letter(names=None):
    """Complaint letter — 4 prose style variants."""
    name   = random_case(random.choice(names) if names else fake.name())
    email  = fake.email()
    phone  = ca_phone()
    city   = random.choice(CITIES)
    prov   = CANADIAN_CITIES_PROV[city]
    pc     = ca_postal(prov)
    addr   = random_case(
        f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    )
    bank   = random_case(random.choice(CANADIAN_BANKS))
    acct   = account_no()
    card   = ca_card()
    amount = dollars(50, 5000)

    bodies = [
        f"I am writing to formally dispute an unauthorized charge. "
        f"My name is {name} and I bank with {bank}. "
        f"On {date.today().isoformat()}, a transaction of {amount} "
        f"appeared on card {card} linked to account {acct}. "
        f"I did not authorize this. Reach me at {phone} or {email}. "
        f"My address is {addr}.",

        f"To whom it may concern at {bank}, I need to report a problem. "
        f"A charge of {amount} appeared which I never made. "
        f"Card used: {card}. My name is {name}, call {phone} "
        f"or email {email}. I live at {addr}.",

        f"Hi, my name is {name}. I bank with {bank}, account {acct}. "
        f"There is a charge for {amount} I don't recognize "
        f"on card {card}. Best reach: {email} or {phone}. "
        f"Address: {addr}.",

        f"{name} — {bank} account {acct} — unauthorized charge {amount} "
        f"on card {card}. Contact {phone} / {email}. "
        f"Address: {addr}. Postal code {pc}.",
    ]

    header = random.choice([
        f"To: Customer Relations, {bank}\nFrom: {name}",
        f"CUSTOMER COMPLAINT\n{bank}",
        f"Dear {bank} Customer Service,",
        f"Formal Complaint — {bank}",
    ])

    text = f"""{header}
Date: {date.today().isoformat()}
{"─"*40}
RE: Unauthorized Transaction — Account {acct}

{random.choice(bodies)}

Sincerely,
{name}
{email}
{phone}
"""
    return {
        "text": text, "doc_type": "COMPLAINT_LETTER",
        "entities": collect(text, [
            (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
            (addr,"ADDRESS"),(bank,"ORG"),
            (acct,"ACCOUNT_NO"),(card,"CREDIT_CARD"),
            (amount,"AMOUNT"),(pc,"POSTAL_CODE"),
        ])
    }


def gen_internal_note(names=None):
    """Pure freeform internal note — no structure, 5 prose variants."""
    customer = random_case(random.choice(names) if names else fake.name())
    officer  = random_case(random.choice(names) if names else fake.name())
    email    = fake.email()
    phone    = ca_phone()
    city     = random.choice(CITIES)
    prov     = CANADIAN_CITIES_PROV[city]
    pc       = ca_postal(prov)
    addr     = random_case(
        f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    )
    bank     = random_case(random.choice(CANADIAN_BANKS))
    acct     = account_no()
    amount   = dollars(500, 200000)
    s        = ca_sin()
    dob      = ca_dob()
    card     = ca_card()

    templates = [
        f"Called {customer} today at {phone} regarding hold on {acct}. "
        f"Confirmed DOB {dob} and SIN {s}. New address: {addr}. "
        f"Email updated to {email}. Balance {amount}. "
        f"Passed to {officer}. — {bank} {date.today().isoformat()}",

        f"Re: {customer} — account {acct}\n"
        f"Customer came into {bank} branch in {city} {date.today().isoformat()}. "
        f"Disputed card charges on {card}. Total disputed: {amount}. "
        f"I ({officer}) took details. Email: {email}, phone {phone}. "
        f"Address: {addr}, postal {pc}. SIN: {s}. Referred to fraud.",

        f"FYI passing to {officer}.\n"
        f"{customer} (DOB: {dob}) called re transfer of {amount} from {acct}. "
        f"Did not authorize. Card {card}. Address {addr}. "
        f"Email {email}. SIN: {s}. Phone {phone}. "
        f"{bank} account flagged. — {date.today().isoformat()}",

        f"Quick note on {customer}: flagged transaction {amount}. "
        f"DOB {dob}, SIN {s}, at {addr}. "
        f"Reachable at {email} or {phone}. Account {acct} at {bank}. "
        f"Card {card} also flagged. {officer} to handle. Postal: {pc}.",

        f"branch handoff — {officer} taking over {customer} file. "
        f"account {acct} under review. customer at {addr}, {pc}. "
        f"contact: {phone} / {email}. disputed {amount}. "
        f"sin {s}. dob {dob}. card: {card}. — {bank}",
    ]

    text = random.choice(templates)

    return {
        "text": text, "doc_type": "INTERNAL_NOTE",
        "entities": collect(text, [
            (customer,"PERSON"),(officer,"PERSON"),
            (email,"EMAIL"),(phone,"PHONE"),
            (addr,"ADDRESS"),(s,"SIN"),(dob,"DOB"),
            (bank,"ORG"),(acct,"ACCOUNT_NO"),(card,"CREDIT_CARD"),
            (amount,"AMOUNT"),(pc,"POSTAL_CODE"),
        ])
    }


# ── Master generator ───────────────────────────────────────────────────────────
GENERATORS = [
    gen_kyc_form,
    gen_wire_transfer,
    gen_loan_application,
    gen_account_statement,
    gen_sar_memo,
    gen_complaint_letter,
    gen_internal_note,
]


def generate_dataset(n: int = 500, names=None) -> list:
    """
    Generate n synthetic banking documents balanced across 7 types.
    Default n=500 for quick testing.
    Change to 7000 for full training run.
    """
    docs = [GENERATORS[i % len(GENERATORS)](names=names) for i in range(n)]
    random.shuffle(docs)
    return docs