"""Thèmes et mise en page de DocQuery, avec widgets Streamlit natifs."""

import streamlit as st

DARK = """
--dq-bg:#0B0F14;--dq-sidebar:#111720;--dq-surface:#111720;
--dq-soft:#151C26;--dq-border:#26303D;--dq-text:#F5F7FA;
--dq-muted:#98A2B3;--dq-accent:#4F7CFF;--dq-success:#2EB67D;--dq-error:#F04438;
color-scheme:dark;
"""
LIGHT = """
--dq-bg:#F5F7F8;--dq-sidebar:#FFFFFF;--dq-surface:#FFFFFF;
--dq-soft:#F0F2F3;--dq-border:#E4E7EA;--dq-text:#111315;
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
    div[data-testid="stMainBlockContainer"] {{ max-width:1170px;
        padding:1.1rem 2rem 8.5rem; }}
    section[data-testid="stSidebar"] {{ background:var(--dq-sidebar);
        border-right:1px solid var(--dq-border); }}
    @media (min-width:769px) {{ section[data-testid="stSidebar"] {{
        width:15rem !important; min-width:15rem !important; }} }}
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
    section[data-testid="stSidebar"] [class*="st-key-command_palette"] button {{
        background:transparent; border:0; color:var(--dq-muted);
        min-height:1.8rem; font-size:.78rem; }}
    section[data-testid="stSidebar"] [class*="st-key-chat_"] button {{
        width:100%; text-align:left; border:0; background:transparent;
        color:var(--dq-muted); font-size:.8rem; padding:.2rem .35rem;
        overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
    section[data-testid="stSidebar"] [class*="st-key-chat_"] button:hover {{
        background:var(--dq-soft); color:var(--dq-text); }}
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
        background:var(--dq-surface)!important; color:var(--dq-text)!important;
        border:1px solid var(--dq-border)!important; border-radius:8px; }}
    [data-testid="stSelectbox"] [data-baseweb="select"] *,
    [data-testid="stSelectbox"] [role="combobox"] {{
        background:transparent!important; color:var(--dq-text)!important;
        fill:var(--dq-muted)!important; }}
    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="popover"] [role="option"],
    [data-baseweb="menu"] {{background:var(--dq-surface)!important;
        color:var(--dq-text)!important;}}
    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="popover"] [aria-selected="true"] {{
        background:var(--dq-soft)!important;color:var(--dq-text)!important;}}
    [data-baseweb="popover"] > div, [data-testid="stPopoverBody"] {{
        background:var(--dq-surface)!important;color:var(--dq-text)!important;
        border-color:var(--dq-border)!important;}}
    [data-testid="stTextInput"] input {{min-height:3.2rem;}}
    [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {{
        border-color:var(--dq-accent);box-shadow:0 0 0 1px var(--dq-accent);}}
    button[kind="primary"] {{background:var(--dq-accent);color:#FFF;
        border-color:var(--dq-accent);border-radius:8px;}}
    button[kind="secondary"], [data-testid="stPopover"] button {{
        background:var(--dq-surface);color:var(--dq-text);
        border:1px solid var(--dq-border);border-radius:7px;}}
    [class*="st-key-suggestion_chips"] button,
    [class*="st-key-api_chips"] button,
    [class*="st-key-related_questions"] button,
    [class*="st-key-api_suggestion_chips"] button {{min-height:2rem;padding:.25rem .75rem;
        border-radius:20px;font-size:.82rem;}}
    [class*="st-key-suggestion_chips"] [data-testid="stHorizontalBlock"],
    [class*="st-key-api_chips"] [data-testid="stHorizontalBlock"],
    [class*="st-key-related_questions"] [data-testid="stHorizontalBlock"],
    [class*="st-key-api_suggestion_chips"] [data-testid="stHorizontalBlock"] {{
        flex-wrap:wrap;row-gap:.4rem;justify-content:flex-start;}}
    [class*="st-key-suggestion_chips"] [data-testid="column"],
    [class*="st-key-api_chips"] [data-testid="column"],
    [class*="st-key-related_questions"] [data-testid="column"],
    [class*="st-key-api_suggestion_chips"] [data-testid="column"] {{
        flex:0 1 auto!important;min-width:fit-content!important;}}
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
    [data-testid="stCode"] pre, [data-testid="stCode"] code {{
        background:var(--dq-soft)!important;color:var(--dq-text)!important;}}
    [data-testid="stCode"] code span {{color:var(--dq-text)!important;}}
    [data-testid="stExpander"], [data-testid="stPopoverBody"],
    [data-testid="stTable"] {{
        background:var(--dq-surface)!important;border-color:var(--dq-border)!important;
        color:var(--dq-text)!important;}}
    [data-testid="stTable"] th, [data-testid="stTable"] td {{
        background:var(--dq-surface)!important;color:var(--dq-text)!important;
        border-color:var(--dq-border)!important;}}
    [data-testid="stAlert"] {{border-radius:8px;}}
    .sidebar-brand {{font-size:1.26rem;font-weight:740;letter-spacing:-.05em;
        margin:.55rem 0 1.2rem;color:var(--dq-text);}}
    .brand-mark {{color:var(--dq-accent);font-size:.75rem;margin-left:.35rem;
        vertical-align:top;}}
    .topbar-brand {{font-size:1.05rem;font-weight:720;color:var(--dq-text);
        letter-spacing:-.04em;}}
    [class*="st-key-topbar"] {{margin:0 0 1.2rem;padding:.32rem .25rem .7rem;
        border-bottom:1px solid var(--dq-border);}}
    [class*="st-key-topbar"] button {{border:0!important;background:transparent!important;
        color:var(--dq-muted)!important;padding:.25rem .4rem!important;
        font-size:.83rem;min-height:2rem;white-space:nowrap;}}
    [class*="st-key-topbar"] button:hover {{background:var(--dq-soft)!important;
        color:var(--dq-text)!important;}}
    [class*="st-key-main_surface"] {{background:var(--dq-surface);
        border:1px solid var(--dq-border);border-radius:24px;
        padding:clamp(1.5rem,4.5vw,3.5rem);min-height:60vh;
        box-shadow:0 8px 30px rgba(0,0,0,.035);}}
    [class*="st-key-main_surface"] > [data-testid="stVerticalBlock"] {{max-width:820px;
        margin:0 auto;}}
    .app-eyebrow {{display:inline-block;padding:.4rem .75rem;
        background:var(--dq-soft);border-radius:999px;color:var(--dq-muted);}}
    .app-title {{margin:1.4rem 0 .6rem;}}
    .app-intro {{max-width:36rem;line-height:1.65;margin-bottom:2.2rem;}}
    [class*="st-key-quick_modes"] {{margin-bottom:2.2rem;}}
    [class*="st-key-quick_modes"] button {{background:var(--dq-soft);
        border:1px solid transparent;border-radius:999px;color:var(--dq-text);
        min-height:2.35rem;font-size:.83rem;white-space:nowrap;}}
    [class*="st-key-quick_modes"] button:hover {{border-color:var(--dq-accent);
        color:var(--dq-accent);}}
    [class*="st-key-conversation_turn_"] {{max-width:720px;padding-top:1.6rem;}}
    [class*="st-key-conversation_turn_"] [data-testid="stDivider"] {{opacity:.35;}}
    [class*="st-key-composer_shell"] {{max-width:900px;margin:0 auto;
        background:var(--dq-surface);border:1px solid var(--dq-border);
        border-radius:20px;padding:.65rem .95rem .7rem;
        box-shadow:0 8px 30px rgba(0,0,0,.06);
        transition:border-color .15s ease,box-shadow .15s ease;}}
    [class*="st-key-composer_shell"]:focus-within {{border-color:var(--dq-accent);
        box-shadow:0 0 0 3px rgba(79,124,255,.12);}}
    [class*="st-key-composer_shell"] [data-testid="stChatInput"] {{border:0;
        background:transparent;box-shadow:none;}}
    [class*="st-key-composer_shell"] [data-testid="stChatInput"] > div {{
        border:0!important;background:transparent!important;box-shadow:none!important;}}
    [class*="st-key-composer_shell"] textarea {{min-height:3rem!important;
        color:var(--dq-text)!important;}}
    [class*="st-key-composer_shortcuts"] [data-testid="stVerticalBlock"] {{
        flex-direction:row;align-items:center;gap:.65rem;}}
    [class*="st-key-composer_shortcuts"] [data-testid="stCaptionContainer"] {{
        font-size:.73rem;color:var(--dq-muted);}}
    [class*="st-key-composer_shortcuts"] button {{border-radius:10px;
        padding:.15rem .6rem;min-height:1.8rem;}}
    [data-testid="stBottomBlockContainer"] {{background:var(--dq-bg)!important;
        padding: .7rem 1rem 1rem!important;}}
    section[data-testid="stSidebar"] [class*="st-key-sidebar_settings"] {{margin-top:1rem;}}
    section[data-testid="stSidebar"] [class*="st-key-sidebar_settings"] button {{
        width:100%;border:0;background:transparent;color:var(--dq-muted);
        text-align:left;min-height:2rem;}}
    [class*="st-key-main_surface"] [data-testid="stFileUploaderDropzone"] {{
        min-height:9rem;border-radius:16px;}}
    button {{transition:background .15s ease,border-color .15s ease,
        transform .15s ease;}}
    @media (prefers-color-scheme:dark) {{
        [class*="st-key-main_surface"] {{box-shadow:none;}}
    }}
    @media (max-width:900px) {{
        [class*="st-key-main_surface"] {{min-height:55vh;}}
        [class*="st-key-topbar"] [data-testid="column"]:first-child {{display:none;}}
    }}
    @media (max-width:640px) {{
        div[data-testid="stMainBlockContainer"] {{padding:1rem .65rem 8rem;}}
        [class*="st-key-main_surface"] {{padding:1.25rem;min-height:50vh;
            border-radius:18px;}}
        [class*="st-key-topbar"] [data-testid="stHorizontalBlock"],
        [class*="st-key-quick_modes"] [data-testid="stHorizontalBlock"] {{
            flex-wrap:wrap;gap:.2rem;}}
        [class*="st-key-topbar"] [data-testid="column"] {{min-width:fit-content!important;
            width:auto!important;flex:0 1 auto!important;}}
        [class*="st-key-topbar"] [data-testid="column"]:nth-child(5) {{display:none;}}
        [class*="st-key-quick_modes"] [data-testid="column"] {{
            min-width:fit-content!important;flex:0 1 auto!important;}}
        .app-title {{font-size:2rem;}}
        [class*="st-key-answer_actions"] [data-testid="stHorizontalBlock"] {{
            flex-wrap:wrap;row-gap:.35rem;}}
        [class*="st-key-answer_actions"] [data-testid="column"] {{
            min-width:calc(50% - .5rem);}}
        .app-intro {{margin-bottom:1.2rem;}}
    }}
    </style>
    """, unsafe_allow_html=True)
