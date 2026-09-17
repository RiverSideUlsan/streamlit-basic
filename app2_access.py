"""app2의 로그인과 API 키 접근 제어를 담당합니다."""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from auth_store import authenticate_user, create_user, init_user_database


KEY_STATE_NAME = "registered_openai_api_key"
KEY_SOURCE_STATE_NAME = "openai_api_key_source"
LOGIN_STATE_NAME = "logged_in_username"
ENV_FILE_PATH = Path(__file__).with_name(".env")

SECURITY_NOTICE = (
    "이 앱에 입력한 내용은 외부 AI 서비스로 전송되고 채팅 DB에 저장됩니다. "
    "주민등록번호, 비밀번호, 결제 정보 등 민감한 정보는 입력하지 마세요."
)


def is_logged_in():
    return LOGIN_STATE_NAME in st.session_state


def require_login():
    if is_logged_in():
        return

    init_user_database()
    st.title("로그인")
    st.warning(SECURITY_NOTICE)
    login_tab, register_tab = st.tabs(["로그인", "회원가입"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("아이디")
            password = st.text_input("비밀번호", type="password")
            submitted = st.form_submit_button("로그인", type="primary")

        if submitted:
            if authenticate_user(username, password):
                st.session_state[LOGIN_STATE_NAME] = username.strip()
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 맞지 않습니다.")

    with register_tab:
        with st.form("register_form", clear_on_submit=True):
            username = st.text_input("새 아이디")
            password = st.text_input("새 비밀번호", type="password")
            submitted = st.form_submit_button("회원가입", type="primary")

        if submitted:
            if create_user(username, password):
                st.success("회원가입이 완료되었습니다. 로그인해 주세요.")
            else:
                st.error(
                    "아이디는 비어 있을 수 없고, 비밀번호는 8자 이상이어야 합니다. "
                    "이미 사용 중인 아이디인지도 확인해 주세요."
                )

    st.stop()


def get_user_id():
    return f"sqlite:{st.session_state[LOGIN_STATE_NAME]}"


def get_username():
    return st.session_state[LOGIN_STATE_NAME]


def logout():
    st.session_state.pop(LOGIN_STATE_NAME, None)
    clear_api_key()
    st.session_state.pop("user_persona_input", None)
    st.session_state.pop("user_persona_example", None)


def get_api_key():
    return st.session_state.get(KEY_STATE_NAME)


def require_api_key():
    if get_api_key():
        return

    st.title("OpenAI API 키 등록 필요")
    st.warning("채팅을 시작하려면 로그인 세션에 OpenAI API 키를 등록해야 합니다.")
    st.page_link("app2_mypage.py", label="마이페이지로 이동", icon="👤")
    st.stop()


def register_api_key(api_key):
    st.session_state[KEY_STATE_NAME] = api_key.strip()
    st.session_state[KEY_SOURCE_STATE_NAME] = "direct"


def register_env_api_key():
    load_dotenv(ENV_FILE_PATH)
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return False

    st.session_state[KEY_STATE_NAME] = api_key
    st.session_state[KEY_SOURCE_STATE_NAME] = "env"
    return True


def clear_api_key():
    st.session_state.pop(KEY_STATE_NAME, None)
    st.session_state.pop(KEY_SOURCE_STATE_NAME, None)
