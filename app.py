import streamlit as st
import pandas as pd

st.set_page_config(page_title="Study Hub", layout="wide")

# ===================== PREMIUM UI THEME ===================== #
st.markdown("""
<style>

/* ================= DESIGN SYSTEM ================= */
:root {
    --bg: #f5f7ff;
    --card: rgba(255,255,255,0.92);
    --text: #0f172a;
    --muted: #64748b;
    --primary: #4f46e5;
    --primary2: #2563eb;
    --border: rgba(15,23,42,0.08);
}

/* ================= GLOBAL ================= */
.stApp {
    background: radial-gradient(circle at top, #eef2ff, #f5f7ff 45%);
    color: var(--text);
    font-family: "Inter", sans-serif;
}

/* Hide Streamlit default UI */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
div[data-testid="stStatusWidget"] {display: none;}

/* ================= LAYOUT ================= */
.block-container {
    padding: 1.2rem 2.2rem;
}

/* ================= TITLE ================= */
h1 {
    font-size: 42px !important;
    font-weight: 900 !important;
    letter-spacing: -1px;
    margin-bottom: 0;
    background: linear-gradient(90deg, #4f46e5, #2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2, h3 {
    font-weight: 800 !important;
}

/* ================= CARDS ================= */
.study-card, .telegram-card {
    background: var(--card);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 18px;
    height: 170px;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    box-shadow: 0 8px 30px rgba(15,23,42,0.06);
    transition: all 0.25s ease;
}

.study-card:hover, .telegram-card:hover {
    transform: translateY(-8px) scale(1.01);
    border-color: rgba(79,70,229,0.35);
    box-shadow: 0 18px 45px rgba(79,70,229,0.18);
}

/* ================= TITLES ================= */
.study-title, .telegram-title {
    font-size: 18px;
    font-weight: 800;
    color: var(--text);
    line-height: 1.3;
}

/* ================= PILLS ================= */
.subject-pill {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    background: linear-gradient(90deg, #eef2ff, #e0e7ff);
    color: #4338ca;
    border: 1px solid #c7d2fe;
}

.category-pill {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    background: linear-gradient(90deg, #f5f3ff, #ede9fe);
    color: #6d28d9;
    border: 1px solid #ddd6fe;
}

/* ================= BUTTONS ================= */
div.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    border: 1px solid rgba(15,23,42,0.1);
    background: white;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #eef2ff, #e0e7ff);
    border-color: #4f46e5;
    color: #4f46e5;
    transform: scale(1.02);
}

/* ================= INPUTS ================= */
input {
    border-radius: 12px !important;
    border: 1px solid rgba(15,23,42,0.1) !important;
}

/* ================= TABS ================= */
div[data-testid="stTabs"] button {
    font-weight: 700;
    padding: 10px 18px;
    border-radius: 10px;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    background: white;
    color: #4f46e5;
    box-shadow: 0 10px 25px rgba(79,70,229,0.15);
}

/* ================= DIVIDER ================= */
hr {
    border: none;
    border-top: 1px solid rgba(15,23,42,0.08);
    margin: 1.2rem 0;
}

</style>
""", unsafe_allow_html=True)

# ===================== HEADER ===================== #
st.title("📚 Study Hub")
st.caption("Your centralized learning dashboard — Resources • Telegram Channels • Bots")

# ===================== LOAD DATA ===================== #
SHEET_URL = "https://docs.google.com/spreadsheets/d/1al3Zy9Kd7YVIorEStPwI2x4C0GFDYBPGqIlVce1GWr8/export?format=csv"

@st.cache_data(ttl=300)
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()
df.columns = df.columns.str.strip()

# ===================== TABS ===================== #
tab1, tab2, tab3 = st.tabs([
    "📂 Resources",
    "📢 Telegram Channels",
    "🤖 Telegram Bots"
])

# =========================================================
# 📂 RESOURCES
# =========================================================
with tab1:

    res_df = df[[
        "Resource_Subject",
        "Resource_Topic",
        "Resource_Tags",
        "Resource_Link"
    ]].copy()

    res_df = res_df.dropna(subset=["Resource_Link"])

    col1, col2 = st.columns([1, 2])

    with col1:
        search = st.text_input("🔎 Search resources", key="res_search")

    with col2:
        subjects = ["All"] + sorted(res_df["Resource_Subject"].dropna().unique().tolist())
        selected_subject = st.selectbox("📘 Subject", subjects, key="res_subject")

    filtered = res_df.copy()

    if selected_subject != "All":
        filtered = filtered[filtered["Resource_Subject"] == selected_subject]

    if search:
        filtered = filtered[
            filtered["Resource_Topic"].str.contains(search, case=False, na=False) |
            filtered["Resource_Tags"].str.contains(search, case=False, na=False)
        ]

    st.markdown("---")

    if filtered.empty:
        st.info("No resources found.")
    else:
        cols = st.columns(3)

        for i, (_, row) in enumerate(filtered.iterrows()):
            with cols[i % 3]:

                st.markdown(f"""
                <div class="study-card">
                    <div>
                        <div class="study-title">📘 {row['Resource_Topic']}</div>
                        <div class="subject-pill">{row['Resource_Subject']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.link_button("📂 Open Resource", row["Resource_Link"], use_container_width=True)

# =========================================================
# 📢 CHANNELS
# =========================================================
with tab2:

    tg_df = df[[
        "Channel_Name_1",
        "Channel_Link_1",
        "Channel_Category_1"
    ]].copy()

    tg_df = tg_df.dropna(subset=["Channel_Link_1"])

    col1, col2 = st.columns([1, 2])

    with col1:
        search_tg = st.text_input("🔎 Search channels", key="tg_search")

    with col2:
        categories = ["All"] + sorted(tg_df["Channel_Category_1"].dropna().unique().tolist())
        selected_category = st.selectbox("📂 Category", categories, key="tg_category")

    filtered_tg = tg_df.copy()

    if selected_category != "All":
        filtered_tg = filtered_tg[filtered_tg["Channel_Category_1"] == selected_category]

    if search_tg:
        filtered_tg = filtered_tg[
            filtered_tg["Channel_Name_1"].str.contains(search_tg, case=False, na=False)
        ]

    st.markdown("---")

    if filtered_tg.empty:
        st.info("No channels found.")
    else:
        cols = st.columns(3)

        for i, (_, row) in enumerate(filtered_tg.iterrows()):
            with cols[i % 3]:

                st.markdown(f"""
                <div class="telegram-card">
                    <div>
                        <div class="telegram-title">📢 {row['Channel_Name_1']}</div>
                        <div class="category-pill">{row['Channel_Category_1']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.link_button("📡 Join Channel", row["Channel_Link_1"], use_container_width=True)

# =========================================================
# 🤖 BOTS
# =========================================================
with tab3:

    bot_df = df[[
        "Channel_Name_2",
        "Channel_Link_2",
        "Channel_Category_2"
    ]].copy()

    bot_df = bot_df.dropna(subset=["Channel_Link_2"])

    col1, col2 = st.columns([1, 2])

    with col1:
        search_bot = st.text_input("🔎 Search bots", key="bot_search")

    with col2:
        bot_categories = ["All"] + sorted(bot_df["Channel_Category_2"].dropna().unique().tolist())
        selected_bot_category = st.selectbox("📂 Bot Category", bot_categories, key="bot_category")

    filtered_bot = bot_df.copy()

    if selected_bot_category != "All":
        filtered_bot = filtered_bot[filtered_bot["Channel_Category_2"] == selected_bot_category]

    if search_bot:
        filtered_bot = filtered_bot[
            filtered_bot["Channel_Name_2"].str.contains(search_bot, case=False, na=False)
        ]

    st.markdown("---")

    if filtered_bot.empty:
        st.info("No bots found.")
    else:
        cols = st.columns(3)

        for i, (_, row) in enumerate(filtered_bot.iterrows()):
            with cols[i % 3]:

                st.markdown(f"""
                <div class="telegram-card">
                    <div>
                        <div class="telegram-title">🤖 {row['Channel_Name_2']}</div>
                        <div class="category-pill">{row['Channel_Category_2']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.link_button("🚀 Open Bot", row["Channel_Link_2"], use_container_width=True)

# ===================== FOOTER ===================== #
st.markdown("---")
st.caption("⚡ Study Hub • Premium UI • Built with Streamlit")
