# app.py
import base64
import re
from pathlib import Path

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

from paths import asset_path

# ──────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dylan Sturdevant — Investment Research & Analytics",
    layout="wide",
    menu_items={"Get help": None, "Report a bug": None, "About": None},
)

# PDFs bundled in ./assets/pdf/
PDFS = {
    "Resume": asset_path("pdf", "Dylan_Sturdevant_Resume.pdf"),
    "Strategy Snapshot": asset_path("pdf", "Strategy_Snapshot.pdf"),
    "Leading Indicators Brief": asset_path("pdf", "Leading_Indicators.pdf"),
    "Financial Conditions Indexes": asset_path("pdf", "Financial_Conditions_Indexes.pdf"),
    "Global Multi-Asset Strategy Evaluation": asset_path("pdf", "Global_Multi_Asset_Strategy_Evaluation.pdf"),
}

# HTML snapshots bundled in ./assets/html/
HTMLS = {
    "Q1": asset_path("html", "CAGR_per_quad_nophase_Q1.html"),
    "Q2": asset_path("html", "CAGR_per_quad_nophase_Q2.html"),
    "Q3": asset_path("html", "CAGR_per_quad_nophase_Q3.html"),
    "Q4": asset_path("html", "CAGR_per_quad_nophase_Q4.html"),
    "Daily Quad Consensus Counts": asset_path("html", "Daily_Quad_Consensus_Counts.html"),
    "Snapshot 63d Rolling CAGR": asset_path("html", "Snapshot_63d_RollingCAGR.html"),
    "Snapshot MAD 20/50": asset_path("html", "Snapshot_MAD_20_50.html"),
    "Snapshot Stoch %D": asset_path("html", "Snapshot_Stoch_D.html"),
}

IMG_STRATEGY = asset_path("img", "Dorian_Road_Investment_Strategy.jpg")

# ──────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────
def pdf_button(label: str, file_path: Path, key: str):
    if file_path.exists():
        st.download_button(
            label=f"📄 {label}",
            data=file_path.read_bytes(),
            file_name=file_path.name,
            mime="application/pdf",
            key=key,
        )
    else:
        st.caption(f"⚠ {label} not found: `{file_path}`")

def show_html(path: Path, height: int = 520):
    """Embed a Plotly HTML export responsively with tight margins."""
    if not path.exists():
        st.caption(f"⚠ HTML not found: {path}")
        return
    raw = path.read_text(encoding="utf-8")
    # Make width fluid, fix height
    for w in ("width: 1600px", "width:1500px", "width:1200px"):
        raw = raw.replace(w, "width: 100%")
    raw = (raw
           .replace('width="1600"', 'width="100%"')
           .replace('width="1500"', 'width="100%"')
           .replace('width="1200"', 'width="100%"')
           .replace('height="900"', f'height="{height}"')
           .replace("height: 900px", f"height: {height}px"))
    # Strip outer wrappers (if present)
    raw = re.sub(r"<!DOCTYPE html>.*?<body[^>]*>", "", raw, flags=re.S)
    raw = re.sub(r"</body>\s*</html>\s*$", "", raw, flags=re.S)
    # Tighten margins
    tighten_css = """
    <style>
      html, body { margin:0!important; padding:0!important; background:transparent!important; }
      .plot-container, .svg-container, .main-svg, .plotly, .plotly-graph-div { margin:0!important; padding:0!important; }
    </style>
    """
    wrapper = f'{tighten_css}<div style="overflow-x:auto; margin:0; border:1px solid rgba(139,94,60,.2); border-radius:12px; box-shadow:0 6px 18px rgba(0,0,0,.08);">{raw}</div>'
    components.html(wrapper, height=height + 20, scrolling=False)

def centered_image(img_path: Path, caption: str | None = None, width: int = 700, nudge_left_px: int = -24):
    if not img_path.exists():
        st.caption(f"⚠ Image not found: {img_path}")
        return
    encoded = base64.b64encode(img_path.read_bytes()).decode()
    st.markdown(
        f"""
        <div style="text-align:center; margin-left:{nudge_left_px}px;">
            <img src="data:image/jpeg;base64,{encoded}" width="{width}" style="border-radius:12px;margin-top:10px;"/>
            {f'<div style="color:#9fb3c8;font-size:13px;margin-top:4px;">{caption}</div>' if caption else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────
# THEME
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
      :root { --bg:#0B1220; --card:#0f172a; --muted:#9fb3c8; }
      .stApp { background: var(--bg) !important; color: #fff !important; }
      .card {
        background: var(--card); border-radius: 16px; padding: 16px;
        border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 10px 30px rgba(0,0,0,0.25);
      }
      .muted { color: var(--muted); }
      .pill {
        display:inline-block; padding: 4px 10px; border-radius: 999px;
        background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.35);
        color: #cfe0ff; font-size: 12px; margin-right: 8px;
      }
      hr { border: none; height: 1px; background: rgba(255,255,255,0.08); margin: 12px 0; }
      h3 { text-align:center; margin-top:20px; margin-bottom:10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
st.sidebar.markdown("### Portfolio Microsite")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Framework", "Dashboards", "Project Highlights"],
)

# ──────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="card" style="padding:28px; text-align:center;">
      <h1 style="margin-bottom:6px;">Dylan Sturdevant</h1>
      <div style="color:#9fb3c8; font-size:18px;">Macro & Multi-Asset Research | Systematic Investment Frameworks</div>
      <hr style="margin:14px auto; width:60%; height:1px; background:rgba(255,255,255,0.1);">
      <div style="color:#9fb3c8; font-size:14px;">
        Linking leading indicators, factor tilts, and market structure to portfolio allocation decisions.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────
# PAGES
# ──────────────────────────────────────────────────────────────
if page == "Overview":
    col1, col2 = st.columns([1.1, 1])
    with col1:
        st.subheader("What I build")
        st.markdown(
            "- Empirical frameworks that quantify how shifts in growth and inflation momentum define economic regimes.\n"
            "- Dashboards that monitor leading indicators, financial conditions, and asset behavior through each regime.\n"
            "- Tools for testing hypotheses about macro drivers and forecasting regime transitions."
        )
        st.caption("This microsite provides a concise overview of my research frameworks and tools for easy internal review.")
    with col2:
        st.subheader("Downloads")
        for label, fp in PDFS.items():
            pdf_button(label, fp, key=f"ov-{label}")

elif page == "Framework":
    # bullets + image
    st.markdown(
        """
        <style>
          .bullet-wrap h4{ margin:0 0 10px 0; font-weight:700; font-size:18px; }
          .bullet-wrap ul{ margin:0; padding-left:22px; line-height:1.65; }
          .bullet-wrap ul li{ font-size:16px; font-weight:600; color:#f3f6fa; margin-bottom:6px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(
            """
            <div class="bullet-wrap" style="display:flex; align-items:center; min-height:500px;">
              <div>
                <h4>How economic regimes are defined</h4>
                <ul>
                  <li>Identify directional momentum of growth and inflation</li>
                  <li>Classify environments by acceleration/deceleration of these signals</li>
                  <li>Quad 1 (Goldilocks): growth up, inflation down</li>
                  <li>Quad 2 (Reflation): growth up, inflation up</li>
                  <li>Quad 3 (Stagflation): growth down, inflation up</li>
                  <li>Quad 4 (Deflation): growth down, inflation down</li>
                </ul>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        centered_image(IMG_STRATEGY, width=700, nudge_left_px=-24)

    # Historical treemaps (CAGR per quad, no phase)
    for q, title in [("Q1","Quad 1 (Goldilocks)"), ("Q2","Quad 2 (Reflation)"),
                     ("Q3","Quad 3 (Stagflation)"), ("Q4","Quad 4 (Deflation)")]:
        if HTMLS[q].exists():
            st.markdown(f"### {title}")
            show_html(HTMLS[q], height=520)

    st.subheader("Financial Conditions Indexes (FCIs)")
    st.markdown(
        "- Forecast growth and inflation with economic indicators & market ratios.\n"
        "- Use Granger causality and lead–lag filters to isolate predictive variables.\n"
        "- Combine via linear models + nonlinear Machine Learning to form composite leading indexes.\n"
        "- Emphasize directional accuracy to anticipate macro turns."
    )

    st.subheader("PDF Downloads")
    pdf_button("Strategy Snapshot", PDFS["Strategy Snapshot"], key="fw-ss")
    pdf_button("Leading Indicator Examples", PDFS["Leading Indicators Brief"], key="fw-li")
    pdf_button("Financial Conditions Indexes", PDFS["Financial Conditions Indexes"], key="fw-fci")

elif page == "Dashboards":
    st.subheader("Daily Dashboards")

    # Daily Quad Consensus
    if HTMLS["Daily Quad Consensus Counts"].exists():
        st.markdown("### Daily Quad Consensus Counts")
        show_html(HTMLS["Daily Quad Consensus Counts"], height=520)

    # 63d Rolling CAGR
    if HTMLS["Snapshot 63d Rolling CAGR"].exists():
        st.markdown("### 63-Day Rolling CAGR Snapshot")
        show_html(HTMLS["Snapshot 63d Rolling CAGR"], height=520)

    # MAD 20/50
    if HTMLS["Snapshot MAD 20/50"].exists():
        st.markdown("### Moving-Average Distance (MAD 20/50)")
        show_html(HTMLS["Snapshot MAD 20/50"], height=520)

    # Stoch %D
    if HTMLS["Snapshot Stoch %D"].exists():
        st.markdown("### Stochastic %D Snapshot")
        show_html(HTMLS["Snapshot Stoch %D"], height=520)

elif page == "Project Highlights":
    st.markdown("### Case Studies")
    g1, g2 = st.columns(2)
    with g2:
        st.markdown("**Behavioral Performance Study: Persistence vs. Reversal Dynamics**")

        st.markdown(
        """
        <a href="https://factor-attribution.streamlit.app/" target="_blank"
           style="display:inline-block; background-color:rgba(255,255,255,0.05);
                  border:1px solid rgba(255,255,255,0.25);
                  border-radius:8px; padding:10px 16px;
                  text-decoration:none; color:#cfe0ff;
                  font-weight:500; font-size:14px; margin-bottom:10px;">
           🌐 Open Live Streamlit App
        </a>
        """,
        unsafe_allow_html=True,
    )

        st.markdown(
            "Task: Test two competing theories of market behavior among S&P 500 constituents (as of Oct 2024) between Q4 2024 and Q1 2025\n"
            "- Momentum hypothesis: Stocks that recently outperformed will continue to outperform\n"
            "- Mean reversion hypothesis: Stocks that recently outperformed will underperform"
        )

    
    with g2:
        st.markdown("**Behavioral Performance Study: Persistence vs. Reversal Dynamics**")

        st.markdown(
        """
        <a href="https://behavorialperformancestudy.streamlit.app/" target="_blank"
           style="display:inline-block; background-color:rgba(255,255,255,0.05);
                  border:1px solid rgba(255,255,255,0.25);
                  border-radius:8px; padding:10px 16px;
                  text-decoration:none; color:#cfe0ff;
                  font-weight:500; font-size:14px; margin-bottom:10px;">
           🌐 Open Live Streamlit App
        </a>
        """,
        unsafe_allow_html=True,
    )

        st.markdown(
            "Task: Test two competing theories of market behavior among S&P 500 constituents (as of Oct 2024) between Q4 2024 and Q1 2025\n"
            "- Momentum hypothesis: Stocks that recently outperformed will continue to outperform\n"
            "- Mean reversion hypothesis: Stocks that recently outperformed will underperform"
        )




elif page == "Contact / Downloads":
    st.subheader("Contact")
    st.write("Email: dylsturdevant@gmail.com")
    st.write("LinkedIn: https://www.linkedin.com/in/dylansturdevant")
    st.divider()
    st.subheader("Bundle Download")
    # (Optional) If you add a combined packet PDF later:
    # pdf_button("Portfolio Packet", asset_path("pdf","Portfolio_Packet.pdf"), key="dl-pack")

# Footer
st.markdown("<hr style='margin-top:30px;'/>", unsafe_allow_html=True)
