import streamlit as st

from chat_app.app2_access import (
    get_user_id,
    get_username,
    is_logged_in,
    logout,
    require_login,
)
from chat_app.chat_store import get_session, init_database


MASCOT_PATH = "assets/pencil.png"
SIDEBAR_CHARACTER_IMAGES = {
    "dawon": {
        "hi": "assets/dawon-female-casual-hi.png",
        "listen": "assets/dawon-female-casual-listen.png",
        "think": "assets/dawon-female-casual-think.png",
        "agree": "assets/dawon-female-casual-agree.png",
    },
    "junho": {
        "hi": "assets/junho-male-casual-hi.png",
        "listen": "assets/junho-male-casual-listen.png",
        "think": "assets/junho-male-casual-think.png",
        "agree": "assets/junho-male-casual-agree.png",
    },
}


def apply_pencil_sketch_style():
    st.html(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #fff9ee;
            background-image:
                radial-gradient(#e8be9344 0.8px, transparent 0.8px),
                linear-gradient(115deg, #fffdf8 0%, #fff5e2 100%);
            background-size: 12px 12px, 100% 100%;
        }

        [data-testid="stSidebar"] {
            background-image:
                repeating-linear-gradient(
                    -18deg,
                    transparent 0,
                    transparent 9px,
                    #e8be9322 10px,
                    transparent 11px
                );
        }

        [data-testid="stForm"],
        [data-testid="stChatMessage"] {
            border: 2px dashed #d99f76;
            border-radius: 20px;
            box-shadow: 3px 4px 0 #f5d4b7;
        }

        [data-testid="stPageLink"] a,
        .stButton > button {
            border: 2px solid #2f5a86;
            box-shadow: 2px 3px 0 #e8be93;
        }

        [data-testid="stPageLink"] a:hover,
        .stButton > button:hover {
            transform: rotate(-1deg) translateY(-1px);
        }
        </style>
        """
    )


st.set_page_config(page_title="배포형 AI 채팅", page_icon="💬", layout="wide")

init_database()
apply_pencil_sketch_style()

page = st.navigation(
    {
        "채팅": [
            st.Page("chat_app/app2_chat.py", title="AI 채팅", icon="💬", default=True),
        ],
        "관리": [
            st.Page("chat_app/app2_mypage.py", title="마이페이지", icon="👤"),
            st.Page("chat_app/app2_history.py", title="대화 내역", icon="🕘"),
        ],
    },
    position="hidden",
)

with st.sidebar:
    character_image_slot = st.empty()
    st.session_state.sidebar_character_image_slot = character_image_slot

    if is_logged_in() and "active_chat_session_id" in st.session_state:
        active_session = get_session(
            get_user_id(),
            st.session_state.active_chat_session_id,
        )
        if active_session:
            mood_key = f"character_mood_{active_session['id']}"
            mood = st.session_state.get(mood_key, "hi")
            image_path = SIDEBAR_CHARACTER_IMAGES.get(
                active_session["persona"],
                {},
            ).get(mood)
            if image_path:
                character_image_slot.image(image_path, width="stretch")

    if is_logged_in():
        st.title(get_username())
    else:
        st.title("채팅")

    st.page_link("chat_app/app2_chat.py", label="AI 채팅", icon="💬", width="stretch")
    st.page_link("chat_app/app2_mypage.py", label="마이페이지", icon="👤", width="stretch")
    st.page_link("chat_app/app2_history.py", label="대화 내역", icon="🕘", width="stretch")

    if is_logged_in():
        st.divider()
        if st.button("로그아웃"):
            logout()
            st.rerun()

require_login()
page.run()
