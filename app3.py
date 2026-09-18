from pathlib import Path

import streamlit as st


APP_PAGE = Path(__file__).with_name("stream_pages") / "main.py"
app = st.App(APP_PAGE)

if __name__ == "__main__":
    app.run()
