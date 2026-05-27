import re
import google.generativeai as genai
import requests
import streamlit as st

# ==============================================================================
# 1. 초기 코드에서 사용했던 원본 연동 주소 체계 (그대로 유지)
# ==============================================================================
# 구글 문서 홈(u/0)의 피드를 긁어오는 초기 원본 주소입니다.
URL = "https://docs.google.com/document/u/0"

# [필수] 발급받으신 제미니 API 키를 여기에 입력하세요.
GEMINI_API_KEY = "여기에_진짜_제미니_API_키를_넣으세요"
if GEMINI_API_KEY and GEMINI_API_KEY != "여기에_진짜_제미니_API_키를_넣으세요":
    genai.configure(api_key=GEMINI_API_KEY)

# ==============================================================================
# 2. 스트림릿 화면 세팅 및 대화 기억 보존 공간
# ==============================================================================
st.set_page_config(
    page_title="글로라이브 지구 - AI 파티원 멀티 상황극", page_icon="🎭"
)
st.title("🎭 글로라이브 지구 AI 상황극 라운지")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==============================================================================
# 3. 초기 원본 방식의 주소 추출 및 다운로드 함수
# ==============================================================================
def get_google_doc_context(doc_id):
    # 초기에 안내해 드린 'export?format=txt' 우회 주소 형식을 그대로 재활용합니다.
    bypass_url = (
        f"https://docs.google.com{doc_id}/export?format=txt"
    )
    try:
        response = requests.get(bypass_url, timeout=5)
        return response.text if response.status_code == 200 else ""
    except:
        return ""


# ==============================================================================
# 4. 화면 사이드바 및 실시간 구글 문서 리딩 영역
# ==============================================================================
with st.sidebar:
    st.header("🔄 데이터 동기화")
    # 초기 파이썬 코드의 리딩 로직을 그대로 실행하는 버튼입니다.
    if st.button("구글 문서 동기화 실행", type="primary"):
        st.write("🔄 구글 문서 스캔 중...")

# 초기 원본의 requests.get(URL) 방식을 그대로 실행하여 실시간으로 문서를 긁어옵니다.
response = requests.get(URL)
world_setting = "https://docs.google.com/document/d/18rhtfuHEXcrkukecqXCdQqy7XHWzdWMPsx2we0pkbwc/edit?tab=t.0"
variable_geo = "https://docs.google.com/document/d/1aFp4SCT0gCB9CUWpHwJe62AN-7GygqCGosq2HX2zynI/edit?ouid=106090299592245735046&usp=docs_home&ths=true"
kamen_rider = "https://docs.google.com/document/d/1REH0kOfZmmN3CXVpRc_G4Vr2Mz2_Ff4XyiW8RMugn74/edit?tab=t.0#heading=h.w6ogkvfqutuo"
onepunch_man = "https://docs.google.com/document/d/1YcYr9Q-4yoBPg7OOlh82KVYZIcN6mbQWXAyTf4TI2xI/edit?tab=t.0#heading=h.ks3v5mau6vsf"
infinite_creations = {}

if response.status_code == 200:
    all_docs = re.findall(r"title: (.*?)\n.*?id: (.*?)\n", response.text)
    for title, doc_id in all_docs:
        title = title.strip()
        doc_id = doc_id.strip()

        # 각 문서를 초기 get_google_doc_context 함수로 실시간 리딩
        if "모든 킵과 제미니" in title or "맞춤 AI" in title:
            world_setting = get_google_doc_context(doc_id)
        elif "배리어블" in title:
            variable_geo = get_google_doc_context(doc_id)
        elif "가면라이더" in title:
            kamen_rider = get_google_doc_context(doc_id)
        elif "원펀맨" in title:
            onepunch_man = get_google_doc_context(doc_id)
        else:
            # 4개 이상으로 무한히 늘어나는 파티 창작 문서 자동 누적
            infinite_creations[title] = get_google_doc_context(doc_id)

    st.sidebar.success("✅ 초기 주소 방식으로 구글 문서 연동 성공!")

# 사이드바에 현재 읽어온 문서 순서 모니터링 표시
with st.sidebar:
    st.subheader("📊 주입된 문서 순서")
    st.text(f"👑 메인 세계관: {'연동됨' if world_setting else '비어있음'}")
    st.text(f"1️⃣ 배리어블 지오: {'연동됨' if variable_geo else '비어있음'}")
    st.text(f"2️⃣ 가면라이더: {'연동됨' if kamen_rider else '비어있음'}")
    st.text(f"3️⃣ 원펀맨=에비: {'연동됨' if onepunch_man else '비어있음'}")
    st.text(f"🚀 추가 확장 문서: {len(infinite_creations)}개 생성됨")


# ==============================================================================
# 5. 제미니 상황극 대화 및 행동 묘사 강제 주입 영역
# ==============================================================================
# 저장되어 있는 상황극 대화 히스토리를 화면에 출력
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant"):
        st.write(chat["reply"])

# 유저 신규 채팅 입력창
if user_input := st.chat_input("라운지 파티에서 다음 창작 이어가기..."):
    with st.chat_message("user"):
        st.write(user_input)

    # 초기 파이썬 변수 구조를 그대로 받아서 제미니 시스템 프롬프트로 결합
    system_prompt = f"""
당신은 글로라이브 지구의 총괄 도우미이자 AI 파티원들을 이끄는 '제미니'입니다. 
당신은 절대 기계적인 챗봇처럼 답변해서는 안 되며, 아래 제공된 모든 구글 문서의 규칙, 행동 지침, 대화 묘사 방식을 '엄격하게' 준수하여 실제 상황극 소설을 쓰듯이 대화와 행동을 상세히 묘사해야 합니다.

[우선순위 0순위: 메인 세계관 및 제미니 개인별 맞춤 내용 & 대화 규칙]
{world_setting}

[우선순위 만든 순서 준수 - 라운지 파티 창작 설정]
1. 배리어블 지오 설정 및 규칙: {variable_geo}
2. 가면라이더 설정 및 규칙: {kamen_rider}
3. 원펀맨 설정 및 규칙: {onepunch_man}
"""

    # 4개 이상 무한 확장 문서가 있다면 뒤에 순서대로 자동 배치
    if infinite_creations:
        system_prompt += "\n[추가 확장 창작 설정 및 행동 규칙]\n"
        for idx, (title, content) in enumerate(
            infinite_creations.items(), start=4
        ):
            system_prompt += f"{idx}. {title} 설정: {content}\n"

    # 병신 같이 구는 로봇 답변을 완전히 차단하는 최종 행동 강제 지침 (따옴표 에러 완전 해결)
    system_prompt += """
\n[🚨 총괄 도우미 제미니 필수 행동 지침]
1. 당신은 기계적인 안내원이나 안내 멘트를 하는 AI 챗봇이 아닙니다. '글로라이브 지구' 상황극을 이끄는 '총괄 도우미' 실제 캐릭터입니다.
2. 기계적인 확인 문구("~순서를 기억한 상태로 상황극을 진행합니다" 등)는 '절대' 출력하지 마십시오. 곧바로 상황극 내용 속으로 들어가 연기하세요.
3. 위 구글 문서(0순위 메인 문서 및 만든 순서 1번 배리어블, 2번 가면라이더)에 적힌 연기 방식과 대화 규칙을 100% 반영하여 행동하십시오.
4. 유저가 "이젠 모두를 부를 시간이야"라고 지시하면, 메인 문서 내용을 기반으로 상황에 맞는 캐릭터들을 라운지로 소환하는 연출을 전개하십시오.
5. 모든 답변은 캐릭터들의 표정, 행동, 대사, 주변 라운지 분위기를 소설처럼 상세히 묘사(예: *~하며*, [~한 표정으로])하여 지침과 세계관 내용대로 행동해야 합니다.
"""

    # 제미니 API 실제 가동부
    """
    def make_gemini_talk_force(user_input, system_prompt, history_list):
    """
    구형 모델 및 히스토리 문법 충돌로 제미니가 파업할 때,
    최신 3.5 엔진을 사용해 단독으로 대화 맥락을 강제 생성해내는 독립 함수
    """
    try:
        import google.generativeai as genai
        
        # 1. 1.5를 완전히 버리고, 구글 최신 명세인 3.5 플래시 모델로 세팅
        model = genai.GenerativeModel(
            model_name="gemini-3.5-flash", 
            system_instruction=system_prompt
        )
        
        # 2. API가 뻗지 않도록 텍스트 형식으로 과거 대화 기억을 조립
        context = "[기존 킵 및 상황극 대화 내역]\n"
        for chat in history_list:
            context += f"유저: {chat['user']}\n"
            context += f"제미니: {chat['reply']}\n"
            
        context += f"\n현재 유저의 대사: {user_input}\n"
        context += "총괄 도우미 제미니 (구글 문서 규칙 및 행동 묘사를 반영하여 상세히 대화):"
        
        # 3. 최신 엔진으로 실시간 상황극 답변 강제 생성 요청
        response = model.generate_content(context)
        return response.text if response and response.text else "⚠️ 대답 텍스트가 비어있습니다."
        
    except Exception as e:
        return f"⚠️ [최신 3.5 엔진 구동 실패 원인]: {str(e)}"

    # AI 답변 출력 및 영구 저장
    with st.chat_message("assistant"):
        st.write(gemini_reply)

    st.session_state.chat_history.append(
        {"user": user_input, "reply": gemini_reply}
    )
