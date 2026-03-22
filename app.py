"""
app.py — Canadian Banking PII Redactor
Streamlit app with colour-coded entity highlighting
"""

import streamlit as st
import pandas as pd
import html

st.set_page_config(
    page_title="Canadian Banking PII Redactor",
    page_icon="🏦",
    layout="wide",
)

# ── Entity colour map ──────────────────────────────────────────────────────────
ENTITY_COLOURS = {
    "PERSON":       "#4472C4",   # Blue
    "ORG":          "#70AD47",   # Green
    "ADDRESS":      "#FF7043",   # Orange
    "EMAIL":        "#AB47BC",   # Purple
    "PHONE":        "#00ACC1",   # Teal
    "ACCOUNT_NO":   "#F4511E",   # Deep Orange
    "TRANSIT_NO":   "#8D6E63",   # Brown
    "CREDIT_CARD":  "#E53935",   # Red
    "SIN":          "#D81B60",   # Pink
    "POSTAL_CODE":  "#546E7A",   # Blue Grey
    "DOB":          "#6D4C41",   # Dark Brown
    "AMOUNT":       "#558B2F",   # Dark Green
    "SWIFT":        "#1565C0",   # Dark Blue
}

REDACTION_MAP = {
    "PERSON":       "[NAME REDACTED]",
    "ORG":          "[ORG REDACTED]",
    "ADDRESS":      "[ADDRESS REDACTED]",
    "EMAIL":        "[EMAIL REDACTED]",
    "PHONE":        "[PHONE REDACTED]",
    "ACCOUNT_NO":   "[ACCOUNT REDACTED]",
    "TRANSIT_NO":   "[TRANSIT REDACTED]",
    "CREDIT_CARD":  "[CARD REDACTED]",
    "SIN":          "[SIN REDACTED]",
    "POSTAL_CODE":  "[POSTAL REDACTED]",
    "DOB":          "[DOB REDACTED]",
    "AMOUNT":       "[AMOUNT REDACTED]",
    "SWIFT":        "[SWIFT REDACTED]",
    "DEFAULT":      "[REDACTED]",
}


# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading NER model...")
def load_model():
    import spacy
    from src.regex_patterns import regex_find, deduplicate
    nlp = spacy.load("./model/model-best")
    return nlp, regex_find, deduplicate


def detect_entities(text, nlp, regex_find, deduplicate):
    """Run spaCy NER + regex fallback, return merged deduplicated entities."""
    doc         = nlp(text)
    spacy_ents  = [(e.start_char, e.end_char, e.label_) for e in doc.ents]
    regex_ents  = regex_find(text)
    combined    = spacy_ents + regex_ents
    return sorted(deduplicate(combined), key=lambda x: x[0])


def redact_text(text, entities):
    """Replace entity spans with redaction tokens."""
    chars = list(text)
    for start, end, label in sorted(entities, key=lambda x: -x[0]):
        token = REDACTION_MAP.get(label, REDACTION_MAP["DEFAULT"])
        chars[start:end] = list(token)
    return "".join(chars)


def highlight_html(text, entities):
    """
    Build HTML with coloured highlights for each entity.
    Original text with coloured background spans.
    """
    if not entities:
        return f"<pre style='font-family:monospace;white-space:pre-wrap'>{html.escape(text)}</pre>"

    result = []
    prev   = 0
    for start, end, label in sorted(entities, key=lambda x: x[0]):
        # Add plain text before this entity
        result.append(html.escape(text[prev:start]))
        # Add highlighted entity
        colour     = ENTITY_COLOURS.get(label, "#BDBDBD")
        entity_txt = html.escape(text[start:end])
        result.append(
            f'<mark style="background:{colour};color:white;'
            f'padding:2px 6px;border-radius:4px;font-weight:bold;'
            f'margin:0 2px" title="{label}">'
            f'{entity_txt}'
            f'<sup style="font-size:0.65em;margin-left:3px">{label}</sup>'
            f'</mark>'
        )
        prev = end
    result.append(html.escape(text[prev:]))

    return (
        f"<div style='font-family:monospace;white-space:pre-wrap;"
        f"line-height:2;font-size:14px'>"
        + "".join(result)
        + "</div>"
    )


def redact_html(text, entities):
    """
    Build HTML of redacted text with coloured redaction tokens.
    """
    if not entities:
        return f"<pre style='font-family:monospace;white-space:pre-wrap'>{html.escape(text)}</pre>"

    result = []
    prev   = 0
    for start, end, label in sorted(entities, key=lambda x: x[0]):
        result.append(html.escape(text[prev:start]))
        colour = ENTITY_COLOURS.get(label, "#BDBDBD")
        token  = REDACTION_MAP.get(label, REDACTION_MAP["DEFAULT"])
        result.append(
            f'<mark style="background:{colour};color:white;'
            f'padding:2px 6px;border-radius:4px;font-weight:bold;'
            f'margin:0 2px">'
            f'{token}'
            f'</mark>'
        )
        prev = end
    result.append(html.escape(text[prev:]))

    return (
        f"<div style='font-family:monospace;white-space:pre-wrap;"
        f"line-height:2;font-size:14px'>"
        + "".join(result)
        + "</div>"
    )


# ── Sample documents ───────────────────────────────────────────────────────────
SAMPLES = {
    "KYC Form": """\
The know-your-customer review for Sarah Kowalski was completed today. \
The customer provided a date of birth of 1984-07-22 and a social insurance \
number of 482-716-930. Their current residential address is recorded as \
47 Lakeshore Blvd W, Toronto, ON M6K 1C3. Contact information on file \
includes phone number 416-555-0192 and email address sarah.kowalski@outlook.com. \
The customer holds account 00152-004-7823941 with transit number 00152-004 at TD Bank.""",

    "Wire Transfer": """\
A wire transfer request was submitted by Omar Farouq, who holds account \
00342-003-9182736 at Royal Bank of Canada. The sender can be reached at \
613-555-0847 or o.farouq@gmail.com. The requested transfer amount is \
$42,500.00 to be sent to Global Trade Corp at HSBC Canada, account \
00891-006-4421198. The receiving institution SWIFT code is HKBCCA2T.""",

    "SAR Memo": """\
This suspicious activity report was prepared by Jing-Wei Huang following \
the identification of unusual transactions on the account of Maria Santos. \
The subject resides at 891 Rideau St, Ottawa, ON K1N 5Y3 and has provided \
613-555-2291 and m.santos@hotmail.com as contact information. Their account \
00671-010-2234891 at Bank of Nova Scotia received deposits totalling \
$185,000.00. SIN on file: 312-445-788.""",

    "Complaint Letter": """\
I am writing to formally dispute an unauthorized transaction. My name is \
Priya Sharma and I have been a customer of CIBC for several years. On \
2025-03-15 I noticed a charge of $312.00 on my card 4532-1122-3344-5566 \
linked to account 00234-004-5512389. I did not authorize this. \
I can be reached at 905-555-0334 or priya.s@gmail.com. \
My mailing address is 22 King St W, Hamilton, ON L8P 1A1.""",

    "Internal Note": """\
I spoke with roberto sanchez today regarding the hold placed on their account. \
They called in at 289-441-9901 and I verified their date of birth as \
1979-11-03 and social insurance number 527-384-910. The customer confirmed \
their new address as 99 Wellington St W, Toronto, ON M5K 1J3. \
Their email is roberto.s@gmail.com. Account 00891-003-7712334 at bmo \
has a disputed balance of $15,750.00. Passed to fatima al-hassan for follow-up.""",
}


# ══════════════════════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════════════════════

st.title("🏦 Canadian Banking Document PII Redactor")
st.caption(
    "Detects and redacts PII using spaCy NER + regex · "
    "Built by [Manpreet Singh](https://linkedin.com/in/manpreet-singh-ds)"
)
st.divider()

# ── Load model ─────────────────────────────────────────────────────────────────
try:
    nlp, regex_find, deduplicate = load_model()
    model_loaded = True
except Exception as e:
    st.warning(f"⚠️ Model not loaded: {e}")
    model_loaded = False

# ── Input ──────────────────────────────────────────────────────────────────────
col_input, col_spacer = st.columns([3, 1])

with col_input:
    doc_type = st.selectbox(
        "Load a sample document",
        ["— paste your own —"] + list(SAMPLES.keys())
    )
    default_text = SAMPLES.get(doc_type, "") if doc_type != "— paste your own —" else ""
    text = st.text_area(
        "Document text",
        value=default_text,
        height=200,
        label_visibility="collapsed",
        placeholder="Paste any banking document here..."
    )
    run = st.button("🔍 Detect & Redact PII", type="primary", use_container_width=True)

# ── Results ────────────────────────────────────────────────────────────────────
if run and text:
    if not model_loaded:
        st.error("Model not loaded. Run notebooks 01-03 first.")
    else:
        with st.spinner("Scanning for PII..."):
            entities = detect_entities(text, nlp, regex_find, deduplicate)

        st.divider()

        # ── Three tabs: Highlighted | Redacted | Entities
        tab1, tab2, tab3 = st.tabs([
            "🎨 Highlighted Original",
            "🛡️ Redacted Output",
            "📊 Entity Breakdown"
        ])

        with tab1:
            st.markdown("**Original text with PII highlighted by entity type:**")
            st.markdown(highlight_html(text, entities), unsafe_allow_html=True)

        with tab2:
            st.markdown("**Redacted text — PII replaced with colour-coded tokens:**")
            st.markdown(redact_html(text, entities), unsafe_allow_html=True)

            # Plain text copy version
            with st.expander("📋 Plain text redacted (for copying)"):
                st.text(redact_text(text, entities))

        with tab3:
            if entities:
                # Summary metrics
                df = pd.DataFrame([
                    {
                        "Original Text": text[s:e],
                        "Label":         label,
                        "Start":         s,
                        "End":           e,
                        "Redacted As":   REDACTION_MAP.get(label,"[REDACTED]"),
                    }
                    for s, e, label in entities
                ])

                # Top metrics row
                cols = st.columns(4)
                cols[0].metric("Total PII Found",  len(entities))
                cols[1].metric("Unique Types",     df["Label"].nunique())
                cols[2].metric("Document Length",  f"{len(text)} chars")
                cols[3].metric("PII Density",      f"{len(entities)/max(len(text.split()),1)*100:.1f}%")

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Original Text": st.column_config.TextColumn(width="medium"),
                        "Label":         st.column_config.TextColumn(width="small"),
                        "Redacted As":   st.column_config.TextColumn(width="medium"),
                    }
                )
            else:
                st.info("No PII detected in this document.")

# ── Colour legend sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.header("🎨 Entity Colour Legend")
    for label, colour in ENTITY_COLOURS.items():
        st.markdown(
            f'<div style="display:flex;align-items:center;margin-bottom:6px">'
            f'<div style="width:16px;height:16px;border-radius:3px;'
            f'background:{colour};margin-right:10px;flex-shrink:0"></div>'
            f'<code style="font-size:12px">{label}</code>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.divider()
    st.header("📈 Model Info")
    if model_loaded:
        st.success("Model loaded ✅")
        st.caption("spaCy NER + regex two-layer pipeline")
        st.caption("Trained on Canadian banking narrative docs")
    else:
        st.error("Model not loaded")

    st.divider()
    st.caption("Built by Manpreet Singh")
    st.caption("[GitHub](https://github.com/mappy92) · [LinkedIn](https://linkedin.com/in/manpreet-singh-ds)")