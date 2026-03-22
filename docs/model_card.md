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
