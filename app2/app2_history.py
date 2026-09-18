import streamlit as st

from app2.app2_access import get_user_id, require_login
from app2.chat_store import list_sessions, list_turns


require_login()

user_id = get_user_id()
sessions = list_sessions(user_id)

st.title("🕘 대화 내역")
st.caption("현재 로그인한 계정의 대화만 확인할 수 있습니다.")

if not sessions:
    st.info("저장된 대화가 없습니다. 채팅에서 새 대화를 시작해 주세요.")
    st.stop()

session_ids = [row["id"] for row in sessions]
session_id = st.selectbox(
    "확인할 세션",
    session_ids,
    format_func=lambda selected_id: next(
        row["title"] for row in sessions if row["id"] == selected_id
    ),
)
turns = list_turns(user_id, session_id)
st.metric("저장된 질문·답변", f"{len(turns)} / 100")

for turn in turns:
    with st.container(border=True):
        st.caption(turn["created_at"])
        with st.chat_message("user"):
            st.markdown(turn["user_text"])
            if turn["file_name"]:
                st.caption(f"첨부 파일: {turn['file_name']}")
        with st.chat_message("assistant"):
            st.markdown(turn["assistant_text"])
        if turn["file_content"]:
            with st.expander("첨부 파일 내용 보기"):
                st.code(turn["file_content"])
