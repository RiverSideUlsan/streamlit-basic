import streamlit as st


st.title("내 계정")
st.write(f"{st.user.name} 님으로 로그인했습니다.")
st.caption("로그아웃은 사이드바에서 할 수 있습니다.")
