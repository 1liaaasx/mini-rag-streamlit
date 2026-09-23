"""Design system et mise en page de DocQuery avec composants Streamlit natifs."""

import streamlit as st


DARK = """
--app-bg:#0B0F14;--sidebar-bg:#101720;--surface:#111720;
--surface-soft:#151C26;--surface-hover:#1B2430;--input-bg:#151C26;
--border:#26303D;--border-hover:#344153;--text:#F5F7FA;
--text-secondary:#98A2B3;--text-muted:#8490A2;--placeholder:#8B96A8;
--accent:#4F7CFF;--accent-hover:#416BE0;--accent-active:#3561D8;--accent-soft:rgba(79,124,255,.12);
--success:#2EB67D;--error:#F04438;--disabled-bg:#1B2430;
--disabled-text:#667085;--shadow:none;color-scheme:dark;
"""

LIGHT = """
--app-bg:#F7F9FC;--sidebar-bg:#FFFFFF;--surface:#FFFFFF;
--surface-soft:#F3F4F6;--surface-hover:#ECEFF3;--input-bg:#FFFFFF;
--border:#E5E7EB;--border-hover:#D1D5DB;--text:#111827;
--text-secondary:#6B7280;--text-muted:#6B7280;--placeholder:#6B7280;
--accent:#4F7CFF;--accent-hover:#416BE0;--accent-active:#3561D8;--accent-soft:#EEF3FF;
--success:#16A34A;--error:#DC2626;--disabled-bg:#F3F4F6;
--disabled-text:#9CA3AF;--shadow:0 8px 30px rgba(0,0,0,.05);color-scheme:light;
"""


def inject_custom_css(theme):
    """Injecte un thème unique et des variantes cohérentes pour les widgets."""
    base = LIGHT if theme == "Light" else DARK
    system = (
        f"@media (prefers-color-scheme:light) {{:root,.stApp {{{LIGHT}}}}}"
        if theme == "System" else ""
    )
    st.markdown(f"""
    <style>
    :root,.stApp {{{base}}}
    {system}
    html,body,.stApp {{background:var(--app-bg);color:var(--text);
        font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,
        "Segoe UI",sans-serif;}}
    .stApp [data-testid="stMarkdownContainer"],.stApp [data-testid="stText"],
    .stApp label {{color:var(--text);}}
    .stApp [data-testid="stCaptionContainer"] {{color:var(--text-secondary);}}
    header[data-testid="stHeader"] {{background:transparent;}}
    div[data-testid="stMainBlockContainer"] {{max-width:1170px;padding:1rem 2rem 9.25rem;}}

    /* Boutons */
    .stButton>button,.stFormSubmitButton>button,[data-testid="stLinkButton"]>a,
    [data-testid="stPopover"]>button {{min-height:40px;padding:0 14px;border-radius:10px;
        font-weight:550;box-shadow:none;transition:background .15s ease,
        border-color .15s ease,color .15s ease,transform .15s ease;}}
    button[kind="primary"],button[data-testid^="stBaseButton-primary"],
    [data-testid="stLinkButton"] a[data-testid="stBaseLinkButton-primary"] {{
        background:var(--accent-hover)!important;color:#FFF!important;
        border:1px solid var(--accent-hover)!important;}}
    button[kind="primary"]:hover,button[data-testid^="stBaseButton-primary"]:hover,
    [data-testid="stLinkButton"] a[data-testid="stBaseLinkButton-primary"]:hover {{
        background:var(--accent-active)!important;
        border-color:var(--accent-active)!important;}}
    button[kind="secondary"],button[data-testid^="stBaseButton-secondary"],
    button[data-testid="stBaseButton-tertiary"],
    [data-testid="stLinkButton"] a[data-testid="stBaseLinkButton-secondary"],
    [data-testid="stPopover"]>button {{
        background:var(--surface-soft)!important;color:var(--text)!important;
        border:1px solid var(--border)!important;}}
    button[kind="secondary"]:hover,button[data-testid^="stBaseButton-secondary"]:hover,
    button[data-testid="stBaseButton-tertiary"]:hover,
    [data-testid="stLinkButton"] a[data-testid="stBaseLinkButton-secondary"]:hover,
    [data-testid="stPopover"]>button:hover {{background:var(--surface-hover)!important;
        border-color:var(--border-hover)!important;color:var(--text)!important;}}
    button[kind="primary"] *,button[data-testid^="stBaseButton-primary"] *,
    [data-testid="stLinkButton"] a[data-testid="stBaseLinkButton-primary"] * {{
        color:#FFF!important;fill:#FFF!important;}}
    button[kind="secondary"] *,button[data-testid^="stBaseButton-secondary"] *,
    button[data-testid="stBaseButton-tertiary"] *,
    [data-testid="stLinkButton"] a[data-testid="stBaseLinkButton-secondary"] *,
    [data-testid="stLinkButton"] a[data-testid="stBaseLinkButton-secondary"]:visited * {{
        color:var(--text)!important;fill:var(--text)!important;}}
    button:disabled,[data-testid="stLinkButton"] a[aria-disabled="true"] {{background:var(--disabled-bg)!important;
        color:var(--disabled-text)!important;border-color:var(--border)!important;
        opacity:.72!important;cursor:not-allowed!important;}}
    button:disabled *,[data-testid="stLinkButton"] a[aria-disabled="true"] * {{
        color:var(--disabled-text)!important;fill:var(--disabled-text)!important;}}
    [class*="st-key-delete_"] button {{color:var(--error)!important;
        background:transparent!important;border-color:transparent!important;}}

    /* Champs, selectbox et menus */
    [data-testid="stTextInputRootElement"],[data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-testid="stSelectbox"] [data-baseweb="select"]>div,
    [data-testid="stSelectbox"] div:has(>input[role="combobox"]) {{background:var(--input-bg)!important;
        color:var(--text)!important;border:1px solid var(--border)!important;
        border-radius:12px!important;caret-color:var(--accent);}}
    [data-testid="stTextInputField"],[data-testid="stTextInput"] input {{min-height:44px;
        color:var(--text)!important;-webkit-text-fill-color:var(--text)!important;}}
    [data-testid="stTextInputField"]::placeholder,[data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder {{
        color:var(--placeholder)!important;opacity:1!important;}}
    [data-testid="stSelectbox"] input[role="combobox"] {{
        min-height:44px;background:transparent!important;color:var(--text)!important;
        -webkit-text-fill-color:var(--text)!important;caret-color:var(--accent)!important;}}
    [data-testid="stSelectbox"] input[role="combobox"]::placeholder {{
        color:var(--placeholder)!important;-webkit-text-fill-color:var(--placeholder)!important;
        opacity:1!important;}}
    [data-testid="stTextInputRootElement"]:focus-within,[data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stSelectbox"] [data-baseweb="select"]>div:focus-within,
    [data-testid="stSelectbox"] div:has(>input[role="combobox"]):focus-within {{
        border-color:var(--accent)!important;box-shadow:0 0 0 3px rgba(79,124,255,.12)!important;
        outline:none!important;}}
    [data-testid="stSelectbox"] [data-baseweb="select"] *,
    [data-testid="stSelectbox"] [role="combobox"] {{color:var(--text)!important;
        fill:var(--text-secondary)!important;}}
    [data-testid="stSelectbox"] button[aria-label="Open"],
    [data-testid="stSelectbox"] button[aria-label="Clear value"] {{
        min-height:40px!important;padding:0 .65rem!important;background:transparent!important;
        border:0!important;color:var(--text-secondary)!important;}}
    [data-testid="stSelectbox"] button,[data-testid="stSelectbox"] svg {{
        color:var(--text-secondary)!important;fill:currentColor!important;}}
    [data-baseweb="popover"] [role="listbox"],[data-baseweb="popover"] [role="option"],
    [data-baseweb="menu"],[data-testid="stPopoverBody"],
    [data-testid="stSelectboxVirtualDropdown"] {{background:var(--surface)!important;
        color:var(--text)!important;border-color:var(--border)!important;}}
    [data-testid="stSelectboxVirtualDropdown"] * {{color:var(--text)!important;}}
    [data-baseweb="popover"] [role="option"]:hover,[data-baseweb="popover"] [aria-selected="true"] {{
        background:var(--surface-hover)!important;color:var(--text)!important;}}
    [data-testid="stSelectboxVirtualDropdown"] [role="option"]:hover,
    [data-testid="stSelectboxVirtualDropdown"] [role="option"][aria-selected="true"],
    [data-testid="stSelectboxVirtualDropdown"] [data-focused="true"] {{
        background:var(--surface-hover)!important;color:var(--text)!important;}}

    /* Sidebar */
    section[data-testid="stSidebar"] {{background:var(--sidebar-bg);border-right:1px solid var(--border);}}
    @media (min-width:769px) {{section[data-testid="stSidebar"] {{width:15rem!important;
        min-width:15rem!important;}}}}
    .sidebar-brand {{margin:.55rem 0 1rem;font-size:1.25rem;font-weight:740;
        letter-spacing:-.04em;color:var(--text);}}
    .brand-mark {{color:var(--accent);font-size:.72rem;margin-left:.35rem;vertical-align:top;}}
    .sidebar-version {{font-size:.82rem;color:var(--text-secondary);padding:.15rem .65rem .35rem;}}
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{margin-top:.9rem;
        font-size:.67rem;font-weight:700;letter-spacing:.09em;color:var(--text-muted);}}
    section[data-testid="stSidebar"] .stButton {{margin:0;}}
    section[data-testid="stSidebar"] [class*="st-key-nav_"] button,
    section[data-testid="stSidebar"] [class*="st-key-chat_"] button,
    section[data-testid="stSidebar"] [class*="st-key-sidebar_settings"] button {{width:100%;
        min-height:34px;padding:.25rem .7rem;text-align:left;background:transparent!important;
        color:var(--text-secondary)!important;border:0!important;
        border-left:2px solid transparent!important;border-radius:8px!important;font-size:.84rem;
        font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}}
    section[data-testid="stSidebar"] [class*="st-key-nav_"] button:hover,
    section[data-testid="stSidebar"] [class*="st-key-chat_"] button:hover,
    section[data-testid="stSidebar"] [class*="st-key-sidebar_settings"] button:hover {{
        background:var(--surface-hover)!important;color:var(--text)!important;}}
    section[data-testid="stSidebar"] [class*="st-key-nav_active_"] button {{
        background:var(--accent-soft)!important;color:var(--text)!important;
        border-left-color:var(--accent)!important;}}
    section[data-testid="stSidebar"] [class*="st-key-new_chat"] button {{width:100%;
        background:var(--surface-soft)!important;color:var(--text)!important;
        border:1px solid var(--border)!important;}}
    section[data-testid="stSidebar"] [class*="st-key-sidebar_settings"] {{margin-top:1rem;}}
    section[data-testid="stSidebar"] [class*="st-key-logout"] button {{width:100%;min-height:34px;
        margin-top:.25rem;padding:.25rem .7rem;text-align:left;background:transparent!important;
        color:var(--text-secondary)!important;border:0!important;border-radius:8px!important;
        font-size:.84rem;font-weight:500;}}
    section[data-testid="stSidebar"] [class*="st-key-logout"] button:hover {{
        background:var(--surface-hover)!important;color:var(--text)!important;}}
    section[data-testid="stSidebar"] [data-testid="stPopover"]>button {{min-height:30px;
        padding:0 .45rem;background:transparent!important;border-color:transparent!important;
        color:var(--text-secondary)!important;}}
    [data-testid="stSidebarCollapseButton"] button {{width:36px!important;height:36px!important;
        min-height:36px!important;padding:0!important;background:transparent!important;
        color:var(--text-secondary)!important;border:1px solid transparent!important;}}
    [data-testid="stSidebarCollapseButton"] button:hover {{background:var(--surface-hover)!important;
        color:var(--text)!important;}}
    [data-testid="stSidebarCollapseButton"] svg {{fill:currentColor!important;}}

    /* Topbar et surface principale */
    .topbar-brand {{font-size:1.05rem;font-weight:720;color:var(--text);letter-spacing:-.04em;}}
    [class*="st-key-topbar"] {{margin:0 0 1rem;padding:.3rem .25rem .65rem;
        border-bottom:1px solid var(--border);}}
    [class*="st-key-topbar"] button {{min-height:32px!important;padding:.2rem .55rem!important;
        border:0!important;background:transparent!important;color:var(--text-secondary)!important;
        font-size:.82rem;white-space:nowrap;}}
    [class*="st-key-topbar"] button:hover {{background:var(--surface-hover)!important;
        color:var(--text)!important;}}
    [class*="st-key-main_surface"] {{min-height:58vh;padding:clamp(1.4rem,4vw,3.25rem);
        background:var(--surface);border:1px solid var(--border);border-radius:24px;
        box-shadow:var(--shadow);}}
    [class*="st-key-main_surface"]>[data-testid="stVerticalBlock"] {{width:100%;max-width:900px;
        margin:0 auto;}}
    .app-eyebrow {{display:inline-block;padding:.42rem .75rem;background:var(--surface-soft);
        color:var(--text-secondary);border-radius:999px;font-size:.78rem;font-weight:650;}}
    .app-title {{margin:1.15rem 0 .5rem;color:var(--text);font-size:clamp(2rem,4vw,2.85rem);
        line-height:1.12;letter-spacing:-.045em;font-weight:680;}}
    .app-intro {{max-width:38rem;margin:0 0 1.8rem;color:var(--text-secondary);
        font-size:1rem;line-height:1.65;}}
    .conversation-heading {{margin:0 0 1.25rem;color:var(--text-secondary);
        font-size:.82rem;font-weight:650;}}

    /* Login */
    [class*="st-key-login_page"] {{width:100%;max-width:460px;margin:clamp(2rem,9vh,6rem) auto 0;}}
    [class*="st-key-login_card"] {{padding:clamp(1.5rem,5vw,2.4rem);background:var(--surface);
        border:1px solid var(--border);border-radius:24px;box-shadow:var(--shadow);}}
    .login-brand {{margin-bottom:2rem;color:var(--text);font-size:1.12rem;font-weight:760;
        letter-spacing:-.035em;}}
    .login-brand span {{margin-left:.35rem;color:var(--accent);font-size:.7rem;vertical-align:top;}}
    .login-title {{margin:0 0 .5rem;color:var(--text);font-size:clamp(1.8rem,5vw,2.35rem);
        line-height:1.15;letter-spacing:-.04em;}}
    .login-intro {{margin:0 0 1.6rem;color:var(--text-secondary);line-height:1.6;}}
    [class*="st-key-login_card"] [data-testid="stForm"] {{padding:0;border:0;}}
    [class*="st-key-login_card"] .stFormSubmitButton>button {{width:100%;margin-top:.65rem;}}
    [class*="st-key-login_language"] {{max-width:180px;margin:1rem auto 0;}}
    [class*="st-key-login_language"] [data-testid="stSelectbox"] label {{display:none;}}

    /* Chips et actions Ghost */
    [class*="st-key-suggestion_chips"] [data-testid="stHorizontalBlock"],
    [class*="st-key-api_chips"] [data-testid="stHorizontalBlock"],
    [class*="st-key-api_suggestion_chips"] [data-testid="stHorizontalBlock"],
    [class*="st-key-related_questions"] [data-testid="stHorizontalBlock"],
    [class*="st-key-docs_examples"] [data-testid="stHorizontalBlock"],
    [class*="st-key-quick_modes"] [data-testid="stHorizontalBlock"] {{flex-wrap:wrap;
        justify-content:flex-start;gap:.45rem;}}
    [class*="st-key-suggestion_chips"] [data-testid="column"],
    [class*="st-key-api_chips"] [data-testid="column"],
    [class*="st-key-api_suggestion_chips"] [data-testid="column"],
    [class*="st-key-related_questions"] [data-testid="column"],
    [class*="st-key-docs_examples"] [data-testid="column"],
    [class*="st-key-quick_modes"] [data-testid="column"] {{flex:0 1 auto!important;
        min-width:fit-content!important;}}
    [class*="st-key-suggestion_chips"] button,[class*="st-key-api_chips"] button,
    [class*="st-key-api_suggestion_chips"] button,[class*="st-key-related_questions"] button,
    [class*="st-key-docs_examples"] button,[class*="st-key-quick_modes"] button {{
        min-height:34px!important;padding:0 12px!important;border-radius:999px!important;
        background:var(--surface-soft)!important;color:var(--text)!important;
        border:1px solid var(--border)!important;font-size:.81rem;}}
    [class*="st-key-suggestion_chips"] button:hover,[class*="st-key-api_chips"] button:hover,
    [class*="st-key-api_suggestion_chips"] button:hover,[class*="st-key-related_questions"] button:hover,
    [class*="st-key-docs_examples"] button:hover,[class*="st-key-quick_modes"] button:hover {{
        background:var(--accent-soft)!important;border-color:var(--accent)!important;}}
    [class*="st-key-answer_actions"] button {{min-height:32px!important;padding:0 9px!important;
        background:transparent!important;color:var(--text-secondary)!important;
        border:1px solid transparent!important;font-size:.79rem;}}
    [class*="st-key-answer_actions"] button:hover {{background:var(--surface-soft)!important;
        color:var(--text)!important;}}

    /* Conversation, sources et résultats */
    [class*="st-key-conversation_turn_"] {{max-width:900px;padding-top:1.35rem;}}
    [class*="st-key-conversation_turn_"] [data-testid="stMarkdownContainer"] p,
    [class*="st-key-conversation_turn_"] [data-testid="stMarkdownContainer"] li {{line-height:1.7;}}
    [class*="st-key-conversation_turn_"] [data-testid="stDivider"] {{opacity:.35;}}
    [class*="st-key-source_card_"] {{margin:.4rem 0;padding:.8rem 0;
        border-bottom:1px solid var(--border);}}
    [class*="st-key-source_card_"] .stButton>button,
    [class*="st-key-source_card_"] .stLinkButton>a {{min-height:32px;padding:0 10px;font-size:.78rem;}}
    [data-testid="stExpander"],[data-testid="stExpander"] details,
    [data-testid="stPopoverBody"],[data-testid="stTable"] {{
        background:var(--surface)!important;border-color:var(--border)!important;color:var(--text)!important;}}
    [data-testid="stExpander"] summary {{background:var(--surface-soft)!important;
        color:var(--text)!important;border-radius:10px;}}
    [data-testid="stExpander"] summary * {{color:var(--text)!important;fill:var(--text)!important;}}
    [data-testid="stExpander"] summary:hover {{background:var(--surface-hover)!important;}}
    [data-testid="stTable"] th,[data-testid="stTable"] td {{background:var(--surface)!important;
        color:var(--text)!important;border-color:var(--border)!important;}}

    /* Composer */
    [data-testid="stBottomBlockContainer"] {{padding:.65rem 1rem 1rem!important;
        background:linear-gradient(180deg,transparent,var(--app-bg) 30%)!important;}}
    [data-testid="stBottomBlockContainer"]>[data-testid="stVerticalBlock"],
    [data-testid="stBottomBlockContainer"]>div {{width:100%!important;max-width:900px!important;
        margin-left:auto!important;margin-right:auto!important;}}
    [class*="st-key-composer_shell"] {{width:100%!important;max-width:900px!important;min-height:94px;
        max-height:130px;margin:0 auto!important;padding:.55rem .75rem .6rem;background:var(--surface);
        border:1px solid var(--border);border-radius:20px;box-shadow:var(--shadow);
        box-sizing:border-box;transition:border-color .15s ease,box-shadow .15s ease;}}
    [class*="st-key-composer_shell"]:focus-within {{border-color:var(--accent);
        box-shadow:0 0 0 3px rgba(79,124,255,.12);}}
    [class*="st-key-composer_shell"] [data-testid="stForm"] {{border:0;padding:0;}}
    [class*="st-key-composer_shell"] [data-testid="stTextInputRootElement"] {{
        background:var(--input-bg)!important;border:1px solid var(--border)!important;}}
    [class*="st-key-composer_shell"] [data-testid="stTextInputField"],
    [class*="st-key-composer_shell"] [data-testid="stTextInput"] input {{min-height:44px;
        background:transparent!important;border:0!important;box-shadow:none!important;
        color:var(--text)!important;-webkit-text-fill-color:var(--text)!important;padding-left:.35rem;}}
    [class*="st-key-composer_shell"] [data-testid="stTextInputField"]::placeholder,
    [class*="st-key-composer_shell"] input::placeholder {{
        color:var(--placeholder)!important;-webkit-text-fill-color:var(--placeholder)!important;
        opacity:1!important;}}
    [class*="st-key-composer_shell"] .stFormSubmitButton>button {{width:40px;min-width:40px;
        max-width:40px;height:40px;min-height:40px;padding:0!important;}}
    [class*="st-key-composer_shortcuts"]>[data-testid="stVerticalBlock"] {{flex-direction:row;
        align-items:center;gap:.45rem;margin-top:.15rem;}}
    [class*="st-key-composer_shortcuts"] [data-testid="stPopover"]>button {{width:34px;
        min-width:34px;height:30px;min-height:30px;padding:0!important;background:transparent!important;
        border-color:transparent!important;}}
    [class*="st-key-composer_shortcuts"] [data-testid="stMarkdownContainer"] {{display:flex;gap:.4rem;}}
    .composer-chip {{display:inline-flex;align-items:center;min-height:26px;padding:0 9px;
        margin-right:.35rem;border:1px solid var(--border);border-radius:999px;
        background:var(--surface-soft);color:var(--text-secondary);font-size:.72rem;}}

    /* Settings, éditeurs, upload et code */
    [class*="st-key-settings_panel"] {{max-width:720px;}}
    [class*="st-key-settings_panel"] h3 {{margin-top:1.5rem;font-size:1.05rem;}}
    [class*="st-key-settings_panel"] [data-testid="stSelectbox"] {{max-width:520px;}}
    [class*="st-key-setting_row_"] {{max-width:620px;padding:.65rem 0;border-top:1px solid var(--border);}}
    [class*="st-key-upload_zone"] {{padding:1.2rem 1.4rem;background:var(--surface-soft);
        border:1px dashed var(--border-hover)!important;border-radius:18px;}}
    [data-testid="stFileUploaderDropzone"] {{min-height:8.5rem;background:var(--surface)!important;
        border-color:var(--border)!important;}}
    [data-testid="stFileUploaderDropzone"] * {{color:var(--text-secondary)!important;}}
    [data-testid="stFileUploaderDropzoneInstructions"] small {{display:none;}}
    [data-testid="stFileUploaderDropzone"] button {{background:var(--surface-soft)!important;
        color:var(--text)!important;border-color:var(--border)!important;}}
    [data-testid="stFileUploaderDropzone"] button * {{color:var(--text)!important;
        fill:var(--text)!important;}}
    [data-testid="stCode"] {{border:1px solid var(--border);max-width:100%;overflow-x:auto;}}
    [data-testid="stCode"] pre,[data-testid="stCode"] code {{background:var(--surface-soft)!important;}}
    [data-testid="stAlert"] {{border-radius:12px;}}
    [data-testid="stToggle"] * {{color:var(--text)!important;}}

    @media (max-width:900px) {{
        [class*="st-key-main_surface"] {{min-height:54vh;}}
        [class*="st-key-topbar"] [data-testid="column"]:first-child {{display:none;}}
    }}
    @media (max-width:640px) {{
        div[data-testid="stMainBlockContainer"] {{padding:.75rem .6rem 9rem;}}
        [class*="st-key-main_surface"] {{padding:1.2rem;min-height:50vh;border-radius:18px;}}
        [class*="st-key-topbar"] [data-testid="stHorizontalBlock"] {{flex-wrap:wrap;gap:.2rem;}}
        [class*="st-key-topbar"] [data-testid="column"] {{min-width:fit-content!important;
            width:auto!important;flex:0 1 auto!important;}}
        [class*="st-key-topbar"] [data-testid="column"]:nth-child(5) {{display:none;}}
        [class*="st-key-answer_actions"] [data-testid="stHorizontalBlock"] {{flex-wrap:wrap;gap:.25rem;}}
        [class*="st-key-answer_actions"] [data-testid="column"] {{min-width:calc(50% - .4rem);}}
        [class*="st-key-composer_shell"] {{border-radius:16px;padding:.45rem .55rem;}}
        [data-testid="stBottomBlockContainer"] {{padding:.5rem .55rem .7rem!important;}}
        .app-title {{font-size:2rem;}}.app-intro {{margin-bottom:1.2rem;}}
        .composer-chip {{padding:0 7px;margin-right:.2rem;font-size:.67rem;}}
        [class*="st-key-login_page"] {{margin-top:1.25rem;}}
        [class*="st-key-login_card"] {{padding:1.35rem;border-radius:18px;}}
    }}
    </style>
    """, unsafe_allow_html=True)
