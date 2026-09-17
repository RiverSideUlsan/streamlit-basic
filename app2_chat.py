import base64
import os
import sqlite3
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

ENV_PATH = Path(__file__).resolve().with_name(".env")
load_dotenv(ENV_PATH)
api_key = os.getenv("OPENAI_API_KEY")

st.title("🤖 OpenAI 멀티모달 AI 챗봇")
st.caption("SQLite 데이터베이스 대화 복원 및 이미지 모달 팝업 첨부 기능이 포함된 챗봇입니다.")

DB_PATH = "chat_history.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content_text TEXT,
            image_bytes BLOB,
            file_name TEXT,
            file_content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def load_messages_from_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content_text, image_bytes, file_name, file_content "
        "FROM messages ORDER BY id ASC"
    )
    rows = cursor.fetchall()
    conn.close()

    messages = []
    for role, text, img, fname, fcontent in rows:
        messages.append(
            {
                "role": role,
                "content_text": text,
                "image_bytes": img,
                "file_name": fname,
                "file_content": fcontent,
            }
        )
    return messages


def save_message_to_db(
    role,
    content_text="",
    image_bytes=None,
    file_name=None,
    file_content=None,
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO messages (role, content_text, image_bytes, file_name, file_content)
        VALUES (?, ?, ?, ?, ?)
        """,
        (role, content_text, image_bytes, file_name, file_content),
    )
    conn.commit()
    conn.close()


def clear_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()


def get_message_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM messages")
    count = cursor.fetchone()[0]
    conn.close()
    return count


init_db()

if "messages" not in st.session_state:
    st.session_state.messages = load_messages_from_db()

if "pending_image" not in st.session_state:
    st.session_state.pending_image = None

if "pending_file" not in st.session_state:
    st.session_state.pending_file = None


@st.dialog("🖼️ 이미지 첨부 (드래그 앤 드롭)")
def upload_image_dialog():
    st.write("이미지 파일을 아래 영역에 **드래그 앤 드롭**하거나 선택해주세요.")
    uploaded_img = st.file_uploader(
        "이미지 파일 선택",
        type=["png", "jpg", "jpeg", "webp"],
        key="modal_img_file",
    )

    if uploaded_img is not None:
        img_bytes = uploaded_img.read()
        st.image(img_bytes, caption="미리보기", width=300)

        col1, col2 = st.columns(2)
        if col1.button("✅ 첨부 완료", type="primary", use_container_width=True):
            st.session_state.pending_image = {
                "name": uploaded_img.name,
                "bytes": img_bytes,
            }
            st.toast("이미지가 첨부되었습니다.")
            st.rerun()

        if col2.button("취소", use_container_width=True):
            st.rerun()


with st.sidebar:
    st.header("⚙️ 챗봇 설정")
    st.caption("OpenAI API Key는 .env의 OPENAI_API_KEY 환경변수를 사용합니다.")

    model_options = [
        "gpt-5.5",
        "gpt-5",
        "gpt-5-mini",
        "o3-mini",
        "o1",
        "gpt-4o",
        "gpt-4o-mini",
        "직접 입력",
    ]
    selected_option = st.selectbox("사용할 모델", model_options, index=0)

    if selected_option == "직접 입력":
        model_name = st.text_input("모델명 입력", value="gpt-5.5")
    else:
        model_name = selected_option

    st.divider()
    st.write("💾 **데이터베이스 및 채팅 기록 관리**")
    db_count = get_message_count()
    st.caption(f"현재 DB 저장된 메시지: **{db_count}개**")

    if st.button("📂 이전 채팅 내역 불러오기", use_container_width=True):
        st.session_state.messages = load_messages_from_db()
        st.success("SQLite에서 이전 채팅 기록을 불러왔습니다.")
        st.rerun()

    if st.button("✨ 새 대화 시작 (화면 비우기)", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_image = None
        st.session_state.pending_file = None
        st.rerun()

    if st.button("🗑️ SQLite 전체 기록 삭제", use_container_width=True):
        clear_db()
        st.session_state.messages = []
        st.session_state.pending_image = None
        st.session_state.pending_file = None
        st.success("데이터베이스의 모든 대화 기록이 삭제되었습니다.")
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("content_text"):
            st.markdown(msg["content_text"])
        if msg.get("image_bytes"):
            st.image(msg["image_bytes"], width=300)
        if msg.get("file_name"):
            st.caption(f"📎 첨부파일: {msg['file_name']}")

st.divider()
col_img_btn, col_file_btn, col_status = st.columns(
    [1.5, 1.5, 4],
    vertical_alignment="center",
)

with col_img_btn:
    if st.button("🖼️ 이미지 첨부 (팝업)", use_container_width=True):
        upload_image_dialog()

with col_file_btn:
    with st.popover("📁 문서/파일 첨부", use_container_width=True):
        st.write("텍스트 또는 소스코드 파일을 첨부하세요.")
        uploaded_doc = st.file_uploader(
            "파일 선택",
            type=["txt", "py", "csv", "json", "md"],
            key="doc_uploader",
        )
        if uploaded_doc is not None:
            doc_text = uploaded_doc.read().decode("utf-8", errors="ignore")
            st.session_state.pending_file = {
                "name": uploaded_doc.name,
                "content": doc_text,
            }
            st.success(f"'{uploaded_doc.name}' 파일이 준비되었습니다.")

with col_status:
    tags = []
    if st.session_state.pending_image:
        tags.append(f"🖼️ 이미지: `{st.session_state.pending_image['name']}`")
    if st.session_state.pending_file:
        tags.append(f"📁 파일: `{st.session_state.pending_file['name']}`")

    if tags:
        st.info("첨부 대기 중: " + " | ".join(tags))
        if st.button("❌ 첨부 취소", key="cancel_attachments"):
            st.session_state.pending_image = None
            st.session_state.pending_file = None
            st.rerun()

prompt = st.chat_input("메시지를 입력하세요...")

if prompt:
    if not api_key:
        st.warning("`.env` 파일에 OPENAI_API_KEY를 설정해주세요.")
        st.stop()

    client = OpenAI(api_key=api_key)
    user_text = prompt
    image_data = st.session_state.pending_image
    file_data = st.session_state.pending_file

    image_bytes_to_store = image_data["bytes"] if image_data else None
    file_name_to_store = file_data["name"] if file_data else None
    file_content_to_store = file_data["content"] if file_data else None

    with st.chat_message("user"):
        st.markdown(user_text)
        if image_bytes_to_store:
            st.image(image_bytes_to_store, width=300)
        if file_name_to_store:
            st.caption(f"📎 첨부파일: {file_name_to_store}")

    save_message_to_db(
        "user",
        user_text,
        image_bytes_to_store,
        file_name_to_store,
        file_content_to_store,
    )
    st.session_state.messages.append(
        {
            "role": "user",
            "content_text": user_text,
            "image_bytes": image_bytes_to_store,
            "file_name": file_name_to_store,
            "file_content": file_content_to_store,
        }
    )

    st.session_state.pending_image = None
    st.session_state.pending_file = None

    formatted_api_messages = []
    for message in st.session_state.messages:
        if message["role"] == "user":
            content_list = []
            if message.get("content_text"):
                content_list.append({"type": "text", "text": message["content_text"]})
            if message.get("file_name") and message.get("file_content"):
                content_list.append(
                    {
                        "type": "text",
                        "text": f"\n[첨부파일({message['file_name']}) 내용]:\n{message['file_content']}",
                    }
                )
            if message.get("image_bytes"):
                b64_img = base64.b64encode(message["image_bytes"]).decode("utf-8")
                content_list.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64_img}"},
                    }
                )
            formatted_api_messages.append(
                {
                    "role": "user",
                    "content": content_list if content_list else message["content_text"],
                }
            )
        else:
            formatted_api_messages.append(
                {"role": "assistant", "content": message["content_text"]}
            )

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=model_name,
            messages=formatted_api_messages,
            stream=True,
        )
        response_text = st.write_stream(stream)

    save_message_to_db("assistant", response_text)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content_text": response_text,
            "image_bytes": None,
            "file_name": None,
            "file_content": None,
        }
    )
