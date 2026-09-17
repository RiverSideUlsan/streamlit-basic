import streamlit as st

from app2_access import logout, require_login
from chat_store import init_database


st.set_page_config(page_title="배포형 AI 채팅", page_icon="💬", layout="wide")

init_database()
require_login()

page = st.navigation(
    {
        "채팅": [
            st.Page("app2_chat.py", title="AI 채팅", icon="💬", default=True),
        ],
        "관리": [
            st.Page("app2_key.py", title="API 키 등록", icon="🔑"),
            st.Page("app2_history.py", title="대화 내역", icon="🕘"),
        ],
    },
    position="sidebar",
)

with st.sidebar:
    st.divider()
    if st.button("로그아웃"):
        logout()
        st.rerun()

page.run()
