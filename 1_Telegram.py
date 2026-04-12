import streamlit as st
import pandas as pd

st.set_page_config(page_title="Telegram Hub", layout="wide")


# ---------------- GLOBAL CSS (ONLY ONCE) ---------------- #
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #f8fafc;
}

/* Title */
h1, h2, h3 {
    color: #0f172a !important;
}

/* Card */
.telegram-card {
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

/* hover effect */
.telegram-card:hover {
    transform: translateY(-3px);
    border-color: #cbd5e1;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}

/* title */
.telegram-title {
    font-size: 20px;
    font-weight: 700;
    color: #0f172a;
}

/* category pill */
.category-pill {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    background: #eff6ff;
    color: #2563eb;
}

/* buttons */
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    border: 1px solid #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ---------------- #
st.title("📢 Telegram Study Hub")
st.caption("JEE / NEET curated channels — clean and fast access")


# ---------------- LOAD DATA ---------------- #
SHEET_URL = "https://docs.google.com/spreadsheets/d/1al3Zy9Kd7YVIorEStPwI2x4C0GFDYBPGqIlVce1GWr8/export?format=csv"


@st.cache_data(ttl=300)
def load_data():
    return pd.read_csv(SHEET_URL)


df = load_data()


# ---------------- VALIDATION ---------------- #
def is_valid_telegram(x):
    return isinstance(x, str) and ("t.me/" in x or "telegram.me/" in x)


required_cols = ["Channel Name", "Telegram Link", "Category"]

if not all(col in df.columns for col in required_cols):
    st.error("Missing required columns: Channel Name, Telegram Link, Category")
    st.stop()


df = df[df["Telegram Link"].apply(is_valid_telegram)]

if df.empty:
    st.warning("No Telegram channels found.")
    st.stop()


# ---------------- TOP FILTERS ---------------- #
col1, col2 = st.columns([1, 2])

with col1:
    search = st.text_input("🔎 Search channels")

with col2:
    categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
    selected_category = st.selectbox("📂 Category", categories)


# ---------------- FILTER DATA ---------------- #
filtered = df.copy()

if selected_category != "All":
    filtered = filtered[filtered["Category"] == selected_category]

if search:
    filtered = filtered[
        filtered["Channel Name"].str.contains(search, case=False, na=False) |
        filtered["Category"].str.contains(search, case=False, na=False)
    ]


# ---------------- TITLE ---------------- #
st.subheader(f"📡 Channels ({len(filtered)})")
st.markdown("---")


# ---------------- CARDS ---------------- #
if len(filtered) == 0:
    st.info("No channels match your filters.")
   

else:
    cols = st.columns(3)
    

    for i, (_, row) in enumerate(filtered.iterrows()):
        with cols[i % 3]:
            

            st.markdown(
                f"""
                <div class="telegram-card">
                    <div>
                        <div class="telegram-title">📢 {row['Channel Name']}</div>
                        <div class="category-pill">{row['Category']}</div>
                    </div>

                   
                </div>
                
                """,
                unsafe_allow_html=True
                
            )
            st.link_button(
                "📡 Join Channel",
                row["Telegram Link"],
                use_container_width=True
            )
            


# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("⚡ Telegram Hub • Clean UI • Streamlit Powered")