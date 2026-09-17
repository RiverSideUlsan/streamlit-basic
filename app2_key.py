import streamlit as st

from app2_access import require_login


require_login()
st.info("API 키와 사용자 페르소나는 마이페이지에서 관리합니다.")
st.page_link("app2_mypage.py", label="마이페이지 열기", icon="👤")
