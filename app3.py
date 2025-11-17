# app.py
import math
import base64
from pathlib import Path
import re
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import streamlit.components.v1 as components  # for embedding saved HTMLs

# ──────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dylan Sturdevant — Investment Research & Analytics",
    layout="wide",
    menu_items={"Get help": None, "Report a bug": None, "About": None},
)

PDFS = {
    "Resume": "assets/pdf/Dylan_Sturdevant_Resume.pdf",
    "Strategy Snapshot": "assets/pdf/Strategy_Snapshot.pdf",
    "Leading Indicators Brief": "assets/pdf/Leading_Indicators.pdf",
    "Financial Conditions Indexes": "assets/pdf/Financial_Conditions_Indexes.pdf",
}

def pdf_button(label: str, file_path: str, key: str):
    p = Path(file_path)
    if p.exists():
        st.download_button(
            label=f"📄 {label}",
            data=p.read_bytes(),
            file_name=p.name,
            mime="application/pdf",
            key=key,
        )
    else:
        st.caption(f"⚠ {label} not found: `{file_path}`")

def show_html(path: Path, height: int = 400, scrolling: bool = False):
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            components.html(f.read(), height=height, scrolling=scrolling)
    else:
        st.caption(f"⚠ HTML not found: {path}")

def centered_image(img_path: Path, caption: str | None = None, width: int = 480, nudge_left_px: int = 0):
    if not img_path.exists():
        st.caption(f"⚠ Image not found: {img_path}")
        return
    encoded = base64.b64encode(img_path.read_bytes()).decode()
    st.markdown(
        f"""
        <div style="text-align:center; margin-left:{nudge_left_px}px;">
            <img src="data:image/jpeg;base64,{encoded}"
                 width="{width}"
                 style="border-radius:12px;margin-top:10px;"/>
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
      .kpi {
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.12);
        padding: 14px; border-radius: 14px;
      }
      .pill {
        display:inline-block; padding: 4px 10px; border-radius: 999px;
        background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.35);
        color: #cfe0ff; font-size: 12px; margin-right: 8px;
      }
      hr { border: none; height: 1px; background: rgba(255,255,255,0.08); margin: 12px 0; }
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
    ["Overview", "Framework", "Dashboards", "Project Highlights", ],
)
privacy = False

def redact(value, mask="—"):
    return mask if privacy else value

# ──────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="card" style="padding:28px; text-align:center;">
      <h1 style="margin-bottom:6px;">Dylan Sturdevant</h1>
      <div style="color:#9fb3c8; font-size:18px;">
        Macro & Multi-Asset Research | Systematic Research & Investment Analytics
      </div>
      <hr style="margin:14px auto; width:60%; border:0; height:1px; background:rgba(255,255,255,0.1);">
      <div style="color:#9fb3c8; font-size:14px;">
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
            "- Dashboards and analytics that monitor leading indicators, financial conditions, and asset behavior through each regime.\n"
            "- Data-driven tools for testing hypotheses about macro drivers and forecasting regime transitions."
        )
        st.caption("This microsite provides a concise overview of my research frameworks and tools for easy internal review.")
    with col2:
        st.subheader("Downloads")
        for label, fp in PDFS.items():
            pdf_button(label, fp, key=f"ov-{label}")

elif page == "Framework":
    st.markdown(
        "<h3 style='text-align:center; margin-top:20px; margin-bottom:10px;'>Quadrant Framework</h3>",
        unsafe_allow_html=True,
    )
    #st.caption("Objective, structured, testable.")

    # paths
    img_path  = Path("assets/img/Dorian_Road_Investment_Strategy.jpg")
    html_path_1 = Path("assets/html/CAGR_per_quad_nophase_Q1.html")
    html_path_2 = Path("assets/html/CAGR_per_quad_nophase_Q2.html")
    html_path_3 = Path("assets/html/CAGR_per_quad_nophase_Q3.html")
    html_path_4 = Path("assets/html/CAGR_per_quad_nophase_Q4.html")



    # tuning knobs
    IMG_WIDTH = 700          # image size
    IMG_HEIGHT_APPROX = 500   # used to vertically center bullets
    NUDGE_LEFT_PX = -24       # move image a bit left

    # --- bullet styling (font, weight, size, spacing, color) ---
    st.markdown(
        """
        <style>
          .bullet-wrap h4{
            margin:0 0 10px 0;
            font-weight:700;          /* heading weight */
            font-size:18px;           /* heading size */
          }
          .bullet-wrap ul{
            margin:0;
            padding-left:22px;
            line-height:1.65;         /* line spacing */
          }
          .bullet-wrap ul li{
            font-size:16px;           /* <<< bullet size */
            font-weight:600;          /* <<< 400=normal, 600=semibold, 700=bold */
            color:#f3f6fa;            /* <<< bullet color */
            margin-bottom:6px;        /* space between bullets */
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # side-by-side: bullets LEFT (vertically centered), image RIGHT (bigger, nudged left)
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown(
            f"""
            <div class="bullet-wrap" style="display:flex; align-items:center; min-height:{IMG_HEIGHT_APPROX}px;">
              <div>
                <h4>How economic regimes are defined</h4>
                <ul>
                  <li>Identify the directional momentum of growth and inflation</li>
                  <li>Macro environments are classified by whether these signals are accelerating/decelerating</li>
                  <li>If growth remains strong while inflation momentum fades, <br> we identify Quad 1 (Goldilocks)</li>
                  <li>When the direction of both growth and inflation is rising, we classify the environment as Quad 2 (Reflation)</li>
                  <li>When growth is falling and inflation is rising, the regime shifts to Quad 3 (Stagflation)</li>
                  <li>If both growth and inflation are decelerating, we enter Quad 4 (Deflation)</li>
                </ul>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    with col2:
        centered_image(img_path, width=IMG_WIDTH, nudge_left_px=NUDGE_LEFT_PX)

    # HTML treemap BELOW both
    def embed_plotly_html_responsive(path: Path, height=520):
        raw = path.read_text(encoding="utf-8")
        # common fixed-width patterns -> make fluid
        for w in ("width: 1600px", "width:1500px", "width:1200px"):
            raw = raw.replace(w, "width: 100%")
        raw = (raw
               .replace('width="1600"', 'width="100%"')
               .replace('width="1500"', 'width="100%"')
               .replace('width="1200"', 'width="100%"')
               .replace('height="900"', f'height="{height}"')
               .replace("height: 900px", f"height: {height}px"))
        html = f'<div style="overflow-x:auto; margin:0 -8px 0 0;">{raw}</div>'
        components.html(html, height=height + 40, scrolling=False)


    st.markdown(
        "<h3 style='text-align:center; margin-top:30px; margin-bottom:10px;'>Historical Quadrant Performance</h3>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        .tooltip {
          position: relative;
          display: inline-block;
          cursor: help;
          color: #cfe0ff;
          border: 1px solid rgba(255,255,255,.18);
          border-radius: 999px;
          padding: 6px 12px;
          font-size: 13px;
        }
        .tooltip .tooltiptext {
          visibility: hidden;
          width: 280px;
          background-color: #1f2937;
          color: #f9fafb;
          text-align: left;
          border-radius: 6px;
          padding: 8px 10px;
          position: absolute;
          z-index: 1;
          bottom: 125%;
          left: 50%;
          margin-left: -140px;
          opacity: 0;
          transition: opacity 0.25s;
          border: 1px solid rgba(255,255,255,.15);
          box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .tooltip:hover .tooltiptext {
          visibility: visible;
          opacity: 1;
        }
        </style>

        <div style="text-align:center; margin-top:8px;">
          <div class="tooltip">ℹ︎ Note — Treemap Interaction
            <span class="tooltiptext">
              <b>Plotly Treemap Tips</b><br>
              • Size scales with number of observations in quadrant as more observations --> greater confidence in relationship holding<br>
              • Click a category (e.g., “Commodities”) to zoom into its components.<br>
              • Click the top gray bar to navigate back to the full view.<br>
              • Hover over tiles for detailed stats (CAGR, Volatility, Sharpe, Observations).<br>
              • Use the color scale to compare performance across assets.
            </span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # usage
    if html_path_1.exists():
        st.markdown(
            "<h3 style='text-align:center; margin-top:10px; margin-bottom:10px;'>Quad 1 (Goldilocks)</h3>",
            unsafe_allow_html=True,
        )
        embed_plotly_html_responsive(html_path_1, height=520)


    if html_path_2.exists():
        st.markdown(
            "<h3 style='text-align:center; margin-top:10px; margin-bottom:10px;'>Quad 2 (Reflation)</h3>",
            unsafe_allow_html=True,
        )
        embed_plotly_html_responsive(html_path_2, height=520)

    if html_path_3.exists():
        st.markdown(
            "<h3 style='text-align:center; margin-top:10px; margin-bottom:10px;'>Quad 3 (Stagflation)</h3>",
            unsafe_allow_html=True,
        )
        embed_plotly_html_responsive(html_path_3, height=520)

    if html_path_4.exists():
        st.markdown(
            "<h3 style='text-align:center; margin-top:10px; margin-bottom:10px;'>Quad 4 (Deflation)</h3>",
            unsafe_allow_html=True,
        )
        embed_plotly_html_responsive(html_path_4, height=520)

    st.subheader("Financial Conditions Indexes (FCIs)")
    st.markdown(
        "- Forecast growth and inflation using hundreds of economic indicators and market ratios.\n"
        "- Apply Granger causality and lead–lag filters to isolate truly predictive variables.\n"
        "- Combine signals through linear regression and nonlinear ML models to form composite leading indexes.\n"
        "- Emphasize directional accuracy over numeric precision — what matters is anticipating macro turns, not chasing decimal points."
    )

    st.subheader("Data to Allocation")

    st.markdown(
        """
        - The economic quad framework directly informs portfolio tilts and risk allocation.  
        - Tilt toward asset classes with favorable risk/reward profiles in each regime, guided by backtests and live signals.  
        - Prioritize capital preservation during regime transitions; reduce exposure to vulnerable assets.  
        - The real edge lies in anticipating regime shifts before they become consensus.  
        <br>
        <span style="color:gray; font-size:0.9em;">
            More detail and methodology can be seen in the PDF downloads below
        </span>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("**PDF Downloads**")
    pdf_button("Brief Strategy Snapshot", PDFS["Strategy Snapshot"], key="fw-ss")
    pdf_button("Leading Indicator Examples", PDFS["Leading Indicators Brief"], key="fw-li")
    pdf_button("Financial Conditions Indexes", PDFS["Financial Conditions Indexes"], key="fw-fci")


elif page == "Factor Attribution":
    l, r = st.columns([1, 1])
    with l:
        st.subheader("Attribution (demo)")
        factors = ["Value", "Quality", "Momentum", "Size", "EM Exposure"]
        contrib = [0.35, 0.20, -0.05, 0.08, 0.12]
        fig_bar = px.bar(
            x=factors,
            y=[None if privacy else v for v in contrib],
            labels={"x": "Factor", "y": "Active Return (bps)"}
        )
        fig_bar.update_layout(
            height=360, margin=dict(l=40, r=20, t=30, b=40),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#9fb3c8"),
            yaxis=dict(color="#9fb3c8", gridcolor="rgba(255,255,255,.06)"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.caption("Replace with your actual attribution output (by period, by regime).")
    with r:
        st.subheader("Notes")
        st.markdown(
            "- Python pipeline (pandas/NumPy/Plotly); outputs to CSV/JSON/PDF.\n"
            "- Decompose active return by **style, sector, selection**; slice by macro regime.\n"
            "- Useful for explaining performance alignment with regime tilts."
        )
        st.markdown("**Docs**")
        pdf_button("Attribution Summary", PDFS["Attribution Summary"], key="fa-doc")

elif page == "Dashboards":
    st.subheader("Daily Dashboards")

    st.markdown(
        """
        Automated dashboards combine **technical analysis** with **macro regime forecasts** to show how markets behave across different economic environments.  
        They help confirm whether asset trends align with the projected quad, or diverge early.

        <br>
        Each panel highlights a different layer of market structure: rolling momentum, relative positioning, or cyclical timing.  
        Together, they create a real-time lens for how liquidity, sentiment, and risk appetite evolve within and between quads.  
                
        <br>
        <br>
        <span style="color:gray; font-size:0.9em;">
            These charts represent just a few examples of the dashboards I monitor daily.  
            Each snapshot is compared against its historical behavior to infer which economic quad the market is pricing in  
            and how far along we are within that regime. Also cross-checked against my Financial Conditions Indexes (FCIs) for confirmation.
        </span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
          .bullet-wrap h4{
            margin:0 0 10px 0;
            font-weight:700;          /* heading weight */
            font-size:18px;           /* heading size */
          }
          .bullet-wrap ul{
            margin:0;
            padding-left:22px;
            line-height:1.65;         /* line spacing */
          }
          .bullet-wrap ul li{
            font-size:16px;           /* <<< bullet size */
            font-weight:600;          /* <<< 400=normal, 600=semibold, 700=bold */
            color:#f3f6fa;            /* <<< bullet color */
            margin-bottom:6px;        /* space between bullets */
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
    <style>
    .tooltip {
      position: relative;
      display: inline-block;
      cursor: help;
      color: #cfe0ff;
      border: 1px solid rgba(255,255,255,.18);
      border-radius: 999px;
      padding: 6px 12px;
      font-size: 13px;
      margin: 0 6px;
    }
    .tooltip .tooltiptext {
      visibility: hidden;
      width: 280px;
      background-color: #1f2937;
      color: #f9fafb;
      text-align: left;
      border-radius: 6px;
      padding: 8px 10px;
      position: absolute;
      z-index: 1;
      bottom: 125%;
      left: 50%;
      margin-left: -140px;
      opacity: 0;
      transition: opacity 0.25s;
      border: 1px solid rgba(255,255,255,.15);
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .tooltip:hover .tooltiptext {
      visibility: visible;
      opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)


    def embed_plotly_html_responsive(path: Path, height=520):
        raw = path.read_text(encoding="utf-8")

        # 1) Make width fluid + fix height
        for w in ("width: 1600px", "width:1500px", "width:1200px"):
            raw = raw.replace(w, "width: 100%")
        raw = (raw
               .replace('width="1600"', 'width="100%"')
               .replace('width="1500"', 'width="100%"')
               .replace('width="1200"', 'width="100%"')
               .replace('height="900"', f'height="{height}"')
               .replace("height: 900px", f"height: {height}px"))

        # 2) Strip outer <html>/<body> wrappers if present to avoid their margins
        raw = re.sub(r"<!DOCTYPE html>.*?<body[^>]*>", "", raw, flags=re.S)  # remove head+open body
        raw = re.sub(r"</body>\s*</html>\s*$", "", raw, flags=re.S)  # remove close tags

        # 3) Nuke trailing whitespace blocks commonly found at the end
        raw = re.sub(r"(\s|&nbsp;|<br\s*/?>|<p>\s*</p>)+$", "", raw, flags=re.S)

        # 4) Remove any inline bottom margins/paddings that add gap
        raw = re.sub(r"margin-bottom\s*:\s*\d+px;?", "margin-bottom:0;", raw, flags=re.I)
        raw = re.sub(r"padding-bottom\s*:\s*\d+px;?", "padding-bottom:0;", raw, flags=re.I)

        # 5) Tighten common Plotly containers
        tighten_css = """
        <style>
          html, body { margin:0!important; padding:0!important; background:transparent!important; }
          .plot-container, .svg-container, .main-svg, .plotly, .plotly-graph-div {
            margin:0!important; padding:0!important;
          }
        </style>
        """

        wrapper = (
            f'{tighten_css}'
            f'<div style="overflow-x:auto; margin:0; border:1px solid rgba(139,94,60,.2);'
            f' border-radius:12px; box-shadow:0 6px 18px rgba(0,0,0,.08);">{raw}</div>'
        )
        components.html(wrapper, height=height + 20, scrolling=False)


    html_path_1 = Path(
        "assets/html/Daily_Quad_Consensus_Counts.html")
    html_path_2 = Path(
        "assets/html/Snapshot_63d_RollingCAGR.html")
    html_path_3 = Path(
        "assets/html/Snapshot_MAD_20_50.html")
    html_path_4 = Path(
        "assets/html/Snapshot_Stoch_D.html")


    if html_path_1.exists():
        st.markdown(
            "<h3 style='text-align:center; margin-top:10px; margin-bottom:10px;'>Daily Quad Consensus Counts</h3>",
            unsafe_allow_html=True,
        )
        embed_plotly_html_responsive(html_path_1, height=520)

    st.markdown("""
    <div style="text-align:center; margin-top:8px;">
      <div class="tooltip">ℹ︎ Note — Chart Interaction
        <span class="tooltiptext">
          <b>Line Chart Interactivity Tips</b><br>
          • Drag to zoom into a custom date range.<br>
          • Single-click a legend item to hide that series.<br>
          • Double-click a legend item to isolate it.<br>
          • Double-click the background to reset view.<br>
          • Single/double-click again to toggle lines back on.
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if html_path_2.exists():
        st.markdown(
            "<h3 style='text-align:center; margin-top:10px; margin-bottom:10px;'>63-Day Rolling CAGR Snapshot</h3>",
            unsafe_allow_html=True,
        )
        embed_plotly_html_responsive(html_path_2, height=520)

    st.markdown("""
    <div style="text-align:center; margin-top:8px;">
      <div class="tooltip">ℹ︎ MAD 20/50
        <span class="tooltiptext">
          <b>Moving Average Distance (20/50)</b><br>
          • Ratio of the 20-day SMA to the 50-day SMA.<br>
          • Values >1 indicate short-term momentum above the medium-term trend.<br>
          • Highlights assets with strengthening or weakening momentum.
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if html_path_3.exists():
        st.markdown(
            "<h3 style='text-align:center; margin-top:10px; margin-bottom:10px;'>Moving-Average Distance (MAD 20/50)</h3>",
            unsafe_allow_html=True,
        )
        embed_plotly_html_responsive(html_path_3, height=520)

    st.markdown("""
    <div style="text-align:center; margin-top:8px;">
      <div class="tooltip">ℹ︎ Stoch %D
        <span class="tooltiptext">
          <b>Stochastic %D</b><br>
          • Derived from <b>%K</b>, which tracks where price closes relative to its 14-day high-low range.<br>
          • %D = 3-day Simple Moving Average of %K → smoother, less noisy signal.<br>
          • Used to confirm momentum shifts: crossovers above/below %D often mark short-term turns.
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if html_path_4.exists():
        st.markdown(
            "<h3 style='text-align:center; margin-top:10px; margin-bottom:10px;'>Stochastic %D Snapshot</h3>",
            unsafe_allow_html=True,
        )
        embed_plotly_html_responsive(html_path_4, height=520)


elif page == "Project Highlights":
    st.markdown(
        "<h3 style='text-align:center; margin-top:20px; margin-bottom:10px;'>Case Studies</h3>",
        unsafe_allow_html=True,
    )
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown("**Factor Attribution & Regime-Aware Exposures**")

        st.markdown(
        """
        <a href="https://factor-attribution.streamlit.app/" target="_blank"
           style="display:inline-block; background-color:rgba(255,255,255,0.05);
                  border:1px solid rgba(255,255,255,0.25);
                  border-radius:8px; padding:10px 16px;
                  text-decoration:none; color:#cfe0ff;
                  font-weight:500; font-size:14px; margin-bottom:10px;">
           🌐 Open Factor Attribution App
        </a>
        """,
        unsafe_allow_html=True,
    )
        
        st.markdown(
            "- Interactive multi-factor dashboard that decomposes fund and ETF returns into systematic exposures across 20+ macro, style, and cross-asset factors (Equity, Rates, Credit, Commodities, FX, Carry, Trend, Inflation, etc.).\n"
            "- Tracks both static and rolling betas to reveal how exposures evolve through market cycles, identifying regime shifts and drivers of performance or drawdown.\n"
            "- Includes Plotly visualizations, current beta snapshots, and automated ranking of high-variance factors to highlight where portfolio behavior is changing most rapidly."
            )

    with g2: 
    st.markdown("**Deviation & BVOL Case Study: Regime-Conditioned Signal Behavior**")

        st.markdown(
        """
        <a href="https://dylan-s-blackwater-case-study.streamlit.app/" target="_blank"
           style="display:inline-block; background-color:rgba(255,255,255,0.05);
                  border:1px solid rgba(255,255,255,0.25);
                  border-radius:8px; padding:10px 16px;
                  text-decoration:none; color:#cfe0ff;
                  font-weight:500; font-size:14px; margin-bottom:10px;">
           🌐 Open BVOL Case Study
        </a>
        """,
        unsafe_allow_html=True,
    )
        
        st.markdown(
            " Analyze how extreme deviation readings and BVOL spikes relate to short-term forward returns, and test whether these signals can form a systematic trading strategy on XRT.\n"
            "- **Deviation analysis**: Built scatterplots of 20-day forward returns vs. deviation levels, fitted trend lines, and calculated hit rates across deviation buckets.\n"
            "- **Deviation backtest**: Tested +2.0 deviation triggers with a 30-day cooldown, evaluating 60-day event-aligned performance, hit rates, and trade-level Sharpe ratios.\n"
            "- **BVOL strategy**: Designed a short-horizon XRT strategy using BVOL percentile/z-score signals and optimized stop-loss rules (fixed % and ATR-based) with historical statistics.."
            )

    
    with g3:
        st.markdown("**Behavioral Performance Study: Persistence vs. Reversal Dynamics**")
        st.link_button("🌐 Open Behavorial Performance App", "https://behavorialperformancestudy.streamlit.app/")
        st.markdown(
            " Test two competing theories of market behavior among S&P 500 constituents (as of Oct 2024) between Q4 2024 and Q1 2025\n"
            "- Momentum hypothesis: Stocks that recently outperformed will continue to outperform\n"
            "- Mean reversion hypothesis: Stocks that recently outperformed will underperform"
        )


elif page == "Contact / Downloads":
    st.subheader("Contact")
    st.write("Email: dylsturdevant@gmail.com")
    st.write("LinkedIn: https://www.linkedin.com/in/dylansturdevant")
    st.divider()
    st.subheader("Bundle Download")
    pdf_button("Portfolio Packet", PDFS["Portfolio Packet"], key="dl-pack")
    st.caption("Prefer a PDF? Download the one-pager pack. Numbers can be shared privately.")



# Footer
st.markdown("<hr style='margin-top:30px;'/>", unsafe_allow_html=True)
