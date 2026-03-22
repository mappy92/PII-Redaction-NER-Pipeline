"""
app.py: Canadian Banking PII Redactor
Professional banking-themed Streamlit app with colour-coded entity highlighting
Built by Manpreet Singh | linkedin.com/in/manpreet-singh-ds
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import html

st.set_page_config(
    page_title="Canadian Banking PII Redactor",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Banking Theme CSS ─────────────────────────────────────────────────────────
BANK_THEME = """
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@400;500;600&display=swap');

/* ── Banking Colour Variables ── */
:root {
    --bank-blue:       #1A3A6B;
    --bank-dark-blue:  #0D1F3C;
    --bank-dark-black:  #000000;
    --bank-mid-blue:   #1E3D6F;
    --bank-gold:       #C9A84C;
    --bank-gold-light: #F0D080;
    --bank-light:      #F5F6FA;
    --bank-border:     #D4D9E8;
    --bank-text:       #1A1A2E;
    --bank-muted:      #5A6A7E;
    --bank-success:    #1B6E3A;
    --bank-danger:     #C0392B;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif !important;
    color: var(--bank-text) !important;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── App background ── */
.stApp {
    background: linear-gradient(160deg, #F5F6FA 0%, #ECEEF5 100%) !important;
}

/* ── Top header bar ── */
.bank-header {
    background: linear-gradient(135deg, var(--bank-dark-blue) 0%, var(--bank-blue) 100%);
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(13,31,60,0.3);
    position: relative;
    overflow: hidden;
}
.bank-header::before {
    content: '';
    position: absolute;
    right: -60px; top: -60px;
    width: 220px; height: 220px;
    background: rgba(201,168,76,0.1);
    border-radius: 50%;
}
.bank-header::after {
    content: '';
    position: absolute;
    right: 60px; bottom: -80px;
    width: 180px; height: 180px;
    background: rgba(201,168,76,0.06);
    border-radius: 50%;
}
.bank-header-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.3px;
    margin: 0 !important;
    line-height: 1.2;
}
.bank-header-title,
.bank-header-title * { color: #FFFFFF !important; }

.bank-header-subtitle {
    font-size: 13px;
    color: rgba(255,255,255,0.70) !important;
    margin-top: 4px;
    font-weight: 400;
    letter-spacing: 0.3px;
}
.bank-header-subtitle,
.bank-header-subtitle * { color: rgba(255,255,255,0.70) !important; }

.bank-badge {
    background: var(--bank-gold);
    color: var(--bank-dark-blue) !important;
    font-weight: 700;
    font-size: 11px;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    white-space: nowrap;
}

/* ── Cards ── */
.bank-card {
    background: #FFFFFF;
    border: 1px solid var(--bank-border);
    border-radius: 10px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(13,31,60,0.07);
}

/* ── Metric cards — dark background ── */
[data-testid="metric-container"] {
    background: var(--bank-dark-blue) !important;
    border: 1px solid rgba(201,168,76,0.3) !important;
    border-radius: 10px !important;
    padding: 16px 20px !important;
    box-shadow: 0 2px 8px rgba(13,31,60,0.2) !important;
}
[data-testid="metric-container"] p,
[data-testid="metric-container"] span,
[data-testid="metric-container"] div,
[data-testid="metric-container"] label {
    color: #FFFFFF !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
    color: rgba(255,255,255,0.6) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--bank-gold-light) !important;
    font-weight: 700 !important;
    font-size: 28px !important;
}

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--bank-blue) 0%, var(--bank-mid-blue) 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 12px 28px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 3px 12px rgba(26,58,107,0.3) !important;
}
.stButton > button[kind="primary"] p,
.stButton > button[kind="primary"] span,
.stButton > button[kind="primary"] div {
    color: #FFFFFF !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 5px 18px rgba(26,58,107,0.45) !important;
    transform: translateY(-1px) !important;
}

/* ── Selectbox & TextArea ── */
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    border: 1.5px solid var(--bank-border) !important;
    border-radius: 8px !important;
    background: #FFFFFF !important;
    font-family: 'Source Sans 3', sans-serif !important;
    color: var(--bank-text) !important;
}
.stSelectbox > div > div:focus-within,
.stTextArea > div > div > textarea:focus {
    border-color: var(--bank-blue) !important;
    box-shadow: 0 0 0 3px rgba(26,58,107,0.12) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bank-light) !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--bank-border) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: var(--bank-muted) !important;
    padding: 8px 16px !important;
}
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] div {
    color: var(--bank-muted) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bank-blue) !important;
    color: #FFFFFF !important;
}
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] div {
    color: #FFFFFF !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--bank-border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bank-dark-black) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] strong {
    color: rgba(255,255,255,0.92) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 15px !important;
    border-bottom: 2px solid var(--bank-gold) !important;
    padding-bottom: 6px !important;
    margin-bottom: 12px !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}
[data-testid="stSidebar"] a {
    color: var(--bank-gold-light) !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: rgba(255,255,255,0.6) !important;
    font-size: 12px !important;
}
[data-testid="stSidebar"] code {
    background: rgba(255,255,255,0.12) !important;
    color: var(--bank-gold-light) !important;
    border-radius: 4px;
    padding: 1px 5px;
}

/* ── Main content — targeted dark text only ── */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stText"] p,
[data-testid="stCaptionContainer"] p,
.section-label,
.stTabs [data-baseweb="tab-panel"] p,
.stTabs [data-baseweb="tab-panel"] span,
.stTabs [data-baseweb="tab-panel"] label,
.stTabs [data-baseweb="tab-panel"] div {
    color: var(--bank-text) !important;
}
[data-testid="stCaptionContainer"] p {
    color: var(--bank-muted) !important;
    font-size: 12px !important;
}



/* ── Tab panels — force white bg (overrides Sapling/extensions) ── */
.stTabs [data-baseweb="tab-panel"] {
    background: #FFFFFF !important;
    border-radius: 0 0 8px 8px !important;
    border: 1px solid var(--bank-border) !important;
    border-top: none !important;
    padding: 16px !important;
}
.stTabs [data-baseweb="tab-panel"] * {
    background-color: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] p,
.stTabs [data-baseweb="tab-panel"] span,
.stTabs [data-baseweb="tab-panel"] div,
.stTabs [data-baseweb="tab-panel"] label {
    color: var(--bank-text) !important;
}

/* ── Status badges ── */
.bank-status-ok {
    background: rgba(27,110,58,0.3);
    border: 1px solid #4ADE80;
    color: #22904a !important;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: 600;
}
.bank-status-err {
    background: rgba(185,28,28,0.3);
    border: 1px solid #FCA5A5;
    color: #FCA5A5 !important;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: 600;
}

/* ── Divider ── */
hr {
    border-color: var(--bank-border) !important;
    margin: 20px 0 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1px solid var(--bank-border) !important;
    border-radius: 8px !important;
    background: #FFFFFF !important;
}

/* ── Section labels ── */
.section-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--bank-muted);
    margin-bottom: 8px;
}

/* ── Gold accent line ── */
.bank-accent-line {
    height: 3px;
    background: linear-gradient(90deg, var(--bank-gold), transparent);
    border-radius: 2px;
    margin-bottom: 20px;
}
</style>
"""

st.markdown(BANK_THEME, unsafe_allow_html=True)

# ── Entity colour map ─────────────────────────────────────────────────────────
ENTITY_COLOURS = {
    "PERSON":       "#1A3A6B",   # Deep Navy
    "ORG":          "#1E3D6F",   # Mid Navy
    "ADDRESS":      "#B45309",   # Amber
    "EMAIL":        "#6D28D9",   # Violet
    "PHONE":        "#0E7490",   # Teal
    "ACCOUNT_NO":   "#C2410C",   # Orange Red
    "TRANSIT_NO":   "#7C3AED",   # Purple
    "CREDIT_CARD":  "#B91C1C",   # Red
    "SIN":          "#BE185D",   # Pink
    "POSTAL_CODE":  "#374151",   # Slate
    "DOB":          "#92400E",   # Brown
    "AMOUNT":       "#1B6E3A",   # Dark Green
    "SWIFT":        "#0D1F3C",   # Dark Navy
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
    try:
        import spacy
        from src.regex_patterns import regex_find, deduplicate
        nlp = spacy.load("model/model-best")
        return nlp, regex_find, deduplicate, True
    except Exception as e:
        return None, None, None, str(e)


def detect_entities(text, nlp, regex_find, deduplicate):
    doc        = nlp(text)
    spacy_ents = [(e.start_char, e.end_char, e.label_) for e in doc.ents]
    regex_ents = regex_find(text)
    combined   = spacy_ents + regex_ents
    return sorted(deduplicate(combined), key=lambda x: x[0])


def redact_text(text, entities):
    chars = list(text)
    for start, end, label in sorted(entities, key=lambda x: -x[0]):
        token = REDACTION_MAP.get(label, REDACTION_MAP["DEFAULT"])
        chars[start:end] = list(token)
    return "".join(chars)


def _html_wrapper(content, bg="#FFFFFF"):
    """Wrap entity HTML in a styled scrollable container."""
    return f"""
    <html><head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500&display=swap');
        body {{
            margin: 0; padding: 20px;
            font-family: 'Source Sans 3', sans-serif;
            font-size: 14px;
            line-height: 2;
            color: #1A1A2E;
            background: {bg};
        }}
        mark {{
            border-radius: 4px;
            padding: 2px 7px;
            font-weight: 600;
            margin: 0 1px;
            color: white;
        }}
        sup {{
            font-size: 0.6em;
            margin-left: 3px;
            opacity: 0.85;
        }}
    </style></head><body>{content}</body></html>
    """


def highlight_html(text, entities):
    if not entities:
        return _html_wrapper(f"<pre style='white-space:pre-wrap'>{html.escape(text)}</pre>")
    result, prev = [], 0
    for start, end, label in sorted(entities, key=lambda x: x[0]):
        result.append(html.escape(text[prev:start]).replace('\n', '<br>'))
        colour = ENTITY_COLOURS.get(label, "#607D8B")
        result.append(
            f'<mark style="background:{colour}">'
            f'{html.escape(text[start:end])}'
            f'<sup>{label}</sup></mark>'
        )
        prev = end
    result.append(html.escape(text[prev:]).replace('\n', '<br>'))
    return _html_wrapper("".join(result))


def redact_html(text, entities):
    if not entities:
        return _html_wrapper(f"<pre style='white-space:pre-wrap'>{html.escape(text)}</pre>", "#F4F7FB")
    result, prev = [], 0
    for start, end, label in sorted(entities, key=lambda x: x[0]):
        result.append(html.escape(text[prev:start]).replace('\n', '<br>'))
        colour = ENTITY_COLOURS.get(label, "#607D8B")
        token  = REDACTION_MAP.get(label, REDACTION_MAP["DEFAULT"])
        result.append(f'<mark style="background:{colour}">{token}</mark>')
        prev = end
    result.append(html.escape(text[prev:]).replace('\n', '<br>'))
    return _html_wrapper("".join(result), "#F4F7FB")


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

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bank-header">
    <div>
        <div class="bank-header-title">🏦 Canadian Banking PII Redactor</div>
        <div class="bank-header-subtitle">
            spaCy NER + Regex two-layer pipeline · Built for regulated, audit-ready redaction
        </div>
    </div>
    <div class="bank-badge">NER Pipeline · v1.0</div>
</div>
<div class="bank-accent-line"></div>
""", unsafe_allow_html=True)

# ── Load model ─────────────────────────────────────────────────────────────────
nlp, regex_find, deduplicate, model_status = load_model()
model_loaded = model_status is True

# ── Input panel ───────────────────────────────────────────────────────────────
col_main, col_side = st.columns([3, 1], gap="large")

with col_main:
    st.markdown('<div class="section-label">Load a sample document</div>', unsafe_allow_html=True)
    doc_type = st.selectbox(
        "Sample", ["Paste your own..."] + list(SAMPLES.keys()),
        label_visibility="collapsed"
    )
    default_text = SAMPLES.get(doc_type, "") if doc_type != "Paste your own..." else ""

    st.markdown('<div class="section-label" style="margin-top:16px">Document text</div>', unsafe_allow_html=True)
    text = st.text_area(
        "Document",
        value=default_text,
        height=220,
        label_visibility="collapsed",
        placeholder="Paste any Canadian banking document here: KYC forms, SARs, wire transfers, internal notes..."
    )

    run = st.button(
        "🔍  Detect & Redact PII",
        type="primary",
        use_container_width=True,
        disabled=not model_loaded
    )

with col_side:
    st.markdown('<div class="section-label">Pipeline status</div>', unsafe_allow_html=True)
    if model_loaded:
        st.markdown(
            '<div class="bank-status-ok">✅ &nbsp;NER Model Ready</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='font-size:12px;color:#5A6A7E;margin-top:6px'>"
            "spaCy <code style='background:#F5F6FA;color:#1A3A6B;border:1px solid #D4D9E8;"
            "border-radius:3px;padding:1px 4px;font-size:11px'>en_core_web_trf</code> "
            "· Canadian banking fine-tune</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="bank-status-err">⚠️ &nbsp;Model Unavailable</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='font-size:12px;color:#B91C1C;margin-top:6px'>Error: {model_status}</p>",
            unsafe_allow_html=True
        )

    st.markdown("<hr style='border-color:#D4D9E8;margin:16px 0'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-label'>About</div>"
        "<p style='font-size:12px;color:#5A6A7E;line-height:1.65;margin-top:4px'>"
        "Two-layer pipeline: spaCy transformer NER catches contextual entities "
        "while regex patterns enforce format-specific rules (SIN, account numbers, postal codes)."
        "</p>",
        unsafe_allow_html=True
    )

# ── Results ────────────────────────────────────────────────────────────────────
if run and text:
    with st.spinner("Scanning document for PII..."):
        entities = detect_entities(text, nlp, regex_find, deduplicate)

    st.markdown("---")

    # Quick metrics row
    total_pii = len(entities)
    df_preview = pd.DataFrame([
        {
            "Original Text": text[s:e],
            "Label":         label,
            "Start":         s,
            "End":           e,
            "Redacted As":   REDACTION_MAP.get(label, "[REDACTED]"),
        }
        for s, e, label in entities
    ]) if entities else pd.DataFrame()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("PII Entities Found",  total_pii)
    m2.metric("Unique Types",        df_preview["Label"].nunique() if not df_preview.empty else 0)
    m3.metric("Document Length",     f"{len(text):,} chars")
    m4.metric("PII Density",
              f"{total_pii / max(len(text.split()), 1) * 100:.1f}%")

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎨  Highlighted Original",
        "🛡️  Redacted Output",
        "📊  Entity Breakdown",
        "ℹ️  About this Project",
    ])

    with tab1:
        st.markdown(
            '<div class="section-label">Original text with PII highlighted by entity type</div>',
            unsafe_allow_html=True
        )
        components.html(highlight_html(text, entities), height=380, scrolling=True)

    with tab2:
        st.markdown(
            '<div class="section-label">Redacted text: PII replaced with colour-coded tokens</div>',
            unsafe_allow_html=True
        )
        components.html(redact_html(text, entities), height=380, scrolling=True)

        with st.expander("📋  Plain text (for copying)"):
            st.text(redact_text(text, entities))

    with tab3:
        if not df_preview.empty:
            st.dataframe(
                df_preview,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Original Text": st.column_config.TextColumn(width="medium"),
                    "Label":         st.column_config.TextColumn(width="small"),
                    "Redacted As":   st.column_config.TextColumn(width="medium"),
                    "Start":         st.column_config.NumberColumn(width="small"),
                    "End":           st.column_config.NumberColumn(width="small"),
                }
            )
        else:
            st.info("No PII detected in this document.")

    with tab4:
        c1, c2 = st.columns([3, 2], gap="large")
        with c1:
            st.markdown("""
<div style='background:#FFFFFF;border:1px solid #D4D9E8;border-radius:10px;padding:28px;'>
<h3 style='font-family:Playfair Display,serif;color:#0D1F3C;font-size:20px;margin-top:0;
border-bottom:2px solid #C9A84C;padding-bottom:8px;margin-bottom:16px'>
🏦 Project Overview
</h3>
<p style='color:#1A1A2E;line-height:1.75;font-size:14px'>
This tool was built to automate PII detection and redaction across Canadian banking
documents: KYC forms, SARs, wire transfer records, complaint letters, and internal notes.
It combines a fine-tuned <strong>spaCy transformer NER model</strong> with a
<strong>regex fallback layer</strong> to achieve high recall on format-specific
entities that context-based models often miss.
</p>
<h4 style='color:#1A3A6B;font-size:14px;margin-top:20px;margin-bottom:8px'>⚙️ Pipeline Architecture</h4>
<p style='color:#1A1A2E;line-height:1.75;font-size:14px'>
<strong>Layer 1: spaCy NER:</strong> Transformer-based model (<code style='background:#F5F6FA;
color:#1A3A6B;border:1px solid #D4D9E8;border-radius:3px;padding:1px 4px'>en_core_web_trf</code>)
fine-tuned on Canadian banking narrative text. Catches contextual entities like PERSON, ORG, ADDRESS.<br><br>
<strong>Layer 2: Regex Patterns:</strong> Format-enforced rules for SIN, account numbers,
transit numbers, SWIFT codes, postal codes, credit cards, and phone numbers.
Catches what context alone misses.<br><br>
<strong>Deduplication:</strong> Span-level merging removes overlapping or duplicate detections
from both layers before rendering.
</p>
<h4 style='color:#1A3A6B;font-size:14px;margin-top:20px;margin-bottom:8px'>📋 Supported Entities</h4>
<p style='color:#1A1A2E;line-height:1.75;font-size:14px'>
PERSON · ORG · ADDRESS · EMAIL · PHONE · ACCOUNT_NO · TRANSIT_NO ·
CREDIT_CARD · SIN · POSTAL_CODE · DOB · AMOUNT · SWIFT
</p>
<h4 style='color:#1A3A6B;font-size:14px;margin-top:20px;margin-bottom:8px'>🏛️ Regulatory Context</h4>
<p style='color:#1A1A2E;line-height:1.75;font-size:14px'>
Built with Canadian banking compliance in mind, covering FINTRAC AML reporting, PIPEDA privacy
requirements, and OSFI data governance standards. Designed to produce audit-ready
redacted documents for downstream model training and compliance workflows.
</p>
</div>
""", unsafe_allow_html=True)

        with c2:
            st.markdown("""
<div style='background:#FFFFFF;border:1px solid #D4D9E8;border-radius:10px;padding:28px;margin-bottom:16px'>
<h3 style='font-family:Playfair Display,serif;color:#0D1F3C;font-size:18px;margin-top:0;
border-bottom:2px solid #C9A84C;padding-bottom:8px;margin-bottom:16px'>
👤 Built by
</h3>
<p style='color:#1A1A2E;font-size:15px;font-weight:700;margin-bottom:4px'>Manpreet Singh</p>
<p style='color:#5A6A7E;font-size:13px;line-height:1.7;margin-top:0'>
Data Scientist · 3+ yrs ML/AI<br>
8+ yrs Software Engineering<br>
MBA (Business Analytics), Brock University
</p>
<div style='margin-top:14px;display:flex;gap:10px;flex-wrap:wrap'>
<a href='https://linkedin.com/in/manpreet-singh-ds' target='_blank'
style='background:#1A3A6B;color:black;text-decoration:none;padding:6px 14px;
border-radius:6px;font-size:12px;font-weight:600'>🔗 LinkedIn</a>
<a href='https://github.com/mappy92' target='_blank'
style='background:#0D1F3C;color:black;text-decoration:none;padding:6px 14px;
border-radius:6px;font-size:12px;font-weight:600'>🐙 GitHub</a>
</div>
</div>

<div style='background:#FFFFFF;border:1px solid #D4D9E8;border-radius:10px;padding:28px'>
<h3 style='font-family:Playfair Display,serif;color:#0D1F3C;font-size:18px;margin-top:0;
border-bottom:2px solid #C9A84C;padding-bottom:8px;margin-bottom:16px'>
🛠️ Tech Stack
</h3>
<div style='display:flex;flex-wrap:wrap;gap:8px'>
""" + "".join([
    f"<span style='background:#F5F6FA;border:1px solid #D4D9E8;color:#1A3A6B;"
    f"border-radius:20px;padding:4px 12px;font-size:12px;font-weight:600'>{t}</span>"
    for t in [
        "Python 3.11", "spaCy 3.7", "en_core_web_trf", "Streamlit",
        "Regex NLP", "Pandas", "Scikit-learn", "Matplotlib",
        "HuggingFace Hub", "Azure ML", "FINTRAC AML", "PIPEDA"
    ]
]) + """
</div>
</div>
""", unsafe_allow_html=True)

elif run and not text:
    st.warning("Please paste or select a document to scan.")


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h2 style='font-size:15px;margin-top:0;font-family:Playfair Display,serif;"
        "color:#0D1F3C;border-bottom:2px solid #C9A84C;padding-bottom:6px'>Entity Legend</h2>",
        unsafe_allow_html=True
    )

    for label, colour in ENTITY_COLOURS.items():
        st.markdown(
            f'<div style="display:flex;align-items:center;margin-bottom:7px;gap:10px">'
            f'<div style="width:13px;height:13px;border-radius:3px;'
            f'background:{colour};flex-shrink:0;border:1px solid rgba(0,0,0,0.1)"></div>'
            f'<span style="font-size:13px;font-weight:500;color:#1A1A2E">{label}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown(
        "<h2 style='font-size:15px;font-family:Playfair Display,serif;"
        "color:#0D1F3C;border-bottom:2px solid #C9A84C;padding-bottom:6px'>Built by</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style='font-size:13px;line-height:1.85;color:#1A1A2E'>
            <strong style='font-size:14px;color:#0D1F3C'>Manpreet Singh</strong><br>
            <span style='color:#5A6A7E'>Data Scientist · 3+ yrs ML/AI</span><br>
            <span style='color:#5A6A7E'>8+ yrs Software Engineering</span><br>
            <span style='color:#5A6A7E'>MBA, Brock University</span><br><br>
            <a href='https://linkedin.com/in/manpreet-singh-ds' target='_blank'
               style='color:#1A3A6B;font-weight:600;text-decoration:none'>🔗 LinkedIn</a>
            &nbsp;·&nbsp;
            <a href='https://github.com/mappy92' target='_blank'
               style='color:#1A3A6B;font-weight:600;text-decoration:none'>🐙 GitHub</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:11px;color:#8A9AB0;line-height:1.7'>"
        "TD Bank · Ministry of Transportation<br>"
        "Azure DP-100 · Power BI · spaCy NER · RAG"
        "</div>",
        unsafe_allow_html=True
    )