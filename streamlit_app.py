import streamlit as st
from openai import OpenAI

# 앱 제목 및 설명 표시
st.title("💬 챗봇")
st.write(
    "이 앱은 OpenAI의 GPT-3.5 모델을 사용하여 응답을 생성하는 간단한 챗봇입니다. "
    "이 앱을 사용하려면 [여기](https://platform.openai.com/account/api-keys)에서 발급받은 OpenAI API 키가 필요합니다. "
    "이 앱을 단계별로 구축하는 방법은 [튜토리얼](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)에서 확인하실 수 있습니다."
)

# `st.text_input`을 통해 사용자로부터 OpenAI API 키를 입력받습니다.
# 참고: API 키를 `./.streamlit/secrets.toml`에 저장하고 `st.secrets`를 통해 액세스할 수도 있습니다.
# 상세 내용: https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API 키", type="password")
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 추가해 주세요.", icon="🗝️")
else:

    # OpenAI 클라이언트를 생성합니다.
    client = OpenAI(api_key=openai_api_key)

    # 채팅 메시지를 저장하기 위한 세션 상태(session state) 변수를 생성합니다.
    # 이를 통해 앱이 재실행되어도 대화 내용이 유지됩니다.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # `st.chat_message`를 사용하여 기존의 채팅 메시지들을 화면에 표시합니다.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자가 메시지를 입력할 수 있는 채팅 입력창을 생성합니다.
    # 이 입력창은 자동으로 페이지 하단에 고정됩니다.
    if prompt := st.chat_input("무엇이 궁금하신가요?"):

        # 사용자가 입력한 메시지를 세션 상태에 저장하고 화면에 표시합니다.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API를 사용하여 응답을 생성합니다.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답을 스트리밍 방식으로 화면에 표시하고 세션 상태에 저장합니다.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
