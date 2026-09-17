"""app2의 로그인과 API 키 접근 제어를 담당합니다."""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


ENV_PATH = Path(__file__).resolve().with_name(".env")
load_dotenv(ENV_PATH)
KEY_STATE_NAME = "registered_openai_api_key"
DEV_LOGIN_ENABLED = os.getenv("STREAMLIT_DEV_LOGIN", "").lower() == "true"
DEV_USER_ID = os.getenv("STREAMLIT_DEV_USER_ID", "local-developer")

SECURITY_NOTICE = (
    "이 앱에 입력한 내용은 외부 AI 서비스로 전송되고 채팅 DB에 저장됩니다. "
    "배포나 접근 제어 설정에 문제가 있으면 대화가 노출될 위험이 있습니다. "
    "주민등록번호, 비밀번호, 결제 정보 등 민감한 정보는 입력하지 마세요."
)


def is_logged_in():
    return DEV_LOGIN_ENABLED or bool(getattr(st.user, "is_logged_in", False))


def is_development_login():
    return DEV_LOGIN_ENABLED


def require_login():
    if is_logged_in():
        return

    st.title("로그인")
    st.warning(SECURITY_NOTICE)
    st.write("채팅과 대화 내역은 로그인한 사용자만 사용할 수 있습니다.")
    st.button("로그인", type="primary", on_click=st.login)
    st.stop()


def get_user_id():
    if DEV_LOGIN_ENABLED:
        return f"development:{DEV_USER_ID}"

    claims = st.user.to_dict()
    provider = claims.get("iss", "oidc")
    subject = claims.get("sub") or claims.get("email")
    return f"{provider}:{subject}"


def get_api_key():
    return st.session_state.get(KEY_STATE_NAME)


def require_api_key():
    if get_api_key():
        return

    st.title("OpenAI API 키 등록 필요")
    st.warning("채팅을 시작하려면 로그인 세션에 OpenAI API 키를 등록해야 합니다.")
    st.page_link("app2_key.py", label="API 키 등록으로 이동", icon="🔑")
    st.stop()


def register_api_key(api_key):
    st.session_state[KEY_STATE_NAME] = api_key.strip()


def register_local_env_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        register_api_key(api_key)
        return True
    return False


def clear_api_key():
    st.session_state.pop(KEY_STATE_NAME, None)
