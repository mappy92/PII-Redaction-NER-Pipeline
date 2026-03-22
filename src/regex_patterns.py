"""
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
        r"\b[1-9]\d{2}[\s\-]\d{3}[\s\-]\d{3}\b(?!\d)"
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
