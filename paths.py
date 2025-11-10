from pathlib import Path
import streamlit as st

APP_DIR = Path(__file__).parent
ASSETS  = APP_DIR / "assets"

def asset_path(*parts) -> Path:
    """Resolve a file in ./assets, warn if missing."""
    p = ASSETS.joinpath(*parts)
    if not p.exists():
        st.warning(f"Missing asset: {p}")
    return p
