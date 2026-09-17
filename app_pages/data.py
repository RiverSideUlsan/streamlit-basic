import pandas as pd
import streamlit as st

st.title("데이터 요소 예제")

df = pd.DataFrame(
    {
        "이름": ["김철수", "이영희", "박민수", "정다은"],
        "점수": [85, 92, 78, 95],
        "합격": [True, True, False, True],
    }
)

st.header("DataFrame과 정적 테이블")
st.dataframe(
    df,
    column_config={"점수": st.column_config.NumberColumn("점수", format="%d점")},
)
st.table(df.head(2))

st.header("데이터 편집기")
edited_df = st.data_editor(df, num_rows="dynamic", key="student_editor")
st.caption(f"현재 행 수: {len(edited_df)}")

st.header("지표와 JSON")
first, second, third = st.columns(3)
first.metric("평균 점수", "87.5점", "+2.3점")
second.metric("합격 인원", "3명", "+1명")
third.metric("합격률", "75%", "5%")
st.json({"학생 수": len(df), "과목": "Streamlit", "편집 가능": True})
