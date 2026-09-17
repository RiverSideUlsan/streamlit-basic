import sqlite3
from pathlib import Path

import streamlit as st

DB_PATH = Path(__file__).resolve().with_name("chat_history.db")

st.title("🕘 과거 채팅 내역")
st.caption("app2.py에서 SQLite에 저장한 채팅 기록을 읽기 전용으로 보여 줍니다.")


def load_history():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, role, content_text, image_bytes, file_name, file_content, created_at
        FROM messages
        ORDER BY id DESC
        """
    )
    messages = cursor.fetchall()
    connection.close()
    return messages


messages = load_history()
st.metric("저장된 메시지", f"{len(messages)}개")

if not messages:
    st.info("저장된 채팅 내역이 없습니다.")

for message_id, role, text, image_bytes, file_name, file_content, created_at in messages:
    with st.container(border=True):
        st.caption(f"기록 #{message_id} · {created_at}")

        with st.chat_message(role):
            if text:
                st.markdown(text)
            if image_bytes:
                st.image(image_bytes, width=300)
            if file_name:
                st.caption(f"첨부 파일: {file_name}")
            if file_content:
                with st.expander("첨부 파일 내용 보기"):
                    st.code(file_content)
