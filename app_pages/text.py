import streamlit as st
import pandas as pd

st.title("📝 텍스트와 출력 (Text Elements) 예제")
st.caption("Streamlit 공식 API Reference의 텍스트 및 출력 관련 주요 요소들을 종류별 탭으로 정리한 예시입니다.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📌 제목 및 기본 텍스트",
    "🎨 마크다운과 스타일",
    "📐 수식 (LaTeX)",
    "💻 코드와 구조화 데이터",
    "🌐 HTML / 도움말 / iframe"
])

# --------------------------------------------------
# 탭 1: 제목 및 기본 텍스트
# --------------------------------------------------
with tab1:
    st.header("1. 제목 및 크기별 텍스트 요소")
    
    st.title("st.title('가장 큰 제목')")
    st.header("st.header('섹션 헤더 H2')")
    st.subheader("st.subheader('하위 헤더 H3')")
    
    st.divider()
    
    st.write("### 2. 일반 텍스트와 설명 텍스트")
    st.text("st.text: 고정폭(Monospace) 폰트로 서식 없이 원본 텍스트를 그대로 출력합니다.")
    st.caption("st.caption: 회색 톤의 작은 글씨로 각주나 부가 설명을 달 때 유용합니다.")
    
    st.write("### 3. 구분선")
    st.write("위와 아래 내용을 나눌 때 `st.divider()`를 사용합니다.")
    st.divider()

# --------------------------------------------------
# 2. 마크다운과 스타일
# --------------------------------------------------
with tab2:
    st.header("🎨 서식 있는 텍스트와 마크다운 (st.markdown)")
    
    st.subheader("1) 기본 서식")
    st.markdown("""
    - **굵은 글씨 (Bold)**: `**텍스트**`
    - *기울임꼴 (Italic)*: `*텍스트*`
    - ~~취소선 (Strikethrough)~~: `~~텍스트~~`
    - `인라인 코드 (Inline Code)`: `` `코드` ``
    """)
    
    st.subheader("2) 컬러 및 하이라이트 스타일")
    st.markdown("""
    - 텍스트 색상: :red[빨강], :blue[파랑], :green[초록], :orange[주황], :violet[보라]
    - 배경 하이라이트: :red-background[빨간 배경], :blue-background[파란 배경], :orange-background[주황 배경]
    - 그라데이션: :rainbow[알록달록 무지개 텍스트]
    """)
    
    st.subheader("3) 인용구와 목록")
    st.markdown("""
    > 💡 **알림**: Streamlit 마크다운은 GFM(GitHub Flavored Markdown)을 완벽하게 지원합니다.
    
    1. 첫 번째 순서
    2. 두 번째 순서
       - 하위 항목 A
       - 하위 항목 B
    """)

    st.subheader("4) 뱃지 (st.badge)")
    st.badge("New Feature", icon=":material/new_releases:")
    st.badge("Verified", icon=":material/verified:", color="green")

# --------------------------------------------------
# 3. 수식 (LaTeX)
# --------------------------------------------------
with tab3:
    st.header("📐 수식 렌더링 (st.latex)")
    st.write("KaTeX 기반으로 복잡한 수학 공식과 과학 수식을 미려하게 표현합니다.")
    
    st.subheader("기본 방정식 및 분수")
    st.latex(r"E = mc^2")
    st.latex(r"f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}")
    
    st.subheader("미적분과 시그마")
    st.latex(r"\int_{a}^{b} x^2 \, dx = \left[ \frac{x^3}{3} \right]_{a}^{b}")
    st.latex(r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}")
    
    st.subheader("행렬 (Matrix)")
    st.latex(r"""
    \begin{pmatrix}
    a & b \\
    c & d
    \end{pmatrix}^{-1}
    =
    \frac{1}{ad-bc}
    \begin{pmatrix}
    d & -b \\
    -c & a
    \end{pmatrix}
    """)

# --------------------------------------------------
# 4. 코드와 구조화 데이터
# --------------------------------------------------
with tab4:
    st.header("💻 코드 블록과 데이터 출력")
    
    st.subheader("1) 코드 블록 (st.code)")
    sample_code = """import streamlit as st

def greet(name: str) -> str:
    return f"반갑습니다, {name}님!"

st.write(greet("Streamlit"))"""
    
    st.code(sample_code, language="python", line_numbers=True)
    
    st.subheader("2) JSON 데이터 뷰어 (st.json)")
    st.caption("JSON 객체를 계층적으로 탐색할 수 있는 인터랙티브 뷰어입니다.")
    user_profile = {
        "name": "홍길동",
        "role": "Developer",
        "skills": ["Python", "Streamlit", "SQL"],
        "preferences": {
            "theme": "Dark",
            "notifications": True
        }
    }
    st.json(user_profile, expanded=True)
    
    st.subheader("3) 코드 표시와 동시 실행 (st.echo)")
    with st.echo():
        # 이 블록 안의 코드는 화면에 소스코드로 보인 후 실제로 실행됩니다.
        total_sum = sum([10, 20, 30, 40])
        st.write(f"계산된 합계: **{total_sum}**")

# --------------------------------------------------
# 5. HTML / 도움말 / iframe
# --------------------------------------------------
with tab5:
    st.header("🌐 고급 출력 (HTML, iframe, 도움말)")
    
    st.subheader("1) 커스텀 HTML 렌더링 (st.html)")
    st.html("""
    <div style="padding: 16px; border-radius: 8px; background-color: #f0f2f6; border-left: 5px solid #ff4b4b;">
        <h4 style="margin: 0; color: #31333F;">📢 커스텀 스타일 카드</h4>
        <p style="margin: 4px 0 0 0; color: #555;"><code>st.html</code>을 사용하여 사용자 정의 CSS 스타일이 적용된 HTML 태그를 삽입할 수 있습니다.</p>
    </div>
    """)
    
    st.subheader("2) API 도움말 문서 뷰어 (st.help)")
    st.caption("함수나 클래스의 Docstring 및 인자 정보를 화면에 표시합니다.")
    st.help(st.write)
    
    st.subheader("3) 외부 웹페이지 임베드 (st.iframe)")
    st.caption("Streamlit 공식 API Reference 사이트 임베드 예시")
    st.iframe("https://docs.streamlit.io/develop/api-reference", height=300)
