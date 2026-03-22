"""
src/document_generator.py  —  VERSION 4: Maximum Variation

7 document types, all pure narrative prose.
- 30+ filler sentences across 4 pools
- 8 templates per generator (up from 5)
- random_case() on names, orgs, addresses
- PII appears in different sentence positions every time
- No form fields, no positional labels
"""

import random
import string
from datetime import date, timedelta
from faker import Faker

fake = Faker("en_CA")

# ── Reference data ─────────────────────────────────────────────────────────────
CANADIAN_BANKS = [
    "Royal Bank of Canada", "TD Bank", "Bank of Nova Scotia",
    "Bank of Montreal", "CIBC", "National Bank of Canada",
    "Desjardins Group", "HSBC Canada", "Laurentian Bank",
    "Canadian Western Bank", "BMO", "RBC", "Scotiabank",
    "ATB Financial", "Meridian Credit Union",
]

CANADIAN_CITIES_PROV = {
    "Toronto": "ON", "Ottawa": "ON", "Mississauga": "ON",
    "Brampton": "ON", "Hamilton": "ON", "London": "ON",
    "Markham": "ON", "Kitchener": "ON", "Windsor": "ON",
    "Barrie": "ON", "Sudbury": "ON",
    "Calgary": "AB", "Edmonton": "AB", "Red Deer": "AB",
    "Vancouver": "BC", "Surrey": "BC", "Burnaby": "BC",
    "Montreal": "QC", "Quebec City": "QC",
    "Halifax": "NS", "Winnipeg": "MB",
}
CITIES     = list(CANADIAN_CITIES_PROV.keys())
INST_CODES = ["002", "003", "004", "006", "010", "016", "030", "039"]

# ── 30+ Filler sentence pools ──────────────────────────────────────────────────

FILLER_GENERAL = [
    "All information has been verified against existing records.",
    "This document is confidential and for internal use only.",
    "Supporting documentation is available upon request.",
    "The matter has been escalated to the relevant department.",
    "Standard processing times of three to five business days apply.",
    "This communication is protected under Canadian privacy legislation.",
    "Please retain this document for your records.",
    "A copy has been filed in the customer record system.",
    "Further verification may be required before processing.",
    "This case has been assigned a priority review status.",
    "Branch staff have been notified and are standing by.",
    "The customer was cooperative throughout the verification process.",
    "All submitted documents have been scanned and stored securely.",
    "This matter will be reviewed at the next compliance meeting.",
    "A follow-up communication will be sent within two business days.",
    "The account has been temporarily restricted pending review.",
    "Customer consent was obtained prior to data collection.",
    "This record is subject to a seven-year retention policy.",
    "No further action is required from the customer at this time.",
    "The case has been logged in the internal tracking system.",
]

FILLER_LEGAL = [
    "This document is governed by the Bank Act (R.S.C., 1991, c. 46).",
    "Personal information is handled in accordance with PIPEDA.",
    "This filing is made pursuant to FINTRAC reporting obligations.",
    "Subject to the Proceeds of Crime (Money Laundering) and Terrorist Financing Act.",
    "Retention period of seven years applies per regulatory requirements.",
    "Unauthorized disclosure of this information is strictly prohibited.",
    "This report is filed under section 7 of the PCMLTFA.",
    "The customer has been advised of their rights under PIPEDA.",
    "Disclosure is limited to authorized personnel only.",
    "This record is protected under the Privacy Act of Canada.",
    "All data handling complies with OSFI Guideline B-10.",
    "The institution has fulfilled its due diligence obligations.",
]

FILLER_INTERNAL = [
    "Flagged for immediate supervisor review.",
    "Cross-referenced with existing customer records — no discrepancies found.",
    "Secondary verification has been completed successfully.",
    "Case forwarded to the compliance department for further review.",
    "Documentation has been reviewed and approved by branch manager.",
    "Follow-up action required within two business days.",
    "The file has been marked as high priority.",
    "Coordinating with fraud prevention team on this matter.",
    "Awaiting response from the customer before proceeding.",
    "Internal audit trail has been updated accordingly.",
    "Risk score has been updated in the customer management system.",
    "Escalated to senior compliance officer for sign-off.",
]

FILLER_PROCEDURAL = [
    "The customer was informed of the outcome via registered mail.",
    "Identity verification was completed using two pieces of government ID.",
    "The transaction has been placed on hold pending investigation.",
    "A case number has been assigned for tracking purposes.",
    "The branch manager has been copied on all correspondence.",
    "Electronic records have been updated to reflect the changes.",
    "The customer acknowledged receipt of this communication.",
    "Biometric verification was completed at the branch.",
    "Telephone verification was used to confirm the customer's identity.",
    "The customer's profile has been updated in the core banking system.",
]

ALL_FILLERS = FILLER_GENERAL + FILLER_LEGAL + FILLER_INTERNAL + FILLER_PROCEDURAL


def pick_filler(n=1):
    """Pick n unique random filler sentences."""
    return " ".join(random.sample(ALL_FILLERS, min(n, len(ALL_FILLERS))))


def pick_fillers_pool(pool, n=1):
    """Pick from a specific pool."""
    return " ".join(random.sample(pool, min(n, len(pool))))


# ── Case variation ─────────────────────────────────────────────────────────────
def rc(text):
    """55% Title, 30% lower, 10% UPPER, 5% unchanged."""
    r = random.random()
    if r < 0.55:    return text
    elif r < 0.85:  return text.lower()
    elif r < 0.95:  return text.upper()
    else:           return text


# ── Banking helpers ────────────────────────────────────────────────────────────
def ca_phone():
    ac = random.choice([
        "416","647","437","905","519","613","604",
        "403","780","514","289","365","343","825",
        "587","778","236","431","204"
    ])
    fmt = random.choice([
        f"{ac}-{random.randint(200,999)}-{random.randint(1000,9999)}",
        f"({ac}) {random.randint(200,999)}-{random.randint(1000,9999)}",
        f"{ac}.{random.randint(200,999)}.{random.randint(1000,9999)}",
        f"+1 {ac} {random.randint(200,999)} {random.randint(1000,9999)}",
    ])
    return fmt

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
    prefix = random.choice(["4","5","4532","5412","4111"])
    g = [str(random.randint(1000,9999)) for _ in range(4)]
    return "-".join(g)

def ca_dob():
    s = date(1950, 1, 1)
    dob = s + timedelta(days=random.randint(0,(date(2003,12,31)-s).days))
    # Vary the format
    fmt = random.choice([
        dob.isoformat(),                                    # 1984-07-22
        dob.strftime("%d/%m/%Y"),                           # 22/07/1984
        dob.strftime("%B %d, %Y"),                          # July 22, 1984
        dob.strftime("%d %B %Y"),                           # 22 July 1984
    ])
    return fmt

def ca_postal(prov="ON"):
    prefix = {
        "ON": random.choice(["M","L","K","N","P"]),
        "BC": "V", "AB": "T", "QC": "H",
        "NS": "B", "MB": "R"
    }
    safe = "ABCEGHJKLMNPRSTVWXYZ"
    p = prefix.get(prov, "M")
    pc = (f"{p}{random.randint(0,9)}{random.choice(safe)} "
          f"{random.randint(0,9)}{random.choice(safe)}{random.randint(0,9)}")
    return pc

def dollars(lo, hi):
    amt = random.randint(lo, hi)
    fmt = random.choice([
        f"${amt:,}.00",
        f"CAD {amt:,}.00",
        f"${amt:,}.00 CAD",
        f"CAD${amt:,}",
    ])
    return fmt

def swift_code():
    return (
        f"{''.join(random.choices(string.ascii_uppercase,k=4))}"
        f"CA{''.join(random.choices('ABCDEFGHJKLMNPRSTUVWXYZ23456789',k=2))}"
    )

def ref_no():
    return f"{''.join(random.choices(string.ascii_uppercase,k=3))}-{''.join(random.choices(string.digits,k=8))}"


# ── Span finding ───────────────────────────────────────────────────────────────
def find_all_spans(text, value):
    spans = []
    value = str(value)
    if not value or len(value) < 2:
        return spans
    start = 0
    while start < len(text):
        idx = text.find(value, start)
        if idx == -1:
            break
        start = idx + len(value)
        spans.append((idx, idx + len(value)))
    return spans

def collect(text, pairs):
    ents = []
    seen = set()
    for value, label in pairs:
        for start, end in find_all_spans(text, str(value)):
            key = (start, end)
            if key not in seen:
                ents.append((start, end, label))
                seen.add(key)
    return ents


# ══════════════════════════════════════════════════════════════════════════════
# KYC — 8 templates
# ══════════════════════════════════════════════════════════════════════════════
def gen_kyc_narrative(names=None):
    name  = rc(random.choice(names) if names else fake.name())
    email = fake.email()
    phone = ca_phone()
    city  = random.choice(CITIES)
    prov  = CANADIAN_CITIES_PROV[city]
    pc    = ca_postal(prov)
    addr  = rc(f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}")
    s     = ca_sin()
    dob   = ca_dob()
    bank  = rc(random.choice(CANADIAN_BANKS))
    acct  = account_no()
    tr    = transit_no()
    ref   = ref_no()

    templates = [
        # 1 — formal summary
        f"The know-your-customer review for {name} was completed on "
        f"{date.today().isoformat()}. The customer provided a date of birth "
        f"of {dob} and a social insurance number of {s}. Their current "
        f"residential address is recorded as {addr}. Contact information "
        f"on file includes phone number {phone} and email address {email}. "
        f"The customer holds account {acct} with transit number {tr} at "
        f"{bank}. Reference: {ref}. {pick_filler(2)}",

        # 2 — onboarding style
        f"During the onboarding process at {bank}, {name} submitted the "
        f"required identification documents. The applicant confirmed their "
        f"address as {addr} and provided {phone} as their primary contact. "
        f"Their date of birth is {dob} and their government-issued "
        f"identification number is {s}. The assigned account number is {acct} "
        f"and the branch transit is {tr}. Correspondence may also be directed "
        f"to {email}. {pick_filler(2)}",

        # 3 — bullet-free summary
        f"Customer verification summary for {name}: the individual resides "
        f"at {addr} and was born on {dob}. The SIN provided was {s}. "
        f"They can be reached at {phone} or via email at {email}. "
        f"Their primary banking account at {bank} is {acct} "
        f"with routing transit {tr}. {pick_fillers_pool(FILLER_LEGAL, 2)}",

        # 4 — regulatory framing
        f"As part of our regulatory KYC obligations at {bank}, we have "
        f"verified the identity of {name}. The customer's date of birth "
        f"is {dob}, and their social insurance number {s} has been confirmed. "
        f"They are currently located at {addr}. "
        f"We have {phone} and {email} on file. "
        f"Account {acct} has been opened with transit {tr}. "
        f"{pick_fillers_pool(FILLER_PROCEDURAL, 2)}",

        # 5 — branch note style
        f"Branch staff completed identity verification for {name} today. "
        f"The customer confirmed their residential address as {addr}, "
        f"postal code {pc}. Date of birth: {dob}. SIN: {s}. "
        f"Best contact is {email} or {phone}. "
        f"Account {acct} established at {bank}, transit {tr}. "
        f"{pick_filler(2)}",

        # 6 — third-person case note
        f"Case reference {ref}: identity verification was performed for "
        f"the customer {name} at {bank}. The individual was born on {dob} "
        f"and holds a social insurance number of {s}. Their mailing address "
        f"is {addr}. The customer's email {email} and telephone {phone} "
        f"have been recorded. Primary account: {acct}, transit: {tr}. "
        f"{pick_fillers_pool(FILLER_INTERNAL, 1)}",

        # 7 — informal internal note
        f"Verified {name} today for KYC at {bank}. Born {dob}, SIN {s}. "
        f"Lives at {addr}. Phone is {phone}, email {email}. "
        f"Set up account {acct} with transit {tr}. Postal: {pc}. "
        f"All docs checked and on file. {pick_filler(1)}",

        # 8 — formal letter opening
        f"This letter confirms that {bank} has completed the mandatory "
        f"customer identification process for {name}. Our records show "
        f"their residential address as {addr} and their date of birth "
        f"as {dob}. The social insurance number {s} has been verified. "
        f"For correspondence, please use {email} or {phone}. "
        f"The account number assigned is {acct}, branch transit {tr}. "
        f"Internal reference: {ref}. {pick_fillers_pool(FILLER_LEGAL, 1)}",
    ]

    text = random.choice(templates)
    return {
        "text": text, "doc_type": "KYC",
        "entities": collect(text, [
            (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
            (addr,"ADDRESS"),(s,"SIN"),(dob,"DOB"),
            (bank,"ORG"),(acct,"ACCOUNT_NO"),(tr,"TRANSIT_NO"),
            (pc,"POSTAL_CODE"),
        ])
    }


# ══════════════════════════════════════════════════════════════════════════════
# WIRE TRANSFER — 8 templates
# ══════════════════════════════════════════════════════════════════════════════
def gen_wire_transfer_narrative(names=None):
    sender    = rc(random.choice(names) if names else fake.name())
    receiver  = rc(random.choice(names) if names else fake.name())
    s_email   = fake.email()
    r_email   = fake.email()
    s_phone   = ca_phone()
    s_acct    = account_no()
    r_acct    = account_no()
    amount    = dollars(500, 250000)
    bank_from = rc(random.choice(CANADIAN_BANKS))
    bank_to   = rc(random.choice(CANADIAN_BANKS))
    swift     = swift_code()
    city      = random.choice(CITIES)
    prov      = CANADIAN_CITIES_PROV[city]
    pc        = ca_postal(prov)
    ref       = ref_no()

    templates = [
        # 1
        f"A wire transfer request was submitted by {sender}, who holds "
        f"account {s_acct} at {bank_from}. The sender can be reached at "
        f"{s_phone} or {s_email}. The requested transfer amount is {amount} "
        f"to be sent to {receiver} at {bank_to}, account {r_acct}. "
        f"The receiving institution SWIFT code is {swift}. "
        f"Postal code on file: {pc}. Reference: {ref}. {pick_filler(2)}",

        # 2
        f"This memo documents the wire transfer initiated by {sender} "
        f"from {bank_from} account {s_acct}. The transfer of {amount} "
        f"is destined for {receiver} whose account {r_acct} is held at "
        f"{bank_to} with SWIFT identifier {swift}. "
        f"The originating customer's email is {s_email} and phone is {s_phone}. "
        f"Beneficiary email on record: {r_email}. {pick_filler(2)}",

        # 3
        f"Transfer authorization {ref}: {sender} has requested that {amount} "
        f"be transferred from account {s_acct} at {bank_from} to {receiver}. "
        f"Destination bank is {bank_to}, account {r_acct}, SWIFT {swift}. "
        f"Contact the sender at {s_phone} or {s_email} for queries. "
        f"Beneficiary contact: {r_email}. Postal reference: {pc}. "
        f"{pick_fillers_pool(FILLER_LEGAL, 2)}",

        # 4
        f"We received a wire transfer instruction from {sender} "
        f"(email: {s_email}, phone: {s_phone}) to move {amount} "
        f"from {bank_from} account {s_acct} to {receiver} at {bank_to}. "
        f"Beneficiary account is {r_acct} and SWIFT code is {swift}. "
        f"Beneficiary email: {r_email}. {pick_filler(2)}",

        # 5
        f"The client {sender} contacted {bank_from} to initiate a transfer. "
        f"From account {s_acct}, a total of {amount} will be sent to "
        f"{receiver}, reachable at {r_email}. "
        f"Destination account {r_acct} at {bank_to}, SWIFT: {swift}. "
        f"Sender contact: {s_phone} and {s_email}. "
        f"Postal: {pc}. {pick_filler(2)}",

        # 6
        f"International transfer on behalf of {sender} to {receiver}. "
        f"Sending {amount} from {bank_from} ({s_acct}) to {bank_to} ({r_acct}). "
        f"SWIFT: {swift}. Sender: {s_email}, {s_phone}. "
        f"Recipient: {r_email}. Ref: {ref}. Postal: {pc}. "
        f"{pick_fillers_pool(FILLER_PROCEDURAL, 2)}",

        # 7
        f"Branch authorized wire transfer for {sender} today. "
        f"Amount: {amount}. From account {s_acct} at {bank_from}. "
        f"To: {receiver}, account {r_acct}, bank {bank_to}, swift {swift}. "
        f"Sender reachable at {s_phone} or {s_email}. "
        f"Beneficiary at {r_email}. {pick_filler(1)}",

        # 8
        f"Wire transfer request received from {sender} via online banking. "
        f"The customer holds account {s_acct} at {bank_from} and wishes "
        f"to transfer {amount} to {receiver} at {bank_to}, account {r_acct}. "
        f"SWIFT code for receiving institution: {swift}. "
        f"We have the sender's phone as {s_phone} and email as {s_email}. "
        f"Beneficiary contact: {r_email}. Postal: {pc}. Ref: {ref}. "
        f"{pick_fillers_pool(FILLER_LEGAL, 1)}",
    ]

    text = random.choice(templates)
    return {
        "text": text, "doc_type": "WIRE_TRANSFER",
        "entities": collect(text, [
            (sender,"PERSON"),(receiver,"PERSON"),
            (s_email,"EMAIL"),(r_email,"EMAIL"),(s_phone,"PHONE"),
            (s_acct,"ACCOUNT_NO"),(r_acct,"ACCOUNT_NO"),
            (bank_from,"ORG"),(bank_to,"ORG"),
            (swift,"SWIFT"),(amount,"AMOUNT"),(pc,"POSTAL_CODE"),
        ])
    }


# ══════════════════════════════════════════════════════════════════════════════
# LOAN APPLICATION — 8 templates
# ══════════════════════════════════════════════════════════════════════════════
def gen_loan_narrative(names=None):
    name     = rc(random.choice(names) if names else fake.name())
    email    = fake.email()
    phone    = ca_phone()
    city     = random.choice(CITIES)
    prov     = CANADIAN_CITIES_PROV[city]
    pc       = ca_postal(prov)
    addr     = rc(f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}")
    s        = ca_sin()
    dob      = ca_dob()
    bank     = rc(random.choice(CANADIAN_BANKS))
    acct     = account_no()
    req_amt  = dollars(5000, 500000)
    income   = dollars(40000, 250000)
    employer = rc(fake.company())
    ref      = ref_no()

    templates = [
        # 1
        f"A loan application was submitted by {name}, currently residing at "
        f"{addr}. The applicant was born on {dob} and their social insurance "
        f"number is {s}. They are employed at {employer} with an annual "
        f"income of {income}. The requested loan amount is {req_amt}. "
        f"Contact details: {phone} and {email}. Their existing account at "
        f"{bank} is {acct}. {pick_filler(2)}",

        # 2
        f"The branch received a credit application from {name} on "
        f"{date.today().isoformat()}. The individual lives at {addr} "
        f"and provided {s} as their government identification. "
        f"Employment confirmed at {employer} with declared income of "
        f"{income}. They have requested {req_amt} in financing. "
        f"Reach them at {phone} or {email}. "
        f"Existing account: {acct} at {bank}. {pick_filler(2)}",

        # 3
        f"Loan assessment for {name} (DOB: {dob}, SIN: {s}): "
        f"The applicant is employed by {employer} earning {income} annually "
        f"and is seeking a personal loan of {req_amt}. They reside at {addr} "
        f"and provided {email} and {phone} as contact information. "
        f"Their account {acct} at {bank} is in good standing. {pick_filler(2)}",

        # 4
        f"Credit application {ref} received from {name}. The applicant "
        f"confirmed their address as {addr}, postal code {pc}. "
        f"Date of birth is {dob} and SIN is {s}. "
        f"Current employer is {employer}, annual income {income}. "
        f"Loan requested: {req_amt}. Bank account {acct} at {bank}. "
        f"Best contact: {email} or call {phone}. {pick_filler(2)}",

        # 5
        f"Our branch manager reviewed the application submitted by {name}, "
        f"who works at {employer} and earns {income} per year. "
        f"The customer is requesting {req_amt} and currently banks with "
        f"{bank} under account {acct}. Their residential address is {addr}. "
        f"SIN on file: {s}. DOB: {dob}. Phone: {phone}. Email: {email}. "
        f"{pick_fillers_pool(FILLER_INTERNAL, 2)}",

        # 6
        f"Loan file for {name}: applicant resides at {addr} and is "
        f"employed full-time at {employer} with verified income of {income}. "
        f"Requesting {req_amt}. SIN {s} confirmed. Born {dob}. "
        f"Contact: {email} / {phone}. Existing {bank} account: {acct}. "
        f"Postal code: {pc}. Ref: {ref}. {pick_fillers_pool(FILLER_LEGAL, 1)}",

        # 7
        f"Personal loan request from {name} at {bank}. "
        f"The individual is currently living at {addr} "
        f"and can be contacted at {phone} or {email}. "
        f"They work for {employer}, earning {income} a year, "
        f"and are applying for {req_amt} in personal credit. "
        f"Their account number is {acct}, DOB is {dob}, SIN is {s}. "
        f"{pick_filler(2)}",

        # 8
        f"Following an in-branch consultation, {name} submitted a formal "
        f"loan application for {req_amt}. The applicant's employer is "
        f"{employer} and their gross annual income is {income}. "
        f"They were born on {dob} and their SIN is {s}. "
        f"Home address: {addr}. Telephone: {phone}. Email: {email}. "
        f"Existing account {acct} at {bank}. Reference number: {ref}. "
        f"{pick_fillers_pool(FILLER_PROCEDURAL, 2)}",
    ]

    text = random.choice(templates)
    return {
        "text": text, "doc_type": "LOAN_APPLICATION",
        "entities": collect(text, [
            (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
            (addr,"ADDRESS"),(s,"SIN"),(dob,"DOB"),
            (bank,"ORG"),(employer,"ORG"),
            (acct,"ACCOUNT_NO"),(req_amt,"AMOUNT"),(income,"AMOUNT"),
            (pc,"POSTAL_CODE"),
        ])
    }


# ══════════════════════════════════════════════════════════════════════════════
# ACCOUNT STATEMENT — 8 templates
# ══════════════════════════════════════════════════════════════════════════════
def gen_statement_narrative(names=None):
    name    = rc(random.choice(names) if names else fake.name())
    email   = fake.email()
    phone   = ca_phone()
    city    = random.choice(CITIES)
    prov    = CANADIAN_CITIES_PROV[city]
    pc      = ca_postal(prov)
    addr    = rc(f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}")
    bank    = rc(random.choice(CANADIAN_BANKS))
    acct    = account_no()
    card    = ca_card()
    balance = dollars(0, 150000)
    avail   = dollars(0, 50000)
    period  = date.today().replace(day=1).isoformat()

    templates = [
        # 1
        f"This monthly statement has been prepared for {name}, "
        f"whose mailing address is {addr}. The account holder can be "
        f"contacted at {phone} or {email}. Their primary account at {bank} "
        f"is {acct}, with linked card {card}. The closing balance for this "
        f"period is {balance}, with available credit of {avail}. "
        f"{pick_filler(2)}",

        # 2
        f"Account statement summary for {name} at {bank}: "
        f"account number {acct}, card on file {card}. "
        f"Statement mailed to {addr}, postal code {pc}. "
        f"Email notifications sent to {email}. Phone on file: {phone}. "
        f"Closing balance this period: {balance}. Available: {avail}. "
        f"{pick_filler(2)}",

        # 3
        f"The following statement covers transactions for the account "
        f"held by {name} at {bank}. The account number is {acct} and "
        f"the associated card is {card}. Statements are mailed to "
        f"{addr} and digital copies sent to {email}. "
        f"Current balance stands at {balance} with {avail} available. "
        f"Contact: {phone}. {pick_filler(2)}",

        # 4
        f"Monthly billing summary: {name} holds account {acct} at {bank}. "
        f"Registered address: {addr}. Contact email: {email}, "
        f"phone: {phone}. Payment card {card} is linked to this account. "
        f"Balance as of statement date: {balance}. "
        f"Credit available: {avail}. {pick_fillers_pool(FILLER_PROCEDURAL, 2)}",

        # 5
        f"Dear {name}, this is your statement from {bank} for account {acct}. "
        f"Your card {card} shows a closing balance of {balance}. "
        f"Available funds are {avail}. We have your address as {addr} "
        f"and your email as {email}. Questions? Call us at {phone}. "
        f"{pick_filler(1)}",

        # 6
        f"Statement period ending {date.today().isoformat()} for {name}. "
        f"Account: {acct} at {bank}. Card on file: {card}. "
        f"Postal address: {addr}, {pc}. "
        f"We reached out to {email} and {phone} this billing cycle. "
        f"Closing balance: {balance}. Available credit: {avail}. "
        f"{pick_fillers_pool(FILLER_LEGAL, 1)}",

        # 7
        f"Prepared for {name} — {bank} account {acct}. "
        f"Statement period: {period} to {date.today().isoformat()}. "
        f"Linked card: {card}. Balance: {balance}. Available: {avail}. "
        f"Mailing address on file: {addr}. Email: {email}. Tel: {phone}. "
        f"{pick_filler(2)}",

        # 8
        f"The account held by {name} at {bank} shows the following activity "
        f"for the current billing period. Account {acct} is associated with "
        f"card {card}. The account holder resides at {addr} and can be "
        f"contacted at {phone} or {email}. The postal code on record is {pc}. "
        f"Closing balance: {balance}. Credit available: {avail}. "
        f"{pick_fillers_pool(FILLER_INTERNAL, 1)}",
    ]

    text = random.choice(templates)
    return {
        "text": text, "doc_type": "ACCOUNT_STATEMENT",
        "entities": collect(text, [
            (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
            (addr,"ADDRESS"),(bank,"ORG"),
            (acct,"ACCOUNT_NO"),(card,"CREDIT_CARD"),
            (balance,"AMOUNT"),(avail,"AMOUNT"),(pc,"POSTAL_CODE"),
        ])
    }


# ══════════════════════════════════════════════════════════════════════════════
# SAR MEMO — 8 templates
# ══════════════════════════════════════════════════════════════════════════════
def gen_sar_narrative(names=None):
    subject  = rc(random.choice(names) if names else fake.name())
    analyst  = rc(random.choice(names) if names else fake.name())
    phone    = ca_phone()
    email    = fake.email()
    city     = random.choice(CITIES)
    prov     = CANADIAN_CITIES_PROV[city]
    pc       = ca_postal(prov)
    addr     = rc(f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}")
    bank     = rc(random.choice(CANADIAN_BANKS))
    acct     = account_no()
    amount   = dollars(10000, 500000)
    s        = ca_sin()
    ref      = ref_no()

    templates = [
        # 1
        f"This suspicious activity report was prepared by {analyst} "
        f"following the identification of unusual transactions on the "
        f"account of {subject}. The subject resides at {addr} and has "
        f"provided {phone} and {email} as contact information. Their "
        f"account {acct} at {bank} received deposits totalling {amount} "
        f"over a short period, which is inconsistent with the customer's "
        f"known financial profile. SIN on file: {s}. Ref: {ref}. "
        f"This report has been filed for FINTRAC review. {pick_filler(2)}",

        # 2
        f"Analyst {analyst} has flagged the account held by {subject} "
        f"at {bank} for suspicious activity. Multiple transactions totalling "
        f"{amount} were recorded on account {acct}. The customer lives at "
        f"{addr} and can be reached at {phone} or {email}. "
        f"SIN verified as {s}. The pattern does not align "
        f"with the customer's declared financial profile. "
        f"Compliance team notified. {pick_fillers_pool(FILLER_LEGAL, 2)}",

        # 3
        f"Following a routine account review, {analyst} identified "
        f"transactions warranting further investigation on the account "
        f"belonging to {subject}. The subject's address is {addr}, "
        f"postal code {pc}. Contact: {email} and {phone}. "
        f"Account {acct} at {bank} shows activity of {amount}. "
        f"Government ID {s} has been verified. Ref: {ref}. "
        f"This report is submitted in compliance with AML regulations. "
        f"{pick_filler(2)}",

        # 4
        f"SAR filed by {analyst} regarding {subject}. The customer, "
        f"whose social insurance number is {s}, maintains account {acct} "
        f"at {bank}. Their registered address is {addr}. "
        f"Reachable via {email} or {phone}. "
        f"A total of {amount} in transactions has been flagged. "
        f"No contact has been made with the subject pending investigation. "
        f"{pick_filler(2)}",

        # 5
        f"The compliance team at {bank} has been notified by {analyst} "
        f"of potential suspicious activity involving {subject}. "
        f"Account {acct} received {amount} in unusual deposits. "
        f"Subject located at {addr} with contact details {phone} and "
        f"{email}. SIN {s} confirmed on file. Ref: {ref}. "
        f"This case has been referred to FINTRAC. {pick_filler(2)}",

        # 6
        f"Internal compliance report — confidential. "
        f"Subject: {subject}. Prepared by: {analyst}. "
        f"The subject holds account {acct} at {bank} and resides at {addr}, "
        f"postal code {pc}. Their SIN is {s}. "
        f"Transactions totalling {amount} have been flagged as suspicious. "
        f"Contact information: {phone} and {email}. Reference: {ref}. "
        f"{pick_fillers_pool(FILLER_LEGAL, 2)}",

        # 7
        f"Report ref {ref}: {analyst} escalated a case involving {subject} "
        f"whose {bank} account {acct} shows unusual cash movements of {amount}. "
        f"The individual lives at {addr} and can be contacted at {email} "
        f"or {phone}. Their government-issued SIN is {s}. "
        f"No prior SAR history on file for this customer. "
        f"{pick_fillers_pool(FILLER_INTERNAL, 2)}",

        # 8
        f"This AML report was triggered automatically and reviewed by "
        f"{analyst}. The flagged account belongs to {subject}, born "
        f"and residing at {addr}. Account {acct} at {bank} received "
        f"{amount} in transactions inconsistent with baseline behaviour. "
        f"Customer contact: {phone} / {email}. SIN: {s}. Postal: {pc}. "
        f"Ref: {ref}. {pick_fillers_pool(FILLER_PROCEDURAL, 2)}",
    ]

    text = random.choice(templates)
    return {
        "text": text, "doc_type": "SAR_MEMO",
        "entities": collect(text, [
            (subject,"PERSON"),(analyst,"PERSON"),
            (email,"EMAIL"),(phone,"PHONE"),
            (addr,"ADDRESS"),(s,"SIN"),
            (bank,"ORG"),(acct,"ACCOUNT_NO"),
            (amount,"AMOUNT"),(pc,"POSTAL_CODE"),
        ])
    }


# ══════════════════════════════════════════════════════════════════════════════
# COMPLAINT LETTER — 8 templates
# ══════════════════════════════════════════════════════════════════════════════
def gen_complaint_narrative(names=None):
    name   = rc(random.choice(names) if names else fake.name())
    email  = fake.email()
    phone  = ca_phone()
    city   = random.choice(CITIES)
    prov   = CANADIAN_CITIES_PROV[city]
    pc     = ca_postal(prov)
    addr   = rc(f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}")
    bank   = rc(random.choice(CANADIAN_BANKS))
    acct   = account_no()
    card   = ca_card()
    amount = dollars(50, 5000)
    ref    = ref_no()

    templates = [
        # 1
        f"I am writing to formally dispute an unauthorized transaction. "
        f"My name is {name} and I have been a customer of {bank} "
        f"for several years. On {date.today().isoformat()}, I noticed a "
        f"charge of {amount} on my card {card}, linked to account "
        f"{acct}. I did not authorize this and request an investigation. "
        f"I can be reached at {phone} or {email}. "
        f"My mailing address is {addr}.",

        # 2
        f"This letter formally notifies {bank} of an unauthorized charge "
        f"of {amount} on my card {card}. My account number is "
        f"{acct} and my name is {name}. I reside at {addr} and the best way "
        f"to reach me is by phone at {phone} or by email at {email}. "
        f"I would appreciate a written response mailed to my address. "
        f"Please quote reference {ref} in your reply.",

        # 3
        f"To the customer relations team at {bank}: my name is {name} and I "
        f"am contacting you regarding a fraudulent transaction of {amount} "
        f"on my account {acct}. The charge appeared on card {card}. "
        f"Please investigate urgently. You can contact me at {phone} "
        f"or {email}. I am located at {addr}, postal code {pc}.",

        # 4
        f"Hi, I am {name} and I bank with {bank}. There is a charge of "
        f"{amount} on my statement that I do not recognize on "
        f"card {card} under account {acct}. I did not make this "
        f"purchase and want it reversed. Please call me at {phone} "
        f"or send an email to {email}. My address is {addr}.",

        # 5
        f"Complaint submitted by {name} regarding {bank} account {acct}. "
        f"A transaction of {amount} appeared on card {card} without "
        f"authorization. The customer can be reached at {email} or {phone}. "
        f"Correspondence address: {addr}. Postal code: {pc}. "
        f"Customer is requesting immediate reversal. Ref: {ref}.",

        # 6
        f"I, {name}, wish to file a formal complaint against {bank}. "
        f"An amount of {amount} was charged to my card {card} without my "
        f"knowledge. This card is linked to account {acct}. "
        f"I have tried calling {phone} but could not resolve the issue. "
        f"Please respond to {email} or in writing to {addr}.",

        # 7
        f"Customer complaint — {bank}. Account: {acct}. Card: {card}. "
        f"Name: {name}. Address: {addr}. Phone: {phone}. Email: {email}. "
        f"Unauthorized charge of {amount} identified on {date.today().isoformat()}. "
        f"Customer requesting reversal and written confirmation. "
        f"Reference number: {ref}.",

        # 8
        f"This is to inform {bank} that I, {name}, have identified "
        f"a suspicious charge of {amount} on card number {card} "
        f"associated with my account {acct}. "
        f"I have not made any such transaction and request an immediate "
        f"chargeback. My home address is {addr} and I can be contacted at "
        f"{phone} or via email at {email}. Postal code {pc}.",
    ]

    text = random.choice(templates)
    return {
        "text": text, "doc_type": "COMPLAINT_LETTER",
        "entities": collect(text, [
            (name,"PERSON"),(email,"EMAIL"),(phone,"PHONE"),
            (addr,"ADDRESS"),(bank,"ORG"),
            (acct,"ACCOUNT_NO"),(card,"CREDIT_CARD"),
            (amount,"AMOUNT"),(pc,"POSTAL_CODE"),
        ])
    }


# ══════════════════════════════════════════════════════════════════════════════
# INTERNAL NOTE — 8 templates
# ══════════════════════════════════════════════════════════════════════════════
def gen_internal_note_narrative(names=None):
    customer = rc(random.choice(names) if names else fake.name())
    officer  = rc(random.choice(names) if names else fake.name())
    email    = fake.email()
    phone    = ca_phone()
    city     = random.choice(CITIES)
    prov     = CANADIAN_CITIES_PROV[city]
    pc       = ca_postal(prov)
    addr     = rc(f"{random.randint(1,9999)} {fake.street_name()}, {city}, {prov} {pc}")
    bank     = rc(random.choice(CANADIAN_BANKS))
    acct     = account_no()
    amount   = dollars(500, 200000)
    s        = ca_sin()
    dob      = ca_dob()
    card     = ca_card()
    ref      = ref_no()

    templates = [
        # 1
        f"I spoke with {customer} today regarding the hold placed on their "
        f"account. They called in at {phone} and I verified their date of "
        f"birth as {dob} and social insurance number {s}. The customer "
        f"confirmed their new address as {addr}. Their email is {email}. "
        f"Account {acct} at {bank} has a disputed balance of {amount}. "
        f"I have passed this file to {officer} for follow-up. Ref: {ref}.",

        # 2
        f"Note from {officer}: the customer {customer} visited our {bank} "
        f"branch today and disputed a card charge of {amount} on card {card} "
        f"linked to account {acct}. I verified their identity using date of "
        f"birth {dob} and SIN {s}. Their current address is {addr}, "
        f"postal {pc}. Best contact: {email} and {phone}.",

        # 3
        f"Passing this file to {officer} for action. The customer {customer} "
        f"called to report an unauthorized transfer of {amount} from account "
        f"{acct} at {bank}. They were born on {dob} and their SIN is {s}. "
        f"Address on file: {addr}. Phone: {phone}. Email: {email}. "
        f"Card {card} has also been flagged. {pick_filler(1)}",

        # 4
        f"Quick note regarding {customer}: flagged transaction of {amount} "
        f"on account {acct}. Customer date of birth is {dob} and SIN is "
        f"{s}. They are currently living at {addr} and can be reached at "
        f"{email} or {phone}. Their card {card} at {bank} is under review. "
        f"{officer} has been assigned to this case. {pick_filler(1)}",

        # 5
        f"Branch handoff from {officer} to compliance: the customer "
        f"{customer} has a disputed transaction of {amount} on account "
        f"{acct} at {bank}. Born {dob}, SIN {s}, address {addr}, "
        f"postal code {pc}. Contact via {phone} or {email}. "
        f"Card on file: {card}. Ref: {ref}. Immediate review requested.",

        # 6
        f"Case ref {ref} — {officer} notes: spoke to {customer} re account "
        f"{acct} at {bank}. Customer disputing {amount} charge on card {card}. "
        f"Verified DOB {dob} and SIN {s}. Address: {addr}. "
        f"Phone: {phone}. Email: {email}. Escalating to fraud team. "
        f"{pick_fillers_pool(FILLER_INTERNAL, 1)}",

        # 7
        f"Internal memo — {officer} to compliance: "
        f"{customer} (SIN: {s}, DOB: {dob}) contacted the branch regarding "
        f"unusual activity on account {acct}. Total amount flagged: {amount}. "
        f"Customer resides at {addr}, postal {pc}. "
        f"Reachable at {phone} or {email}. Bank: {bank}. Card: {card}. "
        f"{pick_fillers_pool(FILLER_LEGAL, 1)}",

        # 8
        f"File update by {officer}: account review for {customer} completed. "
        f"Born {dob}. Government ID (SIN): {s}. "
        f"Lives at {addr}. Correspondence to {email}, calls to {phone}. "
        f"Account {acct} at {bank} flagged for {amount}. "
        f"Card {card} suspended pending investigation. "
        f"Postal: {pc}. Ref: {ref}. {pick_filler(2)}",
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
    gen_kyc_narrative,
    gen_wire_transfer_narrative,
    gen_loan_narrative,
    gen_statement_narrative,
    gen_sar_narrative,
    gen_complaint_narrative,
    gen_internal_note_narrative,
]


def generate_dataset(n: int = 500, names=None) -> list:
    """
    Generate n synthetic banking documents — all pure narrative prose.

    Default n=500 for quick test run.
    Use n=7000 for full training run.

    Each doc type has 8 templates × random_case × random fillers
    = high structural variation, prevents positional overfitting.
    """
    docs = [GENERATORS[i % len(GENERATORS)](names=names) for i in range(n)]
    random.shuffle(docs)
    return docs