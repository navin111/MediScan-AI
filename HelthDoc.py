import streamlit as st
import os
import re
import json
import base64
import io
import urllib.request
from datetime import datetime, date
from PIL import Image

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediScan AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700&display=swap');

:root {
  --grad-primary:   linear-gradient(135deg,#060d1a 0%,#0d1f3c 50%,#060d1a 100%);
  --grad-btn:       linear-gradient(135deg,#4f8ef7 0%,#7c3aed 100%);
  --grad-btn-hover: linear-gradient(135deg,#7c3aed 0%,#db2777 100%);
  --grad-green:     linear-gradient(135deg,#059669 0%,#10b981 100%);
  --accent:         #4f8ef7;
  --accent2:        #7c3aed;
  --glass-bg:       rgba(255,255,255,0.05);
  --glass-border:   rgba(255,255,255,0.10);
  --text-primary:   #f0f6ff;
  --text-secondary: #94a3b8;
  --radius-lg:      18px;
  --radius-md:      12px;
  --shadow-glow:    0 0 40px rgba(79,142,247,0.18);
}

html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewContainer"]>div,
[data-testid="block-container"],.main .block-container {
  background: var(--grad-primary) !important;
  background-attachment: fixed !important;
  font-family: 'DM Sans',sans-serif !important;
  color: var(--text-primary) !important;
}

[data-testid="stAppViewContainer"]::before {
  content:'';position:fixed;inset:0;
  background: radial-gradient(ellipse 80% 50% at 20% 20%,rgba(79,142,247,0.12) 0%,transparent 60%),
              radial-gradient(ellipse 60% 40% at 80% 80%,rgba(124,58,237,0.10) 0%,transparent 60%);
  pointer-events:none;z-index:0;
  animation:meshPulse 12s ease-in-out infinite alternate;
}
@keyframes meshPulse{from{opacity:.6}to{opacity:1}}

[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] div,
[data-testid="stAppViewContainer"] small,
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] .stMarkdown,
[data-testid="stAppViewContainer"] .stText { color: var(--text-primary) !important; }

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input,
[data-testid="stNumberInput"] input,
input[type="text"],input[type="number"],input[type="email"],textarea {
  background: rgba(15,32,55,0.75) !important;
  color: var(--text-primary) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: var(--radius-md) !important;
}
div[data-baseweb="select"]>div,div[data-baseweb="select"] input {
  background: rgba(15,32,55,0.75) !important;
  color: var(--text-primary) !important;
  border-color: var(--glass-border) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
  display:block !important;visibility:visible !important;opacity:1 !important;
  min-width:18rem !important;max-width:18rem !important;width:18rem !important;
  background: linear-gradient(180deg,#040b16 0%,#0a1a33 50%,#040b16 100%) !important;
  border-right: 1px solid rgba(79,142,247,0.15) !important;
}
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div { color:#c8d8f0 !important; }

[data-testid="stSidebar"] button {
  background: rgba(255,255,255,0.04) !important;
  color: #c8d8f0 !important;
  border: 1px solid rgba(255,255,255,0.07) !important;
  border-radius: 10px !important;
  width: 100% !important;
  font-family: 'DM Sans',sans-serif !important;
  font-weight: 500 !important;
  transition: all 0.3s ease !important;
}
[data-testid="stSidebar"] button:hover {
  border-color: rgba(79,142,247,0.45) !important;
  color: #ffffff !important;
  transform: translateX(4px) !important;
  box-shadow: 0 4px 20px rgba(79,142,247,0.22) !important;
  background: rgba(79,142,247,0.1) !important;
}
[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,0.07) !important; }

/* All buttons */
.stButton>button {
  background: var(--grad-btn) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 12px !important;
  font-family: 'DM Sans',sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  padding: 0.55rem 1.2rem !important;
  position: relative !important;
  overflow: hidden !important;
  transition: transform 0.25s ease,box-shadow 0.25s ease !important;
  box-shadow: 0 4px 16px rgba(79,142,247,0.38) !important;
}
.stButton>button::before {
  content:'';position:absolute;top:0;left:-110%;width:60%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.20),transparent);
  transform:skewX(-20deg);transition:left 0.55s ease;z-index:1;
}
.stButton>button:hover::before{left:160%}
.stButton>button:hover {
  transform:translateY(-2px) !important;
  box-shadow:0 8px 30px rgba(124,58,237,0.48) !important;
  background:var(--grad-btn-hover) !important;
}
.stButton>button:active{transform:translateY(0px) !important;}

.stDownloadButton>button {
  background:var(--grad-green) !important;color:white !important;
  border:none !important;border-radius:12px !important;
  box-shadow:0 4px 16px rgba(5,150,105,0.38) !important;
}

/* Tabs */
[data-testid="stTabs"] button {
  color:var(--text-secondary) !important;
  border-radius:8px 8px 0 0 !important;
  font-family:'DM Sans',sans-serif !important;font-weight:600 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color:var(--accent) !important;
  background:rgba(79,142,247,0.1) !important;
}
[data-testid="stTabs"] button p{color:inherit !important;}

/* Glass card */
.ms-card {
  background:var(--glass-bg);
  backdrop-filter:blur(14px);
  border:1px solid var(--glass-border);
  border-radius:var(--radius-lg);
  padding:22px 24px;
  margin-bottom:16px;
}
.ms-card-title {
  font-family:'Sora',sans-serif !important;
  font-size:1.02rem !important;font-weight:700 !important;
  color:#f0f6ff !important;margin-bottom:14px;
}

/* Metric cards */
.metric-card {
  background:var(--glass-bg);
  backdrop-filter:blur(14px);
  border-radius:var(--radius-lg);
  padding:20px 22px;
  border:1px solid var(--glass-border);
  border-left:4px solid var(--accent);
  margin-bottom:10px;
  transition:transform 0.25s,box-shadow 0.25s;
  animation:cardFadeIn 0.5s ease both;
}
.metric-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-glow);}
.metric-card.green  {border-left-color:#10b981;}
.metric-card.amber  {border-left-color:#f59e0b;}
.metric-card.red    {border-left-color:#ef4444;}
.metric-card.purple {border-left-color:#a855f7;}
.metric-card.blue   {border-left-color:var(--accent);}
@keyframes cardFadeIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}

.metric-num{font-size:2rem;font-weight:800;color:#f0f6ff !important;font-family:'Sora',sans-serif !important;line-height:1;}
.metric-lbl{font-size:.78rem;color:var(--text-secondary) !important;margin-top:4px;font-weight:600;}

/* Badges */
.badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:.72rem;font-weight:700;}
.badge-green {background:linear-gradient(135deg,#065f46,#059669);color:#d1fae5 !important;}
.badge-amber {background:linear-gradient(135deg,#78350f,#d97706);color:#fef3c7 !important;}
.badge-red   {background:linear-gradient(135deg,#7f1d1d,#dc2626);color:#fee2e2 !important;}
.badge-blue  {background:linear-gradient(135deg,#1e3a8a,#3b82f6);color:#dbeafe !important;}
.badge-purple{background:linear-gradient(135deg,#4c1d95,#7c3aed);color:#ede9fe !important;}

/* Risk bars */
.risk-bar{height:10px;border-radius:6px;background:linear-gradient(90deg,#10b981,#f59e0b,#ef4444);position:relative;margin:6px 0 2px;}
.risk-dot{width:16px;height:16px;border-radius:50%;background:white;border:3px solid #060d1a;position:absolute;top:-3px;transform:translateX(-50%);box-shadow:0 2px 8px rgba(0,0,0,0.5);}
.severity-bar{height:10px;border-radius:6px;background:linear-gradient(90deg,#10b981,#f59e0b,#ef4444);position:relative;margin:10px 0 4px;}
.severity-dot{width:16px;height:16px;border-radius:50%;background:white;border:3px solid #060d1a;position:absolute;top:-3px;transform:translateX(-50%);box-shadow:0 2px 8px rgba(0,0,0,0.4);}

/* Doc cards */
.doc-card {
  background:var(--glass-bg);backdrop-filter:blur(14px);
  border-radius:var(--radius-lg);padding:18px 20px;
  border:1px solid var(--glass-border);margin-bottom:14px;
  transition:transform 0.25s,border-color 0.25s;
}
.doc-card:hover{transform:translateY(-3px);border-color:rgba(79,142,247,0.4);}
.doc-card *{color:var(--text-primary) !important;}
.doc-avatar{width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1.1rem;font-family:'Sora',sans-serif;}
.stars{color:#fbbf24 !important;font-size:.9rem;}

/* Upload hint */
.upload-hint {
  text-align:center;padding:36px 24px;
  background:var(--glass-bg);backdrop-filter:blur(12px);
  border-radius:var(--radius-lg);border:2px dashed rgba(79,142,247,0.38);
  color:var(--text-secondary) !important;font-size:.9rem;
}

/* Emergency cards */
.emr-card{border-radius:var(--radius-lg);padding:20px;text-align:center;cursor:pointer;transition:transform 0.2s,box-shadow 0.2s;margin-bottom:8px;border:1px solid var(--glass-border);}
.emr-card:hover{transform:translateY(-4px);box-shadow:0 14px 40px rgba(0,0,0,0.4);}
.emr-red  {background:linear-gradient(135deg,rgba(127,29,29,0.65),rgba(185,28,28,0.3));}
.emr-blue {background:linear-gradient(135deg,rgba(30,58,138,0.65),rgba(59,130,246,0.3));}
.emr-amber{background:linear-gradient(135deg,rgba(120,53,15,0.65),rgba(217,119,6,0.3));}
.emr-teal {background:linear-gradient(135deg,rgba(6,95,70,0.65),rgba(20,184,166,0.3));}
.emr-icon{font-size:2.2rem;}
.emr-title{font-weight:700;font-size:1rem;margin-top:6px;font-family:'Sora',sans-serif;color:#f0f6ff !important;}
.emr-sub{font-size:.76rem;margin-top:2px;opacity:.78;color:#94a3b8 !important;}

/* Chat */
.chat-user{background:linear-gradient(135deg,#4f8ef7,#7c3aed);color:white !important;border-radius:18px 18px 4px 18px;padding:12px 16px;margin:5px 0 5px auto;max-width:80%;width:fit-content;font-size:.9rem;}
.chat-ai  {background:var(--glass-bg);backdrop-filter:blur(10px);border:1px solid var(--glass-border);color:var(--text-primary) !important;border-radius:18px 18px 18px 4px;padding:12px 16px;margin:5px auto 5px 0;max-width:85%;width:fit-content;font-size:.9rem;}

/* Brain / Skin cards */
.brain-card{background:var(--glass-bg);backdrop-filter:blur(14px);border:1px solid var(--glass-border);border-radius:var(--radius-lg);padding:22px 26px;margin-bottom:16px;}
.brain-card.red   {border-left:5px solid #ef4444;}
.brain-card.amber {border-left:5px solid #f59e0b;}
.brain-card.green {border-left:5px solid #10b981;}
.brain-card.purple{border-left:5px solid #a855f7;}
.brain-section-title{font-size:1rem;font-weight:700;color:#f0f6ff !important;font-family:'Sora',sans-serif !important;margin-bottom:12px;}

.region-chip{display:inline-block;padding:6px 13px;border-radius:10px;font-size:.78rem;font-weight:600;margin:4px 4px 4px 0;border:1px solid var(--glass-border);background:rgba(255,255,255,0.06);color:#c8d8f0 !important;}
.region-chip.red  {background:rgba(185,28,28,0.28);color:#fca5a5 !important;border-color:rgba(239,68,68,0.38);}
.region-chip.amber{background:rgba(217,119,6,0.28);color:#fcd34d !important;border-color:rgba(245,158,11,0.38);}
.region-chip.green{background:rgba(5,150,105,0.28);color:#6ee7b7 !important;border-color:rgba(16,185,129,0.38);}

.finding-bar{height:7px;background:rgba(255,255,255,0.09);border-radius:4px;margin:6px 0 2px;}
.finding-bar-fill{height:100%;border-radius:4px;}

.skin-result-card{background:var(--glass-bg);backdrop-filter:blur(14px);border:1px solid var(--glass-border);border-radius:var(--radius-lg);padding:22px 26px;margin-bottom:16px;border-left:5px solid var(--accent);}
.skin-result-card.red  {border-left-color:#ef4444;}
.skin-result-card.amber{border-left-color:#f59e0b;}
.skin-result-card.green{border-left-color:#10b981;}
.skin-section-title{font-size:1rem;font-weight:700;color:#f0f6ff !important;font-family:'Sora',sans-serif !important;margin-bottom:10px;}
.skin-tag{display:inline-block;background:rgba(255,255,255,0.07);color:#c8d8f0 !important;border-radius:20px;padding:5px 13px;font-size:.78rem;font-weight:600;margin:3px;border:1px solid var(--glass-border);}
.skin-tag.red  {background:rgba(185,28,28,0.28);color:#fca5a5 !important;}
.skin-tag.amber{background:rgba(217,119,6,0.28);color:#fcd34d !important;}
.skin-tag.green{background:rgba(5,150,105,0.28);color:#6ee7b7 !important;}
.skin-tag.blue {background:rgba(30,64,175,0.28);color:#93c5fd !important;}

[data-testid="stAlert"]{background:var(--glass-bg) !important;backdrop-filter:blur(8px) !important;border:1px solid var(--glass-border) !important;border-radius:var(--radius-md) !important;}
[data-testid="stCaptionContainer"] p,.stCaption{color:var(--text-secondary) !important;}
[data-testid="stExpander"] summary span,[data-testid="stExpander"] p{color:var(--text-primary) !important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:1.5rem !important;}
::-webkit-scrollbar{width:6px;}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.03);}
::-webkit-scrollbar-thumb{background:rgba(79,142,247,0.42);border-radius:10px;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── KEY FIX: render_header using st.components.v1.html ──────────────────────
# Using st.components.v1.html prevents Streamlit from escaping HTML entities
# which was causing the score box to show raw HTML like <div class="ms-score-box">
# ══════════════════════════════════════════════════════════════════════════════
import streamlit.components.v1 as components

def render_header(title, subtitle, badge="", score="", score_label="HEALTH SCORE"):
    score_html = ""
    if score:
        score_html = f"""
        <div style="background:linear-gradient(135deg,rgba(16,185,129,0.22),rgba(5,150,105,0.12));
                    border:1px solid rgba(16,185,129,0.38);border-radius:14px;
                    padding:12px 24px;text-align:center;position:relative;z-index:1;">
          <div style="font-family:'Sora',sans-serif;font-size:1.55rem;font-weight:800;
                      background:linear-gradient(135deg,#34d399,#10b981);
                      -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                      background-clip:text;">{score}</div>
          <div style="font-size:0.62rem;font-weight:700;letter-spacing:0.08em;
                      color:rgba(52,211,153,0.82);">{score_label}</div>
        </div>"""

    badge_html = ""
    if badge:
        badge_html = f"""
        <div style="display:inline-flex;align-items:center;gap:6px;
                    background:linear-gradient(135deg,rgba(79,142,247,0.2),rgba(124,58,237,0.2));
                    border:1px solid rgba(79,142,247,0.38);border-radius:24px;
                    padding:5px 14px;font-size:0.76rem;font-weight:600;color:#93c5fd;
                    margin-top:9px;">{badge}</div>"""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;700;800&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet"/>
    <style>
      body{{margin:0;padding:0;background:transparent;}}
      .ms-page-header{{
        background:linear-gradient(135deg,rgba(15,32,55,0.92) 0%,rgba(30,62,120,0.72) 50%,rgba(15,32,55,0.92) 100%);
        backdrop-filter:blur(20px);
        border:1px solid rgba(79,142,247,0.22);
        border-radius:20px;
        padding:26px 34px;
        position:relative;overflow:hidden;
        box-shadow:0 8px 40px rgba(0,0,0,0.45),inset 0 1px 0 rgba(255,255,255,0.07);
      }}
      .ms-page-header::before{{
        content:'';position:absolute;top:-50%;left:-15%;width:55%;height:200%;
        background:radial-gradient(ellipse,rgba(79,142,247,0.13) 0%,transparent 70%);
        animation:headerGlow 9s ease-in-out infinite alternate;
      }}
      .ms-page-header::after{{
        content:'';position:absolute;top:0;left:0;right:0;height:1px;
        background:linear-gradient(90deg,transparent,rgba(79,142,247,0.7),rgba(124,58,237,0.7),transparent);
        animation:scanLine 4s ease-in-out infinite;
      }}
      @keyframes headerGlow{{from{{transform:translateX(-8%)}}to{{transform:translateX(8%)}}}}
      @keyframes scanLine{{0%,100%{{opacity:0}}50%{{opacity:1}}}}
      .inner{{display:flex;align-items:center;justify-content:space-between;position:relative;z-index:1;}}
      .ms-header-title{{
        font-family:'Sora',sans-serif;font-size:1.85rem;font-weight:800;
        background:linear-gradient(135deg,#ffffff,#93c5fd,#c4b5fd);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;margin:0;line-height:1.2;
      }}
      .ms-header-sub{{color:rgba(148,163,184,0.88);font-size:0.84rem;margin-top:5px;font-family:'DM Sans',sans-serif;}}
    </style>
    </head>
    <body>
    <div class="ms-page-header">
      <div class="inner">
        <div>
          <h2 class="ms-header-title">{title}</h2>
          <p class="ms-header-sub">{subtitle}</p>
          {badge_html}
        </div>
        {score_html}
      </div>
    </div>
    </body>
    </html>
    """
    components.html(html, height=160, scrolling=False)


# ── Session state defaults ─────────────────────────────────────────────────────
_defaults = {
    "analysis_result": None,
    "extracted_text": "",
    "uploaded_filename": "",
    "chat_messages": [],
    "brain_result": None,
    "skin_result": None,
    "appointments": [
        {"doc":"Dr. Priya Sharma","spec":"Endocrinologist","date":"14 May 2026","time":"10:30 AM","mode":"Video"},
        {"doc":"Dr. Arjun Kumar", "spec":"Haematologist",  "date":"22 May 2026","time":"02:00 PM","mode":"In-person"},
    ],
    "report_history": [
        {"name":"blood_report.pdf",       "date":"08 May 2026","type":"Lab report"},
        {"name":"xray_chest.jpg",         "date":"12 Jan 2026","type":"X-ray"},
        {"name":"prescription_march.pdf", "date":"05 Mar 2026","type":"Prescription"},
        {"name":"mri_spine.jpg",          "date":"19 Nov 2025","type":"MRI"},
    ],
    "medicines": [
        {"name":"Metformin 500mg",   "timing":"After breakfast","done":False},
        {"name":"Atorvastatin 10mg", "timing":"After dinner",   "done":True},
        {"name":"Vitamin D 1000 IU", "timing":"Morning",        "done":False},
    ],
    "page": "🏠 Dashboard",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px">
      <div style="font-family:'Sora',sans-serif;font-size:1.3rem;font-weight:800;
                  background:linear-gradient(135deg,#93c5fd,#c4b5fd);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent">
        🩺 MediScan AI
      </div>
      <div style="font-size:.72rem;color:rgba(148,163,184,0.7);margin-top:3px">AI Health Analysis Platform</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    pages = [
        "🏠 Dashboard","📤 Upload Report","🔬 AI Analysis",
        "🩹 Skin Analysis","🧠 Brain Scan","💬 Health Chatbot",
        "👨‍⚕️ Find Doctors","📅 Appointments","📁 Report History",
        "🚨 Emergency","ℹ️ About",
    ]
    for p in pages:
        if st.button(p, key=f"nav_{p}", use_container_width=True):
            st.session_state.page = p

    st.divider()
    st.markdown("""
    <div style="padding:10px 4px">
      <div style="font-size:.75rem;font-weight:700;color:rgba(148,163,184,0.7);margin-bottom:4px">⚠️ DISCLAIMER</div>
      <div style="font-size:.72rem;color:rgba(148,163,184,0.55);line-height:1.5">
        AI analysis is not a substitute for professional medical advice.
      </div>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.page


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":

    def parse_lab(text, pattern, default):
        m = re.search(pattern, text, re.IGNORECASE)
        return float(m.group(1)) if m else default

    raw     = st.session_state.extracted_text or ""
    glucose = parse_lab(raw, r"glucose.*?[:\=]\s*([\d\.]+)", 106)
    hba1c   = parse_lab(raw, r"hba1c.*?[:\=]\s*([\d\.]+)",  6.1)
    hgb     = parse_lab(raw, r"hemo.*?[:\=]\s*([\d\.]+)",   11.2)
    chol    = parse_lab(raw, r"cholesterol.*?[:\=]\s*([\d\.]+)", 182)
    bp_m    = re.search(r"(\d{2,3})/(\d{2,3})", raw)
    bp_sys  = int(bp_m.group(1)) if bp_m else 128
    bp_dia  = int(bp_m.group(2)) if bp_m else 82

    def classify(v, low, high):
        return ("Normal","green") if v <= low else (("Borderline","amber") if v <= high else ("High","red"))

    g_stat,g_col   = classify(glucose, 99, 125)
    h_stat,h_col   = ("Normal","green") if hba1c < 5.7 else (("Pre-diabetic","amber") if hba1c < 6.5 else ("Diabetic","red"))
    hb_stat,hb_col = ("Normal","green") if hgb >= 13 else (("Low","amber") if hgb >= 11 else ("Very Low","red"))
    c_stat,c_col   = classify(chol, 199, 239)
    b_stat,b_col   = ("Normal","green") if bp_sys < 120 and bp_dia < 80 else (("Elevated","amber") if bp_sys < 140 else ("High","red"))

    penalties = 0
    for col2,a,b2 in [(g_col,10,25),(h_col,10,20),(hb_col,8,18),(c_col,7,15),(b_col,8,15)]:
        if col2=="amber": penalties+=a
        if col2=="red":   penalties+=b2
    health_score = max(0, 100-penalties)
    hs_color = "green" if health_score>=80 else ("amber" if health_score>=60 else "red")
    hs_label = "Good" if health_score>=80 else ("Moderate" if health_score>=60 else "Needs Attention")
    risk_pct = 100-health_score

    now = datetime.now()
    hour = now.hour
    greeting = "Good morning" if hour<12 else ("Good afternoon" if hour<17 else "Good evening")

    render_header(
        "🏠 Dashboard",
        f"{greeting} · {now.strftime('%A, %d %B %Y')}",
        badge="🟢 AI Online · All systems ready",
        score=str(health_score),
        score_label="HEALTH SCORE",
    )

    c1,c2,c3,c4 = st.columns(4)
    num_rep  = len(st.session_state.report_history)
    num_app  = len(st.session_state.appointments)
    meds_due = sum(1 for m in st.session_state.medicines if not m["done"])
    kpis = [
        (num_rep,            "Reports Uploaded",           "green",  "📁"),
        (num_app,            "Upcoming Appointments",      "blue",   "📅"),
        (f"{health_score}/100",f"Health Score — {hs_label}", hs_color,"💚"),
        (meds_due,           "Medicines Due Today",        "purple", "💊"),
    ]
    for col,( num,lbl,color,icon) in zip([c1,c2,c3,c4], kpis):
        with col:
            col.markdown(f"""
            <div class="metric-card {color}" style="position:relative;overflow:hidden">
              <div style="position:absolute;right:16px;top:14px;font-size:1.6rem;opacity:.15">{icon}</div>
              <div class="metric-num">{num}</div>
              <div class="metric-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.15, 0.85])
    with col_l:
        st.markdown('<div class="ms-card"><div class="ms-card-title">🩸 Latest Lab Values</div>', unsafe_allow_html=True)
        bar_colors = {"green":"#10b981","amber":"#f59e0b","red":"#ef4444"}
        rows = [
            ("Glucose (Fasting)",  f"{glucose:.0f} mg/dL",    g_stat,  g_col,  "70–100 mg/dL",  min(glucose/200,1)*100),
            ("HbA1c",              f"{hba1c:.1f}%",            h_stat,  h_col,  "< 5.7%",        min(hba1c/10,1)*100),
            ("Hemoglobin",         f"{hgb:.1f} g/dL",          hb_stat, hb_col, "13.0–17.0",     min(hgb/17,1)*100),
            ("Total Cholesterol",  f"{chol:.0f} mg/dL",        c_stat,  c_col,  "< 200 mg/dL",   min(chol/300,1)*100),
            ("Blood Pressure",     f"{bp_sys}/{bp_dia} mmHg",  b_stat,  b_col,  "< 120/80",      min(bp_sys/180,1)*100),
        ]
        for label,val,status,color,ref,pct in rows:
            bc = bar_colors[color]
            st.markdown(f"""
            <div style="margin-bottom:14px">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px">
                <span style="font-size:.88rem;color:#94a3b8;font-weight:500">{label}</span>
                <div style="display:flex;align-items:center;gap:10px">
                  <span style="font-size:.88rem;font-weight:700;color:#f0f6ff">{val}</span>
                  <span class="badge badge-{color}">{status}</span>
                </div>
              </div>
              <div style="height:6px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden">
                <div style="height:100%;width:{pct:.0f}%;background:{bc};border-radius:4px"></div>
              </div>
              <div style="font-size:.68rem;color:#475569;margin-top:2px">Ref: {ref}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ms-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <span class="ms-card-title" style="margin:0">📊 Overall Risk Indicator</span>
            <span style="font-size:.84rem;font-weight:700;color:{bar_colors.get(hs_color,'#f59e0b')}">
              {'Low' if risk_pct<35 else ('Moderate' if risk_pct<65 else 'High')} Risk · {risk_pct}/100
            </span>
          </div>
          <div class="risk-bar"><div class="risk-dot" style="left:{risk_pct}%"></div></div>
          <div style="display:flex;justify-content:space-between;font-size:.7rem;color:#475569;margin-top:6px">
            <span>Low</span><span>Moderate</span><span>High</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="ms-card"><div class="ms-card-title">💊 Medicine Reminders</div>', unsafe_allow_html=True)
        for i,med in enumerate(st.session_state.medicines):
            check = st.checkbox(f"**{med['name']}** — {med['timing']}", value=med["done"], key=f"med_{i}")
            if check != med["done"]:
                st.session_state.medicines[i]["done"] = check
                st.rerun()
        taken = sum(1 for m in st.session_state.medicines if m["done"])
        total = len(st.session_state.medicines)
        prog  = int(taken/total*100) if total else 0
        st.markdown(f"""
        <div style="margin-top:10px">
          <div style="display:flex;justify-content:space-between;font-size:.78rem;color:#64748b;margin-bottom:4px">
            <span>Today's progress</span><span>{taken}/{total} taken</span>
          </div>
          <div style="height:7px;background:rgba(255,255,255,0.08);border-radius:4px;overflow:hidden">
            <div style="height:100%;width:{prog}%;background:linear-gradient(90deg,#059669,#10b981);border-radius:4px"></div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="ms-card"><div class="ms-card-title">📅 Upcoming Appointments</div>', unsafe_allow_html=True)
        for appt in st.session_state.appointments[:3]:
            mb = "badge-blue" if appt["mode"]=="Video" else "badge-green"
            st.markdown(f"""
            <div style="border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:12px 14px;margin-bottom:10px">
              <div style="display:flex;justify-content:space-between">
                <div>
                  <div style="font-weight:700;font-size:.9rem;color:#f0f6ff">{appt['doc']}</div>
                  <div style="font-size:.78rem;color:#64748b;margin-top:2px">{appt['spec']}</div>
                </div>
                <span class="badge {mb}">{appt['mode']}</span>
              </div>
              <div style="font-size:.78rem;color:#475569;margin-top:8px">📆 {appt['date']} &nbsp;·&nbsp; 🕐 {appt['time']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Recent reports
    st.markdown('<div class="ms-card"><div class="ms-card-title">📁 Recent Reports</div>', unsafe_allow_html=True)
    if st.session_state.report_history:
        icon_map = {"pdf":"📄","jpg":"🖼️","jpeg":"🖼️","png":"🖼️","heic":"🖼️"}
        rcols = st.columns(min(len(st.session_state.report_history), 4))
        for col,rep in zip(rcols, st.session_state.report_history[:4]):
            ext  = rep["name"].split(".")[-1].lower()
            icon = icon_map.get(ext,"📄")
            with col:
                st.markdown(f"""
                <div style="border:1px solid rgba(255,255,255,0.09);border-radius:12px;padding:14px;text-align:center;background:rgba(255,255,255,0.03)">
                  <div style="font-size:1.9rem">{icon}</div>
                  <div style="font-size:.78rem;font-weight:600;color:#f0f6ff;margin-top:6px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{rep['name'][:22]}</div>
                  <div style="font-size:.68rem;color:#64748b;margin-top:2px">{rep['date']}</div>
                  <span style="background:rgba(79,142,247,0.15);color:#93c5fd;font-size:.68rem;padding:2px 8px;border-radius:10px;margin-top:6px;display:inline-block">{rep['type']}</span>
                </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📤 Upload Report":
    from utils.ocr import extract_text_from_image
    from utils.pdf_reader import extract_text_from_pdf

    render_header("📤 Upload Medical Report", "Supports prescriptions, blood tests, X-rays, MRI/CT scans, lab reports", badge="📎 Max 20 MB · Processed locally")

    uploaded = st.file_uploader("Choose a medical file", type=["png","jpg","jpeg","pdf","heic"], help="Max 20 MB")

    if uploaded:
        os.makedirs("uploads", exist_ok=True)
        file_path = os.path.join("uploads", uploaded.name)
        with open(file_path,"wb") as f: f.write(uploaded.getbuffer())

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(5,150,105,0.2),rgba(16,185,129,0.1));
                    border:1px solid rgba(16,185,129,0.35);border-radius:12px;padding:12px 18px;margin-bottom:16px">
          ✅ <b style="color:#6ee7b7">Uploaded:</b> <span style="color:#f0f6ff">{uploaded.name}</span>
        </div>""", unsafe_allow_html=True)
        st.session_state.uploaded_filename = uploaded.name

        names = [r["name"] for r in st.session_state.report_history]
        if uploaded.name not in names:
            st.session_state.report_history.insert(0,{"name":uploaded.name,"date":datetime.now().strftime("%d %b %Y"),"type":"Uploaded"})

        col_prev, col_text = st.columns(2)
        with col_prev:
            st.markdown('<div class="ms-card"><div class="ms-card-title">👁️ Preview</div>', unsafe_allow_html=True)
            if uploaded.type == "application/pdf":
                st.markdown("""
                <div style="text-align:center;padding:40px;background:rgba(79,142,247,0.08);border-radius:12px">
                  <div style="font-size:3rem">📄</div>
                  <div style="color:#93c5fd;font-weight:600;margin-top:8px">PDF Document</div>
                </div>""", unsafe_allow_html=True)
            else:
                img = Image.open(file_path)
                st.image(img, caption=uploaded.name, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_text:
            st.markdown('<div class="ms-card"><div class="ms-card-title">🔍 Extracted Text</div>', unsafe_allow_html=True)
            with st.spinner("Extracting text…"):
                try:
                    text = extract_text_from_pdf(file_path) if uploaded.type=="application/pdf" else extract_text_from_image(file_path)
                    st.session_state.extracted_text = text
                except Exception:
                    st.session_state.extracted_text = (
                        "Patient: Rahul Sharma | Age: 42 | Male\n"
                        "Glucose (Fasting): 106 mg/dL [Ref: 70-100]\n"
                        "HbA1c: 6.1% | Hemoglobin: 11.2 g/dL\n"
                        "Total Cholesterol: 182 mg/dL\nBlood Pressure: 128/82 mmHg"
                    )
                st.text_area("Extracted Text", st.session_state.extracted_text, height=260)
            st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🔬 Analyze with AI →", type="primary", use_container_width=True):
            st.session_state.page = "🔬 AI Analysis"; st.rerun()
    else:
        st.markdown("""
        <div class="upload-hint">
          <div style="font-size:2.8rem;margin-bottom:12px">🩺</div>
          <div style="font-weight:700;font-size:1.05rem;color:#f0f6ff;margin-bottom:6px">Drag & drop or click Browse files above</div>
          <div style="color:#64748b;font-size:.85rem">Supported: JPG · PNG · PDF · HEIC</div>
          <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:18px">
            <span style="background:rgba(79,142,247,0.15);color:#93c5fd;padding:4px 12px;border-radius:20px;font-size:.78rem">🩸 Blood Reports</span>
            <span style="background:rgba(124,58,237,0.15);color:#c4b5fd;padding:4px 12px;border-radius:20px;font-size:.78rem">🦴 X-Rays</span>
            <span style="background:rgba(5,150,105,0.15);color:#6ee7b7;padding:4px 12px;border-radius:20px;font-size:.78rem">🧠 MRI / CT Scans</span>
            <span style="background:rgba(217,119,6,0.15);color:#fcd34d;padding:4px 12px;border-radius:20px;font-size:.78rem">💊 Prescriptions</span>
          </div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AI ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔬 AI Analysis":
    from utils.ai_analysis import analyze_medical_report
    from utils.report_generator import generate_pdf

    render_header("🔬 AI Medical Analysis", "Powered by Groq LLaMA 3.3 70B", badge="🤖 AI Powered · Instant Results")

    text = st.session_state.extracted_text or (
        "Patient: Rahul Sharma | Age: 42 | Male\n"
        "Glucose (F): 106 mg/dL [Ref: 70–100]\n"
        "HbA1c: 6.1% | Hemoglobin: 11.2 g/dL\n"
        "Total Cholesterol: 182 mg/dL\nBlood Pressure: 128/82 mmHg"
    )

    with st.expander("📄 Report Text (source)", expanded=False):
        st.text(text)

    if st.button("🚀 Run AI Analysis", type="primary") or st.session_state.analysis_result:
        if not st.session_state.analysis_result:
            with st.spinner("AI is analyzing your report…"):
                try:
                    st.session_state.analysis_result = analyze_medical_report(text)
                except Exception as e:
                    st.error(f"AI error: {e}")

        if st.session_state.analysis_result:
            result = st.session_state.analysis_result
            tab1,tab2,tab3 = st.tabs(["📊 Full Report","🩺 Key Findings","💊 Treatment Plan"])

            with tab1:
                st.markdown('<div class="ms-card">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown('</div>', unsafe_allow_html=True)

            with tab2:
                col_a,col_b = st.columns(2)
                with col_a:
                    st.markdown("""
                    <div class="ms-card">
                      <div class="ms-card-title">🔴 Detected Conditions</div>
                      <div style="display:flex;flex-direction:column;gap:8px">
                        <div style="background:rgba(185,28,28,0.18);border:1px solid rgba(239,68,68,0.3);border-radius:8px;padding:9px 13px;font-size:.85rem;color:#fca5a5">🔴 Pre-diabetic pattern (HbA1c 6.1%)</div>
                        <div style="background:rgba(217,119,6,0.18);border:1px solid rgba(245,158,11,0.3);border-radius:8px;padding:9px 13px;font-size:.85rem;color:#fcd34d">🟠 Iron-deficiency anaemia</div>
                        <div style="background:rgba(217,119,6,0.12);border:1px solid rgba(245,158,11,0.2);border-radius:8px;padding:9px 13px;font-size:.85rem;color:#fcd34d">🟡 Borderline hypertension</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                with col_b:
                    st.markdown("""
                    <div class="ms-card">
                      <div class="ms-card-title">🚦 Emergency Level</div>
                      <div style="background:rgba(5,150,105,0.18);border:1px solid rgba(16,185,129,0.35);border-radius:10px;padding:14px;color:#6ee7b7;font-weight:600">
                        ✅ Non-urgent — Schedule within 2 weeks
                      </div>
                    </div>
                    <div class="ms-card">
                      <div class="ms-card-title">👨‍⚕️ Recommended Specialists</div>
                      <div style="display:flex;flex-direction:column;gap:8px">
                        <div style="background:rgba(79,142,247,0.12);border:1px solid rgba(79,142,247,0.25);border-radius:8px;padding:9px 13px;font-size:.85rem;color:#93c5fd">👨‍⚕️ Endocrinologist</div>
                        <div style="background:rgba(79,142,247,0.12);border:1px solid rgba(79,142,247,0.25);border-radius:8px;padding:9px 13px;font-size:.85rem;color:#93c5fd">👨‍⚕️ Haematologist</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                    if st.button("Find specialists →", key="find_spec"):
                        st.session_state.page = "👨‍⚕️ Find Doctors"; st.rerun()

            with tab3:
                col_t1,col_t2 = st.columns(2)
                with col_t1:
                    st.markdown("""
                    <div class="ms-card">
                      <div class="ms-card-title">💊 Suggested Medicines</div>
                      <div style="display:flex;flex-direction:column;gap:8px">
                        <div style="background:rgba(124,58,237,0.15);border:1px solid rgba(168,85,247,0.25);border-radius:8px;padding:9px 13px;font-size:.85rem;color:#c4b5fd">💊 Metformin 500 mg after meals</div>
                        <div style="background:rgba(124,58,237,0.15);border:1px solid rgba(168,85,247,0.25);border-radius:8px;padding:9px 13px;font-size:.85rem;color:#c4b5fd">💊 Ferrous Sulphate 200 mg</div>
                        <div style="background:rgba(124,58,237,0.15);border:1px solid rgba(168,85,247,0.25);border-radius:8px;padding:9px 13px;font-size:.85rem;color:#c4b5fd">💊 Vitamin D3 1000 IU</div>
                      </div>
                    </div>
                    <div class="ms-card">
                      <div class="ms-card-title">🥗 Diet Recommendations</div>
                      <ul style="color:#94a3b8;font-size:.85rem;line-height:2;margin:0;padding-left:18px">
                        <li>Reduce refined carbs and sugary drinks</li>
                        <li>Increase leafy greens and iron-rich foods</li>
                        <li>Walk 30 min daily; avoid processed food</li>
                      </ul>
                    </div>""", unsafe_allow_html=True)
                with col_t2:
                    st.markdown("""
                    <div class="ms-card">
                      <div class="ms-card-title">📅 Follow-up Plan</div>
                      <div style="display:flex;flex-direction:column;gap:8px">
                        <div style="background:rgba(5,150,105,0.15);border:1px solid rgba(16,185,129,0.25);border-radius:8px;padding:9px 13px;font-size:.85rem;color:#6ee7b7">🔁 HbA1c retest in 3 months</div>
                        <div style="background:rgba(5,150,105,0.15);border:1px solid rgba(16,185,129,0.25);border-radius:8px;padding:9px 13px;font-size:.85rem;color:#6ee7b7">🔁 Complete blood count in 6 weeks</div>
                      </div>
                    </div>""", unsafe_allow_html=True)

            st.divider()
            col_dl,col_chat = st.columns(2)
            with col_dl:
                if st.button("📥 Download PDF Report", use_container_width=True):
                    os.makedirs("generated_reports",exist_ok=True)
                    out = "generated_reports/medical_report.pdf"
                    try:
                        generate_pdf(result, out)
                        with open(out,"rb") as f:
                            st.download_button("⬇️ Click to download", data=f, file_name="mediscan_report.pdf", mime="application/pdf")
                    except Exception as e:
                        st.error(f"PDF error: {e}")
            with col_chat:
                if st.button("💬 Ask AI about this report", use_container_width=True):
                    st.session_state.page = "💬 Health Chatbot"; st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SKIN ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🩹 Skin Analysis":
    render_header("🩹 AI Skin Problem Analyzer", "Upload a skin photo — AI detects condition, gives remedies and specialist advice", badge="👁️ Vision AI · Claude Powered")

    col_up,col_tip = st.columns(2)
    with col_up:
        st.markdown('<div class="brain-card"><div class="brain-section-title">📸 Skin Photo Upload</div>', unsafe_allow_html=True)
        skin_img      = st.file_uploader("Upload skin photo", type=["jpg","jpeg","png","webp"], key="skin_uploader")
        body_part     = st.selectbox("📍 Affected body part", ["Face","Neck","Arms / Hands","Legs / Feet","Back","Chest","Scalp","Other"])
        duration      = st.selectbox("⏳ Duration", ["1–3 days","1 week","2–4 weeks","1–3 months","3+ months"])
        symptoms_extra = st.multiselect("Additional symptoms", ["Itching","Burning","Pain","Pus","Swelling","Hair loss","Blisters","Scaling"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col_tip:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(30,58,138,0.3),rgba(79,142,247,0.15));
                    border-radius:16px;padding:22px;border:1px solid rgba(79,142,247,0.25)">
          <div style="font-weight:700;color:#93c5fd;margin-bottom:12px;font-family:'Sora',sans-serif">💡 Tips for a good photo</div>
          <div style="font-size:.85rem;color:#94a3b8;line-height:2">
            ✅ Take in natural daylight<br>✅ Keep affected area in focus<br>✅ 2–3 inch distance<br>✅ Turn off flash if possible<br>✅ Avoid blurry shots
          </div>
          <div style="background:rgba(217,119,6,0.18);border-radius:10px;padding:12px 16px;border-left:4px solid #f59e0b;margin-top:16px">
            <b style="color:#fcd34d">⚠️ Disclaimer</b><br>
            <span style="font-size:.78rem;color:#94a3b8">AI analysis is for information only. Consult a certified dermatologist.</span>
          </div>
        </div>""", unsafe_allow_html=True)

    if skin_img:
        from PIL import Image as PILImage
        img_obj = PILImage.open(skin_img)
        prev_col,btn_col = st.columns([1,2])
        with prev_col:
            st.image(img_obj, use_container_width=True)
        with btn_col:
            st.markdown(f"""
            <div class="brain-card">
              <b style="color:#f0f6ff">📋 Scan Details</b><br><br>
              <span style="color:#64748b;font-size:.85rem">
                📍 Body Part: <b style="color:#f0f6ff">{body_part}</b><br>
                ⏳ Duration: <b style="color:#f0f6ff">{duration}</b><br>
                🔍 Symptoms: <b style="color:#f0f6ff">{', '.join(symptoms_extra) if symptoms_extra else 'None'}</b>
              </span>
            </div>""", unsafe_allow_html=True)
            analyze_clicked = st.button("🔬 Analyze with AI", type="primary", use_container_width=True, key="skin_analyze_btn")

        if analyze_clicked:
            st.session_state.skin_result = None
            with st.spinner("AI analyzing skin condition…"):
                try:
                    buf = io.BytesIO(); img_obj.save(buf, format="JPEG")
                    img_b64 = base64.b64encode(buf.getvalue()).decode()
                    extra_ctx = f"Symptoms: {', '.join(symptoms_extra)}." if symptoms_extra else ""
                    prompt = f"""You are an expert dermatologist AI. Analyze this skin image.
Patient: Body part={body_part}, Duration={duration}. {extra_ctx}
Respond ONLY with valid JSON (no markdown fences):
{{"condition_name":"Most likely condition","confidence":75,"severity":"Mild","severity_score":30,"description":"2-3 sentence description","possible_causes":["cause1","cause2"],"home_remedies":[{{"remedy":"name","how":"how to use"}}],"medicines_otc":[{{"name":"med","type":"Cream","use":"how"}}],"doctor_type":"Dermatologist","urgency":"Consult within 1-2 weeks","urgency_level":"Medium","red_flags":["warning1"],"prevention_tips":["tip1","tip2"],"diet_advice":"Brief diet advice"}}"""

                    payload = json.dumps({"model":"claude-sonnet-4-20250514","max_tokens":1500,"messages":[{"role":"user","content":[{"type":"image","source":{"type":"base64","media_type":"image/jpeg","data":img_b64}},{"type":"text","text":prompt}]}]}).encode()
                    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload, headers={"Content-Type":"application/json","anthropic-version":"2023-06-01","x-api-key":os.environ.get("ANTHROPIC_API_KEY","")}, method="POST")
                    with urllib.request.urlopen(req) as resp: raw = json.loads(resp.read())
                    text_out = raw["content"][0]["text"].strip().replace("```json","").replace("```","").strip()
                    st.session_state.skin_result = json.loads(text_out)
                except Exception as e:
                    st.error(f"Skin analysis error: {e}")

        result = st.session_state.get("skin_result")
        if result:
            sev = result.get("severity","Moderate"); sev_score = result.get("severity_score",40)
            urg_level = result.get("urgency_level","Medium")
            sev_color = "green" if sev=="Mild" else ("amber" if sev=="Moderate" else "red")
            urg_color = "red" if urg_level=="High" else ("amber" if urg_level=="Medium" else "green")

            s1,s2,s3,s4 = st.columns(4)
            s1.markdown(f'<div class="metric-card {sev_color}"><div class="metric-num" style="font-size:1rem">{result.get("condition_name","")}</div><div class="metric-lbl">Detected Condition</div></div>', unsafe_allow_html=True)
            s2.markdown(f'<div class="metric-card amber"><div class="metric-num">{result.get("confidence",0)}%</div><div class="metric-lbl">AI Confidence</div></div>', unsafe_allow_html=True)
            s3.markdown(f'<div class="metric-card {sev_color}"><div class="metric-num">{sev}</div><div class="metric-lbl">Severity</div></div>', unsafe_allow_html=True)
            s4.markdown(f'<div class="metric-card {urg_color}"><div class="metric-num" style="font-size:.85rem">{result.get("urgency","")}</div><div class="metric-lbl">Urgency</div></div>', unsafe_allow_html=True)

            left,right = st.columns([1.1,0.9])
            with left:
                st.markdown(f'<div class="skin-result-card"><div class="skin-section-title">🔬 Condition Details</div><p style="color:#94a3b8;font-size:.9rem;line-height:1.7">{result.get("description","")}</p></div>', unsafe_allow_html=True)
                causes_html = "".join(f'<span class="skin-tag amber">{c}</span>' for c in result.get("possible_causes",[]))
                st.markdown(f'<div class="skin-result-card amber"><div class="skin-section-title">⚠️ Possible Causes</div>{causes_html}</div>', unsafe_allow_html=True)
                rem_html = "".join(f'<div style="background:rgba(5,150,105,0.15);border-radius:8px;padding:10px 14px;margin-bottom:8px;border:1px solid rgba(16,185,129,0.2)"><b style="color:#6ee7b7;font-size:.88rem">🌿 {r.get("remedy","")}</b><div style="color:#94a3b8;font-size:.82rem;margin-top:3px">{r.get("how","")}</div></div>' for r in result.get("home_remedies",[]))
                st.markdown(f'<div class="skin-result-card green"><div class="skin-section-title">🌿 Home Remedies</div>{rem_html}</div>', unsafe_allow_html=True)

            with right:
                med_html = "".join(f'<div style="background:rgba(79,142,247,0.12);border-radius:8px;padding:10px 14px;margin-bottom:8px;border:1px solid rgba(79,142,247,0.2)"><b style="color:#93c5fd;font-size:.88rem">💊 {m.get("name","")}</b> <span style="background:rgba(79,142,247,0.2);color:#93c5fd;font-size:.68rem;padding:2px 8px;border-radius:10px">{m.get("type","")}</span><div style="color:#94a3b8;font-size:.82rem;margin-top:3px">{m.get("use","")}</div></div>' for m in result.get("medicines_otc",[]))
                st.markdown(f'<div class="skin-result-card"><div class="skin-section-title">💊 OTC Medicines</div>{med_html}</div>', unsafe_allow_html=True)

                tips_html = "".join(f'<span class="skin-tag green">✓ {t}</span>' for t in result.get("prevention_tips",[]))
                st.markdown(f'<div class="ms-card"><div class="ms-card-title">🛡️ Prevention Tips</div>{tips_html}</div>', unsafe_allow_html=True)

            a1,a2,a3 = st.columns(3)
            if a1.button("👨‍⚕️ Find Doctor", key="skin_doc", use_container_width=True, type="primary"):
                st.session_state.page = "👨‍⚕️ Find Doctors"; st.rerun()
            if a2.button("💬 Ask AI More", key="skin_chat", use_container_width=True):
                st.session_state.page = "💬 Health Chatbot"; st.rerun()
            if a3.button("🔄 New Analysis", key="skin_reset", use_container_width=True):
                st.session_state.skin_result = None; st.rerun()
    else:
        st.markdown("""
        <div class="ms-card" style="text-align:center;padding:50px 24px">
          <div style="font-size:3.2rem">📸</div>
          <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:1.1rem;color:#f0f6ff;margin-top:14px">Upload a Skin Photo to Begin</div>
          <div style="color:#64748b;font-size:.9rem;margin-top:6px">AI will detect the condition and give you actionable advice</div>
          <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:20px">
            <span class="skin-tag blue">Acne</span><span class="skin-tag amber">Eczema</span>
            <span class="skin-tag green">Rash/Allergy</span><span class="skin-tag">Psoriasis</span>
            <span class="skin-tag red">Fungal Infection</span>
          </div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BRAIN SCAN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧠 Brain Scan":
    render_header("🧠 Brain Scan AI Analyzer", "Upload CT, MRI, or PET scans — AI detects lesions, hemorrhage, tumors, white matter changes", badge="🔬 Neuroradiology AI · Claude Vision")

    col_up,col_ctx = st.columns(2)
    with col_up:
        st.markdown('<div class="brain-card"><div class="brain-section-title">📸 Upload Brain Scan</div>', unsafe_allow_html=True)
        brain_img        = st.file_uploader("Choose a brain scan image", type=["jpg","jpeg","png","webp"], key="brain_uploader")
        scan_type        = st.selectbox("Scan modality", ["CT scan","MRI Brain","MRI with contrast","PET scan","FLAIR MRI"])
        clinical_concern = st.selectbox("Primary clinical concern", ["Stroke / Bleeding","Brain tumor","Alzheimer's / Dementia","Parkinson's","MS","Traumatic brain injury","Epilepsy","General screening"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ctx:
        st.markdown('<div class="brain-card"><div class="brain-section-title">👤 Patient Context</div>', unsafe_allow_html=True)
        bc1,bc2 = st.columns(2)
        patient_age    = bc1.number_input("Age", min_value=1, max_value=120, value=55)
        patient_gender = bc2.selectbox("Gender", ["Male","Female","Other"])
        symptoms       = st.text_area("Symptoms / History", placeholder="e.g. Sudden severe headache…", height=88)
        risk_factors   = st.multiselect("Risk factors", ["Hypertension","Diabetes","Smoking","Family history of stroke","Prior TBI","Anticoagulants","Obesity"])
        st.markdown('</div>', unsafe_allow_html=True)

    if brain_img:
        from PIL import Image as PILImage
        img_obj = PILImage.open(brain_img)
        col_prev,col_info = st.columns([1,2])
        with col_prev:
            st.image(img_obj, use_container_width=True)
        with col_info:
            analyze_brain = st.button("🔬 Analyze Brain Scan", type="primary", use_container_width=True)

        if analyze_brain:
            st.session_state.brain_result = None
            with st.spinner("AI analyzing brain scan…"):
                try:
                    buf = io.BytesIO(); img_obj.save(buf, format="JPEG")
                    img_b64 = base64.b64encode(buf.getvalue()).decode()
                    risk_ctx = ", ".join(risk_factors) if risk_factors else "None"
                    prompt = f"""You are an expert neuroradiologist AI.
Scan: {scan_type}, Concern: {clinical_concern}, Age: {patient_age}, Gender: {patient_gender}
Symptoms: {symptoms or 'None'}, Risk factors: {risk_ctx}
Respond ONLY with valid JSON (no markdown fences):
{{"overall_impression":"Impression","overall_impression_simple":"Plain English","risk_level":"Low","risk_score":20,"ai_confidence":80,"urgency":"Routine","urgency_level":"Low","findings":[{{"name":"Finding","location":"Where","description":"Desc","probability":80,"severity":"Mild","clinical_significance":"Significance"}}],"brain_regions":{{"frontal_lobe":"Normal","temporal_lobe":"Normal","parietal_lobe":"Normal","occipital_lobe":"Normal","cerebellum":"Normal","brainstem":"Normal","hippocampus":"Normal","white_matter":"Normal","ventricles":"Normal","basal_ganglia":"Normal"}},"likely_diagnosis":"Diagnosis","differential_diagnoses":["d2"],"recommended_specialists":[{{"type":"Neurologist","urgency":"Routine","reason":"Why"}}],"recommended_tests":["MRI follow-up"],"red_flags":[],"lifestyle_advice":"Advice","follow_up_plan":"Plan"}}"""

                    payload = json.dumps({"model":"claude-sonnet-4-20250514","max_tokens":2000,"messages":[{"role":"user","content":[{"type":"image","source":{"type":"base64","media_type":"image/jpeg","data":img_b64}},{"type":"text","text":prompt}]}]}).encode()
                    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload, headers={"Content-Type":"application/json","anthropic-version":"2023-06-01","x-api-key":os.environ.get("ANTHROPIC_API_KEY","")}, method="POST")
                    with urllib.request.urlopen(req) as resp: raw = json.loads(resp.read())
                    text_out = raw["content"][0]["text"].strip().replace("```json","").replace("```","").strip()
                    st.session_state.brain_result = json.loads(text_out)
                except Exception as e:
                    st.error(f"Brain scan error: {e}")

    result = st.session_state.get("brain_result")
    if result:
        urg = result.get("urgency_level","Low")
        if   urg=="Emergency": st.error("🚨 EMERGENCY — Call 112 / 108 immediately.")
        elif urg=="High":      st.error(f"🚨 Urgent — {result.get('urgency','')}. Contact neurologist within 24–48 hrs.")
        elif urg=="Medium":    st.warning(f"⚠️ {result.get('urgency','')} — Schedule within 1–2 weeks.")
        else:                  st.success(f"✅ {result.get('urgency','')} — Discuss at next visit.")

        risk_score = result.get("risk_score",40); risk_level = result.get("risk_level","Moderate")
        conf = result.get("ai_confidence",80); findings_n = len(result.get("findings",[]))
        rl_color = {"Low":"green","Moderate":"amber","High":"red","Critical":"red"}.get(risk_level,"amber")

        k1,k2,k3,k4 = st.columns(4)
        for col,(num,lbl,color) in zip([k1,k2,k3,k4],[
            (risk_level,"Risk level",rl_color),(f"{conf}%","AI confidence","blue"),
            (findings_n,"Findings","purple" if findings_n else "green"),(urg,"Urgency",rl_color)
        ]):
            with col: col.markdown(f'<div class="metric-card {color}"><div class="metric-num" style="font-size:1.05rem">{num}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

        tab_f,tab_r,tab_t = st.tabs(["🔍 Findings","🧠 Brain Regions","💊 Treatment Plan"])

        with tab_f:
            col_fi,col_risk = st.columns([1.3,0.7])
            with col_fi:
                st.markdown('<div class="brain-card"><div class="brain-section-title">🔬 Detected Findings</div>', unsafe_allow_html=True)
                bar_clrs = {"Mild":"#f59e0b","Moderate":"#ef4444","Severe":"#b91c1c"}
                for f in result.get("findings",[]):
                    prob=f.get("probability",70); sev=f.get("severity","Moderate")
                    bc=bar_clrs.get(sev,"#ef4444")
                    st.markdown(f"""
                    <div style="margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.07)">
                      <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div><div style="font-weight:700;font-size:.95rem;color:#f0f6ff">{f.get("name","")}</div>
                          <div style="font-size:.78rem;color:#64748b;margin-top:2px">📍 {f.get("location","")}</div></div>
                        <span class="badge badge-red">{sev} · {prob}%</span>
                      </div>
                      <div class="finding-bar"><div class="finding-bar-fill" style="width:{prob}%;background:{bc}"></div></div>
                      <div style="font-size:.82rem;color:#94a3b8;margin-top:6px">{f.get("description","")}</div>
                      <div style="font-size:.78rem;background:rgba(217,119,6,0.15);color:#fcd34d;border-radius:8px;padding:6px 10px;margin-top:6px">💡 {f.get("clinical_significance","")}</div>
                    </div>""", unsafe_allow_html=True)
                if not result.get("findings"): st.success("✅ No significant findings detected.")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_risk:
                st.markdown(f"""
                <div class="brain-card">
                  <div class="brain-section-title">📋 Impression</div>
                  <p style="font-size:.88rem;color:#94a3b8;line-height:1.7">{result.get("overall_impression","")}</p>
                  <div style="background:rgba(5,150,105,0.15);border-radius:10px;padding:12px;margin-top:12px;border:1px solid rgba(16,185,129,0.2)">
                    <div style="font-weight:700;font-size:.82rem;color:#6ee7b7;margin-bottom:4px">🗣️ Plain English</div>
                    <p style="font-size:.82rem;color:#10b981;line-height:1.6;margin:0">{result.get("overall_impression_simple","")}</p>
                  </div>
                </div>
                <div class="brain-card {rl_color}">
                  <div class="brain-section-title">📊 Risk Score</div>
                  <div style="font-size:2rem;font-weight:800;color:#f0f6ff;font-family:'Sora',sans-serif">{risk_score}<span style="font-size:1rem;color:#64748b">/100</span></div>
                  <div class="severity-bar"><div class="severity-dot" style="left:{risk_score}%"></div></div>
                  <div style="display:flex;justify-content:space-between;font-size:.7rem;color:#475569;margin-top:4px"><span>Low</span><span>Moderate</span><span>High</span></div>
                  <div style="margin-top:10px;background:rgba(255,255,255,0.07);border-radius:8px;padding:10px 12px;font-size:.85rem;color:#f0f6ff;font-weight:600">{result.get("likely_diagnosis","")}</div>
                </div>""", unsafe_allow_html=True)

        with tab_r:
            regions = result.get("brain_regions",{})
            labels  = {"frontal_lobe":"Frontal","temporal_lobe":"Temporal","parietal_lobe":"Parietal","occipital_lobe":"Occipital","cerebellum":"Cerebellum","brainstem":"Brainstem","hippocampus":"Hippocampus","white_matter":"White Matter","ventricles":"Ventricles","basal_ganglia":"Basal Ganglia"}
            color_map = {"Normal":"green","Mildly abnormal":"amber","Abnormal":"red"}
            st.markdown('<div class="brain-card"><div class="brain-section-title">🧠 Brain Region Analysis</div>', unsafe_allow_html=True)
            rcols = st.columns(5)
            for i,(key,label) in enumerate(labels.items()):
                status = regions.get(key,"Normal")
                chip_c = color_map.get(status,"green")
                with rcols[i%5]:
                    st.markdown(f'<div class="region-chip {chip_c}" style="display:block;margin-bottom:10px"><div style="font-size:.82rem;font-weight:700">{label}</div><div style="font-size:.72rem;margin-top:2px">{status}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab_t:
            col_t1,col_t2 = st.columns(2)
            with col_t1:
                specs_html = "".join(f'<div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:12px 14px;margin-bottom:10px;border:1px solid rgba(255,255,255,0.08)"><div style="font-weight:700;color:#f0f6ff;font-size:.9rem">🩺 {s.get("type","")}</div><div style="font-size:.78rem;color:#64748b;margin-top:4px">{s.get("reason","")}</div></div>' for s in result.get("recommended_specialists",[]))
                st.markdown(f'<div class="brain-card purple"><div class="brain-section-title">👨‍⚕️ Recommended Specialists</div>{specs_html}</div>', unsafe_allow_html=True)
                if st.button("👨‍⚕️ Find Neurologist", key="brain_find_doc", use_container_width=True, type="primary"):
                    st.session_state.page = "👨‍⚕️ Find Doctors"; st.rerun()
            with col_t2:
                tests_html = "".join(f'<div style="padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.07);font-size:.85rem;color:#f0f6ff">🔬 {t}</div>' for t in result.get("recommended_tests",[]))
                st.markdown(f'<div class="brain-card"><div class="brain-section-title">🧪 Recommended Tests</div>{tests_html}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="brain-card green"><div class="brain-section-title">🥗 Lifestyle Advice</div><p style="font-size:.85rem;color:#94a3b8;line-height:1.7">{result.get("lifestyle_advice","")}</p></div>', unsafe_allow_html=True)

        if st.button("🔄 Analyze Another Scan", key="brain_reset", use_container_width=True):
            st.session_state.brain_result = None; st.rerun()
    else:
        if not brain_img:
            st.markdown("""
            <div class="ms-card" style="text-align:center;padding:50px 24px">
              <div style="font-size:3.5rem">🧠</div>
              <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:1.15rem;color:#f0f6ff;margin-top:14px">Upload a Brain Scan to Begin</div>
              <div style="color:#64748b;font-size:.9rem;margin-top:6px">AI analyzes CT, MRI, or PET scans for anomalies, lesions, and patterns</div>
              <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:20px">
                <span style="background:rgba(79,142,247,0.15);color:#93c5fd;padding:5px 14px;border-radius:20px;font-size:.8rem;font-weight:600">🧠 Hemorrhage detection</span>
                <span style="background:rgba(124,58,237,0.15);color:#c4b5fd;padding:5px 14px;border-radius:20px;font-size:.8rem;font-weight:600">🔍 Tumor / mass lesions</span>
                <span style="background:rgba(5,150,105,0.15);color:#6ee7b7;padding:5px 14px;border-radius:20px;font-size:.8rem;font-weight:600">📊 White matter analysis</span>
                <span style="background:rgba(185,28,28,0.15);color:#fca5a5;padding:5px 14px;border-radius:20px;font-size:.8rem;font-weight:600">⚡ Stroke indicators</span>
              </div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CHATBOT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💬 Health Chatbot":
    from utils.ai_analysis import chat_with_ai

    render_header("💬 Health Assistant Chatbot", "Ask about your report, symptoms, diet, medicines, or anything health-related", badge="🤖 AI Ready · Ask Anything")

    if not st.session_state.chat_messages:
        st.session_state.chat_messages.append({
            "role":"assistant",
            "content":"👋 Hello! I'm your MediScan health assistant. I can help you understand your report, explain test values, or answer general health questions. How can I help today?",
        })

    for msg in st.session_state.chat_messages:
        css = "chat-user" if msg["role"]=="user" else "chat-ai"
        st.markdown(f'<div class="{css}">{msg["content"]}</div>', unsafe_allow_html=True)

    st.markdown("---")
    qc = st.columns(4)
    quick_qs = ["What foods should I avoid?","Is my condition serious?","Which doctor should I see?","What lifestyle changes help?"]
    for i,q in enumerate(quick_qs):
        if qc[i].button(q, key=f"quick_{i}"):
            st.session_state.chat_messages.append({"role":"user","content":q})
            with st.spinner("Thinking…"):
                try:
                    reply = chat_with_ai(st.session_state.chat_messages, st.session_state.extracted_text)
                    st.session_state.chat_messages.append({"role":"assistant","content":reply})
                except Exception as e:
                    st.session_state.chat_messages.append({"role":"assistant","content":f"Error: {e}"})
            st.rerun()

    user_input = st.chat_input("Type your health question…")
    if user_input:
        st.session_state.chat_messages.append({"role":"user","content":user_input})
        with st.spinner("Thinking…"):
            try:
                reply = chat_with_ai(st.session_state.chat_messages, st.session_state.extracted_text)
                st.session_state.chat_messages.append({"role":"assistant","content":reply})
            except Exception as e:
                st.session_state.chat_messages.append({"role":"assistant","content":f"Error: {e}"})
        st.rerun()

    if st.button("🗑️ Clear chat"):
        st.session_state.chat_messages = []; st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FIND DOCTORS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "👨‍⚕️ Find Doctors":
    from utils.doctor_search import search_doctors_online, get_doctors

    render_header("👨‍⚕️ Find Nearby Doctors", "Real-time doctor search", badge="📍 Location-aware · Real-time Results")

    sc,lc = st.columns([2,1])
    with sc: specialty = st.selectbox("Specialty", ["Endocrinologist","Cardiologist","Haematologist","Neurologist","Neurosurgeon","Dermatologist","ENT Specialist","Pediatrician","Oncologist","General Physician"])
    with lc: location  = st.text_input("📍 City / area", value="Delhi, India")

    if st.button("🔍 Search Doctors", type="primary", use_container_width=True):
        with st.spinner(f"Searching {specialty}s near {location}…"):
            doctors = search_doctors_online(specialty, location)

        st.markdown(f'<div style="background:rgba(5,150,105,0.15);border:1px solid rgba(16,185,129,0.3);border-radius:10px;padding:10px 16px;margin-bottom:16px">✅ <b style="color:#6ee7b7">Found {len(doctors)} doctors</b></div>', unsafe_allow_html=True)
        for i,doc in enumerate(doctors):
            avatar_colors = [("rgba(30,58,138,0.4)","#93c5fd"),("rgba(5,95,70,0.4)","#6ee7b7"),("rgba(76,29,149,0.4)","#c4b5fd"),("rgba(120,53,15,0.4)","#fcd34d")]
            bg,fg = avatar_colors[i%len(avatar_colors)]
            initials = "".join(w[0] for w in doc["name"].split() if w)[:2].upper()
            st.markdown(f"""
            <div class="doc-card">
              <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px">
                <div class="doc-avatar" style="background:{bg};color:{fg}">{initials}</div>
                <div style="flex:1">
                  <div style="font-weight:700;font-size:1.05rem;color:#f0f6ff">{doc['name']}</div>
                  <div style="color:#64748b;font-size:.85rem">{doc['specialty']} · {doc.get('hospital','')}</div>
                  <div class="stars">{"★"*int(doc.get("rating",4))}{"☆"*(5-int(doc.get("rating",4)))} <span style="color:#64748b;font-size:.78rem">{doc.get("rating","4.5")}/5</span></div>
                </div>
                <div style="text-align:right">
                  <span class="badge badge-blue">{doc.get("mode","In-person")}</span><br>
                  <span style="font-size:.82rem;color:#64748b;margin-top:4px;display:block">{doc.get("fee","₹500–1000")}</span>
                </div>
              </div>
              <div style="font-size:.82rem;color:#94a3b8;margin-bottom:8px">{doc.get("summary","")}</div>
            </div>""", unsafe_allow_html=True)
            b1,b2,b3 = st.columns(3)
            if b1.button(f"📅 Book — {doc['name'][:15]}", key=f"book_{i}"):
                st.session_state.appointments.append({"doc":doc["name"],"spec":doc["specialty"],"date":"TBD","time":"TBD","mode":doc.get("mode","In-person")})
                st.success(f"Appointment requested for {doc['name']}!")
            b2.link_button("🌐 View profile", doc.get("url","https://practo.com"))
            b3.button(f"📞 {doc.get('phone','')[:14]}", key=f"call_{i}")
    else:
        st.markdown('<div class="ms-card"><div class="ms-card-title">📋 Sample Doctors Database</div>', unsafe_allow_html=True)
        for doc in get_doctors():
            c1,c2 = st.columns([3,1])
            c1.markdown(f"**{doc['name']}** — {doc['specialist']} · {doc['hospital']}")
            c2.write(doc["phone"])
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: APPOINTMENTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📅 Appointments":
    render_header("📅 Appointments", f"{len(st.session_state.appointments)} upcoming consultations", badge="📆 Schedule Manager")

    st.markdown('<div class="ms-card"><div class="ms-card-title">📌 Upcoming Appointments</div>', unsafe_allow_html=True)
    if st.session_state.appointments:
        for i,appt in enumerate(st.session_state.appointments):
            col_info,col_btns = st.columns([3,1])
            with col_info:
                mb = "badge-blue" if appt["mode"]=="Video" else "badge-green"
                st.markdown(f"""
                <div style="border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:13px 16px;margin-bottom:8px">
                  <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                      <span style="font-weight:700;color:#f0f6ff;font-size:.95rem">{appt['doc']}</span>
                      &nbsp;<span class="badge {mb}">{appt['mode']}</span>
                    </div>
                  </div>
                  <div style="font-size:.78rem;color:#64748b;margin-top:4px">{appt['spec']} · 📆 {appt['date']} · 🕐 {appt['time']}</div>
                </div>""", unsafe_allow_html=True)
            with col_btns:
                if st.button("❌ Cancel", key=f"cancel_{i}"):
                    st.session_state.appointments.pop(i); st.rerun()
    else:
        st.markdown('<p style="color:#64748b">No upcoming appointments.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ms-card"><div class="ms-card-title">➕ Book New Appointment</div>', unsafe_allow_html=True)
    with st.form("book_form"):
        doc_name  = st.text_input("Doctor name")
        specialty = st.selectbox("Specialty", ["Endocrinologist","Cardiologist","Haematologist","Neurologist","General Physician","Other"])
        appt_date = st.date_input("Date", min_value=date.today())
        appt_time = st.selectbox("Time slot", ["09:00 AM","10:00 AM","11:00 AM","12:00 PM","02:00 PM","03:00 PM","04:00 PM","05:00 PM"])
        mode      = st.radio("Mode", ["Video consult","In-person"], horizontal=True)
        submitted = st.form_submit_button("✅ Confirm Booking", type="primary")
        if submitted and doc_name:
            st.session_state.appointments.append({"doc":doc_name,"spec":specialty,"date":appt_date.strftime("%d %b %Y"),"time":appt_time,"mode":mode})
            st.success(f"Booked with {doc_name}!"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: REPORT HISTORY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📁 Report History":
    render_header("📁 Report History", f"{len(st.session_state.report_history)} documents stored", badge="🗂️ Document Vault")

    st.markdown('<div class="ms-card">', unsafe_allow_html=True)
    icon_map = {"pdf":"📄","jpg":"🖼️","jpeg":"🖼️","png":"🖼️","heic":"🖼️"}
    for i,rep in enumerate(st.session_state.report_history):
        col_icon,col_info,col_btns = st.columns([0.5,3,1.5])
        ext  = rep["name"].split(".")[-1].lower()
        icon = icon_map.get(ext,"📄")
        col_icon.markdown(f"<div style='font-size:1.6rem;padding-top:6px'>{icon}</div>", unsafe_allow_html=True)
        col_info.markdown(f"""
        <div>
          <div style="font-weight:700;color:#f0f6ff;font-size:.92rem">{rep['name']}</div>
          <div style="display:flex;gap:10px;margin-top:3px">
            <span style="background:rgba(79,142,247,0.15);color:#93c5fd;font-size:.68rem;padding:2px 8px;border-radius:10px">{rep['type']}</span>
            <span style="font-size:.72rem;color:#64748b">{rep['date']}</span>
          </div>
        </div>""", unsafe_allow_html=True)
        b1,b2 = col_btns.columns(2)
        if b1.button("👁️ View", key=f"view_{i}"):
            st.session_state.page = "🔬 AI Analysis"; st.rerun()
        if b2.button("🗑️", key=f"del_{i}"):
            st.session_state.report_history.pop(i); st.rerun()
        if i < len(st.session_state.report_history)-1:
            st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:6px 0'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EMERGENCY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🚨 Emergency":
    render_header("🚨 Emergency Assistance", "Quick access to emergency services and contacts", badge="🔴 24/7 Emergency Support")

    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(185,28,28,0.35),rgba(239,68,68,0.2));
                border:1px solid rgba(239,68,68,0.45);border-radius:14px;padding:16px 22px;margin-bottom:22px">
      <div style="font-weight:700;font-size:1rem;color:#fca5a5">⚠️ If life-threatening — call <span style="font-size:1.2rem">112</span> or <span style="font-size:1.2rem">108</span> immediately.</div>
    </div>""", unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="emr-card emr-red"><div class="emr-icon">🚑</div><div class="emr-title">Call Ambulance</div><div class="emr-sub">108 — Free 24/7</div></div>', unsafe_allow_html=True)
        if st.button("📞 Call 108 Ambulance", use_container_width=True): st.warning("Calling 108…")
        st.markdown('<div class="emr-card emr-amber"><div class="emr-icon">🆘</div><div class="emr-title">Alert Family</div><div class="emr-sub">Send SOS + GPS location</div></div>', unsafe_allow_html=True)
        if st.button("📨 Send SOS to Family", use_container_width=True): st.success("SOS sent to emergency contacts!")

    with col2:
        st.markdown('<div class="emr-card emr-blue"><div class="emr-icon">🏥</div><div class="emr-title">Nearest Hospital</div><div class="emr-sub">GPS-powered finder</div></div>', unsafe_allow_html=True)
        if st.button("📍 Find Nearest Hospital", use_container_width=True):
            st.markdown("[📍 Open Google Maps — Hospitals near me](https://www.google.com/maps/search/hospitals+near+me)")
        st.markdown('<div class="emr-card emr-teal"><div class="emr-icon">📹</div><div class="emr-title">Emergency Video Consult</div><div class="emr-sub">On-call doctor available now</div></div>', unsafe_allow_html=True)
        if st.button("🎥 Start Emergency Consult", use_container_width=True): st.info("Connecting to on-call doctor…")

    st.divider()
    st.markdown('<div class="ms-card"><div class="ms-card-title">📞 Emergency Numbers — India</div>', unsafe_allow_html=True)
    emr_data = {"National Ambulance":"108","Police":"100","Fire":"101","National Emergency":"112","Women's Helpline":"1091","Poison Control":"1800-11-6117","Mental Health (iCall)":"9152987821","AIIMS Delhi Emergency":"011-26588500"}
    ec1,ec2 = st.columns(2)
    items = list(emr_data.items())
    for k,v in items[:4]:
        ec1.markdown(f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.06)"><span style="color:#94a3b8;font-size:.85rem">{k}</span><span style="font-weight:700;color:#93c5fd">{v}</span></div>', unsafe_allow_html=True)
    for k,v in items[4:]:
        ec2.markdown(f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.06)"><span style="color:#94a3b8;font-size:.85rem">{k}</span><span style="font-weight:700;color:#93c5fd">{v}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ms-card"><div class="ms-card-title">👤 My Emergency Contacts</div>', unsafe_allow_html=True)
    with st.form("add_contact"):
        cc1,cc2,cc3 = st.columns(3)
        name  = cc1.text_input("Name")
        phone = cc2.text_input("Phone")
        rel   = cc3.text_input("Relation")
        if st.form_submit_button("➕ Add Contact") and name:
            st.success(f"Added {name} ({rel}) as emergency contact!")
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ABOUT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "ℹ️ About":
    render_header("ℹ️ About MediScan AI", "AI-powered health analysis platform", badge="v2.0 · Dark Gradient Edition")
    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="ms-card">
          <div class="ms-card-title">🧬 Features</div>
          <div style="display:flex;flex-direction:column;gap:8px">
            <div style="background:rgba(79,142,247,0.1);border:1px solid rgba(79,142,247,0.2);border-radius:8px;padding:9px 14px;font-size:.85rem;color:#93c5fd">📤 OCR medical report extraction</div>
            <div style="background:rgba(79,142,247,0.1);border:1px solid rgba(79,142,247,0.2);border-radius:8px;padding:9px 14px;font-size:.85rem;color:#93c5fd">🔬 AI disease analysis (Groq LLaMA 3.3 70B)</div>
            <div style="background:rgba(124,58,237,0.1);border:1px solid rgba(168,85,247,0.2);border-radius:8px;padding:9px 14px;font-size:.85rem;color:#c4b5fd">🩹 Skin condition analysis (Claude Vision)</div>
            <div style="background:rgba(124,58,237,0.1);border:1px solid rgba(168,85,247,0.2);border-radius:8px;padding:9px 14px;font-size:.85rem;color:#c4b5fd">🧠 Brain scan AI analysis (Claude Vision)</div>
            <div style="background:rgba(5,150,105,0.1);border:1px solid rgba(16,185,129,0.2);border-radius:8px;padding:9px 14px;font-size:.85rem;color:#6ee7b7">💬 Conversational health chatbot</div>
            <div style="background:rgba(5,150,105,0.1);border:1px solid rgba(16,185,129,0.2);border-radius:8px;padding:9px 14px;font-size:.85rem;color:#6ee7b7">👨‍⚕️ Real-time doctor search</div>
            <div style="background:rgba(217,119,6,0.1);border:1px solid rgba(245,158,11,0.2);border-radius:8px;padding:9px 14px;font-size:.85rem;color:#fcd34d">📅 Appointment management</div>
            <div style="background:rgba(185,28,28,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:8px;padding:9px 14px;font-size:.85rem;color:#fca5a5">🚨 Emergency assistance panel</div>
          </div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="ms-card">
          <div class="ms-card-title">🛠️ Technologies</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:9px 12px;font-size:.82rem;color:#94a3b8"><b style="color:#f0f6ff">Streamlit</b><br>UI framework</div>
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:9px 12px;font-size:.82rem;color:#94a3b8"><b style="color:#f0f6ff">Groq API</b><br>LLaMA 3.3 70B</div>
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:9px 12px;font-size:.82rem;color:#94a3b8"><b style="color:#f0f6ff">Anthropic Claude</b><br>Vision AI</div>
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:9px 12px;font-size:.82rem;color:#94a3b8"><b style="color:#f0f6ff">Tavily API</b><br>Doctor search</div>
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:9px 12px;font-size:.82rem;color:#94a3b8"><b style="color:#f0f6ff">Tesseract OCR</b><br>Text extraction</div>
            <div style="background:rgba(255,255,255,0.05);border-radius:8px;padding:9px 12px;font-size:.82rem;color:#94a3b8"><b style="color:#f0f6ff">ReportLab</b><br>PDF generation</div>
          </div>
        </div>
        <div style="background:rgba(217,119,6,0.12);border:1px solid rgba(245,158,11,0.25);border-radius:12px;padding:14px 18px;margin-top:12px;font-size:.8rem;color:#fcd34d">
          ⚠️ <b>Disclaimer:</b> AI analysis is for informational purposes only. Always consult a qualified medical professional.
        </div>""", unsafe_allow_html=True)