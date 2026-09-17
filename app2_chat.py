import os

import streamlit as st
from openai import OpenAI

from app2_access import get_api_key, get_user_id, require_api_key, require_login
from chat_store import create_session, get_session, list_sessions, list_turns, save_turn


require_login()
require_api_key()

user_id = get_user_id()
sessions = list_sessions(user_id)

if "active_chat_session_id" not in st.session_state and sessions:
    st.session_state.active_chat_session_id = sessions[0]["id"]

with st.sidebar:
    st.subheader("내 채팅 세션")
    if st.button("새 채팅", type="primary"):
        st.session_state.active_chat_session_id = create_session(user_id)
        st.rerun()

    if sessions:
        session_ids = [row["id"] for row in sessions]
        selected_session_id = st.selectbox(
            "대화 선택",
            session_ids,
            index=session_ids.index(st.session_state.active_chat_session_id)
            if st.session_state.active_chat_session_id in session_ids
            else 0,
            format_func=lambda session_id: next(
                row["title"] for row in sessions if row["id"] == session_id
            ),
        )
        st.session_state.active_chat_session_id = selected_session_id

if "active_chat_session_id" not in st.session_state:
    st.session_state.active_chat_session_id = create_session(user_id)

session_id = st.session_state.active_chat_session_id
if not get_session(user_id, session_id):
    st.session_state.active_chat_session_id = create_session(user_id)
    session_id = st.session_state.active_chat_session_id

turns = list_turns(user_id, session_id)

st.title("💬 AI 채팅")
st.caption("세션당 최근 100개의 질문·답변 묶음만 저장됩니다.")
st.warning("민감한 개인정보나 비밀번호는 입력하지 마세요.")

for turn in turns:
    with st.chat_message("user"):
        st.markdown(turn["user_text"])
        if turn["file_name"]:
            st.caption(f"첨부 파일: {turn['file_name']}")
    with st.chat_message("assistant"):
        st.markdown(turn["assistant_text"])

uploaded_file = st.file_uploader(
    "텍스트 파일 첨부 (선택)",
    type=["txt", "md", "py", "csv", "json"],
)

model_name = st.selectbox(
    "모델",
    [os.getenv("OPENAI_MODEL", "gpt-5.6-luna"), "gpt-5.5", "gpt-5-mini"],
)
prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    file_name = uploaded_file.name if uploaded_file else None
    file_content = (
        uploaded_file.getvalue().decode("utf-8", errors="replace")
        if uploaded_file
        else None
    )
    user_message = prompt
    if file_content:
        user_message += f"\n\n[첨부 파일: {file_name}]\n{file_content}"

    messages = []
    for turn in turns:
        messages.append({"role": "user", "content": turn["user_text"]})
        messages.append({"role": "assistant", "content": turn["assistant_text"]})
    messages.append({"role": "user", "content": user_message})

    with st.chat_message("user"):
        st.markdown(prompt)
        if file_name:
            st.caption(f"첨부 파일: {file_name}")

    try:
        client = OpenAI(api_key=get_api_key())
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=True,
            )
            assistant_text = st.write_stream(stream)
    except Exception as error:
        st.error(f"AI 응답을 받지 못했습니다: {error}")
    else:
        save_turn(
            user_id,
            session_id,
            prompt,
            assistant_text,
            file_name=file_name,
            file_content=file_content,
        )
        st.rerun()
