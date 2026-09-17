import numpy as np
import streamlit as st

st.title("미디어 요소 예제")

st.header("이미지")
image_data = np.zeros((180, 320, 3), dtype=np.uint8)
image_data[:, :160] = [0, 170, 255]
image_data[:, 160:] = [255, 200, 0]
st.image(image_data, caption="NumPy 배열로 만든 예제 이미지")

st.header("오디오")
sample_rate = 8_000
seconds = 1
time = np.linspace(0, seconds, sample_rate * seconds, endpoint=False)
audio_data = (0.3 * np.sin(2 * np.pi * 440 * time)).astype(np.float32)
st.audio(audio_data, sample_rate=sample_rate)

st.header("비디오와 PDF")
st.video("https://www.w3schools.com/html/mov_bbb.mp4")
st.caption("PDF는 파일 경로 또는 bytes가 있을 때 st.pdf로 표시할 수 있습니다.")
st.code("st.pdf(open('document.pdf', 'rb').read())", language="python")

st.header("앱 로고")
st.caption("st.logo는 실제 로고 파일 또는 URL을 지정해 앱 전체에 적용합니다.")
st.code("st.logo('logo.png', link='https://streamlit.io')", language="python")
