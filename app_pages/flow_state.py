import time

import pandas as pd
import streamlit as st

st.title("실행 흐름, 캐시, 세션 상태")


@st.cache_data
def make_sample_data():
    return pd.DataFrame({"번호": range(1, 6), "값": [10, 20, 30, 40, 50]})


st.header("st.cache_data")
st.dataframe(make_sample_data())
st.caption("같은 실행 환경에서는 함수의 결과를 캐시해 다시 사용할 수 있습니다.")

st.header("st.session_state")
if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("카운터 증가", icon=":material/add:"):
    st.session_state.counter += 1

st.metric("현재 카운터", st.session_state.counter)

st.header("form과 fragment")
with st.form("search_form"):
    keyword = st.text_input("검색어")
    search = st.form_submit_button("검색", icon=":material/search:")

if search:
    st.write(f"검색어: {keyword}")


@st.fragment
def clock_fragment():
    st.caption(f"fragment 실행 시각: {time.strftime('%H:%M:%S')}")
    if st.button("fragment만 다시 실행", key="fragment_rerun"):
        st.rerun(scope="fragment")


clock_fragment()

st.header("공식 코드 예시")
st.code(
    """# 현재 스크립트를 즉시 다시 실행
st.rerun()

# 이후 코드를 실행하지 않음
st.stop()

# URL 쿼리 매개변수 읽기
st.write(st.query_params)""",
    language="python",
)
