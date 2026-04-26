import streamlit as st
import pandas as pd
import pickle
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Based Autism Prediction System",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #f0ede6 !important;
    color: #1a1a2e !important;
    font-family: 'Times New Roman', Times, serif !important;
}

[data-testid="stHeader"], footer, #MainMenu { display:none !important; }
[data-testid="stSidebar"] { display:none !important; }
[data-testid="stAppViewContainer"] > section:first-child { padding-top:0 !important; }
[data-testid="stMainBlockContainer"] { padding: 0 40px 60px !important; }

/* ---------- TOPBAR ---------- */
.topbar {
    width: 100%;
    background: #12122a;
    padding: 0 52px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 16px rgba(0,0,0,0.25);
    position: relative;
    z-index: 200;
}
.topbar-brand {
    font-family: 'Times New Roman', Times, serif;
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.8px;
}
.topbar-right {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    letter-spacing: 1.8px;
    text-transform: uppercase;
}

/* ---------- STEP PROGRESS BAR ---------- */
.prog-bar {
    background: #ffffff;
    border-bottom: 1px solid #e4e0d8;
    padding: 20px 0 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    margin-bottom: 0;
}
.steps-row {
    display: flex;
    align-items: flex-start;
    justify-content: center;
}
.s-col { display: flex; flex-direction: column; align-items: center; }
.s-node {
    width: 38px; height: 38px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Times New Roman', Times, serif;
    font-size: 15px; font-weight: 700;
    border: 2px solid #d1d5db;
    color: #9ca3af;
    background: #fff;
    transition: all 0.3s;
}
.s-node.done   { background: #7c3aed; border-color: #7c3aed; color: #fff; }
.s-node.active { background: #fff; border-color: #7c3aed; color: #7c3aed; box-shadow: 0 0 0 5px rgba(124,58,237,0.1); }
.s-line { width: 110px; height: 2px; background: #e2e8f0; margin-top: 18px; }
.s-line.done { background: #7c3aed; }
.s-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 10.5px; color: #9ca3af;
    margin-top: 8px; letter-spacing: 0.8px;
    text-transform: uppercase;
}
.s-lbl.done   { color: #7c3aed; }
.s-lbl.active { color: #7c3aed; font-weight: 600; }

/* ---------- FORM SECTION HEADER ---------- */
.fsec {
    text-align: center;
    padding: 48px 0 32px;
}
.fsec h2 {
    font-family: 'Times New Roman', Times, serif;
    font-size: clamp(26px, 3.5vw, 40px);
    font-weight: 700;
    color: #12122a;
    margin-bottom: 8px;
}
.fsec p {
    font-family: 'Inter', sans-serif;
    color: #64748b; font-size: 14px;
}

/* ---------- FORM CARD ---------- */
.fc {
    background: #ffffff;
    border: 1px solid #e4e0d8;
    border-radius: 20px;
    padding: 36px 32px 28px;
    margin-bottom: 22px;
    box-shadow: 0 4px 22px rgba(0,0,0,0.05);
    position: relative;
    overflow: hidden;
}
.fc::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
}
.fc-title {
    font-family: 'Times New Roman', Times, serif;
    font-size: 21px; font-weight: 700;
    color: #12122a; margin-bottom: 4px;
}
.fc-sub {
    font-family: 'Inter', sans-serif;
    font-size: 12.5px; color: #94a3b8;
    margin-bottom: 26px;
}

/* ---------- HOW-IT-WORKS ---------- */
.hiw-wrap {
    padding: 60px 0 52px;
    text-align: center;
    background: #f0ede6;
}
.hiw-label {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 12px;
}
.hiw-title {
    font-family: 'Times New Roman', Times, serif;
    font-size: clamp(26px, 3.5vw, 42px);
    font-weight: 700;
    color: #12122a;
    margin-bottom: 8px;
}
.hiw-sub {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    color: #64748b;
    margin-bottom: 44px;
}
.hiw-grid {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 22px;
    margin-bottom: 52px;
}
.hiw-card {
    background: #ffffff;
    border: 1px solid #e4e0d8;
    border-radius: 20px;
    padding: 40px 28px 32px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    transition: transform 0.25s, box-shadow 0.25s;
    text-align: center;
}
.hiw-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 36px rgba(124,58,237,0.12);
}
.hiw-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
}
.hiw-num {
    font-family: 'Times New Roman', Times, serif;
    font-size: 64px;
    font-weight: 700;
    color: #7c3aed;
    line-height: 1;
    margin-bottom: 18px;
}
.hiw-card-title {
    font-family: 'Times New Roman', Times, serif;
    font-size: 20px;
    font-weight: 700;
    color: #12122a;
    margin-bottom: 10px;
}
.hiw-card-desc {
    font-family: 'Inter', sans-serif;
    font-size: 13.5px;
    color: #374151;
    line-height: 1.7;
}

/* ---------- BEHAVIOUR CARD ---------- */
.bc {
    background: #faf9f6;
    border: 1.5px solid #e4e0d8;
    border-radius: 14px;
    padding: 16px 18px 10px;
    margin-bottom: 4px;
    transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}
.bc:hover {
    border-color: #c4b5fd;
    box-shadow: 0 4px 16px rgba(124,58,237,0.09);
    background: #fff;
}
.bc-num {
    font-family: 'Inter', sans-serif;
    font-size: 9.5px; color: #7c3aed;
    letter-spacing: 2.5px; margin-bottom: 6px;
    font-weight: 700; text-transform: uppercase;
}
.bc-q {
    font-family: 'Times New Roman', Times, serif;
    font-size: 14.5px; color: #2d3748; line-height: 1.55;
}

/* ---------- RESULT ---------- */
.res-wrap { text-align: center; padding: 68px 24px 48px; }
.res-badge {
    display: inline-block;
    padding: 10px 30px; border-radius: 100px;
    font-family: 'Inter', sans-serif;
    font-size: 11.5px; font-weight: 700;
    letter-spacing: 2.5px; text-transform: uppercase;
    margin-bottom: 28px;
}
.res-badge.pos { background:#fef2f2; color:#dc2626; border:1.5px solid #fca5a5; }
.res-badge.neg { background:#f0fdf4; color:#16a34a; border:1.5px solid #86efac; }
.res-badge.med { background:#fffbeb; color:#d97706; border:1.5px solid #fcd34d; }
.res-main {
    font-family: 'Times New Roman', Times, serif;
    font-size: clamp(30px, 5vw, 52px);
    font-weight: 700; margin-bottom: 18px; line-height: 1.18;
}
.res-main.pos { color: #dc2626; }
.res-main.neg { color: #16a34a; }
.res-main.med { color: #d97706; }
.res-desc {
    font-family: 'Inter', sans-serif;
    color: #64748b; font-size: 15px;
    max-width: 560px; margin: 0 auto 32px; line-height: 1.78;
}

/* ---------- RISK LEVEL PILL ---------- */
.risk-pill {
    display: inline-block;
    padding: 6px 24px;
    border-radius: 100px;
    font-family: 'Inter', sans-serif;
    font-size: 13px; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: 36px;
}
.risk-pill.high   { background: #fef2f2; color: #dc2626; border: 1.5px solid #fca5a5; }
.risk-pill.medium { background: #fffbeb; color: #d97706; border: 1.5px solid #fcd34d; }
.risk-pill.low    { background: #f0fdf4; color: #16a34a; border: 1.5px solid #86efac; }

/* confidence */
.cw { max-width: 440px; margin: 0 auto 36px; }
.cw-row {
    display: flex; justify-content: space-between;
    font-family: 'Inter', sans-serif;
    font-size: 13px; color: #64748b; margin-bottom: 10px;
}
.cw-track { height: 10px; background: #e2e8f0; border-radius: 100px; overflow: hidden; }
.cw-fill  { height: 100%; border-radius: 100px; transition: width 0.8s ease; }
.cw-fill.hi  { background: linear-gradient(90deg, #ef4444, #f97316); }
.cw-fill.med { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.cw-fill.lo  { background: linear-gradient(90deg, #22c55e, #4ade80); }

/* stats row */
.stats-row {
    display: flex; justify-content: center; gap: 32px;
    margin-bottom: 40px;
}
.stat-box {
    background: #fff;
    border: 1px solid #e4e0d8;
    border-radius: 14px;
    padding: 16px 28px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    min-width: 130px;
}
.stat-val {
    font-family: 'Times New Roman', Times, serif;
    font-size: 28px; font-weight: 700; color: #12122a;
}
.stat-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 11px; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 1px;
    margin-top: 4px;
}

/* disclaimer */
.disc {
    background: #f5f3ff;
    border: 1px solid #ddd6fe;
    border-left: 4px solid #7c3aed;
    border-radius: 10px;
    padding: 16px 22px;
    font-family: 'Inter', sans-serif;
    font-size: 13px; color: #4c1d95;
    max-width: 640px; margin: 0 auto;
    line-height: 1.7; text-align: left;
}

/* ---------- WIDGET OVERRIDES ---------- */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stRadio"] label {
    font-family: 'Times New Roman', Times, serif !important;
    color: #2d3748 !important; font-size: 15px !important; font-weight: 700 !important;
}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
}
div[data-testid="stButton"] > button {
    font-family: 'Times New Roman', Times, serif !important;
    font-size: 16px !important; font-weight: 700 !important;
    border-radius: 10px !important; transition: all 0.2s !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
    border: none !important;
    box-shadow: 0 6px 24px rgba(124,58,237,0.4) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(124,58,237,0.5) !important;
}
div[data-testid="stSpinner"] > div { border-top-color: #7c3aed !important; }
</style>
""", unsafe_allow_html=True)

# ── LOAD MODEL ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    try:
        m = pickle.load(open(os.path.join(BASE_DIR, "best_model.pkl"), "rb"))
        e = pickle.load(open(os.path.join(BASE_DIR, "encoders.pkl"),   "rb"))
        return m, e
    except Exception as ex:
        st.error(f"Could not load model files: {ex}")
        return None, None

model, encoders = load_artifacts()

# ── BEHAVIOUR QUESTIONS ───────────────────────────────────────────────────────
B_QUESTIONS = [
    ("Eye Contact",          "Does the person avoid eye contact or seem disinterested in faces?"),
    ("Routine Rigidity",     "Does the person prefer strict routines and get upset with small changes?"),
    ("Sensory Sensitivity",  "Does the person show strong sensitivity to sounds, lights, or textures?"),
    ("Social Cues",          "Does the person have difficulty understanding gestures or facial expressions?"),
    ("Repetitive Behaviour", "Does the person display repetitive movements like hand-flapping or rocking?"),
    ("Communication",        "Does the person have noticeable delays or difficulties in speech?"),
    ("Social Withdrawal",    "Does the person avoid social interactions or prefer to be alone?"),
    ("Limited Interests",    "Does the person have limited interests or play repetitively with the same objects?"),
    ("Unusual Postures",     "Does the person show unusual body movements or postures?"),
    ("Sensory-Seeking",      "Does the person show sensory-seeking or sensory-avoiding behaviours?"),
]

# ── RISK LEVEL HELPER ─────────────────────────────────────────────────────────
def get_risk(pred, conf):
    """Return (label, css_class) based on prediction and confidence."""
    if pred == 1:
        if conf >= 75:
            return "High Risk", "high"
        else:
            return "Moderate Risk", "medium"
    else:
        if conf >= 75:
            return "Low Risk", "low"
        else:
            return "Borderline", "medium"

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in {"page": "home", "personal": {}, "result": None, "conf": None, "score": None}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go(p):
    st.session_state.page = p
    st.rerun()

# ── TOP NAV (inner pages only) ───────────────────────────────────────────────
if st.session_state.page != "home":
    st.markdown("""
    <div class="topbar">
        <div class="topbar-brand">AI Based Autism Prediction System</div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  HOME
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":

    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"],
    [data-testid="stMainBlockContainer"],
    section.main, .block-container {
        background: #0d0b26 !important;
        padding-bottom: 0 !important;
    }
    .hero-home {
        min-height: 88vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0 8vw 60px;
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(ellipse 80% 60% at 15% 40%, rgba(124,58,237,0.22) 0%, transparent 55%),
            radial-gradient(ellipse 60% 70% at 85% 25%, rgba(6,182,212,0.18) 0%, transparent 55%),
            radial-gradient(ellipse 55% 55% at 50% 95%, rgba(99,102,241,0.14) 0%, transparent 50%),
            linear-gradient(155deg, #0d0b26 0%, #161438 40%, #1e1b4b 75%, #0d0b26 100%);
    }
    .hero-home::before {
        content:''; position:absolute;
        width:600px; height:600px; border-radius:50%;
        border:1px solid rgba(124,58,237,0.13);
        top:-160px; left:-160px;
        animation: ringspin 35s linear infinite; pointer-events:none;
    }
    .hero-home::after {
        content:''; position:absolute;
        width:420px; height:420px; border-radius:50%;
        border:1px solid rgba(6,182,212,0.10);
        bottom:-100px; right:-100px;
        animation: ringspin 25s linear infinite reverse; pointer-events:none;
    }
    @keyframes ringspin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
    .hero-glow2 {
        position:absolute; width:360px; height:360px; border-radius:50%;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
        top:50%; left:50%; transform:translate(-50%,-50%); pointer-events:none;
    }
    .h-tag {
        font-family: 'Inter', sans-serif;
        font-size: 10.5px; letter-spacing: 5px;
        text-transform: uppercase; color: #a78bfa;
        margin-bottom: 22px; position: relative;
    }
    .h-title {
        font-family: 'Times New Roman', Times, serif;
        font-size: clamp(40px, 6.5vw, 82px); font-weight: 700;
        color: #ffffff; line-height: 1.1; margin-bottom: 28px;
        position: relative; text-shadow: 0 4px 40px rgba(0,0,0,0.45);
        letter-spacing: -0.5px;
    }
    .h-title em { color: #a78bfa; font-style: italic; }
    .h-divider {
        width:56px; height:2px;
        background: linear-gradient(90deg, #7c3aed, #06b6d4);
        border-radius:2px; margin: 0 auto 24px; position:relative;
    }
    .h-slogan {
        font-family: 'Times New Roman', Times, serif;
        font-size: 16px; font-style: italic;
        color: rgba(255,255,255,0.65); margin-bottom: 40px;
        height: 28px; letter-spacing: 0.3px;
        position: relative; overflow: hidden;
        width: 100%; text-align: center;
    }
    .slogan-line {
        display: block; overflow: hidden; white-space: nowrap;
        width: 0; position: absolute; left: 50%; transform: translateX(-50%);
        animation: typeloop 20s steps(45, end) infinite;
    }
    .slogan-line:nth-child(1) { animation-delay: 0s; }
    .slogan-line:nth-child(2) { animation-delay: 5s; }
    .slogan-line:nth-child(3) { animation-delay: 10s; }
    .slogan-line:nth-child(4) { animation-delay: 15s; }
    @keyframes typeloop {
        0%   { width:0; opacity:1; }
        18%  { width:100%; opacity:1; }
        22%  { width:100%; opacity:1; }
        25%  { width:100%; opacity:0; }
        100% { width:0; opacity:0; }
    }
    .h-cursor { display:inline-block; color:#a78bfa; font-style:normal; animation: cblink 0.85s step-end infinite; }
    @keyframes cblink { 0%,100%{opacity:1} 50%{opacity:0} }
    .home-stats {
        display: flex; gap: 40px; justify-content: center;
        margin-top: 48px; position: relative;
    }
    .home-stat {
        text-align: center;
    }
    .home-stat-val {
        font-family: 'Times New Roman', Times, serif;
        font-size: 28px; font-weight: 700; color: #ffffff;
    }
    .home-stat-lbl {
        font-family: 'Inter', sans-serif;
        font-size: 10px; color: rgba(255,255,255,0.75);
        text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px;
    }
    [data-testid="stMainBlockContainer"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        background: #0d0b26 !important;
    }
    div.home-btn-wrap {
        background: #0d0b26 !important;
        display: flex; flex-direction: column; align-items: center;
        justify-content: center;
        padding: 30px 0 60px; margin-top: -2px;
        width: 100%;
    }
    div.home-btn-wrap [data-testid="stButton"] {
        display: flex; justify-content: center;
    }
    div.home-btn-wrap [data-testid="stButton"] > button {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 18px !important; font-weight: 700 !important;
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        color: #fff !important; border: none !important;
        border-radius: 12px !important; padding: 16px 56px !important;
        box-shadow: 0 8px 32px rgba(124,58,237,0.45) !important;
        min-width: 220px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-home">
        <div class="hero-glow2"></div>
        <div class="h-title">
            AI Based Autism<br><em>Prediction System</em>
        </div>
        <div class="h-divider"></div>
        <div class="h-slogan">
            <span class="slogan-line">Empowering early awareness through AI<span class="h-cursor">|</span></span>
            <span class="slogan-line">Predict. Understand. Act early<span class="h-cursor">|</span></span>
            <span class="slogan-line">Intelligent screening in under 5 minutes<span class="h-cursor">|</span></span>
            <span class="slogan-line">Because early detection changes everything<span class="h-cursor">|</span></span>
        </div>
        <div class="home-stats">
            <div class="home-stat">
                <div class="home-stat-val">10</div>
                <div class="home-stat-lbl">Behavioural Indicators</div>
            </div>
            <div class="home-stat">
                <div class="home-stat-val">3</div>
                <div class="home-stat-lbl">Simple Steps</div>
            </div>
            <div class="home-stat">
                <div class="home-stat-val">ML</div>
                <div class="home-stat-lbl">Powered Model</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="home-btn-wrap">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Get Started  →", type="primary", key="home_btn", use_container_width=True):
            go("personal")
    st.markdown('</div>', unsafe_allow_html=True)

    # How It Works section
    st.markdown("""
    <div class="hiw-wrap">
        <div class="hiw-label">Process</div>
        <div class="hiw-title">How It Works</div>
        <div class="hiw-sub">Three simple steps to get your screening result</div>
        <div class="hiw-grid">
            <div class="hiw-card">
                <div class="hiw-num">01</div>
                <div class="hiw-card-title">Personal Details</div>
                <div class="hiw-card-desc">Enter basic demographic information including age, gender, ethnicity, and medical background of the individual.</div>
            </div>
            <div class="hiw-card">
                <div class="hiw-num">02</div>
                <div class="hiw-card-title">Behavioural Questions</div>
                <div class="hiw-card-desc">Answer 10 evidence-based behavioural indicator questions covering communication, social, and sensory patterns.</div>
            </div>
            <div class="hiw-card">
                <div class="hiw-num">03</div>
                <div class="hiw-card-title">AI Result</div>
                <div class="hiw-card-desc">Receive an instant prediction with risk level (Low / Moderate / High) and model confidence percentage.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  PERSONAL INFO
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "personal":

    st.markdown("""
    <div class="prog-bar">
        <div class="steps-row">
            <div class="s-col">
                <div class="s-node active">1</div>
                <div class="s-lbl active">Personal</div>
            </div>
            <div class="s-line"></div>
            <div class="s-col">
                <div class="s-node">2</div>
                <div class="s-lbl">Behaviour</div>
            </div>
            <div class="s-line"></div>
            <div class="s-col">
                <div class="s-node">3</div>
                <div class="s-lbl">Result</div>
            </div>
        </div>
    </div>
    <div class="fsec">
        <h2>Personal Details</h2>
        <p>Step 1 of 2 — Information about the individual being assessed</p>
    </div>
    """, unsafe_allow_html=True)

    if not encoders:
        st.error("Model files not found. Place best_model.pkl and encoders.pkl in the same folder.")
        st.stop()

    st.markdown('<div class="fc"><div class="fc-title">Basic Information</div><div class="fc-sub">Demographic details of the individual being screened</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        age    = st.number_input("Age (years)", min_value=0, max_value=100, value=20, step=1)
        eth    = st.selectbox("Ethnicity", options=list(encoders["ethnicity"].classes_))
    with col_b:
        gender  = st.selectbox("Gender", options=list(encoders["gender"].classes_),
                               format_func=lambda x: "Male" if x == "m" else "Female")
        country = st.selectbox("Country of Residence", options=list(encoders["contry_of_res"].classes_))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fc"><div class="fc-title">Medical & Background</div><div class="fc-sub">Additional context that improves prediction accuracy</div>', unsafe_allow_html=True)
    col_c, col_d = st.columns(2)
    with col_c:
        jaundice   = st.radio("Born with Jaundice?",        options=["no", "yes"], horizontal=True, format_func=str.capitalize)
        fam_autism = st.radio("Family member with Autism?", options=["no", "yes"], horizontal=True, format_func=str.capitalize)
    with col_d:
        used_app = st.radio("Used a screening app before?", options=["no", "yes"], horizontal=True, format_func=str.capitalize)
        relation = st.selectbox("Who is completing this form?", options=list(encoders["relation"].classes_))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    btn_back, _, btn_next = st.columns([1, 3, 2])
    with btn_back:
        if st.button("← Back", type="secondary", use_container_width=True):
            go("home")
    with btn_next:
        if st.button("Continue to Behaviour Questions →", type="primary", use_container_width=True):
            st.session_state.personal = {
                "age": age, "gender": gender, "ethnicity": eth,
                "jaundice": jaundice, "austim": fam_autism,
                "contry_of_res": country, "used_app_before": used_app,
                "relation": relation,
            }
            go("behaviour")


# ════════════════════════════════════════════════════════════════════════════
#  BEHAVIOUR
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "behaviour":

    st.markdown("""
    <div class="prog-bar">
        <div class="steps-row">
            <div class="s-col">
                <div class="s-node done">1</div>
                <div class="s-lbl done">Personal</div>
            </div>
            <div class="s-line done"></div>
            <div class="s-col">
                <div class="s-node active">2</div>
                <div class="s-lbl active">Behaviour</div>
            </div>
            <div class="s-line"></div>
            <div class="s-col">
                <div class="s-node">3</div>
                <div class="s-lbl">Result</div>
            </div>
        </div>
    </div>
    <div class="fsec">
        <h2>Behavioural Indicators</h2>
        <p>Step 2 of 2 — Answer honestly based on observed behaviour of the individual</p>
    </div>
    """, unsafe_allow_html=True)

    answers = {}
    lc, rc  = st.columns(2)
    for i, (label, question) in enumerate(B_QUESTIONS):
        with (lc if i % 2 == 0 else rc):
            st.markdown(f"""
            <div class="bc">
                <div class="bc-num">Q{i+1:02d} &nbsp;·&nbsp; {label.upper()}</div>
                <div class="bc-q">{question}</div>
            </div>
            """, unsafe_allow_html=True)
            val = st.radio("", options=["No", "Yes"], key=f"bq{i}",
                           horizontal=True, label_visibility="collapsed")
            answers[f"A{i+1}_Score"] = 1 if val == "Yes" else 0
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    auto_score   = sum(answers.values())
    result_score = st.number_input(
        f"Behavioural Score — auto-calculated: {auto_score}/10 (override if needed)",
        min_value=0, max_value=10, value=auto_score, step=1
    )

    st.markdown("<br>", unsafe_allow_html=True)
    b1, _, b2 = st.columns([1, 3, 2])
    with b1:
        if st.button("← Back", type="secondary", use_container_width=True):
            go("personal")
    with b2:
        if st.button("Run Prediction →", type="primary", use_container_width=True):
            if not st.session_state.personal:
                st.error("Personal information missing. Please go back to Step 1.")
            else:
                with st.spinner("Analysing responses and running AI model..."):
                    time.sleep(1.2)
                p = st.session_state.personal
                try:
                    inp = {
                        **{f"A{i+1}_Score": answers[f"A{i+1}_Score"] for i in range(10)},
                        "age":             float(p.get("age", 0)),
                        "gender":          encoders["gender"].transform([p["gender"]])[0],
                        "ethnicity":       encoders["ethnicity"].transform([p["ethnicity"]])[0],
                        "jaundice":        encoders["jaundice"].transform([p["jaundice"]])[0],
                        "austim":          encoders["austim"].transform([p["austim"]])[0],
                        "contry_of_res":   encoders["contry_of_res"].transform([p["contry_of_res"]])[0],
                        "used_app_before": encoders["used_app_before"].transform([p["used_app_before"]])[0],
                        "result":          float(result_score),
                        "relation":        encoders["relation"].transform([p["relation"]])[0],
                    }
                    df_inp = pd.DataFrame([inp])
                    pred   = model.predict(df_inp)[0]
                    proba  = model.predict_proba(df_inp)[0][1]
                    st.session_state.result = int(pred)
                    st.session_state.conf   = round(float(proba) * 100, 1)
                    st.session_state.score  = result_score
                    go("result")
                except Exception as e:
                    st.error(f"Prediction error: {e}")


# ════════════════════════════════════════════════════════════════════════════
#  RESULT
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "result":

    pred  = st.session_state.result
    conf  = st.session_state.conf
    score = st.session_state.score

    if pred is None:
        go("personal")

    risk_label, risk_cls = get_risk(pred, conf)
    is_pos = (pred == 1)

    # Choose confidence fill class
    if conf >= 75 and is_pos:
        fill_cls = "hi"
    elif conf >= 75 and not is_pos:
        fill_cls = "lo"
    else:
        fill_cls = "med"

    desc = (
        "The screening suggests a <strong>higher probability</strong> of Autism Spectrum Disorder. "
        "This is <em>not</em> a diagnosis — please consult a qualified healthcare professional for a complete evaluation."
        if is_pos else
        "The screening suggests a <strong>lower probability</strong> of Autism Spectrum Disorder. "
        "Continue observing development and consult a professional if any concerns persist."
    )

    st.markdown("""
    <div class="prog-bar">
        <div class="steps-row">
            <div class="s-col">
                <div class="s-node done">1</div>
                <div class="s-lbl done">Personal</div>
            </div>
            <div class="s-line done"></div>
            <div class="s-col">
                <div class="s-node done">2</div>
                <div class="s-lbl done">Behaviour</div>
            </div>
            <div class="s-line done"></div>
            <div class="s-col">
                <div class="s-node done active">3</div>
                <div class="s-lbl active">Result</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="res-wrap">
        <div class="res-badge {'pos' if is_pos else 'neg'}">
            {'⚠ Autism Traits Detected' if is_pos else '✓ Low Autism Indicators'}
        </div>
        <div class="res-main {'pos' if is_pos else 'neg'}">
            {'Higher Likelihood of ASD' if is_pos else 'Lower Likelihood of ASD'}
        </div>
        <div class="risk-pill {risk_cls}">Risk Level: {risk_label}</div>
        <div class="res-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box">
            <div class="stat-val">{conf}%</div>
            <div class="stat-lbl">Confidence</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{score}/10</div>
            <div class="stat-lbl">Behavioural Score</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{risk_label}</div>
            <div class="stat-lbl">Risk Level</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Confidence bar
    st.markdown(f"""
    <div class="cw">
        <div class="cw-row">
            <span>Model Confidence</span>
            <strong style="font-family:'Times New Roman',serif;color:#12122a;">{conf}%</strong>
        </div>
        <div class="cw-track">
            <div class="cw-fill {fill_cls}" style="width:{conf}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disc">
        <strong>Important Notice:</strong> NeuroSense is an AI-powered screening tool, not a medical diagnosis.
        Results are probabilistic estimates based on behavioural patterns. Always seek evaluation
        from a licensed clinical psychologist or developmental paediatrician for an official assessment.
        The model was trained on the UCI Autism Screening dataset. Accuracy: ~95% on test set.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    r1, _, r3 = st.columns([1, 2, 1])
    with r1:
        if st.button("← Redo Assessment", type="secondary", use_container_width=True):
            st.session_state.result = None
            st.session_state.conf   = None
            st.session_state.score  = None
            go("personal")
    with r3:
        if st.button("Back to Home", type="secondary", use_container_width=True):
            go("home")
