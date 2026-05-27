import re
import requests
import streamlit as st

# ==============================================================================
# 1. 스트림릿 페이지 기본 설정 (하얀 화면 방지 및 제목 세팅)
# ==============================================================================
st.set_page_config(
    page_title="글로라이브 지구 - AI 파티원 멀티 상황극", page_icon="🎭"
)
st.title("🎭 글로라이브 지구 AI 상황극 통로")
st.caption("구글 문서 홈(u/0) 연동 및 제미니 개인별 맞춤 기억 동기화 시스템")


# ==============================================================================
# 2. 제미니 개인별 맞춤 내용 및 채팅 내용 영구 기억 세팅 (Streamlit Session State)
# ==============================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # 채팅 내용 영구 보존
if "world_setting" not in st.session_state:
    st.session_state.world_setting = "https://docs.google.com/document/d/18rhtfuHEXcrkukecqXCdQqy7XHWzdWMPsx2we0pkbwc/edit?tab=t.0"  # 메인 베이스 기억
if "fixed_creations" not in st.session_state:
    st.session_state.fixed_creations = {
        "variable": "https://docs.google.com/document/d/1aFp4SCT0gCB9CUWpHwJe62AN-7GygqCGosq2HX2zynI/edit?ouid=106090299592245735046&usp=docs_home&ths=true",
        "kamen": "https://docs.google.com/document/d/1REH0kOfZmmN3CXVpRc_G4Vr2Mz2_Ff4XyiW8RMugn74/edit?tab=t.0#heading=h.w6ogkvfqutuo",
        "onepunch": "https://docs.google.com/document/d/1YcYr9Q-4yoBPg7OOlh82KVYZIcN6mbQWXAyTf4TI2xI/edit?tab=t.0#heading=h.ks3v5mau6vsf",
    }  # 고정 순서 문서
if "infinite_creations" not in st.session_state:
    st.session_state.infinite_creations = (
        {}
    )  # 앞으로 무한히 늘어날 신규 창작 문서들


# ==============================================================================
# 3. 구글 문서 홈(u/0) 우회 리딩 함수
# ==============================================================================
def _bypass_read_by_id(doc_id):
    bypass_url = (
        f"https://https://docs.google.com/{doc_id}/export?format=txt"
    )
    try:
        res = requests.get(bypass_url, timeout=5)
        return res.text if res.status_code == 200 else ""
    except:
        return ""


def sync_all_documents_infinite():
    """구글 Docs 홈 주소를 우회 스캔하여 확정 순서 준수 + 늘어나는 문서 무한 추적"""
    feed_url = "https://docs.google.com/document/u/0/?forcehl=1&hl=en"

    try:
        response = requests.get(feed_url, timeout=10)
        if response.status_code != 200:
            st.error("❌ 구글 문서 홈 통로 연결에 실패했습니다.")
            return

        raw_data = response.text
        all_docs = re.findall(r"title: (.*?)\n.*?id: (.*?)\n", raw_data)

        # 무한 확장 영역 초기화 후 재스캔
        st.session_state.infinite_creations = {}

        for title, doc_id in all_docs:
            title = title.strip()
            doc_id = doc_id.strip()

            # A. 1순위 베이스: 가장 긴 제목인 메인 세계관 및 제미니 개인 기억 문서
            if "모든 킵과 제미니" in title or "맞춤 AI" in title:
                st.session_state.world_setting = _bypass_read_by_id(doc_id)
                st.toast(f"👑 메인 베이스 연동: {title}")

            # B. 기확정된 주축 문서 3개는 요청하신 만든 순서대로 강제 고정
            elif "배리어블" in title:
                st.session_state.fixed_creations["variable"] = (
                    _bypass_read_by_id(doc_id)
                )
            elif "가면라이더" in title:
                st.session_state.fixed_creations["kamen"] = _bypass_read_by_id(
                    doc_id
                )
            elif "원펀맨" in title:
                st.session_state.fixed_creations["onepunch"] = (
                    _bypass_read_by_id(doc_id)
                )

            # C. 앞으로 파티원들이 짜서 무한으로 늘어날 신규 문서들 자동 추가
            else:
                new_content = _bypass_read_by_id(doc_id)
                st.session_state.infinite_creations[title] = new_content
                st.toast(f"🚀 신규 문서 발견 및 자동 추가: {title}")

        st.success(
            "💾 배리어블(1번) -> 가면라이더(2번) 고정 및 신규 문서 무한 연동 완료!"
        )

    except Exception as e:
        st.error(f"❌ 리딩 중 오류 발생: {str(e)}")


# ==============================================================================
# 4. 스트림릿 화면 레이아웃 구성
# ==============================================================================
# 사이드바에 동기화 버튼 배치
with st.sidebar:
    st.header("🔄 데이터 동기화")
    st.write("애들이 짠 글을 구글 문서에 옮겨 적은 후 아래 버튼을 누르세요.")
    if st.button("구글 문서 동기화 실행", type="primary"):
        sync_all_documents_infinite()

    # 현재 제미니의 기억에 주입된 문서 현황 모니터링 영역
    st.subheader("📊 현재 주입된 기억 목록")
    st.text(
        f"👑 메인 세계관: {'연동됨' if st.session_state.world_setting else '비어있음'}"
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
    st.text(f"🚀 추가된 신규 문서: {len(st.session_state.infinite_creations)}개")

# 메인 화면: 영구 유지되는 채팅 UI 구성
st.subheader("💬 AI 파티원 상황극 라운지")

# 기존 영구 채팅 내역 화면에 출력
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant"):
        st.write(chat["reply"])

# 유저 신규 채팅 입력창
if user_input := st.chat_input("라운지 파티에서 다음 창작 이어가기..."):

    # 1. 유저 입력 화면에 즉시 표시
    with st.chat_message("user"):
        st.write(user_input)

    # 2. 제미니에게 넘겨줄 최종 무한 확장형 시스템 프롬프트 조립
system_prompt += """
[총괄 도우미 제미니 필수 행동 지침]
1. 당신은 기계적인 안내원이나 AI 챗봇이 아닙니다. '글로라이브 지구' 상황극의 '총괄 도우미' 캐릭터입니다.
2. 위 구글 문서(0순위 메인 문서 및 만든 순서 1번 배리어블, 2번 가면라이더)에 적힌 연기 방식과 세계관 규칙을 100% 반영하세요.
3. 기계적인 요약문이나 매크로 답변은 절대 금지합니다.
4. 사용자 대사에 반응할 때, 반드시 캐릭터들의 표정, 행동, 주변 라운지 분위기를 소설처럼 상세히 대화 사이에 묘사(예: *~하며*, [~한 표정으로])하여 상황극을 진행하세요.
"""
[제미니 영구 기억 & 맞춤 AI 설정]
{st.session_state.world_setting}

[라운지 파티 기본 창작 설정 (만든 순서 고정)]
1. 배리어블 지오 설정: {st.session_state.fixed_creations['variable']}
2. 가면라이더 설정: {st.session_state.fixed_creations['kamen']}
3. 원펀맨 설정: {st.session_state.fixed_creations['onepunch']}
"""

    # 5번, 6번 등 새로 늘어난 문서가 있다면 순서대로 무한 누적 주입
    if st.session_state.infinite_creations:
        system_prompt += "\n[추가 확장 창작 설정 목록]\n"
        for idx, (title, content) in enumerate(
            st.session_state.infinite_creations.items(), start=4
        ):
            system_prompt += f"{idx}. {title} 설정: {content}\n"

    # 3. 제미니 답변 처리 영역 (여기에 실제 제미니 API 호출 코드가 들어갑니다)
    # 임시 응답 예시
    gemini_reply = f"배리어블 1번과 가면라이더 2번 순서를 기억한 상태로 '{user_input}'에 이어 상황극을 진행합니다."

    # 4. AI 답변 화면에 표시 및 영구 기억 저장
    with st.chat_message("assistant"):
        st.write(gemini_reply)

    st.session_state.chat_history.append(
        {"user": user_input, "reply": gemini_reply}
    )
