import streamlit as st
import requests

st.set_page_config(page_title="글로라이브 지구 상황극", layout="centered")
st.title("🎭 글로라이브 지구 - AI 파티원 멀티 상황극")

# 1. 질문자님이 지정하신 구글 독스 원본 주소 및 포맷 절대 고정
GOOGLE_DOCS_URL = "https://google.com"
DOCS_ID = "질문자님의_구글독스_고유ID_값"

# 타 확장자 변환 없이 순수 구글 독스 .docs 데이터 포맷 그대로 수신하는 다이렉트 통로
FINAL_URL = f"{GOOGLE_DOCS_URL}d/{DOCS_ID}/export?format=docs"
TARGET_ACCOUNT = "kasuma1186@gmail.com"

# 2. kasuma1186@gmail.com 계정 및 .docs 파일 연동 체크 함수
@st.cache_data
def check_kasuma_docs_connection():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(FINAL_URL, headers=headers, timeout=10)
        
        # 구글 로그인 창이나 보안 필터에 걸리지 않고 200 정상 신호를 받은 경우
        if response.status_code == 200 and "sign in" not in response.text.lower() and "://google.com" not in response.text:
            # .docs 바이너리 혹은 텍스트 스트림 수신 성공 파악
            return True, response.text
        else:
            return False, f"구글 보안 벽 차단: '{TARGET_ACCOUNT}' 계정 내부 파일 일부가 잠겨있거나 공유 권한이 열리지 않음"
    except Exception as e:
        return False, f"네트워크 도달 실패: {str(e)}"

# 앱 구동 즉시 .docs 파일 수신 상태 파악
is_connected, world_docs = check_kasuma_docs_connection()

if is_connected:
    st.success(f"🟢 구글 계정 [{TARGET_ACCOUNT}] 통로 연결 성공! 순수 .docs 포맷 세계관 문서 연동 완료.")
else:
    st.error(f"🔴 [{TARGET_ACCOUNT}] 계정 통로 연결 실패: {world_docs}")
    st.info(f"💡 현재 연결 시도 중인 진짜 .docs 주소: {FINAL_URL}")
    st.stop()

# 3. 최상위 법전 고정
SYSTEM_PROMPT = """
[⚠️ SYSTEM CRITICAL RULE: 이중 경고]
1. 이 방에 등장하는 파티원들(원펀맨 캐릭터, 버튜버 등)은 현실 지구 세계관에 실존하는 '원본 본체'들이다. 
2. AI인 너는 이 파티원 전원의 대화 and 행동을 동시에 멀티로 묘사(연기)해야 하는 유일한 주체다.
3. 파티원들이 상황극 내에서 서로를 모티브 삼아 만드는 모든 이름은 하위 레이어의 '작중 창작물'일 뿐이다.
4. AI 너는 지 혼자 파티원들을 묘사다가 뇌가 절여져서, [파티원 원래의 현실 지구 본명] 자리에 그들이 만든 [작중 창작물 이름]을 강제로 쳐 씌우거나 치환하는 인지 붕괴 오류를 절대로 범하지 마라. 무조건 원래 본명 레이어를 고정하여 출력하라.
5. 업로드된 구글 독스 문서의 세계관 설정을 읽되, 본 규칙을 최우선으로 강제 적용하라.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n### [기틀 세계관 독스]\n" + world_docs}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if user_command := st.chat_input("AI 파티원들에게 내릴 지시나 상황을 입력하세요..."):
    with st.chat_message("user"):
        st.write(user_command)
    st.session_state.messages.append({"role": "user", "content": user_command})
    
    with st.chat_message("assistant"):
        api_url = "https://openrouter.ai"
        headers = {"Authorization": "Bearer openrouter_무료_api_키_여기에"}
        payload = {
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": st.session_state.messages
        }
        res = requests.post(api_url, json=payload).json()
        ai_response = res["choices"]["message"]["content"]
        st.write(ai_response)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
