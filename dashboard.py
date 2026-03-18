# ══════════════════════════════════════════════════════════════════════
#  BRAND INTELLIGENCE  —  dashboard.py
#  Full analysis dashboard for brand intelligence CSV files.
#  Run: streamlit run dashboard.py
# ══════════════════════════════════════════════════════════════════════

import io
import re
import html as _html_mod
from collections import Counter

import streamlit as st
import pandas as pd

# ─── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Brand Intelligence Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

:root {
    --bg:        #f5f0e8;
    --bg2:       #ede8dc;
    --ink:       #1a1410;
    --ink2:      #4a3f35;
    --ink3:      #8a7968;
    --accent:    #c4391a;
    --accent2:   #2d6a4f;
    --accent3:   #1a4a7a;
    --border:    #c8bfb0;
    --card:      #faf7f2;
    --gold:      #b8860b;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Mono', monospace;
    background: var(--bg) !important;
    color: var(--ink);
}

#MainMenu, footer, header { visibility: hidden; }
.stApp { background: var(--bg) !important; }

/* ── Masthead ── */
.masthead {
    border-top: 4px solid var(--ink);
    border-bottom: 1px solid var(--ink);
    padding: 2rem 0 1.5rem;
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
}
.masthead::before {
    content: '';
    position: absolute;
    top: 8px;
    left: 0; right: 0;
    border-top: 1px solid var(--ink);
}
.masthead h1 {
    font-family: 'Playfair Display', serif;
    font-weight: 900;
    font-size: 3.2rem;
    color: var(--ink);
    letter-spacing: -0.02em;
    margin: 0 0 0.3rem 0;
    line-height: 1;
}
.masthead .sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--ink3);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin: 0;
}
.masthead .rule {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1rem 0 0;
    justify-content: center;
}
.masthead .rule-line {
    flex: 1;
    max-width: 200px;
    height: 1px;
    background: var(--border);
}
.masthead .rule-diamond {
    color: var(--accent);
    font-size: 0.9rem;
}

/* ── Upload zone ── */
.upload-zone {
    border: 2px dashed var(--border);
    border-radius: 4px;
    padding: 3rem 2rem;
    text-align: center;
    background: var(--card);
    margin: 2rem auto;
    max-width: 600px;
}
.upload-zone h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: var(--ink);
    margin: 0 0 0.5rem 0;
}
.upload-zone p {
    font-size: 0.75rem;
    color: var(--ink3);
    margin: 0;
}

/* ── Stat strip ── */
.stat-strip {
    display: flex;
    border: 1px solid var(--border);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 2rem;
    background: var(--card);
}
.stat-cell {
    flex: 1;
    padding: 1.2rem 1rem;
    text-align: center;
    border-right: 1px solid var(--border);
    position: relative;
}
.stat-cell:last-child { border-right: none; }
.stat-cell .num {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: var(--ink);
    line-height: 1;
    display: block;
}
.stat-cell .num.accent { color: var(--accent); }
.stat-cell .num.green  { color: var(--accent2); }
.stat-cell .num.blue   { color: var(--accent3); }
.stat-cell .lbl {
    font-size: 0.65rem;
    color: var(--ink3);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    display: block;
    margin-top: 0.3rem;
}

/* ── Section headers ── */
.section-head {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    margin: 2rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--ink);
}
.section-head h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--ink);
    margin: 0;
}
.section-head .count {
    font-size: 0.7rem;
    color: var(--ink3);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── Pagination ── */
.pagination-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 1.2rem 0;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    margin: 1.5rem 0;
    background: var(--card);
}
.page-info {
    font-size: 0.72rem;
    color: var(--ink3);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    text-align: center;
    min-width: 160px;
}
.page-info strong {
    color: var(--ink);
    font-size: 0.85rem;
}

/* ── Brand cards ── */
.brand-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    transition: box-shadow 0.2s;
}
.brand-card:hover {
    box-shadow: 4px 4px 0 var(--border);
}
.brand-card .card-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 0.8rem;
    gap: 1rem;
}
.brand-card h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--ink);
    margin: 0;
    line-height: 1.2;
}
.brand-card .domain-pill {
    font-size: 0.68rem;
    color: var(--accent3);
    font-family: 'IBM Plex Mono', monospace;
    background: #e8f0f8;
    padding: 0.2rem 0.6rem;
    border-radius: 2px;
    text-decoration: none;
    white-space: nowrap;
    border: 1px solid #c0d0e0;
}
.brand-card .contact-row {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-bottom: 0.8rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px dashed var(--border);
}
.brand-card .contact-item {
    font-size: 0.73rem;
    color: var(--ink2);
    display: flex;
    align-items: center;
    gap: 0.3rem;
}
.brand-card .contact-item .icon { color: var(--accent); }
.brand-card .contact-item a { color: var(--accent3); text-decoration: none; }
.brand-card .contact-item a:hover { text-decoration: underline; }
.brand-card .intel-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    margin-top: 0.8rem;
}
.brand-card .intel-item {}
.brand-card .intel-label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--accent);
    font-weight: 500;
    margin-bottom: 0.2rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.brand-card .intel-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}
.brand-card .intel-text {
    font-size: 0.78rem;
    color: var(--ink2);
    line-height: 1.65;
}
.brand-card .summary-block {
    margin-bottom: 0.8rem;
    padding: 0.8rem;
    background: var(--bg2);
    border-left: 3px solid var(--accent);
}
.brand-card .summary-label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--accent);
    margin-bottom: 0.3rem;
}
.brand-card .summary-text {
    font-size: 0.82rem;
    color: var(--ink);
    line-height: 1.7;
    font-family: 'IBM Plex Mono', monospace;
}
.brand-card .hook-block {
    margin-top: 0.8rem;
    padding: 0.8rem 1rem;
    background: #f0f7f0;
    border: 1px solid #b8d8c0;
    border-radius: 2px;
}
.brand-card .hook-label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--accent2);
    margin-bottom: 0.3rem;
}
.brand-card .hook-text {
    font-size: 0.82rem;
    color: #1a3a2a;
    line-height: 1.65;
    font-style: italic;
    font-family: 'Playfair Display', serif;
}
.brand-card .partner-block {
    margin-top: 0.6rem;
    padding: 0.6rem 1rem;
    background: #f0f4fa;
    border: 1px solid #b8c8e0;
    border-radius: 2px;
}
.brand-card .partner-label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--accent3);
    margin-bottom: 0.2rem;
}
.brand-card .partner-text {
    font-size: 0.78rem;
    color: #1a2a3a;
    line-height: 1.6;
}

/* ── Coverage bars ── */
.coverage-row {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    margin-bottom: 1.5rem;
}
.cov-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.cov-label {
    font-size: 0.68rem;
    color: var(--ink2);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    width: 110px;
    flex-shrink: 0;
}
.cov-bar-bg {
    flex: 1;
    height: 10px;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 1px;
    overflow: hidden;
}
.cov-bar-fill {
    height: 100%;
    background: var(--accent);
    border-radius: 1px;
    transition: width 0.5s ease;
}
.cov-bar-fill.green { background: var(--accent2); }
.cov-bar-fill.blue  { background: var(--accent3); }
.cov-pct {
    font-size: 0.68rem;
    color: var(--ink3);
    width: 38px;
    text-align: right;
    flex-shrink: 0;
}

/* ── Word cloud table ── */
.word-table {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.5rem;
}
.word-chip {
    font-size: 0.68rem;
    padding: 0.2rem 0.6rem;
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
    border: 1px solid var(--border);
    background: var(--bg2);
    color: var(--ink2);
}
.word-chip.lg { font-size: 0.85rem; background: var(--card); color: var(--ink); border-color: var(--ink3); }
.word-chip.xl { font-size: 1rem; background: #fff0ec; color: var(--accent); border-color: var(--accent); font-weight: 500; }

/* ── Streamlit overrides ── */
.stTextInput input, .stSelectbox > div > div, .stMultiSelect > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    color: var(--ink) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
}
label, .stTextInput label, .stSelectbox label, .stMultiSelect label {
    color: var(--ink3) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
.stButton > button {
    background: var(--ink) !important;
    color: var(--bg) !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.5rem !important;
}
.stButton > button:hover { background: var(--accent) !important; }
.stFileUploader { background: var(--card) !important; border: 2px dashed var(--border) !important; border-radius: 4px !important; }
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid var(--ink) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    color: var(--ink3) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    background: transparent !important;
    border: none !important;
    padding: 0.6rem 1.4rem !important;
}
.stTabs [aria-selected="true"] {
    color: var(--ink) !important;
    border-bottom: 2px solid var(--accent) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { background: transparent !important; padding: 1.5rem 0 0 !important; }
.stExpander { border: 1px solid var(--border) !important; border-radius: 2px !important; background: var(--card) !important; }
.stExpander summary { font-family: 'IBM Plex Mono', monospace !important; font-size: 0.75rem !important; color: var(--ink) !important; }
.stDownloadButton > button {
    background: transparent !important;
    color: var(--accent3) !important;
    border: 1px solid var(--accent3) !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--border); }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ────────────────────────────────────────────────────────────────────

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "their", "they", "this", "that", "these", "those", "it", "its",
    "as", "we", "our", "us", "has", "have", "not", "can", "also",
    "which", "who", "more", "into", "through", "while", "brand", "brands",
    "products", "product", "customers", "customer", "market", "make",
    "making", "made", "help", "helps", "offer", "offers", "use", "uses",
}

def _val(v) -> str:
    s = str(v).strip()
    return "" if s.lower() in ("nan", "none", "") else s

def _safe(v) -> str:
    s = _val(v)
    s = _html_mod.escape(s)
    s = s.replace("\n", "<br>")
    return s

def _pct(n, total) -> float:
    return round(n / total * 100, 1) if total else 0

def _word_freq(series: pd.Series, top_n: int = 40) -> list[tuple[str, int]]:
    words = []
    for text in series.dropna():
        for w in re.findall(r"[a-zA-Z]{4,}", str(text).lower()):
            if w not in STOPWORDS:
                words.append(w)
    return Counter(words).most_common(top_n)

def _coverage(df: pd.DataFrame, col: str) -> float:
    return _pct(
        (df[col].astype(str).str.strip()
         .replace({"nan": "", "None": "", "none": ""}) != "").sum(),
        len(df)
    )


# ─── Pagination helper ───────────────────────────────────────────────────────────

PAGE_SIZE = 20   # cards per page — change this to whatever feels right

def paginate(data: pd.DataFrame, key: str) -> pd.DataFrame:
    """
    Slices `data` to the current page and renders prev/next controls.
    `key` must be unique per tab so pages don't interfere with each other.
    Returns the sliced dataframe for the current page.
    """
    total_items = len(data)
    total_pages = max(1, -(-total_items // PAGE_SIZE))   # ceiling division

    # Init page in session state
    state_key = f"page_{key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = 1

    # Reset to page 1 when filters change (detected by total changing)
    size_key = f"size_{key}"
    if st.session_state.get(size_key) != total_items:
        st.session_state[state_key] = 1
        st.session_state[size_key]  = total_items

    current_page = st.session_state[state_key]

    # ── Top pagination bar ────────────────────────────────────────────────
    _render_pagination(key, current_page, total_pages, total_items, position="top")

    # ── Slice data ────────────────────────────────────────────────────────
    start = (current_page - 1) * PAGE_SIZE
    end   = start + PAGE_SIZE
    return data.iloc[start:end]


def _render_pagination(key, current_page, total_pages, total_items, position="top"):
    """Renders the prev / page-info / next control row."""
    state_key = f"page_{key}"

    col_prev, col_info, col_next = st.columns([1, 2, 1])

    with col_prev:
        if st.button(
            "← Prev",
            key=f"prev_{key}_{position}",
            disabled=(current_page <= 1),
            use_container_width=True,
        ):
            st.session_state[state_key] -= 1
            st.rerun()

    with col_info:
        start_item = (current_page - 1) * PAGE_SIZE + 1
        end_item   = min(current_page * PAGE_SIZE, total_items)
        st.markdown(
            f'<div class="page-info">'
            f'Page <strong>{current_page}</strong> of <strong>{total_pages}</strong>'
            f'<br>{start_item}–{end_item} of {total_items} brands'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col_next:
        if st.button(
            "Next →",
            key=f"next_{key}_{position}",
            disabled=(current_page >= total_pages),
            use_container_width=True,
        ):
            st.session_state[state_key] += 1
            st.rerun()


def render_bottom_pagination(key):
    """Call this after rendering cards to show bottom nav too."""
    state_key = f"page_{key}"
    size_key  = f"size_{key}"
    total_items  = st.session_state.get(size_key, 0)
    total_pages  = max(1, -(-total_items // PAGE_SIZE))
    current_page = st.session_state.get(state_key, 1)
    _render_pagination(key, current_page, total_pages, total_items, position="bottom")


# ─── Masthead ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <p class="sub">Brand Intelligence</p>
    <h1>Analysis Dashboard</h1>
    <div class="rule">
        <div class="rule-line"></div>
        <span class="rule-diamond">◈</span>
        <div class="rule-line"></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── File upload ────────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Upload brand intelligence CSV",
    type=["csv"],
    label_visibility="collapsed",
)

if uploaded is None:
    st.markdown("""
    <div class="upload-zone">
        <h3>Upload Your CSV</h3>
        <p>Brand, Domain, Founder, LinkedIn, Contact Email, Contact Phone,<br>
        Website, Brand Summary, Unique Angles, Pain Points, Outreach Hook, Partnership Angle</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Load data ──────────────────────────────────────────────────────────────────
try:
    df = pd.read_csv(uploaded).fillna("")
except Exception as e:
    st.error(f"Could not read CSV: {e}")
    st.stop()

df.columns = [c.strip() for c in df.columns]

if "Linkdin" in df.columns and "LinkedIn" not in df.columns:
    df = df.rename(columns={"Linkdin": "LinkedIn"})
elif "LinkedIn" not in df.columns:
    df["LinkedIn"] = ""

for col in ["Brand", "Domain", "Founder", "LinkedIn", "Contact Email",
            "Contact Phone", "Website", "Brand Summary", "Unique Angles",
            "Pain Points", "Outreach Hook", "Partnership Angle"]:
    if col not in df.columns:
        df[col] = ""

total = len(df)
if total == 0:
    st.warning("CSV is empty.")
    st.stop()

# ─── Coverage stats ──────────────────────────────────────────────────────────────
has_email   = (df["Contact Email"].astype(str).str.strip().replace({"nan":"","None":""}) != "").sum()
has_phone   = (df["Contact Phone"].astype(str).str.strip().replace({"nan":"","None":""}) != "").sum()
has_summary = (df["Brand Summary"].astype(str).str.strip().replace({"nan":"","None":""}) != "").sum()
has_founder = (df["Founder"].astype(str).str.strip().replace({"nan":"","None":""}) != "").sum()
has_domain  = (df["Domain"].astype(str).str.strip().replace({"nan":"","None":""}) != "").sum()

# ─── Stat strip ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-strip">
    <div class="stat-cell">
        <span class="num">{total}</span>
        <span class="lbl">Total Brands</span>
    </div>
    <div class="stat-cell">
        <span class="num green">{has_email}</span>
        <span class="lbl">With Email</span>
    </div>
    <div class="stat-cell">
        <span class="num blue">{has_phone}</span>
        <span class="lbl">With Phone</span>
    </div>
    <div class="stat-cell">
        <span class="num accent">{has_summary}</span>
        <span class="lbl">Analysed</span>
    </div>
    <div class="stat-cell">
        <span class="num">{has_founder}</span>
        <span class="lbl">Founder Known</span>
    </div>
    <div class="stat-cell">
        <span class="num">{has_domain}</span>
        <span class="lbl">Domains Found</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ───────────────────────────────────────────────────────────────────────
tab_brands, tab_intel, tab_outreach, tab_data = st.tabs([
    "◈  Brand Profiles",
    "◈  Intelligence Analysis",
    "◈  Outreach Arsenal",
    "◈  Raw Data",
])


# ════════════════════════════════════════════════════════════════════════════════
#  TAB 1  —  BRAND PROFILES
# ════════════════════════════════════════════════════════════════════════════════
with tab_brands:

    fc1, fc2, fc3 = st.columns([2, 1.5, 1.5])
    with fc1:
        search = st.text_input("Search", placeholder="Search by brand name…", label_visibility="collapsed")
    with fc2:
        filter_email = st.selectbox("Email", ["All", "Has Email", "No Email"], label_visibility="collapsed")
    with fc3:
        filter_phone = st.selectbox("Phone", ["All", "Has Phone", "No Phone"], label_visibility="collapsed")

    filtered = df.copy()
    if search.strip():
        filtered = filtered[filtered["Brand"].astype(str).str.contains(search.strip(), case=False, na=False)]
    if filter_email == "Has Email":
        filtered = filtered[filtered["Contact Email"].astype(str).str.strip().replace({"nan": "", "None": ""}) != ""]
    elif filter_email == "No Email":
        filtered = filtered[filtered["Contact Email"].astype(str).str.strip().replace({"nan": "", "None": ""}) == ""]
    if filter_phone == "Has Phone":
        filtered = filtered[filtered["Contact Phone"].astype(str).str.strip().replace({"nan": "", "None": ""}) != ""]
    elif filter_phone == "No Phone":
        filtered = filtered[filtered["Contact Phone"].astype(str).str.strip().replace({"nan": "", "None": ""}) == ""]

    st.markdown(
        f'<div class="section-head"><h2>Brand Profiles</h2>'
        f'<span class="count">{len(filtered)} of {total} brands</span></div>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("No brands match the current filters.")
    else:
        # ── Paginate ──────────────────────────────────────────────────────
        page_df = paginate(filtered.reset_index(drop=True), key="brands")

        for _, row in page_df.iterrows():
            brand    = _val(row.get("Brand", ""))
            domain   = _val(row.get("Domain", ""))
            founder  = _val(row.get("Founder", ""))
            linkedin = _val(row.get("LinkedIn", ""))
            email    = _val(row.get("Contact Email", ""))
            phone    = _val(row.get("Contact Phone", ""))
            summary  = _val(row.get("Brand Summary", ""))
            angles   = _val(row.get("Unique Angles", ""))
            pain     = _val(row.get("Pain Points", ""))
            hook     = _val(row.get("Outreach Hook", ""))
            partner  = _val(row.get("Partnership Angle", ""))

            if not brand:
                continue

            d_url = (domain if domain.startswith("http") else f"https://{domain}") if domain else "#"
            domain_pill = f'<a href="{d_url}" target="_blank" class="domain-pill">{domain or "no domain"}</a>' if domain else '<span class="domain-pill" style="color:#aaa;">no domain</span>'

            contact_items = []
            if founder:
                contact_items.append(f'<span class="contact-item"><span class="icon">◈</span> {_safe(founder)}</span>')
            if email:
                contact_items.append(f'<span class="contact-item"><span class="icon">✉</span> <a href="mailto:{email}">{email}</a></span>')
            if phone:
                contact_items.append(f'<span class="contact-item"><span class="icon">◎</span> {phone}</span>')
            if linkedin:
                contact_items.append(f'<span class="contact-item"><span class="icon">⊕</span> <a href="{linkedin}" target="_blank">LinkedIn</a></span>')
            else:
                contact_items.append(f'<span class="contact-item" style="color:#aaa;"><span class="icon">⊕</span> LinkedIn (n/a)</span>')

            contact_html = "".join(contact_items)

            summary_html = ""
            if summary and not summary.startswith("SCRAPE_FAILED"):
                summary_html = f"""
                <div class="summary-block">
                    <div class="summary-label">Brand Summary</div>
                    <div class="summary-text">{_safe(summary)}</div>
                </div>"""

            intel_items = []
            if angles:
                intel_items.append(("Unique Angles", angles))
            if pain:
                intel_items.append(("Pain Points", pain))

            intel_html = ""
            if intel_items:
                cells = "".join([
                    f'<div class="intel-item">'
                    f'<div class="intel-label">{label}</div>'
                    f'<div class="intel-text">{_safe(text)}</div>'
                    f'</div>'
                    for label, text in intel_items
                ])
                intel_html = f'<div class="intel-grid">{cells}</div>'

            hook_html = ""
            if hook:
                hook_html = f"""
                <div class="hook-block">
                    <div class="hook-label">✦ Outreach Hook</div>
                    <div class="hook-text">"{_safe(hook)}"</div>
                </div>"""

            partner_html = ""
            if partner:
                partner_html = f"""
                <div class="partner-block">
                    <div class="partner-label">◉ Partnership Angle</div>
                    <div class="partner-text">{_safe(partner)}</div>
                </div>"""

            card_parts = [
                '<div class="brand-card">',
                '<div class="card-top">',
                f'<h3>{_safe(brand)}</h3>',
                f'{domain_pill}',
                '</div>',
                f'<div class="contact-row">{contact_html}</div>',
                summary_html,
                intel_html,
                hook_html,
                partner_html,
                '</div>',
            ]
            st.markdown("".join(card_parts), unsafe_allow_html=True)

        # ── Bottom pagination ──────────────────────────────────────────────
        render_bottom_pagination("brands")


# ════════════════════════════════════════════════════════════════════════════════
#  TAB 2  —  INTELLIGENCE ANALYSIS
# ════════════════════════════════════════════════════════════════════════════════
with tab_intel:

    st.markdown('<div class="section-head"><h2>Data Coverage</h2></div>', unsafe_allow_html=True)

    coverage_fields = [
        ("Domain",          _coverage(df, "Domain"),             "accent"),
        ("Contact Email",   _coverage(df, "Contact Email"),      "green"),
        ("Contact Phone",   _coverage(df, "Contact Phone"),      "blue"),
        ("Founder",         _coverage(df, "Founder"),            "accent"),
        ("Brand Summary",   _coverage(df, "Brand Summary"),      "green"),
        ("Unique Angles",   _coverage(df, "Unique Angles"),      "blue"),
        ("Pain Points",     _coverage(df, "Pain Points"),        "accent"),
        ("Outreach Hook",   _coverage(df, "Outreach Hook"),      "green"),
        ("Partnership",     _coverage(df, "Partnership Angle"),  "blue"),
        ("LinkedIn",        _coverage(df, "LinkedIn"),           "accent"),
    ]

    bars_html = ""
    for label, pct, color in coverage_fields:
        bars_html += f"""
        <div class="cov-item">
            <span class="cov-label">{label}</span>
            <div class="cov-bar-bg">
                <div class="cov-bar-fill {color}" style="width:{pct}%"></div>
            </div>
            <span class="cov-pct">{pct}%</span>
        </div>"""
    st.markdown(f'<div class="coverage-row">{bars_html}</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-head"><h2>Pain Point Keywords</h2></div>', unsafe_allow_html=True)
        pain_words = _word_freq(df["Pain Points"], 30)
        if pain_words:
            max_count = pain_words[0][1]
            chips = ""
            for word, count in pain_words:
                ratio = count / max_count
                cls = "xl" if ratio > 0.6 else ("lg" if ratio > 0.3 else "")
                chips += f'<span class="word-chip {cls}">{word} <sup style="opacity:0.5;">{count}</sup></span>'
            st.markdown(f'<div class="word-table">{chips}</div>', unsafe_allow_html=True)
        else:
            st.caption("No pain point data available.")

    with col_b:
        st.markdown('<div class="section-head"><h2>Unique Angle Keywords</h2></div>', unsafe_allow_html=True)
        angle_words = _word_freq(df["Unique Angles"], 30)
        if angle_words:
            max_count = angle_words[0][1]
            chips = ""
            for word, count in angle_words:
                ratio = count / max_count
                cls = "xl" if ratio > 0.6 else ("lg" if ratio > 0.3 else "")
                chips += f'<span class="word-chip {cls}">{word} <sup style="opacity:0.5;">{count}</sup></span>'
            st.markdown(f'<div class="word-table">{chips}</div>', unsafe_allow_html=True)
        else:
            st.caption("No unique angle data available.")

    st.markdown('<div class="section-head"><h2>Incomplete Records</h2><span class="count">Brands missing key fields</span></div>', unsafe_allow_html=True)

    def _missing(row):
        missing = []
        for col in ["Domain", "Contact Email", "Contact Phone", "Brand Summary", "Founder"]:
            if not _val(row.get(col, "")):
                missing.append(col)
        return ", ".join(missing)

    incomplete = df.copy()
    incomplete["Missing Fields"] = incomplete.apply(_missing, axis=1)
    incomplete = incomplete[incomplete["Missing Fields"] != ""][["Brand", "Domain", "Missing Fields"]]

    if incomplete.empty:
        st.success("All records are complete.")
    else:
        st.dataframe(
            incomplete,
            use_container_width=True,
            hide_index=True,
            height=min(400, 40 + len(incomplete) * 35),
        )


# ════════════════════════════════════════════════════════════════════════════════
#  TAB 3  —  OUTREACH ARSENAL
# ════════════════════════════════════════════════════════════════════════════════
with tab_outreach:

    st.markdown(
        '<div class="section-head"><h2>Outreach Arsenal</h2>'
        '<span class="count">Ready-to-use hooks and partnership angles</span></div>',
        unsafe_allow_html=True,
    )

    outreach_df = df[
        (df["Outreach Hook"].astype(str).str.strip().replace({"nan": "", "None": ""}) != "") |
        (df["Partnership Angle"].astype(str).str.strip().replace({"nan": "", "None": ""}) != "")
    ].copy().reset_index(drop=True)

    if outreach_df.empty:
        st.info("No outreach data available yet. Run the Brand Analyser to generate hooks.")
    else:
        st.markdown(
            f'<p style="font-size:0.72rem;color:var(--ink3);margin-bottom:1.5rem;">'
            f'{len(outreach_df)} brands with outreach content</p>',
            unsafe_allow_html=True,
        )

        # ── Paginate outreach cards ───────────────────────────────────────
        page_outreach = paginate(outreach_df, key="outreach")

        for _, row in page_outreach.iterrows():
            brand   = _val(row.get("Brand", ""))
            email   = _val(row.get("Contact Email", ""))
            hook    = _val(row.get("Outreach Hook", ""))
            partner = _val(row.get("Partnership Angle", ""))
            pain    = _val(row.get("Pain Points", ""))

            if not brand:
                continue

            email_badge = (
                f'<span style="font-size:0.68rem;color:var(--accent2);background:#f0f7f0;'
                f'padding:0.15rem 0.5rem;border:1px solid #b8d8c0;border-radius:2px;">{email}</span>'
                if email else
                '<span style="font-size:0.68rem;color:var(--ink3);">no email</span>'
            )

            hook_section = ""
            if hook:
                hook_section = f"""
                <div style="margin:0.8rem 0 0.5rem;">
                    <div style="font-size:0.6rem;text-transform:uppercase;letter-spacing:0.15em;color:var(--accent2);margin-bottom:0.3rem;">✦ Opening Hook</div>
                    <div style="font-size:0.88rem;font-family:'Playfair Display',serif;font-style:italic;color:#1a3a2a;line-height:1.7;padding:0.6rem 0.8rem;background:#f0f7f0;border-left:3px solid var(--accent2);">"{_safe(hook)}"</div>
                </div>"""

            partner_section = ""
            if partner:
                partner_section = f"""
                <div style="margin:0.5rem 0 0;">
                    <div style="font-size:0.6rem;text-transform:uppercase;letter-spacing:0.15em;color:var(--accent3);margin-bottom:0.3rem;">◉ Why Partner With Us</div>
                    <div style="font-size:0.78rem;color:#1a2a3a;line-height:1.65;padding:0.5rem 0.8rem;background:#f0f4fa;border-left:3px solid var(--accent3);">{_safe(partner)}</div>
                </div>"""

            pain_section = ""
            if pain:
                pain_section = f"""
                <div style="margin:0.5rem 0 0;">
                    <div style="font-size:0.6rem;text-transform:uppercase;letter-spacing:0.15em;color:var(--accent);margin-bottom:0.3rem;">⚠ Known Pain Points</div>
                    <div style="font-size:0.75rem;color:var(--ink2);line-height:1.6;">{_safe(pain)}</div>
                </div>"""

            outreach_parts = [
                '<div class="brand-card">',
                '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.6rem;">',
                f'<h3 style="font-family:sans-serif;font-size:1.1rem;font-weight:700;color:var(--ink);margin:0;">{_safe(brand)}</h3>',
                email_badge,
                '</div>',
                hook_section,
                partner_section,
                pain_section,
                '</div>',
            ]
            st.markdown("".join(outreach_parts), unsafe_allow_html=True)

        render_bottom_pagination("outreach")

        # ── Copy-ready snippets (paginated separately) ────────────────────
        st.markdown(
            '<div class="section-head"><h2>Copy-Ready Snippets</h2>'
            '<span class="count">Click to expand</span></div>',
            unsafe_allow_html=True,
        )

        snippet_df = df[
            df["Outreach Hook"].astype(str).str.strip().replace({"nan": "", "None": ""}) != ""
        ].copy().reset_index(drop=True)

        page_snippets = paginate(snippet_df, key="snippets")

        for _, row in page_snippets.iterrows():
            brand   = _val(row.get("Brand", ""))
            email   = _val(row.get("Contact Email", ""))
            hook    = _val(row.get("Outreach Hook", ""))
            partner = _val(row.get("Partnership Angle", ""))

            if not brand or not hook:
                continue

            with st.expander(f"  {brand}  {'· ' + email if email else ''}"):
                snippet = f"""Hi,

{hook}

{partner if partner else ''}

Would love to explore how we can work together.

Best regards"""
                st.text_area(
                    "Email draft",
                    value=snippet.strip(),
                    height=180,
                    key=f"snippet_{brand}_{_}",
                    label_visibility="collapsed",
                )

        render_bottom_pagination("snippets")


# ════════════════════════════════════════════════════════════════════════════════
#  TAB 4  —  RAW DATA
# ════════════════════════════════════════════════════════════════════════════════
with tab_data:

    st.markdown('<div class="section-head"><h2>Raw Data</h2></div>', unsafe_allow_html=True)

    raw_search = st.text_input("Search raw data", placeholder="Filter…", label_visibility="collapsed")
    raw_filtered = df.copy()
    if raw_search.strip():
        raw_filtered = raw_filtered[
            raw_filtered.apply(
                lambda row: any(raw_search.strip().lower() in str(v).lower() for v in row),
                axis=1,
            )
        ]

    display_raw = raw_filtered.copy()
    for col in ["Brand Summary", "Unique Angles", "Pain Points", "Outreach Hook", "Partnership Angle"]:
        if col in display_raw.columns:
            display_raw[col] = display_raw[col].astype(str).apply(
                lambda x: x[:80] + "…" if len(x) > 80 else x
            )

    st.dataframe(
        display_raw,
        use_container_width=True,
        height=500,
        hide_index=True,
        column_config={
            "Domain":   st.column_config.LinkColumn("Domain",   display_text="🌐 Open"),
            "Website":  st.column_config.LinkColumn("Website",  display_text="🌐 Open"),
            "LinkedIn": st.column_config.LinkColumn("LinkedIn", display_text="🔗 Open"),
        },
    )

    dl_buf = io.BytesIO()
    raw_filtered.to_csv(dl_buf, index=False)
    dl_buf.seek(0)
    st.download_button(
        label="⬇  Download filtered CSV",
        data=dl_buf,
        file_name="brand_intelligence_export.csv",
        mime="text/csv",
    )
    