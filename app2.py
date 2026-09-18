from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).parent
APP_PAGE = PROJECT_ROOT / "stream_pages" / "main.py"

app = st.App(APP_PAGE)

if __name__ == "__main__":
    app.run()
