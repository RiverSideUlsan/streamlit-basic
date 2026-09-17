import streamlit as st

st.title("연결, 보안, 설정 예제")

st.info("이 페이지는 비밀값 또는 외부 서비스 설정이 필요한 API의 공식 사용 형태를 보여 줍니다.")

st.header("연결과 secrets")
st.code(
    """# .streamlit/secrets.toml에 연결 정보를 별도로 저장합니다.
conn = st.connection("pets_db", type="sql")
df = conn.query("SELECT * FROM pet_owners")
st.dataframe(df)

# 비밀값은 코드에 쓰지 않고 st.secrets로 읽습니다.
api_key = st.secrets["api_key"]""",
    language="python",
)

st.header("인증")
st.code(
    """# 인증 제공자 설정 후 사용합니다.
st.login()

if st.user.is_logged_in:
    st.write(f"환영합니다, {st.user.name}!")
    if st.button("로그아웃"):
        st.logout()""",
    language="python",
)

st.header("설정과 컨텍스트")
st.code(
    """# 현재 설정 확인
value = st.get_option("theme.base")

# 브라우저 세션 컨텍스트
locale = st.context.locale""",
    language="python",
)

st.header("앱 테스트")
st.code(
    """from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py")
at.run()
assert not at.exception""",
    language="python",
)
