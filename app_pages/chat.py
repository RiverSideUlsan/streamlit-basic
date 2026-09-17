import streamlit as st

st.title("채팅 요소 예제")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "안녕하세요. Streamlit 채팅 예제입니다."}
    ]

for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    reply = f"입력한 메시지: {prompt}"
    st.session_state.chat_messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write_stream(word + " " for word in reply.split())

if st.button("대화 초기화", icon=":material/delete:"):
    st.session_state.chat_messages = []
    st.rerun()
