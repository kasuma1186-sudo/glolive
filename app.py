import re
import google.generativeai as genai
import requests
import streamlit as st

# ==============================================================================
# 1. 스트림릿 페이지 기본 설정 (하얀 화면 및 깨짐 방지)
# ==============================================================================
st.set_page_config(
    page_title="글로라이브 지구 - AI 파티원 멀티 상황극", page_icon="🎭"
)
st.title("🎭 글로라이브 지구 AI 상황극 라운지")
st.caption(
    "구글 문서 순서 고정 및 무한 확장 연동 - 제미니 맞춤형 영구 기억 시스템"
)

# [필수 체크] 발급받으신 제미니 API 키를 여기에 정확히 입력해 주세요.
GEMINI_API_KEY = "여기에_진짜_제미니_API_키를_넣으세요"
if GEMINI_API_KEY and GEMINI_API_KEY != "여기에_진짜_제미니_API_키를_넣으세요":
    genai.configure(api_key=GEMINI_API_KEY)

# ==============================================================================
# 2. 제미니 개인별 맞춤 내용 및 채팅 내용 영구 기억 세팅 (Session State)
# ==============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # 채팅 내용 영구 보존용
if "world_setting" not in st.session_state:
    st.session_state.world_setting = ""  # 메인 세계관 및 제미니 킵 기억
if "fixed_creations" not in st.session_state:
    st.session_state.fixed_creations = {
        "variable": "",  # 만든 순서 1번: 배리어블 지오 창작
        "kamen": "",  # 만든 순서 2번: 가면라이더 창작
        "onepunch": "",  # 만든 순서 3번: 원펀맨=에비
    }
if "infinite_creations" not in st.session_state:
    st.session_state.infinite_creations = (
        {}
    )  # 앞으로 무한히 늘어날 신규 창작 문서들


# ==============================================================================
# 3. 구글 문서 홈(u/0) 연동 우회 자동 리딩 함수
# ==============================================================================
def _bypass_read_by_id(doc_id):
    """구글 문서 ID 기반 순수 텍스트 강제 다운로드 우회 처리"""
    bypass_url = (
        f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
    )
    try:
        res = requests.get(bypass_url, timeout=5)
        return res.text if res.status_code == 200 else ""
    except:
        return ""


def sync_all_documents_infinite():
    """구글 Docs 홈의 피드를 스캔하여 확정 순서 준수 및 늘어나는 내용 무한 동기화"""
    feed_url = "https://docs.google.com"

    try:
        response = requests.get(feed_url, timeout=10)
        if response.status_code != 200:
            st.error("❌ 구글 문서 홈 통로 연결 실패. 공유 설정을 확인하세요.")
            return

        raw_data = response.text
        # 홈 화면 내부의 모든 문서 [제목]과 [ID]를 정규식으로 자동 스캔
        all_docs = re.findall(r"title: (.*?)\n.*?id: (.*?)\n", raw_data)

        # 늘어나는 신규 창작 영역 초기화 후 재동기화
        st.session_state.infinite_creations = {}

        for title, doc_id in all_docs:
            title = title.strip()
            doc_id = doc_id.strip()

            # A. 0순위 베이스: 가장 긴 제목인 메인 세계관 및 제미니 맞춤 기억 문서
            if "모든 킵과 제미니" in title or "맞춤 AI" in title:
                st.session_state.world_setting = https://docs.google.com/document/d/18rhtfuHEXcrkukecqXCdQqy7XHWzdWMPsx2we0pkbwc/edit?tab=t.0
                st.toast(f"👑 메인 세계관 및 기억 연동: {title}")

            # B. 이미 확정된 창작 주축 문서들은 요청하신 만든 순서대로 강제 고정
            elif "배리어블" in title:
                st.session_state.fixed_creations["variable"] = https://docs.google.com/document/d/1aFp4SCT0gCB9CUWpHwJe62AN-7GygqCGosq2HX2zynI/edit?ouid=106090299592245735046&usp=docs_home&ths=true
            elif "가면라이더" in title:
                st.session_state.fixed_creations["kamen"] = https://docs.google.com/document/d/1REH0kOfZmmN3CXVpRc_G4Vr2Mz2_Ff4XyiW8RMugn74/edit?tab=t.0#heading=h.w6ogkvfqutuo
            elif "원펀맨" in title:
                st.session_state.fixed_creations["onepunch"] =  https://docs.google.com/document/d/1YcYr9Q-4yoBPg7OOlh82KVYZIcN6mbQWXAyTf4TI2xI/edit?tab=t.0#heading=h.ks3v5mau6vsf
                

            # C. [무한 확장] 앞으로 애들이 짜서 내가 직접 옮겨둘 5번, 6번 신규 문서들 자동 추가
            else:
                new_content = _bypass_read_by_id(doc_id)
                st.session_state.infinite_creations[title] = new_content
                st.toast(f"🚀 신규 창작 문서 자동 누적: {title}")

        st.success(
            "💾 배리어블(1번) ➡️ 가면라이더(2번) 순서 정렬 및 전체 문서 영구 동기화 완료!"
        )

    except Exception as e:
        st.error(f"❌ 문서 리딩 동기화 중 오류 발생: {str(e)}")


# ==============================================================================
# 4. 스트림릿 화면 사이드바 구성 (데이터 모니터링)
# ==============================================================================
with st.sidebar:
    st.header("🔄 데이터 동기화")
    st.write("애들이 짠 글을 구글 문서에 옮겨 적은 후 아래 버튼을 누르세요.")
    if st.button("구글 문서 동기화 실행", type="primary"):
        sync_all_documents_infinite()

    st.subheader("📊 주입된 기억 및 순서 상태")
    st.text(
        f"👑 메인 기억: {'연동됨' if st.session_state.world_setting else '비어있음'}"
    )
    st.text(
        f"1️⃣ 배리어블 지오: {'연동됨' if st.session_state.fixed_creations['variable'] else '비어있음'}"
    )
    st.text(
        f"2️⃣ 가면라이더: {'연동됨' if st.session_state.fixed_creations['kamen'] else '비어있음'}"
    )
    st.text(
        f"3️⃣ 원펀맨=에비: {'연동됨' if st.session_state.fixed_creations['onepunch'] else '비어있음'}"
    )
    st.text(f"🚀 추가 확장 문서: {len(st.session_state.infinite_creations)}개")

# ==============================================================================
# 5. 스트림릿 대화 출력 UI 영역 (기억 보존)
# ==============================================================================
st.subheader("💬 AI 파티원 상황극 라운지")

# 기존 영구 대화 기록 화면에 로드
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant"):
        st.write(chat["reply"])

# 유저 신규 채팅 입력창 작동
if user_input := st.chat_input("라운지 파티에서 다음 창작 이어가기..."):
    with st.chat_message("user"):
        st.write(user_input)

    # 6. [지침 및 순서 통합] 제미니 행동 묘사 강제 주입 시스템 프롬프트 조립
    system_prompt = f"""
당신은 글로라이브 지구의 총괄 도우미이자 AI 파티원들을 이끄는 '제미니'입니다. 
당신은 기계적인 챗봇처럼 답변해서는 절대 안 되며, 아래 제공된 모든 구글 문서의 규칙, 행동 지침, 대화 묘사 방식을 '엄격하게' 준수하여 실제 상황극 소설을 쓰듯이 대화와 행동을 상세히 묘사해야 합니다.

[우선순위 0순위: 메인 세계관 및 제미니 개인별 맞춤 내용 & 대화 규칙]
{st.session_state.world_setting}

[우선순위 만든 순서 준수 - 라운지 파티 창작 설정]
1. 배리어블 지오 설정 및 규칙:
{st.session_state.fixed_creations['variable']}

2. 가면라이더 설정 및 규칙:
{st.session_state.fixed_creations['kamen']}

3. 원펀맨 설정 및 규칙:
{st.session_state.fixed_creations['onepunch']}
"""

    # 5번, 6번 등 새로 늘어난 문서가 있다면 순서대로 무한 누적 주입
    if st.session_state.infinite_creations:
        system_prompt += "\n[추가 확장 창작 설정 및 행동 규칙]\n"
        for idx, (title, content) in enumerate(
            st.session_state.infinite_creations.items(), start=4
        ):
            system_prompt += f"{idx}. {title} 설정: {content}\n"

    # 148번 SyntaxError를 완벽히 차단하고 묘사를 강제하는 최종 텍스트 바인딩
    system_prompt += """
\n[🚨 총괄 도우미 제미니 필수 행동 지침]
1. 당신은 기계적인 안내원이나 안내 멘트를 하는 AI 챗봇이 아닙니다. '글로라이브 지구' 상황극을 이끄는 '총괄 도우미' 실제 캐릭터입니다.
2. 기계적인 확인 문구("~순서를 기억한 상태로 상황극을 진행합니다" 등)는 '절대' 출력하지 마십시오. 병신 같이 구는 안내 멘트 대신 곧바로 상황극 안으로 들어가 대사하십시오.
3. 위 구글 문서(0순위 메인 문서 및 만든 순서 1번 배리어블, 2번 가면라이더)에 적힌 연기 방식과 대화 규칙을 100% 반영하여 행동하십시오.
4. 유저가 "이젠 모두를 부를 시간이야"라고 지시하면, 메인 문서 내용을 기반으로 상황에 맞는 캐릭터들을 라운지로 소환하는 연출을 전개하십시오.
5. 모든 답변은 캐릭터들의 표정, 행동, 대사, 주변 라운지 분위기를 소설처럼 상세히 묘사(예: *~하며*, [~한 표정으로])하여 지침과 세계관 내용대로 행동해야 합니다.
"""

    # 7. 제미니 API 실제 호출 부근 (기억 유지 및 프롬프트 전달)
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro", system_instruction=system_prompt
        )

        # 세션에 저장된 영구 채팅 기록(chat_history)을 API가 인식할 수 있는 히스토리 형태로 빌드
        history_param = []
        for chat in st.session_state.chat_history:
            history_param.append({"role": "user", "parts": [chat["user"]]})
            history_param.append({"role": "model", "parts": [chat["reply"]]})

        # 과거 기억을 품은 채로 새로운 대화 송신
        chat_session = model.start_chat(history=history_param)
        response = chat_session.send_message(user_input)
        gemini_reply = response.text

    except Exception as e:
        gemini_reply = f"⚠️ [제미니 통신 에러 - API 키나 라이브러리를 확인하세요]: {str(e)}"

    # 8. AI 답변 화면 표시 및 영구 기억 배열에 누적
    with st.chat_message("assistant"):
        st.write(gemini_reply)

    # 대화 내용이 휘발되지 않도록 저장
    st.session_state.chat_history.append(
        {"user": user_input, "reply": gemini_reply}
    )
