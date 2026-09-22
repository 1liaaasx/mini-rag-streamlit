"""Thèmes et mise en page de DocQuery, avec widgets Streamlit natifs."""

import streamlit as st

DARK = """
--dq-bg:#0B0F14;--dq-sidebar:#111720;--dq-surface:#151C26;
--dq-soft:#1B2532;--dq-border:#26303D;--dq-text:#F5F7FA;
--dq-muted:#98A2B3;--dq-accent:#4F7CFF;--dq-success:#2EB67D;--dq-error:#F04438;
color-scheme:dark;
"""
LIGHT = """
--dq-bg:#F7F9FC;--dq-sidebar:#FFFFFF;--dq-surface:#FFFFFF;
--dq-soft:#F3F4F6;--dq-border:#E5E7EB;--dq-text:#111827;
--dq-muted:#6B7280;--dq-accent:#4F7CFF;--dq-success:#16A34A;--dq-error:#DC2626;
color-scheme:light;
"""


def inject_custom_css(theme):
    base = LIGHT if theme == "Light" else DARK
    system = f"@media (prefers-color-scheme: light) {{:root, .stApp {{{LIGHT}}}}}" if theme == "System" else ""
    st.markdown(f"""
    <style>
    :root, .stApp {{{base}}}
    {system}
    html, body, .stApp {{ background:var(--dq-bg); color:var(--dq-text);
        font-family:Inter,ui-sans-serif,system-ui,sans-serif; }}
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stText"], .stApp label {{ color:var(--dq-text); }}
    .stApp [data-testid="stCaptionContainer"] {{ color:var(--dq-muted); }}
    header[data-testid="stHeader"] {{ background:transparent; }}
    div[data-testid="stMainBlockContainer"] {{ max-width:850px;
        padding:3.3rem 1.8rem 4rem; }}
    section[data-testid="stSidebar"] {{ background:var(--dq-sidebar);
        border-right:1px solid var(--dq-border); }}
    @media (min-width:769px) {{ section[data-testid="stSidebar"] {{
        width:15.6rem !important; min-width:15.6rem !important; }} }}
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
        margin-top:.8rem; font-size:.68rem; font-weight:650; letter-spacing:.09em;
        color:var(--dq-muted); }}
    section[data-testid="stSidebar"] h2 {{ font-size:1.22rem; margin-bottom:1.2rem; }}
    section[data-testid="stSidebar"] .stButton {{ margin:0; }}
    section[data-testid="stSidebar"] [class*="st-key-nav_"] button {{
        width:100%; min-height:2rem; margin:0; padding:.22rem .72rem;
        border:0; border-left:2px solid transparent; border-radius:5px;
        background:transparent; color:var(--dq-muted); text-align:left;
        font-weight:500; font-size:.85rem; box-shadow:none; }}
    section[data-testid="stSidebar"] [class*="st-key-nav_"] button:hover {{
        color:var(--dq-text); background:var(--dq-soft); }}
    section[data-testid="stSidebar"] [class*="st-key-nav_active_"] button {{
        color:var(--dq-text); background:var(--dq-soft);
        border-left-color:var(--dq-accent); }}
    section[data-testid="stSidebar"] [class*="st-key-new_chat"] button {{
        width:100%; background:var(--dq-surface); border:1px solid var(--dq-border);
        border-radius:6px; color:var(--dq-text); min-height:2.2rem; }}
    section[data-testid="stSidebar"] [data-testid="stExpander"] {{
        margin-top:.8rem; border:0; background:transparent; }}
    .app-eyebrow {{color:var(--dq-muted);font-size:.8rem;font-weight:600;}}
    .app-title {{margin:.65rem 0 .4rem;color:var(--dq-text);
        font-size:clamp(2rem,4vw,3rem);letter-spacing:-.045em;
        font-weight:650;line-height:1.15;}}
    .app-intro {{color:var(--dq-muted);margin:0 0 1.8rem;font-size:.97rem;}}
    .conversation-heading {{color:var(--dq-muted);font-size:.83rem;
        font-weight:600;margin:0 0 1.4rem;}}
    [data-testid="stForm"] {{ border:0; padding:0; }}
    [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
        background:var(--dq-surface); color:var(--dq-text);
        border:1px solid var(--dq-border); border-radius:8px; }}
    [data-testid="stTextInput"] input {{min-height:3.2rem;}}
    [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {{
        border-color:var(--dq-accent);box-shadow:0 0 0 1px var(--dq-accent);}}
    button[kind="primary"] {{background:var(--dq-accent);color:#FFF;
        border-color:var(--dq-accent);border-radius:8px;}}
    button[kind="secondary"], [data-testid="stPopover"] button {{
        background:var(--dq-surface);color:var(--dq-text);
        border:1px solid var(--dq-border);border-radius:7px;}}
    [class*="st-key-suggestion_chips"] button,
    [class*="st-key-api_chips"] button {{min-height:2rem;padding:.25rem .75rem;
        border-radius:20px;font-size:.82rem;}}
    [class*="st-key-conversation_turn_"] {{max-width:720px;padding-top:1.3rem;}}
    [class*="st-key-conversation_turn_"] [data-testid="stMarkdownContainer"] p,
    [class*="st-key-conversation_turn_"] [data-testid="stMarkdownContainer"] li {{
        line-height:1.72;}}
    [class*="st-key-answer_actions"] button {{background:transparent;
        border:0;min-height:1.75rem;padding:.2rem .45rem;
        color:var(--dq-muted);font-size:.82rem;}}
    [class*="st-key-answer_actions"] button:hover {{color:var(--dq-accent);}}
    [class*="st-key-upload_zone"] {{background:var(--dq-surface);
        border:1px dashed var(--dq-border)!important;border-radius:12px;
        padding:1.15rem 1.4rem;}}
    [data-testid="stFileUploaderDropzone"] {{background:var(--dq-soft);
        border-color:var(--dq-border);}}
    [data-testid="stFileUploaderDropzoneInstructions"] small {{display:none;}}
    [data-testid="stFileUploaderDropzone"] button {{color:var(--dq-text);
        border-color:var(--dq-border);background:var(--dq-surface);}}
    div[data-testid="stTabs"] button {{color:var(--dq-muted);}}
    div[data-testid="stTabs"] button[aria-selected="true"] {{color:var(--dq-text);}}
    [data-testid="stCode"] {{border:1px solid var(--dq-border);max-width:100%;
        overflow-x:auto;}}
    [data-testid="stExpander"], [data-testid="stPopoverBody"] {{
        background:var(--dq-surface);border-color:var(--dq-border);}}
    [data-testid="stAlert"] {{border-radius:8px;}}
    @media (max-width:640px) {{
        div[data-testid="stMainBlockContainer"] {{padding:2.1rem 1rem 3rem;}}
        [class*="st-key-answer_actions"] [data-testid="stHorizontalBlock"] {{
            flex-wrap:wrap;row-gap:.35rem;}}
        [class*="st-key-answer_actions"] [data-testid="column"] {{
            min-width:calc(50% - .5rem);}}
        .app-intro {{margin-bottom:1.2rem;}}
    }}
    </style>
    """, unsafe_allow_html=True)
