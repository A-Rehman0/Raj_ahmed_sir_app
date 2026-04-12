import streamlit as st
import pandas as pd

st.set_page_config(page_title="Study Hub", layout="wide")

# ---------------- GLOBAL CSS ---------------- #
st.markdown("""
<style>
.stApp { background-color: #f8fafc; }

h1, h2, h3 { color: #0f172a !important; }

/* Study Card */
.study-card, .telegram-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px;
    height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: 0.2s ease;
}

.study-card:hover, .telegram-card:hover {
    transform: translateY(-3px);
    border-color: #cbd5e1;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}

.study-title, .telegram-title {
    font-size: 18px;
    font-weight: 700;
    color: #0f172a;
}

.subject-pill {
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 12px;
    background: #ecfeff;
    color: #0e7490;
}

.category-pill {
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 12px;
    background: #eff6ff;
    color: #2563eb;
}

div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    border: 1px solid #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.title("📚 Study Hub")
st.caption("Resources + Telegram Channels in one place")

# ---------------- LOAD DATA ---------------- #
SHEET_URL = "https://docs.google.com/spreadsheets/d/1al3Zy9Kd7YVIorEStPwI2x4C0GFDYBPGqIlVce1GWr8/export?format=csv"

@st.cache_data(ttl=300)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# ---------------- CREATE TABS ---------------- #
tab1, tab2 = st.tabs(["📂 Resources", "📢 Telegram Channels"])

# =========================================================
# 📂 TAB 1 — RESOURCES
# =========================================================
with tab1:

    def is_valid_link(x):
        return isinstance(x, str) and x.startswith("http")

    res_df = df[df["Link"].apply(is_valid_link)]

    col1, col2 = st.columns([1, 2])

    with col1:
        search = st.text_input("🔎 Search resources", key="res_search")

    with col2:
        subjects = ["All"] + sorted(res_df["Subject"].dropna().unique().tolist())
        selected_subject = st.selectbox("📘 Subject", subjects, key="res_subject")

    filtered = res_df.copy()

    if selected_subject != "All":
        filtered = filtered[filtered["Subject"] == selected_subject]

    if search:
        filtered = filtered[
            filtered["Topic"].str.contains(search, case=False, na=False) |
            filtered["Tags"].str.contains(search, case=False, na=False)
        ]

    st.markdown("---")

    if len(filtered) == 0:
        st.info("No resources found.")
    else:
        cols = st.columns(3)

        for i, (_, row) in enumerate(filtered.iterrows()):
            with cols[i % 3]:

                st.markdown(f"""
                <div class="study-card">
                    <div>
                        <div class="study-title">📘 {row['Topic']}</div>
                        <div class="subject-pill">{row['Subject']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.link_button("📂 Open Resource", row["Link"], use_container_width=True)


# =========================================================
# 📢 TAB 2 — TELEGRAM
# =========================================================
with tab2:

    def is_valid_telegram(x):
        return isinstance(x, str) and ("t.me/" in x or "telegram.me/" in x)

    tg_df = df[df["Telegram Link"].apply(is_valid_telegram)]

    col1, col2 = st.columns([1, 2])

    with col1:
        search_tg = st.text_input("🔎 Search channels", key="tg_search")

    with col2:
        categories = ["All"] + sorted(tg_df["Category"].dropna().unique().tolist())
        selected_category = st.selectbox("📂 Category", categories, key="tg_category")

    filtered_tg = tg_df.copy()

    if selected_category != "All":
        filtered_tg = filtered_tg[filtered_tg["Category"] == selected_category]

    if search_tg:
        filtered_tg = filtered_tg[
            filtered_tg["Channel Name"].str.contains(search_tg, case=False, na=False) |
            filtered_tg["Category"].str.contains(search_tg, case=False, na=False)
        ]

    st.markdown("---")

    if len(filtered_tg) == 0:
        st.info("No channels found.")
    else:
        cols = st.columns(3)

        for i, (_, row) in enumerate(filtered_tg.iterrows()):
            with cols[i % 3]:

                st.markdown(f"""
                <div class="telegram-card">
                    <div>
                        <div class="telegram-title">📢 {row['Channel Name']}</div>
                        <div class="category-pill">{row['Category']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.link_button("📡 Join Channel", row["Telegram Link"], use_container_width=True)


# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("⚡ Study Hub • Clean UI • Streamlit Powered")
