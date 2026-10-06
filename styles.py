import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    :root {
        --bg: #09090b;
        --card: #111216;
        --card2: #17181d;
        --text: #f4f4f5;
        --muted: #9b9ca3;
        --crimson: #6f1828;
        --crimson2: #8e2638;
        --silver: #b8bac1;
        --positive: #69a77b;
        --negative: #b45b66;
        --border: rgba(255,255,255,.08);
    }

    .stApp { background: var(--bg); color: var(--text); }
    section[data-testid="stSidebar"] { background: #0d0e11; border-right: 1px solid var(--border); }
    div[data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 14px;
    }
    .brand { display:flex; align-items:center; gap:14px; margin: 6px 0 24px 0; }
    .brand-mark {
        width:42px; height:42px; border-radius:12px;
        display:flex; align-items:center; justify-content:center;
        background: linear-gradient(145deg, #7e2031, #351018);
        border:1px solid rgba(255,255,255,.12);
        font-weight:800; font-size:21px;
    }
    .brand-name { font-size:28px; font-weight:750; letter-spacing:-.7px; }
    .brand-tag { font-size:9px; color:var(--muted); letter-spacing:2px; margin-top:1px; }
    .ticker {
        color:#b8bac1; font-size:14px; letter-spacing:1px;
        border:1px solid var(--border); border-radius:7px; padding:4px 8px;
        vertical-align:middle;
    }
    h1,h2,h3 { letter-spacing:-.3px; }
    .stButton>button, .stLinkButton>a {
        border-radius:10px !important;
        border:1px solid rgba(142,38,56,.65) !important;
    }
    </style>
    """, unsafe_allow_html=True)
