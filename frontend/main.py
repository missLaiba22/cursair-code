import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

DEFAULT_BACKEND_URL = "https://codesparkai.onrender.com"


def resolve_backend_url() -> str:
    if os.environ.get("BACKEND_URL"):
        return os.environ["BACKEND_URL"]
    try:
        return st.secrets["BACKEND_URL"]
    except Exception:
        return DEFAULT_BACKEND_URL


BACKEND_URL = resolve_backend_url().rstrip("/")

st.set_page_config(
    page_title="CodeSpark AI — Your AI Pair Programmer",
    page_icon="⚡",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f6f5fb 0%, #f1f0fa 100%);
    }

    /* ---- Sidebar: same violet family as the hero/buttons ---- */
    [data-testid="stSidebar"] {
        background: linear-gradient(195deg, #2c1a63 0%, #4c1d78 55%, #6b21a8 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebar"] * { color: #ede9fe !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }

    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 10px;
    }
    [data-testid="stSidebar"] input {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 7px !important;
    }

    .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1120px; }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ---- Hero ---- */
    .hero {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #c026d3 100%);
        padding: 2.5rem 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 12px 30px -10px rgba(124, 58, 237, 0.55);
        animation: fadeInUp 0.5s ease-out;
    }
    .hero h1 { font-size: 2.4rem; font-weight: 800; margin-bottom: 0.4rem; color: white; }
    .hero p.tagline { font-size: 1.15rem; font-weight: 400; opacity: 0.95; margin-bottom: 0; }
    .badge-row { margin-top: 1rem; }
    .badge {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.35);
        color: white;
        padding: 0.28rem 0.8rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.4rem;
    }

    /* ---- Feature cards: fixed min-height so all rows line up ---- */
    .feature-card {
        background: #ffffff;
        border: 1px solid #ece9fb;
        border-radius: 16px;
        padding: 1.15rem 1.2rem;
        min-height: 185px;
        display: flex;
        flex-direction: column;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        animation: fadeInUp 0.6s ease-out both;
        box-shadow: 0 2px 6px rgba(31, 25, 90, 0.05);
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 14px 28px -10px rgba(76, 29, 149, 0.25);
    }
    .feature-card .icon-chip {
        width: 38px; height: 38px;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem;
        margin-bottom: 0.6rem;
        flex-shrink: 0;
    }
    .feature-card h4 { margin: 0 0 0.35rem 0; font-size: 1rem; color: #1e1b3a; }
    .feature-card p { margin: 0; font-size: 0.85rem; color: #625f7a; line-height: 1.4; }

    .chip-violet { background: #ede9fe; color: #6d28d9; }
    .chip-amber  { background: #fef3c7; color: #b45309; }
    .chip-sky    { background: #e0f2fe; color: #0369a1; }
    .chip-rose   { background: #ffe4e6; color: #be123c; }
    .chip-emerald{ background: #d1fae5; color: #047857; }

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
    }
    .stTabs [aria-selected="true"] { color: #6d28d9 !important; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #7c3aed !important; }

    /* ---- Buttons ---- */
    .stButton>button {
        border-radius: 9px;
        font-weight: 600;
        padding: 0.5rem 1.3rem;
        border: none;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px -6px rgba(124, 58, 237, 0.55);
        color: white;
    }

    /* ---- Select boxes (e.g. Language) - tinted instead of white ---- */
    div[data-baseweb="select"] > div {
        background-color: #f3f0fd !important;
        border: 1.5px solid #c4b5fd !important;
        border-radius: 9px !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #a78bfa !important;
    }
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #ece9fb !important;
    }
    li[role="option"]:hover {
        background-color: #ede9fe !important;
    }

    /* ---- Text areas: subtle tint so they match the theme too ---- */
    .stTextArea textarea {
        background-color: #faf9ff !important;
        border: 1.5px solid #e6e1fa !important;
        border-radius: 9px !important;
    }
    .stTextArea textarea:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 1px #a78bfa !important;
    }

    /* ---- Output cards (bordered containers) ---- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        border: 1px solid #e6e3f7 !important;
        box-shadow: 0 4px 14px rgba(76, 29, 149, 0.08);
        animation: fadeInUp 0.35s ease-out;
    }
    .section-title {
        font-weight: 700;
        color: #1e1b3a;
        font-size: 0.95rem;
        margin-bottom: 0.4rem;
        display: flex; align-items: center; gap: 0.4rem;
    }

    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Hero section
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>⚡ CodeSpark AI</h1>
        <p class="tagline">Your AI pair programmer — generate, optimize, debug, and
        understand code in seconds, right from your browser.</p>
        <div class="badge-row">
            <span class="badge">🐍 FastAPI</span>
            <span class="badge">✨ Gemini 2.5</span>
            <span class="badge">🎈 Streamlit</span>
            <span class="badge">⚡ Real-time</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Feature highlights
# ---------------------------------------------------------------------------
feat_cols = st.columns(5)
features = [
    ("✨", "Generate", "Turn plain English into working code in any language.", "chip-violet"),
    ("⚡", "Optimize", "Get cleaner, faster versions of code you already have.", "chip-amber"),
    ("📖", "Explain", "Understand unfamiliar code in plain language.", "chip-sky"),
    ("🐛", "Debug", "Spot issues and get a fixed version instantly.", "chip-rose"),
    ("✅", "Test", "Auto-generate unit tests for your functions.", "chip-emerald"),
]
for i, (col, (icon, title, desc, chip_class)) in enumerate(zip(feat_cols, features)):
    with col:
        st.markdown(
            f"""
            <div class="feature-card" style="animation-delay:{i * 0.08}s">
                <div class="icon-chip {chip_class}">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")


# ---------------------------------------------------------------------------
# Backend helper
# ---------------------------------------------------------------------------
def api_call(endpoint: str, data: dict):
    try:
        response = requests.post(f"{BACKEND_URL}/{endpoint}", json=data, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(
            f"Couldn't reach the backend at `{BACKEND_URL}`. "
            "Make sure the FastAPI server is running and BACKEND_URL is set correctly."
        )
    except requests.exceptions.HTTPError as e:
        detail = ""
        try:
            detail = e.response.json().get("detail", "")
        except Exception:
            pass
        st.error(f"Backend returned an error: {detail or e}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling `{endpoint}`: {e}")
    return None


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ CodeSpark AI")
    st.caption("An AI pair programmer built with FastAPI + Gemini.")
    st.divider()
    with st.expander("⚙️ Settings"):
        st.text_input("Backend URL", value=BACKEND_URL, disabled=True)
        st.caption("Set via the `BACKEND_URL` environment variable / Streamlit secret.")
    st.divider()
    st.markdown(
        "**About this project**\n\n"
        "a FastAPI backend wrapping Google Gemini, paired with this "
        "Streamlit frontend."
    )

# ---------------------------------------------------------------------------
# Main tool tabs
# ---------------------------------------------------------------------------
tab_generate, tab_optimize, tab_explain, tab_debug, tab_test = st.tabs(
    ["✨ Generate", "⚡ Optimize", "📖 Explain", "🐛 Debug", "✅ Unit Tests"]
)

with tab_generate:
    st.subheader("Code Generator")
    prompt = st.text_area("Describe what you want the code to do", height=140, key="gen_prompt")
    language = st.selectbox("Language", ["python", "javascript", "typescript", "go", "java", "c++"])
    if st.button("Generate Code", type="primary", key="gen_btn"):
        if not prompt.strip():
            st.warning("Enter a prompt first.")
        else:
            with st.spinner("Generating..."):
                result = api_call("generate_code/", {"prompt": prompt, "language": language})
            if result:
                with st.container(border=True):
                    st.markdown('<div class="section-title">✨ Generated Code</div>', unsafe_allow_html=True)
                    st.code(result.get("code", ""), language=language)

with tab_optimize:
    st.subheader("Code Optimizer")
    code_to_optimize = st.text_area("Paste code to optimize", height=200, key="opt_code")
    if st.button("Optimize Code", type="primary", key="opt_btn"):
        if not code_to_optimize.strip():
            st.warning("Paste some code first.")
        else:
            with st.spinner("Optimizing..."):
                result = api_call("optimize_code/", {"code": code_to_optimize})
            if result:
                with st.container(border=True):
                    st.markdown('<div class="section-title">⚡ Optimized Code</div>', unsafe_allow_html=True)
                    st.code(result.get("optimized_code", ""), language="python")

with tab_explain:
    st.subheader("Code Explainer")
    code_to_explain = st.text_area("Paste code to explain", height=200, key="exp_code")
    if st.button("Explain Code", type="primary", key="exp_btn"):
        if not code_to_explain.strip():
            st.warning("Paste some code first.")
        else:
            with st.spinner("Explaining..."):
                result = api_call("explain_code/", {"code": code_to_explain})
            if result:
                with st.container(border=True):
                    st.markdown('<div class="section-title">📖 Explanation</div>', unsafe_allow_html=True)
                    st.write(result.get("explanation", ""))

with tab_debug:
    st.subheader("Debug Assistant")
    debug_code_input = st.text_area("Paste code to debug", height=200, key="debug_code")
    if st.button("Debug Code", type="primary", key="debug_btn"):
        if not debug_code_input.strip():
            st.warning("Paste some code first.")
        else:
            with st.spinner("Analyzing..."):
                result = api_call("debug_code/", {"code": debug_code_input})
            if result:
                text = result.get("result", "")
                issues_start = text.find("ISSUES:")
                suggestions_start = text.find("SUGGESTIONS:")
                updated_code_start = text.find("UPDATED CODE:")

                with st.container(border=True):
                    if issues_start != -1:
                        st.markdown('<div class="section-title">🔍 Issues Identified</div>', unsafe_allow_html=True)
                        st.write(text[issues_start:suggestions_start if suggestions_start != -1 else None])

                    if suggestions_start != -1:
                        st.markdown('<div class="section-title">💡 Suggestions</div>', unsafe_allow_html=True)
                        st.write(text[suggestions_start:updated_code_start if updated_code_start != -1 else None])

                    if updated_code_start != -1:
                        st.markdown('<div class="section-title">🐛 Updated Code</div>', unsafe_allow_html=True)
                        st.code(text[updated_code_start:], language="python")

                    if issues_start == -1 and suggestions_start == -1 and updated_code_start == -1:
                        st.write(text)

with tab_test:
    st.subheader("Unit Test Generator")
    test_code_input = st.text_area("Paste code you need unit tests for", height=200, key="test_code")
    if st.button("Generate Unit Tests", type="primary", key="test_btn"):
        if not test_code_input.strip():
            st.warning("Paste some code first.")
        else:
            with st.spinner("Writing tests..."):
                result = api_call("generate_unit_tests/", {"code": test_code_input})
            if result:
                with st.container(border=True):
                    st.markdown('<div class="section-title">✅ Unit Tests</div>', unsafe_allow_html=True)
                    st.code(result.get("unit_tests", ""), language="python")

st.divider()
st.caption("This is a demo project. Do not paste proprietary or sensitive code into the public deployment.")