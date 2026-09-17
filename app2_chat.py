import os

import streamlit as st
from openai import OpenAI

from app2_access import get_api_key, get_user_id, require_api_key, require_login
from chat_store import create_session, get_session, list_sessions, list_turns, save_turn
from persona_store import load_persona


PERSONAS = {
    "dawon": {
        "label": "다온 · 직장인 여성",
        "image": "assets/female-casual-hi.png",
        "images": {
            "hi": "assets/female-casual-hi.png",
            "listen": "assets/female-casual-listen.png",
            "think": "assets/female-casual-think.png",
            "agree": "assets/female-casual-agree.png",
        },
        "file_name": "다온.md",
    },
    "junho": {
        "label": "준호 · 직장인 남성",
        "image": "assets/male-casual-hi.png",
        "images": {
            "hi": "assets/male-casual-hi.png",
            "listen": "assets/male-casual-listen.png",
            "think": "assets/male-casual-think.png",
            "agree": "assets/male-casual-agree.png",
        },
        "file_name": "준호.md",
    },
}


def character_image(persona_config, mood="hi"):
    return persona_config["images"].get(mood, persona_config["image"])


@st.dialog("새 채팅: 대화상대 선택")
def show_persona_selector(user_id):
    st.write("대화할 캐릭터를 선택하세요.")

    columns = st.columns(len(PERSONAS))
    for column, (persona_id, persona_config) in zip(columns, PERSONAS.items()):
        persona = load_persona(persona_config)
        with column:
            st.image(character_image(persona_config), width="stretch")
            st.subheader(persona["label"])
            st.caption(persona["intro"])
            if st.button(
                "이 캐릭터와 시작",
                key=f"start_chat_{persona_id}",
                type="primary",
                width="stretch",
            ):
                st.session_state.active_chat_session_id = create_session(
                    user_id,
                    persona=persona_id,
                )
                st.rerun()


def session_label(session_id, sessions):
    session = next(row for row in sessions if row["id"] == session_id)
    persona_config = PERSONAS.get(session["persona"], PERSONAS["dawon"])
    persona = load_persona(persona_config)
    return f"{persona['label']} · {session['title']}"


require_login()
require_api_key()

user_id = get_user_id()
sessions = list_sessions(user_id)

if "active_chat_session_id" not in st.session_state and sessions:
    st.session_state.active_chat_session_id = sessions[0]["id"]

with st.sidebar:
    st.subheader("채팅")
    if st.button("새 채팅", type="primary", width="stretch"):
        show_persona_selector(user_id)
        st.stop()

    character_image_slot = st.empty()

    if sessions:
        session_ids = [row["id"] for row in sessions]
        selected_session_id = st.selectbox(
            "대화 선택",
            session_ids,
            index=session_ids.index(st.session_state.active_chat_session_id)
            if st.session_state.active_chat_session_id in session_ids
            else 0,
            format_func=lambda session_id: session_label(session_id, sessions),
        )
        st.session_state.active_chat_session_id = selected_session_id

    model_name = st.selectbox(
        "모델 선택",
        [os.getenv("OPENAI_MODEL", "gpt-5.6-luna"), "gpt-5.5", "gpt-5-mini"],
    )

if "active_chat_session_id" not in st.session_state:
    show_persona_selector(user_id)
    st.stop()

session_id = st.session_state.active_chat_session_id
session = get_session(user_id, session_id)
if not session:
    del st.session_state.active_chat_session_id
    show_persona_selector(user_id)
    st.stop()

persona_config = PERSONAS.get(session["persona"], PERSONAS["dawon"])
persona = load_persona(persona_config)
turns = list_turns(user_id, session_id)
reaction_state_key = f"character_mood_{session_id}"
if reaction_state_key not in st.session_state:
    st.session_state[reaction_state_key] = (
        turns[-1]["assistant_mood"] if turns else "hi"
    )

character_image_slot.image(
    character_image(persona_config, st.session_state[reaction_state_key]),
    width=170,
)

st.title(f"💬 {persona['label']}와 채팅")
st.caption(persona["intro"])
st.warning("민감한 개인정보나 비밀번호는 입력하지 마세요.")

for turn in turns:
    with st.chat_message("user"):
        st.markdown(turn["user_text"])
        if turn["file_name"]:
            st.caption(f"첨부 파일: {turn['file_name']}")
    with st.chat_message(
        "assistant",
        avatar=character_image(persona_config, turn["assistant_mood"]),
    ):
        st.markdown(turn["assistant_text"])

with st.bottom:
    uploaded_file = st.file_uploader(
        "텍스트 파일 첨부 (선택)",
        type=["txt", "md", "py", "csv", "json"],
    )
    prompt = st.chat_input(f"{persona['label']}에게 메시지를 입력하세요")

if prompt:
    st.session_state[reaction_state_key] = "listen"
    character_image_slot.image(character_image(persona_config, "listen"), width=170)

    file_name = uploaded_file.name if uploaded_file else None
    file_content = (
        uploaded_file.getvalue().decode("utf-8", errors="replace")
        if uploaded_file
        else None
    )
    user_message = prompt
    if file_content:
        user_message += f"\n\n[첨부 파일: {file_name}]\n{file_content}"

    messages = [{"role": "system", "content": persona["system"]}]
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
        st.session_state[reaction_state_key] = "think"
        character_image_slot.image(character_image(persona_config, "think"), width=170)
        with st.chat_message(
            "assistant",
            avatar=character_image(persona_config, "think"),
        ):
            stream = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=True,
            )
            assistant_text = st.write_stream(stream)
    except Exception as error:
        st.session_state[reaction_state_key] = "hi"
        character_image_slot.image(character_image(persona_config), width=170)
        st.error(f"AI 응답을 받지 못했습니다. {error}")
    else:
        st.session_state[reaction_state_key] = "agree"
        character_image_slot.image(character_image(persona_config, "agree"), width=170)
        save_turn(
            user_id,
            session_id,
            prompt,
            assistant_text,
            file_name=file_name,
            file_content=file_content,
            assistant_mood="agree",
        )
        st.rerun()
