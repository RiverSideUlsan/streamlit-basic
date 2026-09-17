import streamlit as st

st.set_page_config(page_title="Streamlit API Reference 예제", layout="wide")

pages = {
    "시작": [
        st.Page("app_pages/home.py", title="예제 안내", icon=":material/home:"),
    ],
    "페이지 요소": [
        st.Page("app_pages/text.py", title="텍스트와 출력", icon=":material/text_fields:"),
        st.Page("app_pages/data.py", title="데이터", icon=":material/table_chart:"),
        st.Page("app_pages/charts.py", title="차트와 지도", icon=":material/monitoring:"),
        st.Page("app_pages/inputs.py", title="입력 위젯", icon=":material/input:"),
        st.Page("app_pages/media.py", title="미디어", icon=":material/perm_media:"),
        st.Page("app_pages/layout.py", title="레이아웃", icon=":material/view_quilt:"),
        st.Page("app_pages/chat.py", title="채팅", icon=":material/chat:"),
        st.Page("app_pages/status.py", title="상태와 알림", icon=":material/notifications:"),
    ],
    "앱 로직": [
        st.Page("app_pages/flow_state.py", title="실행 흐름과 상태", icon=":material/account_tree:"),
        st.Page("app_pages/connections.py", title="연결, 보안, 설정", icon=":material/settings:"),
    ],
}

page = st.navigation(pages, position="hidden")

with st.sidebar:
    st.subheader("👤 이승렬")
    st.caption("Streamlit 공식 API Reference 기반의 주요 기능 및 컴포넌트를 직접 확인하고 학습할 수 있는 실습 가이드 앱입니다.")
    st.divider()
    for section, page_list in pages.items():
        st.caption(section)
        for p in page_list:
            st.page_link(p)

page.run()
