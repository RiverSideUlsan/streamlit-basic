import streamlit as st

st.title("상태와 알림 예제")

st.success("성공 메시지")
st.info("안내 메시지")
st.warning("경고 메시지")
st.error("오류 메시지")
st.exception(RuntimeError("예외 표시 예제입니다."))

st.header("진행 상태")
progress = st.progress(60, text="작업 진행률 60%")
if st.button("완료로 변경", icon=":material/done:"):
    progress.progress(100, text="작업 완료")
    st.balloons()
    st.toast("작업이 완료되었습니다.")

with st.spinner("짧은 작업을 표시하는 spinner 예제"):
    st.write("spinner 내부 내용")

with st.status("상태 컨테이너", expanded=True) as status:
    st.write("첫 번째 단계")
    st.write("두 번째 단계")
    status.update(label="완료", state="complete")

with st.skeleton(height=80):
    st.write("불러오는 중에 보여 줄 자리입니다.")

if st.button("눈 내리기", icon=":material/ac_unit:"):
    st.snow()
