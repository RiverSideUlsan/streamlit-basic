import datetime

import pandas as pd
import streamlit as st

st.title("입력 위젯 예제")

with st.form("basic_input_form"):
    name = st.text_input("이름 입력", value="홍길동")
    memo = st.text_area("메모 입력", placeholder="여러 줄로 입력할 수 있습니다.")
    age = st.number_input("나이 입력", min_value=1, max_value=100, value=25)
    submitted = st.form_submit_button("입력 확인", icon=":material/check:")

if submitted:
    st.success(f"입력 결과: {name}, {age}세")
    st.write(memo)

left, middle, right = st.columns(3)
with left:
    st.checkbox("약관에 동의합니다")
    st.toggle("알림 받기")
    st.radio("선호 계절", ["봄", "여름", "가을", "겨울"])
    st.selectbox("좋아하는 과일", ["사과", "바나나", "딸기", "포도"])
with middle:
    st.multiselect("취미", ["독서", "운동", "게임", "여행"])
    st.segmented_control("보기 방식", ["목록", "카드", "표"])
    st.pills("관심 태그", ["Python", "데이터", "AI"], selection_mode="multi")
    st.select_slider("크기", ["S", "M", "L", "XL"])
with right:
    st.slider("점수", 0, 100, 70)
    st.date_input("날짜", datetime.date.today())
    st.datetime_input("일정", datetime.datetime.now())
    st.time_input("시간", datetime.time(9, 0))
    st.color_picker("색상", "#00aaff")

st.header("파일·카메라·오디오 입력")
uploaded_file = st.file_uploader("파일 업로드", type=["csv", "txt"])
camera_image = st.camera_input("사진 촬영")
audio = st.audio_input("음성 녹음")
if uploaded_file:
    st.write(f"업로드한 파일: {uploaded_file.name}")
if camera_image:
    st.image(camera_image)
if audio:
    st.audio(audio)

st.header("버튼과 페이지네이션")
if st.button("일반 버튼", icon=":material/touch_app:"):
    st.toast("버튼을 눌렀습니다.")
st.download_button("CSV 내려받기", data=pd.DataFrame({"번호": [1, 2, 3]}).to_csv(index=False), file_name="sample.csv")
st.link_button("공식 문서", "https://docs.streamlit.io", icon=":material/open_in_new:")

page = st.pagination(3, key="input_pagination")
st.write(f"현재 {page}페이지입니다.")
