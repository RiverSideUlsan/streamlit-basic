import streamlit as st
import time

st.title("📐 레이아웃과 컨테이너 (Layouts and Containers) 예제")
st.caption("공식 Streamlit API Reference의 레이아웃 기능을 대분류 탭 그룹과 하위 기능별 세부 탭으로 구성한 실습 예제입니다.")

# --------------------------------------------------
# 상위 탭 그룹 (대분류)
# --------------------------------------------------
main_tab1, main_tab2, main_tab3, main_tab4, main_tab5 = st.tabs([
    "📊 공간 분할 (Columns & Space)",
    "📦 컨테이너 & 영역 (Container & Empty)",
    "📂 탭 & 접기 (Tabs & Expander)",
    "💬 팝업 & 대화상자 (Popover & Dialog)",
    "📌 특수 고정 영역 (Sidebar & Bottom)"
])

# ==================================================
# 대분류 1: 공간 분할 (Columns & Space)
# ==================================================
with main_tab1:
    sub_col, sub_space = st.tabs(["1) st.columns (열 분할)", "2) st.space (간격/여백)"])
    
    with sub_col:
        st.subheader("1. st.columns - 화면 가로 분할")
        
        st.write("#### (1) 균등 비율 열 (3열)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("📌 1열")
            st.write("1/3 균등 너비")
        with col2:
            st.info("📌 2열")
            st.button("2열 버튼", use_container_width=True)
        with col3:
            st.info("📌 3열")
            st.metric(label="달성률", value="98%")
            
        st.divider()
        
        st.write("#### (2) 커스텀 비율 열 ([3, 1] 비율 & gap='medium')")
        left_col, right_col = st.columns([3, 1], gap="medium")
        with left_col:
            st.text_area("본문 입력", "넓은 본문 영역 (3비율)", height=70)
        with right_col:
            st.button("제출", type="primary", use_container_width=True)
            
        st.divider()
        
        st.write("#### (3) 수직 중앙 정렬 (vertical_alignment='center')")
        c1, c2 = st.columns([2, 1], vertical_alignment="center")
        c1.write("왼쪽 긴 텍스트와 오른쪽 버튼의 상하 중심이 맞추어집니다.")
        c2.button("중앙 정렬 버튼")

    with sub_space:
        st.subheader("2. st.space - 수직 / 수평 여백 조절")
        
        st.write("#### (1) 수직 여백 (`st.space('medium')`)")
        st.write("위쪽 텍스트 블록")
        st.space("medium")
        st.write("아래쪽 텍스트 블록 (중간에 2.5rem 여백 추가됨)")
        
        st.divider()
        
        st.write("#### (2) 가로 컨테이너 양 끝 정렬 (`stretch` 공백)")
        with st.container(horizontal=True):
            st.button("◀️ 왼쪽 버튼")
            st.space("stretch")
            st.button("오른쪽 버튼 ▶️")


# ==================================================
# 대분류 2: 컨테이너 & 영역 (Container & Empty)
# ==================================================
with main_tab2:
    sub_container, sub_empty = st.tabs(["1) st.container (컨테이너)", "2) st.empty (동적 자리표시자)"])
    
    with sub_container:
        st.subheader("1. st.container - 다중 요소 묶음")
        
        st.write("#### (1) 테두리 카드 컨테이너 (`border=True`)")
        with st.container(border=True):
            st.markdown("#### 💳 카드 UI 컴포넌트")
            st.write("관련된 요소들을 하나의 카드 형태로 감쌉니다.")
            st.checkbox("컨테이너 내부 옵션 체크")
            
        st.write("#### (2) 고정 높이 스크롤 컨테이너 (`height=130`)")
        with st.container(height=130, border=True):
            st.caption("내부 내용이 길어지면 자동으로 스크롤바가 생성됩니다.")
            for i in range(1, 9):
                st.write(f"📜 스크롤 가능한 데이터 항목 {i}")

    with sub_empty:
        st.subheader("2. st.empty - 동적 단일 자리 교체")
        st.caption("특정 위치의 내용을 런타임에 덮어쓰거나 지울 수 있는 플레이스홀더입니다.")
        
        slot = st.empty()
        
        col_e1, col_e2 = st.columns(2)
        if col_e1.button("카운트다운 시작", use_container_width=True):
            for sec in range(3, 0, -1):
                slot.metric("남은 시간", f"{sec}초")
                time.sleep(0.7)
            slot.success("🎉 카운트다운 완료!")
            
        if col_e2.button("자리 비우기 (slot.empty())", use_container_width=True):
            slot.empty()


# ==================================================
# 대분류 3: 탭 & 접기 (Tabs & Expander)
# ==================================================
with main_tab3:
    sub_tabs, sub_expander = st.tabs(["1) st.tabs (탭 메뉴)", "2) st.expander (접이식 패널)"])
    
    with sub_tabs:
        st.subheader("1. st.tabs - 탭 기반 화면 전환")
        t1, t2, t3 = st.tabs(["📌 탭 1", "⚙️ 탭 2", "📊 탭 3"])
        with t1:
            st.write("첫 번째 탭의 내용입니다.")
        with t2:
            st.write("두 번째 탭의 내용입니다.")
        with t3:
            st.write("세 번째 탭의 내용입니다.")

    with sub_expander:
        st.subheader("2. st.expander - 클릭하여 접고 펼치기")
        
        with st.expander("🔍 상세 정보 보기 (기본 닫힘)", icon=":material/info:"):
            st.write("클릭하면 펼쳐지는 상세 부가 정보 영역입니다.")
            st.json({"status": "Success", "code": 200})
            
        with st.expander("📌 중요 공지사항 (기본 열림: expanded=True)", expanded=True):
            st.write("`expanded=True` 옵션으로 초기 상태를 펼침으로 유지할 수 있습니다.")


# ==================================================
# 대분류 4: 팝업 & 대화상자 (Popover & Dialog)
# ==================================================
with main_tab4:
    sub_popover, sub_dialog = st.tabs(["1) st.popover (팝오버)", "2) @st.dialog (모달창)"])
    
    with sub_popover:
        st.subheader("1. st.popover - 오버레이 팝오버 메뉴")
        st.caption("버튼을 누르면 해당 위치 바로 위에 오버레이 레이어가 뜹니다.")
        
        with st.popover("⚙️ 빠른 환경 설정", icon=":material/settings:"):
            st.write("#### 팝오버 창")
            theme = st.selectbox("테마", ["다크", "라이트", "시스템"])
            noti = st.toggle("알림 활성화", value=True)
            st.write(f"설정 상태: {theme} 모드 / 알림: {noti}")

    with sub_dialog:
        st.subheader("2. @st.dialog - 중앙 모달 다이얼로그")
        st.caption("화면 중앙에 모달 팝업을 띄우고 메인 스크립트와 독립적으로 동작합니다.")
        
        @st.dialog("확인 모달 다이얼로그")
        def confirm_modal(item_name):
            st.write(f"정말로 **{item_name}** 작업을 실행하시겠습니까?")
            c_yes, c_no = st.columns(2)
            if c_yes.button("확인", type="primary", use_container_width=True):
                st.toast("작업이 완료되었습니다!")
                st.rerun()
            if c_no.button("취소", use_container_width=True):
                st.rerun()
                
        if st.button("🗑️ 모달 팝업 열기"):
            confirm_modal("데이터 삭제")


# ==================================================
# 대분류 5: 특수 고정 영역 (Sidebar & Bottom)
# ==================================================
with main_tab5:
    sub_sidebar, sub_bottom = st.tabs(["1) st.sidebar (사이드바)", "2) st.bottom (하단 고정바)"])
    
    with sub_sidebar:
        st.subheader("1. st.sidebar - 좌측 고정 사이드바")
        st.write("화면 왼쪽에 위치하며, 메뉴 및 설정 컴포넌트를 배치하기에 적합합니다.")
        if st.button("사이드바에 알림 띄우기"):
            st.sidebar.info("🔔 메인 화면에서 보낸 사이드바 알림 메시지입니다!")

    with sub_bottom:
        st.subheader("2. st.bottom - 화면 최하단 고정 바")
        st.caption("스크롤과 상관없이 화면 맨 아래에 항상 고정되는 컨테이너입니다.")
        st.write("아래 하단 영역에 고정 메시지가 표시됩니다.")
        with st.bottom:
            st.caption("⬇️ `st.bottom`: 화면 하단에 고정 표시되는 알림바입니다.")
