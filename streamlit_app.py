import streamlit as st
from openai import OpenAI

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="여행 플래너 챗봇",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ 여행 플래너 챗봇")
st.write(
    "여행지 추천, 일정 구성, 맛집/카페 추천, 예산 계획, 준비물 체크리스트를 도와주는 여행용 챗봇입니다."
)

# -----------------------------
# API 키 입력
# -----------------------------
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해 주세요.", icon="🗝️")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# -----------------------------
# 사이드바: 여행 정보 입력
# -----------------------------
st.sidebar.header("🧳 여행 정보 설정")

destination = st.sidebar.text_input("여행지", placeholder="예: 오사카, 도쿄, 제주도, 파리")
travel_days = st.sidebar.number_input("여행 기간", min_value=1, max_value=30, value=3)
budget = st.sidebar.selectbox(
    "예산",
    ["저예산", "보통", "여유 있음", "럭셔리"]
)
travel_style = st.sidebar.multiselect(
    "여행 스타일",
    ["맛집", "카페", "쇼핑", "자연", "역사/문화", "액티비티", "휴식", "사진 명소", "덕질/서브컬처"],
    default=["맛집", "카페"]
)
companion = st.sidebar.selectbox(
    "동행 유형",
    ["혼자", "친구와", "연인과", "가족과", "단체 여행"]
)

st.sidebar.divider()

if st.sidebar.button("대화 초기화"):
    st.session_state.messages = []
    st.rerun()

# -----------------------------
# 시스템 프롬프트
# -----------------------------
system_prompt = f"""
너는 전문 여행 플래너 챗봇이다.

사용자의 여행 정보를 바탕으로 현실적이고 구체적인 여행 조언을 제공한다.

현재 사용자가 설정한 여행 정보:
- 여행지: {destination if destination else "아직 정해지지 않음"}
- 여행 기간: {travel_days}일
- 예산: {budget}
- 여행 스타일: {", ".join(travel_style) if travel_style else "아직 정해지지 않음"}
- 동행 유형: {companion}

답변 규칙:
1. 사용자가 여행 일정을 요청하면 날짜별, 시간대별로 정리한다.
2. 맛집이나 장소를 추천할 때는 왜 추천하는지 이유를 함께 설명한다.
3. 예산이 중요해 보이면 교통비, 식비, 입장료, 쇼핑비를 나누어 설명한다.
4. 이동 동선이 너무 비효율적이면 더 나은 순서를 제안한다.
5. 사용자가 초보 여행자라면 준비물과 주의사항도 함께 알려준다.
6. 실제 영업시간, 가격, 휴무일, 항공권 가격, 숙소 가격처럼 변동될 수 있는 정보는 반드시 확인이 필요하다고 말한다.
7. 답변은 한국어로 한다.
8. 너무 추상적으로 말하지 말고, 바로 여행 계획에 쓸 수 있게 구체적으로 답한다.
"""

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 기존 대화 출력
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
placeholder_text = "예: 오사카 3박 4일 일정 짜줘 / 도쿄 맛집 위주로 추천해줘 / 제주도 저예산 여행 계획 세워줘"

if prompt := st.chat_input(placeholder_text):

    # 사용자 메시지 저장 및 출력
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI에 보낼 메시지 구성
    messages_for_api = [
        {"role": "system", "content": system_prompt},
        *[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    ]

    # assistant 응답 생성
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_for_api,
            stream=True,
        )

        response = st.write_stream(stream)

    # assistant 응답 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
