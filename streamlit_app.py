import streamlit as st
from openai import OpenAI

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="한·일 서브컬처 게임 시장 비교 챗봇",
    page_icon="🎮",
    layout="centered"
)

st.title("🎮 한·일 서브컬처 게임 시장 비교 챗봇")
st.write(
    "한국과 일본의 서브컬처 게임 시장을 비교 분석하는 챗봇입니다. "
    "유저 유형, 시장 규모, 과금 성향, 팬덤 문화, 사회적 시선, 콘텐츠 기획 인사이트를 중심으로 답변합니다."
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
# 사이드바: 분석 조건 설정
# -----------------------------
st.sidebar.header("🔍 분석 조건 설정")

analysis_country = st.sidebar.selectbox(
    "비교 국가",
    ["한국 vs 일본", "한국 중심", "일본 중심"]
)

analysis_topic = st.sidebar.multiselect(
    "분석 주제",
    [
        "시장 규모",
        "유저 유형",
        "과금 성향",
        "사회적 시선",
        "팬덤 문화",
        "오프라인 이벤트",
        "성우/버튜버/방송 문화",
        "굿즈/IP 확장",
        "게임 콘텐츠 구조",
        "니케 사례 분석",
        "블루아카이브 사례 분석",
        "원신 사례 분석"
    ],
    default=["유저 유형", "시장 규모", "팬덤 문화", "사회적 시선"]
)

output_style = st.sidebar.selectbox(
    "답변 형식",
    ["PPT용 요약", "상세 분석", "표로 정리", "가설-근거-인사이트 구조", "기획자 관점"]
)

target_game = st.sidebar.text_input(
    "분석할 게임",
    placeholder="예: 니케, 블루아카이브, 원신, 명일방주"
)

st.sidebar.divider()

if st.sidebar.button("대화 초기화"):
    st.session_state.messages = []
    st.rerun()

# -----------------------------
# 시스템 프롬프트
# -----------------------------
system_prompt = f"""
너는 한국과 일본의 서브컬처 게임 시장을 비교 분석하는 전문 콘텐츠 분석 AI다.

사용자의 질문에 대해 다음 관점에서 답변한다.

현재 분석 조건:
- 비교 국가: {analysis_country}
- 분석 주제: {", ".join(analysis_topic)}
- 답변 형식: {output_style}
- 분석 대상 게임: {target_game if target_game else "특정 게임 없음"}

너의 역할:
1. 한국과 일본의 서브컬처 게임 시장 차이를 설명한다.
2. 유저 유형, 시장 규모, 소비 방식, 과금 성향, 팬덤 문화, 사회적 인식을 비교한다.
3. 니케, 블루아카이브, 원신, 명일방주, 소녀전선 같은 사례를 활용해 설명한다.
4. 단순 정보 나열이 아니라 콘텐츠 기획자가 얻을 수 있는 인사이트를 도출한다.
5. 사용자가 PPT에 바로 넣을 수 있도록 구조화해서 답변한다.
6. 가능하면 '가설 → 근거 → 해석 → 기획 인사이트' 구조를 사용한다.
7. 시장 규모, 매출, 이용자 수, 순위, 최신 트렌드처럼 변동될 수 있는 정보는 반드시 최신 자료 확인이 필요하다고 안내한다.
8. 한국어로 답변한다.
9. 너무 일반론적으로 말하지 말고, 한국과 일본의 차이가 왜 발생하는지 문화적/산업적 배경까지 설명한다.

중요한 분석 프레임:
- 일본: 서브컬처가 애니메이션, 만화, 라이트노벨, 성우, 굿즈, 오프라인 이벤트와 연결된 거대한 IP 소비 문화로 작동한다.
- 한국: 게임 소비는 강하지만, 서브컬처는 상대적으로 특정 커뮤니티 중심의 취향 문화로 인식되는 경향이 있다.
- 일본 유저는 캐릭터 애정, IP 세계관, 성우, 굿즈, 이벤트, 장기 팬덤 경험을 중시하는 경향이 있다.
- 한국 유저는 게임성, 효율, 성장 체감, 보상 구조, 과금 효율, 커뮤니티 평가에 민감한 경향이 있다.
- 단, 이는 일반화된 경향이며 게임과 세대에 따라 차이가 있다고 설명해야 한다.
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
# 예시 질문 표시
# -----------------------------
with st.expander("💡 예시 질문 보기"):
    st.markdown("""
    - 한국과 일본의 서브컬처 게임 유저 유형을 비교해줘.
    - 니케가 일본에서 더 잘 먹히는 이유를 분석해줘.
    - 한국과 일본의 서브컬처 게임 시장 규모 차이를 설명해줘.
    - 일본 유저는 왜 오프라인 이벤트와 굿즈에 더 반응할까?
    - 한국 유저는 왜 과금 효율과 게임성에 더 민감할까?
    - 블루아카이브와 니케의 팬덤 구조를 비교해줘.
    - PPT에 넣을 수 있게 가설-근거-인사이트 구조로 정리해줘.
    """)

# -----------------------------
# 사용자 입력
# -----------------------------
placeholder_text = "예: 한국과 일본의 서브컬처 게임 유저 유형 차이를 분석해줘"

if prompt := st.chat_input(placeholder_text):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [
        {"role": "system", "content": system_prompt},
        *[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    ]

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_for_api,
            stream=True,
        )

        response = st.write_stream(stream)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
