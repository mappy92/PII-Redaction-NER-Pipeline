"""
src/document_generator.py

7 Canadian banking document templates — mix of structured forms AND
unstructured narrative text to reflect real-world document variance.

Realism features added:
  - Random filler sentences injected between sections
  - PII embedded inside prose paragraphs (not just form fields)
  - Typos / informal language in complaint letters
  - 7th doc type: freeform internal bank note (pure narrative)
  - Email present in ALL document types

Document types:
  1. KYC Form                 (structured form)
  2. Wire Transfer Request    (semi-structured)
  3. Personal Loan Application(structured form)
  4. Account Statement Header (structured)
  5. SAR Memo                 (structured + narrative paragraph)
  6. Customer Complaint Letter(mostly unstructured prose)
  7. Internal Bank Note       (pure freeform narrative — most realistic)
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
    "Vancouver": "BC", "Montreal": "QC", "Halifax": "NS",
}
CITIES = list(CANADIAN_CITIES_PROV.keys())
INST_CODES = ["002", "003", "004", "006", "010", "016"]

# ── Random filler sentence pools ──────────────────────────────────────────────
# These are injected between sections to simulate real document noise.
# They do NOT contain PII so they won't confuse annotation.

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
    "Our records are updated on the next business day following submission.",
    "Standard service fees may apply. Please refer to the fee schedule.",
    "This is a system-generated document. No signature is required.",
    "If you believe this was sent in error, please disregard and notify us.",
    "All transactions are monitored for compliance with applicable regulations.",
    "This notice supersedes all previous communications on this matter.",
    "Please allow additional time during peak periods.",
    "Contact our 24-hour helpline for urgent inquiries.",
]

FILLER_LEGAL = [
    "This document is issued pursuant to the Bank Act (R.S.C., 1991, c. 46).",
    "Personal information is collected under the authority of PIPEDA.",
    "Subject to FINTRAC reporting requirements under the PCMLTFA.",
    "This communication may constitute a record under OSFI guidelines.",
    "Governed by the laws of the Province of Ontario and applicable federal law.",
    "This report is filed in compliance with AML/ATF program requirements.",
    "Disclosure to unauthorized parties is strictly prohibited.",
    "Retention period: 7 years from date of issue per regulatory requirements.",
]

FILLER_INTERNAL = [
    "Flagged for supervisor review.",
    "Escalated to compliance team on receipt.",
    "Case assigned to fraud investigation unit.",
    "Pending secondary verification.",
    "Cross-referenced with existing customer profile — discrepancy noted.",
    "Reviewed by branch manager prior to processing.",
    "Customer was not present during initial review.",
    "Documentation forwarded to head office for final approval.",
    "Follow-up scheduled for next business day.",
    "File marked sensitive — restrict access.",
]


def pick_fillers(pool, n=1):
    """Return n random filler sentences joined by newline."""
    return "\n".join(random.sample(pool, min(n, len(pool))))


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
    prefix = {"ON":random.choice(["M","L","K","N","P"]),
               "BC":"V","AB":"T","QC":"H","NS":"B"}
    safe = "ABCEGHJKLMNPRSTVWXYZ"
    p = prefix.get(prov,"M")
    return f"{p}{random.randint(0,9)}{random.choice(safe)} {random.randint(0,9)}{random.choice(safe)}{random.randint(0,9)}"

def dollars(lo, hi):
    return f"${random.randint(lo,hi):,}.00"

def find_all_spans(text, value):
    spans = []
    value = str(value)
    start = 0
    while True:
        idx = text.find(value, start)
        if idx == -1:
            break
        # Check character before and after — must be a word boundary
        before = text[idx-1] if idx > 0 else " "
        after  = text[idx+len(value)] if idx+len(value) < len(text) else " "
        # Skip if this match is inside a larger word/token (e.g. name inside email)
        if before.isalnum() or after.isalnum():
            start = idx + 1
            continue
        spans.append((idx, idx + len(value)))
        start = idx + len(value)
    return spans


def collect(text, pairs):
    ents = []
    for value, label in pairs:
        for start, end in find_all_spans(text, str(value)):
            ents.append((start, end, label))
    return ents

# ── Document generators ────────────────────────────────────────────────────────

def gen_kyc_form(names=None):
    """Structured KYC form with random filler lines between sections."""
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

    # Randomly inject 1-2 filler lines between sections
    filler1 = pick_fillers(FILLER_GENERAL, random.randint(1,2))
    filler2 = pick_fillers(FILLER_LEGAL,   random.randint(1,2))

    text = f"""CUSTOMER IDENTIFICATION FORM (KYC)
{bank}
{filler1}
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
─────────────────────────────────────
{filler2}

I certify the above information is accurate.
Signature: ________________    Date: {date.today().isoformat()}
"""
    return {"text":text,"doc_type":"KYC",
            "entities":collect(text,[
                (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
                (addr,"ADDRESS"),(s,"SIN"),(dob,"DOB"),
                (bank,"ORG"),(acct,"ACCOUNT_NO"),(tr,"TRANSIT_NO"),(pc,"POSTAL_CODE"),
            ])}


def gen_wire_transfer(names=None):
    """Wire transfer with filler + a short narrative sentence."""
    sender    = random.choice(names) if names else fake.name()
    receiver  = random.choice(names) if names else fake.name()
    s_email   = fake.email()
    r_email   = fake.email()
    s_phone   = ca_phone()
    s_acct    = account_no()
    r_acct    = account_no()
    amount    = dollars(500, 250000)
    bank_from = random.choice(CANADIAN_BANKS)
    bank_to   = random.choice(CANADIAN_BANKS)
    swift     = f"{''.join(random.choices(string.ascii_uppercase,k=4))}CA{''.join(random.choices('ABCDEFGHJKLMNPRSTUVWXYZ23456789',k=2))}"
    ref       = f"WR-{''.join(random.choices(string.digits,k=8))}"
    city      = random.choice(CITIES)
    prov      = CANADIAN_CITIES_PROV[city]
    pc        = ca_postal(prov)

    # Random narrative sentence about the transfer purpose
    purposes  = [
        f"This transfer was initiated following a verbal agreement between the parties on {date.today().isoformat()}.",
        f"The sender {sender} has authorized this transfer via online banking.",
        f"Transfer requested by {sender} via phone on {date.today().isoformat()}. Branch staff verified identity.",
        f"Amount of {amount} approved by branch manager. Supporting documentation on file.",
    ]
    narrative = random.choice(purposes)
    filler    = pick_fillers(FILLER_LEGAL, 1)

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
Email:              {r_email}
Account Number:     {r_acct}
Bank:               {bank_to}
SWIFT / BIC:        {swift}
Postal Code:        {pc}

TRANSFER DETAILS
Amount:             {amount} CAD
Authorization Date: {date.today().isoformat()}

{narrative}
{filler}
"""
    return {"text":text,"doc_type":"WIRE_TRANSFER",
            "entities":collect(text,[
                (sender,"PERSON"),(receiver,"PERSON"),
                (s_email,"EMAIL"),(r_email,"EMAIL"),(s_phone,"PHONE"),
                (s_acct,"ACCOUNT_NO"),(r_acct,"ACCOUNT_NO"),
                (bank_from,"ORG"),(bank_to,"ORG"),
                (swift,"SWIFT"),(amount,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


def gen_loan_application(names=None):
    """Loan application with an informal notes section at the bottom."""
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

    # Branch officer informal note — unstructured prose with PII
    officer_notes = random.choice([
        f"Spoke with applicant {name} by phone at {phone}. Confirmed employment at {employer}. Seemed credible.",
        f"Customer {name} visited branch on {date.today().isoformat()}. Email on file: {email}. Docs verified.",
        f"Application submitted online by {name}. Follow-up call to {phone} required. Address confirmed: {addr}.",
        f"Branch officer note: {name} provided all documents in person. SIN verified. Contact via {email}.",
    ])
    filler = pick_fillers(FILLER_GENERAL, random.randint(1,2))

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
─────────────────────────────────────
{filler}

OFFICER NOTES:
{officer_notes}

By submitting, the applicant authorizes {bank} to verify all information.
"""
    return {"text":text,"doc_type":"LOAN_APPLICATION",
            "entities":collect(text,[
                (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
                (addr,"ADDRESS"),(s,"SIN"),(dob,"DOB"),
                (bank,"ORG"),(employer,"ORG"),
                (acct,"ACCOUNT_NO"),(req_amt,"AMOUNT"),(income,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


def gen_account_statement(names=None):
    """Account statement with a short customer message paragraph."""
    name    = random.choice(names) if names else fake.name()
    email   = fake.email()
    phone   = ca_phone()
    city    = random.choice(CITIES)
    prov    = CANADIAN_CITIES_PROV[city]
    pc      = ca_postal(prov)
    addr    = f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    bank    = random.choice(CANADIAN_BANKS)
    acct    = account_no()
    card    = ca_card()
    balance = dollars(0, 150000)
    avail   = dollars(0, 50000)
    filler  = pick_fillers(FILLER_GENERAL, random.randint(1,2))

    text = f"""{bank}
MONTHLY ACCOUNT STATEMENT
─────────────────────────────────────
Account Holder:     {name}
Mailing Address:    {addr}
Email on File:      {email}
Phone on File:      {phone}

Account Number:     {acct}
Linked Card:        {card}

Period: {date.today().replace(day=1).isoformat()} to {date.today().isoformat()}
Closing Balance:    {balance}
Available Credit:   {avail}
─────────────────────────────────────
{filler}

For questions contact {bank} customer service.
Paperless statements are available at {email}.
"""
    return {"text":text,"doc_type":"ACCOUNT_STATEMENT",
            "entities":collect(text,[
                (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
                (addr,"ADDRESS"),(bank,"ORG"),
                (acct,"ACCOUNT_NO"),(card,"CREDIT_CARD"),
                (balance,"AMOUNT"),(avail,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


def gen_sar_memo(names=None):
    """SAR memo with a detailed narrative paragraph — most realistic AML format."""
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

    # Long unstructured narrative — PII buried in prose
    narratives = [
        f"On {date.today().isoformat()}, analyst {analyst} identified unusual activity on the account held by {subject} "
        f"at {addr}. The account {acct} received a series of cash deposits totalling {amount} over a 72-hour period. "
        f"The customer was contacted at {phone} and {email} but did not provide a satisfactory explanation. "
        f"The pattern is inconsistent with the customer's known income profile. This report is filed for FINTRAC review.",

        f"The subject, {subject}, residing at {addr}, has been flagged by automated monitoring. "
        f"Account {acct} was used for multiple transfers that deviate from established behaviour. "
        f"Total flagged value: {amount}. The customer's email {email} and phone {phone} are on file. "
        f"SIN verified as {s}. Preparing file for escalation.",

        f"This SAR was initiated by {analyst} following a tip received on {date.today().isoformat()}. "
        f"The subject {subject} at {addr} conducted transactions totalling {amount}. "
        f"Contact details: {phone}, {email}. Account reference: {acct}. "
        f"Compliance team has been notified. No further contact with subject pending investigation.",
    ]
    narrative = random.choice(narratives)
    filler    = pick_fillers(FILLER_LEGAL, 2)

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
─────────────────────────────────────
NARRATIVE:
{narrative}
─────────────────────────────────────
{filler}
Tipping off the subject is prohibited under PCMLTFA.
"""
    return {"text":text,"doc_type":"SAR_MEMO",
            "entities":collect(text,[
                (subject,"PERSON"),(analyst,"PERSON"),
                (email,"EMAIL"),(phone,"PHONE"),
                (addr,"ADDRESS"),(s,"SIN"),
                (bank,"ORG"),(acct,"ACCOUNT_NO"),
                (amount,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


def gen_complaint_letter(names=None):
    """Complaint letter — mostly unstructured prose, informal tone, PII in paragraphs."""
    name   = random.choice(names) if names else fake.name()
    email  = fake.email()
    phone  = ca_phone()
    city   = random.choice(CITIES)
    prov   = CANADIAN_CITIES_PROV[city]
    pc     = ca_postal(prov)
    addr   = f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    bank   = random.choice(CANADIAN_BANKS)
    acct   = account_no()
    card   = ca_card()
    amount = dollars(50, 5000)

    # Varied informal prose styles
    bodies = [
        f"I am writing to formally dispute an unauthorized charge on my account. "
        f"My name is {name} and I have been a customer of {bank} for several years. "
        f"On {date.today().isoformat()}, I noticed a transaction of {amount} on card {card} "
        f"linked to account {acct}. I did not authorize this. "
        f"Please reach me at {phone} or {email}. My address is {addr}.",

        f"To whom it may concern at {bank}, I need to report a problem with my account {acct}. "
        f"A charge of {amount} appeared on {date.today().isoformat()} which I never made. "
        f"The card used was {card}. I'm really frustrated by this. "
        f"My name is {name}, you can call me at {phone} or email {email}. "
        f"I live at {addr} and would like a written response mailed to this address.",

        f"Hi, my name is {name}. I bank with {bank} and my account number is {acct}. "
        f"I just checked my statement and there's a charge for {amount} that I don't recognize "
        f"on my card ending in {card[-4:]} (full number: {card}). "
        f"Can you please look into this? Best way to reach me is {email} or {phone}. "
        f"Address for correspondence: {addr}.",
    ]

    text = f"""To: Customer Relations, {bank}
From: {name}
Date: {date.today().isoformat()}
─────────────────────────────────────
RE: Unauthorized Transaction — Account {acct}

{random.choice(bodies)}

Sincerely,
{name}
{email}
{phone}
"""
    return {"text":text,"doc_type":"COMPLAINT_LETTER",
            "entities":collect(text,[
                (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
                (addr,"ADDRESS"),(bank,"ORG"),
                (acct,"ACCOUNT_NO"),(card,"CREDIT_CARD"),
                (amount,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


def gen_internal_note(names=None):
    """
    NEW — Pure freeform internal bank note.
    No fixed format. PII appears naturally in prose.
    Simulates handoff notes, case summaries, internal emails.
    Most realistic doc type — tests model on unstructured text.
    """
    customer  = random.choice(names) if names else fake.name()
    officer   = random.choice(names) if names else fake.name()
    email     = fake.email()
    phone     = ca_phone()
    city      = random.choice(CITIES)
    prov      = CANADIAN_CITIES_PROV[city]
    pc        = ca_postal(prov)
    addr      = f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}"
    bank      = random.choice(CANADIAN_BANKS)
    acct      = account_no()
    amount    = dollars(500, 200000)
    s         = ca_sin()
    dob       = ca_dob()
    card      = ca_card()

    # Multiple varied note templates — all prose, no fixed fields
    templates = [
        f"Called {customer} today at {phone} regarding the hold on account {acct}. "
        f"Customer was agitated but cooperative. Confirmed DOB as {dob} and SIN {s}. "
        f"They mentioned their address has changed — new address is {addr}. "
        f"Email updated to {email}. Balance in question is {amount}. "
        f"Passed to {officer} for follow-up. — {bank} internal note {date.today().isoformat()}",

        f"Re: {customer} — account {acct}\n"
        f"Customer came in to {bank} branch in {city} on {date.today().isoformat()}. "
        f"Wanted to dispute card charges on {card}. Total disputed: {amount}. "
        f"I ({officer}) took the details. Customer's email is {email}, phone {phone}. "
        f"Address on file: {addr}, postal code {pc}. SIN provided and verified: {s}. "
        f"Referred to fraud team. No further action from my end.",

        f"FYI — passing this to you, {officer}.\n"
        f"Customer {customer} (DOB: {dob}) called in about a transfer of {amount} from account {acct}. "
        f"Says they didn't make it. Card on file is {card}. "
        f"I confirmed address as {addr} and email {email}. "
        f"SIN on file: {s}. Reach them at {phone}. "
        f"{bank} account flagged pending review. — {date.today().isoformat()}",

        f"Quick note on {customer}: customer profile review triggered by transaction of {amount}. "
        f"DOB {dob}, SIN {s}, currently at {addr}. "
        f"Reachable via {email} or {phone}. Account {acct} at {bank} temporarily restricted. "
        f"Card {card} also flagged. {officer} to handle customer contact. "
        f"Postal code on file: {pc}.",
    ]

    text = random.choice(templates)

    return {"text":text,"doc_type":"INTERNAL_NOTE",
            "entities":collect(text,[
                (customer,"PERSON"),(officer,"PERSON"),
                (email,"EMAIL"),(phone,"PHONE"),
                (addr,"ADDRESS"),(s,"SIN"),(dob,"DOB"),
                (bank,"ORG"),(acct,"ACCOUNT_NO"),(card,"CREDIT_CARD"),
                (amount,"AMOUNT"),(pc,"POSTAL_CODE"),
            ])}


# ── Master generator ───────────────────────────────────────────────────────────

GENERATORS = [
    gen_kyc_form,
    gen_wire_transfer,
    gen_loan_application,
    gen_account_statement,
    gen_sar_memo,
    gen_complaint_letter,
    gen_internal_note,       # NEW — pure unstructured prose
]


def generate_dataset(n: int = 5000, names=None) -> list:
    """
    Generate n synthetic banking documents, balanced across all 7 types.
    names: list of Canadian full names to use as PERSON entities.
    """
    docs = [GENERATORS[i % len(GENERATORS)](names=names) for i in range(n)]
    random.shuffle(docs)
    return docs
