import numpy as np
import pandas as pd
import streamlit as st

st.title("차트와 지도 예제")

rng = np.random.default_rng(42)
chart_data = pd.DataFrame(
    rng.normal(size=(20, 3)).cumsum(axis=0),
    columns=["A 지점", "B 지점", "C 지점"],
)

left, right = st.columns(2)
with left:
    st.subheader("선·영역 차트")
    st.line_chart(chart_data)
    st.area_chart(chart_data)
with right:
    st.subheader("막대·산점도")
    st.bar_chart(chart_data)
    scatter_data = pd.DataFrame(
        {"x": rng.normal(size=50), "y": rng.normal(size=50), "size": rng.uniform(10, 100, 50)}
    )
    st.scatter_chart(scatter_data, x="x", y="y", size="size")

st.header("지도")
map_data = pd.DataFrame(
    {"lat": 37.5665 + rng.normal(scale=0.02, size=20), "lon": 126.9780 + rng.normal(scale=0.02, size=20)}
)
st.map(map_data)

st.header("다이어그램")
st.mermaid_chart(
    """
    graph LR
        A[데이터] --> B[Streamlit]
        B --> C[차트]
    """
)
st.graphviz_chart("digraph { Streamlit -> Data; Data -> Chart; }")
