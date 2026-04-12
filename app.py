import streamlit as st
import pandas as pd

st.set_page_config(page_title="Study Hub", layout="wide")


# ---------------- GLOBAL CSS (SAME STYLE AS TELEGRAM) ---------------- #
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #f8fafc;
}

/* Titles */
h1, h2, h3 {
    color: #0f172a !important;
}

/* Card */
.study-card {
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

/* hover */
.study-card:hover {
    transform: translateY(-3px);
    border-color: #cbd5e1;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}

/* title */
.study-title {
    font-size: 18px;
    font-weight: 700;
    color: #0f172a;
}

/* subject pill */
.subject-pill {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    background: #ecfeff;
    color: #0e7490;
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
st.title("📚 Study Hub")
st.caption("Validated Google Sheets + Clean Resource Access")


# ---------------- LOAD DATA ---------------- #
SHEET_URL = "https://docs.google.com/spreadsheets/d/1al3Zy9Kd7YVIorEStPwI2x4C0GFDYBPGqIlVce1GWr8/export?format=csv"


@st.cache_data(ttl=300)
def load_data():
    return pd.read_csv(SHEET_URL)


df = load_data()


# ---------------- CLEAN DATA ---------------- #
def is_valid_link(x):
    return isinstance(x, str) and x.startswith("http")


df["valid"] = df["Link"].apply(is_valid_link)
df = df[df["valid"] == True]


# ---------------- TOP FILTERS ---------------- #
col1, col2 = st.columns([1, 2])

with col1:
    search = st.text_input("🔎 Search resources")

with col2:
    subjects = ["All"] + sorted(df["Subject"].dropna().unique().tolist())
    selected_subject = st.selectbox("📘 Subject", subjects)


# ---------------- FILTER DATA ---------------- #
filtered = df.copy()

if selected_subject != "All":
    filtered = filtered[filtered["Subject"] == selected_subject]

if search:
    filtered = filtered[
        filtered["Topic"].str.contains(search, case=False, na=False) |
        filtered["Tags"].str.contains(search, case=False, na=False)
    ]


# ---------------- TITLE ---------------- #
st.subheader(f"📂 Resources ({len(filtered)})")
st.markdown("---")


# ---------------- CARDS ---------------- #
if len(filtered) == 0:
    st.info("No resources found.")

else:
    cols = st.columns(3)

    for i, (_, row) in enumerate(filtered.iterrows()):
        with cols[i % 3]:

            st.markdown(
                f"""
                <div class="study-card">
                    <div>
                        <div class="study-title">📘 {row['Topic']}</div>
                        <div class="subject-pill">{row['Subject']}</div>
                    </div>

                   
                </div>
                """,
                unsafe_allow_html=True
            )

            st.link_button(
                "📂 Open Resource",
                row["Link"],
                use_container_width=True
            )


# ---------------- FOOTER ---------------- #
st.markdown("---")
st.caption("⚡ Study Hub • Clean UI • Streamlit Powered")