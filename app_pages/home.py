import streamlit as st

st.title("이승렬")
st.title("Streamlit API Reference 예제")
st.caption("공식 API Reference의 분류에 맞춰 구성한 실행형 예제 모음입니다.")

st.info("왼쪽 사이드 메뉴에서 원하는 분류를 선택하세요.")

with st.container(border=True):
    st.subheader("구성")
    st.markdown(
        """
        - 페이지 요소: 텍스트, 데이터, 차트, 입력, 미디어, 레이아웃, 채팅, 상태
        - 앱 로직: 실행 흐름, 캐시와 세션 상태, 연결·보안·설정
        - 모든 예제는 Streamlit 내장 API를 중심으로 작성했습니다.
        """
    )

st.link_button(
    "공식 Streamlit API Reference 열기",
    "https://docs.streamlit.io/develop/api-reference",
    icon=":material/open_in_new:",
)
