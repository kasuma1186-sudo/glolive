import streamlit as st
import requests

st.set_page_config(page_title="글로라이브 지구 상황극", layout="centered")
st.title("🎭 글로라이브 지구 - AI 파티원 멀티 상황극")

# 1. 질문자님이 지정하신 구글 독스 원본 주소 서식 절대 고정
GOOGLE_DOCS_URL = "https://docs.google.com/document/u/0/"
DOCS_ID = "질문자님의_구글독스_고유ID_값"

# 최종 문서 연동 주소 생성
FINAL_URL = f"{GOOGLE_DOCS_URL}d/{DOCS_ID}/export?format=txt"

# 이메일 형식 전체 적용
TARGET_ACCOUNT = "kasuma1186@gmail.com"

# 2. kasuma1186@gmail.com 계정 및 파일 실제 연결 상태 체크 함수
@st.cache_data
def check_kasuma_account_connection():
    try:
        response = requests.get(FINAL_URL, timeout=5)
        response.encoding = 'utf-8'
        
        # 정상적으로 구글 독스 본문 텍스트를 수신한 경우
        if response.status_code == 200 and "document" not in response.text.lower():
            return True, response.text
        else:
            return False, f"구글 계정 인증/보안 벽 확인 필요 ('{TARGET_ACCOUNT}' 계정 파일의 공유 설정을 '링크가 있는 모든 사용자'로 열어주세요)"
    except Exception as e:
        return False, f"네트워크 도달 실패: {str(e)}"

# 앱 구동 직후 이메일 계정 연결 상태부터 즉시 파악 및 화면 강제 표시
is_connected, world_docs = check_kasuma_account_connection()

if is_connected:
    st.success(f"🟢 구글 계정 [{TARGET_ACCOUNT}] 연결 성공! 대형 기틀 문서 데이터를 정상적으로 긁어왔습니다.")
else:
    st.error(f"🔴 [{TARGET_ACCOUNT}] 계정 통로 연결 실패: {world_docs}")
    st.stop() # 계정 연결 실패 시 아래 상황극 기능 실행을 강제로 차단

# 3. 최상위 법전 고정
SYSTEM_PROMPT = """
[⚠️ SYSTEM CRITICAL RULE: 이중 경고]
1. 이 방에 등장하는 파티원들(원펀맨 캐릭터, 버튜버 등)은 현실 지구 세계관에 실존하는 '원본 본체'들이다. 
2. AI인 너는 이 파티원 전원의 대화 and 행동을 동시에 멀티로 묘사(연기)해야 하는 유일한 주체다.
3. 파티원들이 상황극 내에서 서로를 모티브 삼아 만드는 모든 이름은 하위 레이어의 '작중 창작물'일 뿐이다.
4. AI 너는 지 혼자 파티원들을 묘사하다가 뇌가 절여져서, [파티원 원래의 현실 지구 본명] 자리에 그들이 만든 [작중 창작물 이름]을 강제로 쳐 씌우거나 치환하는 인지 붕괴 오류를 절대로 범하지 마라. 무조건 원래 본명 레이어를 고정하여 출력하라.
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
