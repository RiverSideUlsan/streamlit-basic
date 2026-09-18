from pathlib import Path

import streamlit as st


HOME_PAGE_PATH = Path(__file__).with_name("home.py")

st.title("내비게이션 기능 실습")
st.write("Streamlit의 페이지 이동 기능을 직접 확인하는 페이지입니다.")

with st.container(border=True):
    st.subheader("st.page_link")
    st.write("링크를 눌러 홈 페이지로 이동합니다.")
    st.page_link(HOME_PAGE_PATH, label="홈으로 이동", width="stretch")

with st.container(border=True):
    st.subheader("st.switch_page")
    st.write("버튼을 누르면 코드에서 홈 페이지로 바로 전환합니다.")
    if st.button("홈으로 전환", type="primary"):
        st.switch_page(HOME_PAGE_PATH)

with st.container(border=True):
    st.subheader("외부 문서 링크")
    st.page_link(
        "https://docs.streamlit.io/develop/api-reference/navigation",
        label="Streamlit 내비게이션 API 문서 열기",
        icon=":material/open_in_new:",
    )
