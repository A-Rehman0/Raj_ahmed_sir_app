import streamlit as st
import pandas as pd

st.set_page_config(page_title="Study Hub", layout="wide")

# ---------------- HIDE STREAMLIT UI ---------------- #
st.markdown("""
<style>

/* ================= BASE ================= */

.stApp {
    background-color: #ffffff;
    color: #0f172a;
    font-family: "Inter", sans-serif;
}

/* Hide Streamlit UI */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
div[data-testid="stStatusWidget"] {display: none;}
.block-container {padding-top: 0rem; padding-left: 2rem; padding-right: 2rem;}

/* ================= PAGE TITLE ================= */

h1 {
    font-size: 34px !important;
    font-weight: 900 !important;
    letter-spacing: -0.5px;
    color: #0f172a !important;
}

h2, h3 {
    font-weight: 800 !important;
    color: #111827 !important;
}

/* ================= CARDS (PREMIUM CLEAN STYLE) ================= */

.study-card, .telegram-card {
    background: #ffffff;
    border: 1.8px solid #e5e7eb;
    border-radius: 18px;
    padding: 18px;
    height: 160px;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    transition: all 0.25s ease;
}

/* hover premium lift */
.study-card:hover, .telegram-card:hover {
    transform: translateY(-6px);
    border-color: #2563eb;
    box-shadow: 0 10px 25px rgba(37,99,235,0.15);
}

/* ================= TITLES ================= */

.study-title, .telegram-title {
    font-size: 18px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.3;
}

/* ================= TAG PILLS ================= */

.subject-pill {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;

    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
}

.category-pill {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;

    background: #f5f3ff;
    color: #6d28d9;
    border: 1px solid #ddd6fe;
}

/* ================= BUTTONS ================= */

div.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    border: 1.5px solid #e5e7eb;
    background: #ffffff;
    color: #0f172a;
    transition: all 0.2s ease;
    padding: 0.5rem 1rem;
}

/* hover button */
div.stButton > button:hover {
    border-color: #2563eb;
    background: #eff6ff;
    color: #1d4ed8;
}

/* ================= SEARCH / SELECT BOX ================= */

input, selectbox {
    border-radius: 10px !important;
}

/* ================= GRID SPACING ================= */

.element-container {
    margin-bottom: 10px;
}

hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 1rem 0;
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
df.columns = df.columns.str.strip()

# ---------------- TABS ---------------- #
tab1, tab2, tab3 = st.tabs([
    "📂 Resources",
    "📢 Telegram Channels",
    "🤖 Telegram Bots"
])

# =========================================================
# 📂 RESOURCES TAB
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

    if len(filtered) == 0:
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

                st.link_button(
                    "📂 Open Resource",
                    row["Resource_Link"],
                    use_container_width=True
                )

# =========================================================
# 📢 TELEGRAM CHANNELS TAB
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

    if len(filtered_tg) == 0:
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

                st.link_button(
                    "📡 Join Channel",
                    row["Channel_Link_1"],
                    use_container_width=True
                )

# =========================================================
# 🤖 TELEGRAM BOTS TAB
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

    if len(filtered_bot) == 0:
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

                st.link_button(
                    "🚀 Open Bot",
                    row["Channel_Link_2"],
                    use_container_width=True
                )

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("⚡ Study Hub • Clean UI • Streamlit Powered")
