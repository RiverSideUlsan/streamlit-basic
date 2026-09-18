import streamlit as st

from app2.app2_access import (
    SECURITY_NOTICE,
    get_api_key,
    get_user_id,
    register_api_key,
    register_env_api_key,
    require_login,
)
from app2.chat_store import (
    AVAILABLE_MODELS,
    get_user_model,
    get_user_persona,
    save_user_model,
    save_user_persona,
)


PERSONA_EXAMPLES = {
    "직장인": (
        "나는 월요일부터 금요일까지 오전 9시부터 오후 6시까지 일하는 직장인이다.\n"
        "주요 관심사는 업무 우선순위, 동료와의 소통, 이직·성장, 일·생활 균형이다.\n"
        "답변은 바로 실행할 수 있는 3단계 계획과 짧은 예시를 중심으로 듣고 싶다.\n"
        "무조건적인 격려보다 현실적인 선택지와 장단점을 함께 알려주면 좋겠다."
    ),
    "학습자": (
        "나는 파이썬과 데이터 분석을 배우는 초보 학습자다.\n"
        "아직 낯선 용어가 많으므로 전문 용어는 쉬운 말로 풀어 설명해 줬으면 한다.\n"
        "한 번에 많은 내용을 주기보다, 따라 할 수 있는 짧은 코드 예시와 확인 질문을 선호한다.\n"
        "막혔을 때는 정답만 주기보다 원인을 찾는 순서도 알려주면 좋겠다."
    ),
    "창업 준비자": (
        "나는 소규모 AI 서비스 창업을 준비하고 있으며, 고객 문제를 검증하는 단계에 있다.\n"
        "관심사는 고객 인터뷰, MVP 기능 범위, 가격 정책, 경쟁 서비스 차별화다.\n"
        "아이디어를 이야기하면 가설, 검증 방법, 성공 기준, 다음 행동 순서로 정리해 줬으면 한다.\n"
        "큰 비용이나 긴 개발보다 이번 주에 할 수 있는 작은 실험을 먼저 제안해 주면 좋겠다."
    ),
}


def load_persona_example():
    example_name = st.session_state.user_persona_example
    if example_name != "직접 작성":
        st.session_state.user_persona_input = PERSONA_EXAMPLES[example_name]


require_login()

user_id = get_user_id()
st.session_state.setdefault("user_persona_input", get_user_persona(user_id))

st.title("👤 마이페이지")

with st.container(border=True):
    st.subheader("OpenAI API 키 사용 방식")
    st.warning(SECURITY_NOTICE)
    key_method = st.radio(
        "API 키 방식",
        ["직접 등록", ".env의 API 키 사용"],
        horizontal=True,
    )

    if key_method == "직접 등록":
        api_key = st.text_input(
            "OpenAI API 키",
            type="password",
            placeholder="sk-...",
        )
        if st.button("현재 세션에 키 등록", type="primary"):
            if api_key.strip():
                register_api_key(api_key)
                st.success("현재 로그인 세션에 API 키를 등록했습니다.")
            else:
                st.info("OpenAI API 키를 입력해 주세요.")
    else:
        st.caption("프로젝트 .env 파일의 OPENAI_API_KEY를 현재 로그인 세션에서 사용합니다.")
        if st.button(".env API 키 사용", type="primary"):
            if register_env_api_key():
                st.success(".env의 API 키를 현재 로그인 세션에 적용했습니다.")
            else:
                st.warning(".env에서 사용할 OPENAI_API_KEY를 찾지 못했습니다.")

    if get_api_key():
        st.caption("현재 로그인 세션에 API 키가 적용되어 있습니다.")

with st.container(border=True):
    st.subheader("채팅 모델")
    selected_model = st.selectbox(
        "AI 채팅에서 사용할 모델",
        AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(get_user_model(user_id)),
    )
    if st.button("모델 저장", type="primary"):
        save_user_model(user_id, selected_model)
        st.success("채팅 모델을 저장했습니다.")

with st.container(border=True):
    st.subheader("내 페르소나")
    st.caption("저장한 내용은 채팅할 때 캐릭터가 참고합니다.")
    st.selectbox(
        "예시 불러오기",
        ["직접 작성", *PERSONA_EXAMPLES],
        key="user_persona_example",
        on_change=load_persona_example,
    )
    st.text_area(
        "사용자 페르소나",
        key="user_persona_input",
        height=180,
        placeholder="나의 상황, 관심사, 원하는 대화 방식 등을 적어 보세요.",
    )
    if st.button("페르소나 저장", type="primary"):
        save_user_persona(user_id, st.session_state.user_persona_input)
        st.session_state.persona_updated_notice = True
        st.success("사용자 페르소나를 저장했습니다. 채팅 상대가 바로 참고합니다.")
