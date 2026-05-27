import streamlit as st
import requests

st.set_page_config(page_title="글로라이브 지구 상황극", layout="centered")
st.title("🎭 글로라이브 지구 - AI 파티원 멀티 상황극")

# 1. 질문자님이 지정하신 구글 독스 원본 주소 서식 절대 고정
GOOGLE_DOCS_URL = "https://google.com"
TARGET_ACCOUNT = "kasuma1186@gmail.com"

# 계정 연결 상태 체크 함수
@st.cache_data
def check_kasuma_docs_connection():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(GOOGLE_DOCS_URL, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            return True, response.text
        else:
            return False, f"구글 보안 필터 반응 (상태 코드: {response.status_code})"
    except Exception as e:
        return False, f"네트워크 도달 실패: {str(e)}"

is_connected, world_docs = check_kasuma_docs_connection()

if is_connected:
    st.success(f"🟢 구글 계정 [{TARGET_ACCOUNT}] 통로 연결 성공! 지정 주소 연동 완료.")
else:
    st.error(f"🔴 [{TARGET_ACCOUNT}] 계정 통로 연결 실패: {world_docs}")
    st.stop()

# [⚠️ 필수 입력] openrouter.ai에서 무료로 발급받은 sk-or-v1-... 비밀번호를 여기에 붙여넣으세요.
API_KEY = "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"

# 2. 최상위 법전 고정 (본명 사수 이중 경고)
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
        if API_KEY == "여기에_복사한_sk_로_시작하는_키_붙여넣기" or not API_KEY:
            st.error("❌ OpenRouter API 키가 비어있습니다. 코드 34번째 줄에 진짜 키를 입력하고 다시 커밋하세요.")
        else:
            api_url = "https://openrouter.ai"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": st.session_state.messages
            }
            try:
                res = requests.post(api_url, json=payload, headers=headers)
                # 에러 메시지 덮어쓰기 방지용 JSON 분석 안전장치
                if res.status_code == 200:
                    ai_response = res.json()["choices"][0]["message"]["content"]
                    st.write(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    st.error(f"❌ AI 엔진 오류 (코드 {res.status_code}): {res.text}")
            except Exception as e:
                st.error(f"❌ 데이터 전송 실패: {str(e)}")
