"""Styles sobres de DocQuery ; les widgets restent des composants Streamlit natifs."""

import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
    :root { color-scheme: dark; }
    html, body, .stApp { background: #0B0F14; color: #F5F7FA;
        font-family: Inter, ui-sans-serif, system-ui, sans-serif; }
    header[data-testid="stHeader"] { background: transparent; }
    div[data-testid="stMainBlockContainer"] { max-width: 980px; padding: 4rem 2.3rem 5rem; }
    section[data-testid="stSidebar"] { background: #111720; border-right: 1px solid #26303D; }
    section[data-testid="stSidebar"] button { text-align: left; border-radius: 8px; }
    section[data-testid="stSidebar"] button[kind="primary"] {
        background: #202B3F; color: #F5F7FA; border-color: #4F7CFF;
    }
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        margin-top: 1rem; letter-spacing: .06em; color: #98A2B3;
    }
    .app-eyebrow { color: #98A2B3; font-size: .85rem; font-weight: 600; }
    .app-title { margin: .6rem 0; color: #F5F7FA; font-size: clamp(2rem, 5vw, 3.2rem);
        letter-spacing: -.04em; font-weight: 650; line-height: 1.15; }
    .app-intro { color: #98A2B3; margin: 0 0 2rem; font-size: 1rem; }
    [data-testid="stForm"] { border: 0; padding: 0; }
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
        background: #151C26; color: #F5F7FA; border: 1px solid #394555; border-radius: 9px;
    }
    [data-testid="stTextInput"] input { min-height: 3.5rem; }
    [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
        border-color: #4F7CFF; box-shadow: 0 0 0 1px #4F7CFF;
    }
    button[kind="primary"] { background: #4F7CFF; color: white; border-radius: 8px; }
    button[kind="secondary"] { background: #151C26; border-color: #26303D;
        color: #D7DFEA; border-radius: 8px; }
    div[data-testid="stTabs"] button { color: #B1BBC9; }
    div[data-testid="stTabs"] button[aria-selected="true"] { color: #F5F7FA; }
    [data-testid="stCode"] { border: 1px solid #26303D; }
    [data-testid="stExpander"] { background: #111720; border: 1px solid #26303D;
        border-radius: 9px; }
    div[data-testid="stAlert"] { border-radius: 8px; }
    @media (max-width: 640px) {
        div[data-testid="stMainBlockContainer"] { padding: 2.5rem 1rem 3rem; }
        .app-intro { margin-bottom: 1.5rem; }
    }
    </style>
    """, unsafe_allow_html=True)
