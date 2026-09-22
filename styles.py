"""Styles de l’interface DocQuery."""

import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
        :root { color-scheme: dark; }
        html, body, .stApp {
            background: #0B0F14;
            color: #F5F7FA;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                BlinkMacSystemFont, "Segoe UI", sans-serif;
        }
        #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }
        div[data-testid="stMainBlockContainer"] {
            max-width: 1050px;
            padding: 3.5rem 2rem 5rem;
        }
        .app-eyebrow {
            color: #98A2B3; font-size: .76rem; font-weight: 600;
            letter-spacing: .12em; text-transform: uppercase;
        }
        .app-title {
            margin: .65rem 0 .7rem; color: #F5F7FA;
            font-size: clamp(2.15rem, 5vw, 3.15rem);
            font-weight: 650; line-height: 1.12; letter-spacing: -.04em;
        }
        .app-intro {
            margin: 0 0 1.8rem; max-width: 650px; color: #B1BBC9;
            font-size: 1.08rem; line-height: 1.7;
        }
        .app-steps {
            margin: 1.15rem 0 2.1rem; color: #98A2B3;
            font-size: .84rem; letter-spacing: .01em;
        }
        .st-key-upload_card, .st-key-question_card, .st-key-answer_card {
            background: #151C26;
            border: 1px solid #26303D !important;
            border-radius: 16px !important;
            padding: 1.4rem 1.55rem;
            margin-bottom: 1.05rem;
        }
        .section-title {
            margin: 0 0 .28rem; color: #F5F7FA;
            font-size: 1.22rem; font-weight: 620; letter-spacing: -.02em;
        }
        .section-description {
            margin: 0 0 1.15rem; color: #98A2B3;
            font-size: .93rem; line-height: 1.55;
        }
        .empty-note {
            margin: .7rem 0 0; color: #98A2B3;
            font-size: .84rem;
        }
        .file-name {
            overflow-wrap: anywhere; color: #F5F7FA;
            font-size: .98rem; font-weight: 600;
        }
        .file-details {
            margin-top: .3rem; color: #98A2B3; font-size: .84rem;
        }
        .ready-label {
            display: inline-flex; align-items: center; gap: .55rem;
            margin-top: 1rem; color: #BCEAD6;
            font-size: .85rem; font-weight: 600;
        }
        .ready-dot {
            width: .5rem; height: .5rem; border-radius: 50%;
            background: #2EB67D;
        }
        .st-key-upload_card [data-testid="stFileUploaderDropzone"] {
            background: #111720; border: 1px dashed #394555;
            border-radius: 10px;
        }
        .st-key-upload_card [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #4F7CFF;
        }
        .st-key-question_card input {
            background: #111720; color: #F5F7FA;
            border: 1px solid #394555; border-radius: 9px;
            min-height: 3rem;
        }
        .st-key-question_card input:focus {
            border-color: #4F7CFF; box-shadow: 0 0 0 2px #4F7CFF33;
        }
        .st-key-question_card button[kind="primary"] {
            background: #4F7CFF; border: 1px solid #4F7CFF;
            border-radius: 9px; color: #FFFFFF; min-height: 3rem;
            font-weight: 600;
        }
        .st-key-question_card button[kind="primary"]:hover {
            background: #416DEB; border-color: #416DEB; color: #FFFFFF;
        }
        .st-key-question_card button[kind="secondary"] {
            background: #111720; color: #D7DFEA;
            border: 1px solid #26303D; border-radius: 8px;
            text-align: left; min-height: 2.6rem;
        }
        .st-key-question_card button[kind="secondary"]:hover {
            border-color: #4F7CFF; color: #F5F7FA;
        }
        section[data-testid="stSidebar"] {
            border-right: 1px solid #26303D;
        }
        div[data-testid="stTabs"] button {
            color: #B1BBC9;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #F5F7FA;
        }
        [data-testid="stCode"] { border: 1px solid #26303D; }
        .st-key-answer_card [data-testid="stMarkdownContainer"] {
            color: #E5EAF1; font-size: 1rem; line-height: 1.75;
        }
        .st-key-answer_card [data-testid="stMarkdownContainer"] p,
        .st-key-answer_card [data-testid="stMarkdownContainer"] li {
            line-height: 1.75;
        }
        .st-key-answer_card [data-testid="stExpander"] {
            background: #111720; border: 1px solid #26303D;
            border-radius: 9px; margin-top: .7rem;
        }
        div[data-testid="stAlert"] { border-radius: 9px; }
        @media (max-width: 640px) {
            div[data-testid="stMainBlockContainer"] {
                padding: 2.6rem 1rem 3rem;
            }
            .st-key-upload_card, .st-key-question_card, .st-key-answer_card {
                padding: 1.1rem 1rem;
            }
            .app-steps { margin-bottom: 1.55rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

