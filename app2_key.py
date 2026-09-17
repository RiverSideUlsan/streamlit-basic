import streamlit as st

from app2_access import (
    SECURITY_NOTICE,
    get_api_key,
    register_api_key,
    require_login,
)


require_login()


st.title("🔑 OpenAI API 키 등록")
st.warning(SECURITY_NOTICE)
st.caption("키는 브라우저의 현재 로그인 세션에만 보관하며, 채팅 DB에는 저장하지 않습니다.")

api_key = st.text_input("OpenAI API 키", type="password", placeholder="sk-...")
if st.button("키 등록", type="primary"):
    if api_key.strip():
        register_api_key(api_key)
        st.success("현재 로그인 세션에 API 키를 등록했습니다.")
    else:
        st.info("OpenAI API 키를 입력해 주세요.")

if get_api_key():
    st.page_link("app2_chat.py", label="채팅 시작", icon="💬")
