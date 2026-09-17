import streamlit as st

st.set_page_config(page_title="OpenAI 멀티모달 챗봇", page_icon="🤖", layout="wide")

page = st.navigation(
    {
        "채팅": [
            st.Page(
                "app2_chat.py",
                title="OpenAI 멀티모달 챗봇",
                icon=":material/chat:",
                default=True,
            ),
        ],
        "기록": [
            st.Page(
                "app2_history.py",
                title="과거 채팅 내역",
                icon=":material/history:",
            ),
        ],
    },
    position="sidebar",
)

page.run()
