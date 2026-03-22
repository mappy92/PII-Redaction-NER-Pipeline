"""
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
