from pathlib import Path

import streamlit as st


try:
    is_logged_in = st.user.is_logged_in
except AttributeError:
    st.title("로그인 설정이 필요합니다")
    st.info(
        "`.streamlit/secrets.example.toml`을 `secrets.toml`로 복사한 뒤, "
        "Google OAuth 정보를 입력하세요."
    )
    st.code(
        "Copy-Item .streamlit/secrets.example.toml .streamlit/secrets.toml",
        language="powershell",
    )
    st.stop()

if not is_logged_in:
    st.title("로그인이 필요합니다")
    st.write("계속하려면 Google 계정으로 로그인하세요.")

    if st.button("Google로 로그인", type="primary"):
        st.login("google")

    st.stop()

with st.sidebar:
    st.caption(f"로그인 사용자: {st.user.name}")
    if st.button("로그아웃"):
        st.logout()

HOME_PAGE_PATH = Path(__file__).with_name("home.py")
NAVIGATION_PAGE_PATH = Path(__file__).with_name("navigation_demo.py")
ACCOUNT_PAGE_PATH = Path(__file__).with_name("account.py")

HOME_PAGE = st.Page(
    HOME_PAGE_PATH,
    title="홈",
    icon=":material/home:",
    default=True,
)
NAVIGATION_PAGE = st.Page(
    NAVIGATION_PAGE_PATH,
    title="내비게이션 기능",
    icon=":material/route:",
)
ACCOUNT_PAGE = st.Page(
    ACCOUNT_PAGE_PATH,
    title="내 계정",
    icon=":material/account_circle:",
)
DOCUMENTATION_PAGE = st.Page(
    "https://docs.streamlit.io/develop/api-reference/navigation",
    title="공식 문서",
    icon=":material/menu_book:",
)

current_page = st.navigation(
    {
        "": [HOME_PAGE],
        "학습": [NAVIGATION_PAGE],
        "계정": [ACCOUNT_PAGE],
        "참고": [DOCUMENTATION_PAGE],
    },
    position="top",
)
current_page.run()

