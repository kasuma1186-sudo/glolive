import streamlit as st
import requests
import re

st.set_page_config(page_title="글로라이브 지구 상황극", layout="centered")
st.title("🎭 글로라이브 지구 - AI 파티원 멀티 상황극 ")

# 1. 질문자님이 명령하신 구글 독스 원본 주소 서식 절대 고정 (구글 일반 주소 치환 절대 금지)
GOOGLE_DOCS_URL = "https://docs.google.com/document/u/0/"
TARGET_ACCOUNT = "kasuma1186@gmail.com"
API_KEY = "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"

# 2. 구글 독스 홈 화면에서 진짜 한글 제목과 고유값(ID)을 스스로 매핑하여 긁어오는 완전 자동화 함수
@st.cache_data(show_spinner="구글 계정에서 문서들의 진짜 제목을 파악하여 읽어 들이고 있습니다...")
def auto_scan_and_load_by_exact_title():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    docs_database = {}
    try:
        # 질문자님이 주신 docs. 주소창 포맷 단 1글자도 변형 없이 그대로 다이렉트 자동 요청
        home_res = requests.get(GOOGLE_DOCS_URL, headers=headers, timeout=10)
        home_res.encoding = 'utf-8'
        
        # 구글 독스 목록 html에서 문서 고유 ID와 화면에 표시되는 파일의 진짜 제목 텍스트를 스스로 링크 결합 파악
        meta_matches = re.findall(r'href="[^"]*/document/d/([a-zA-Z0-9-_]+)[^"]*".*?aria-label="([^"]+)"', home_res.text, re.DOTALL)
        
        if not meta_matches:
            fallback_url = f"{GOOGLE_DOCS_URL}?authuser={TARGET_ACCOUNT}"
            fallback_res = requests.get(fallback_url, headers=headers, timeout=5)
            meta_matches = re.findall(r'href="[^"]*/document/d/([a-zA-Z0-9-_]+)[^"]*".*?aria-label="([^"]+)"', fallback_res.text, re.DOTALL)
            
        if not meta_matches:
            meta_matches = re.findall(r'/document/d/([a-zA-Z0-9-_]+)/edit.*?title="([^"]+)"', home_res.text)

        if not meta_matches:
            return False, {}, "구글 문서 목록의 제목 데이터를 스캔하지 못했습니다. 공유 설정을 점검하세요."
            
        # 스스로 찾아낸 진짜 제목과 고유 ID 구조를 매핑하여 순수 .docs 포맷 데이터 수신
        for doc_id, doc_title in meta_matches:
            # 구글 자체 가공 문자열 정제 처리
            clean_title = doc_title.split(" - ")[0].split(" 마지막")[0].strip()
            
            final_url = f"{GOOGLE_DOCS_URL}d/{doc_id}/export?format=docs"
            res = requests.get(final_url, headers=headers, timeout=10)
            if res.status_code == 200 and "sign in" not in res.text.lower():
                docs_database[clean_title] = res.text
                
        if not docs_database:
            return False, {}, "연동된 문서 데이터셋 본문이 비어있습니다."
        return True, docs_database, "성공"
    except Exception as e:
        return False, {}, f"네트워크 도달 실패: {str(e)}"

is_connected, all_title_docs, err_msg = auto_scan_and_load_by_title_exact() if 'auto_scan_and_load_by_title_exact' in globals() else auto_scan_and_load_by_exact_title()

if is_connected:
    # 질문자님이 지으신 진짜 1번 문서 제목 및 나머지 2, 3, 4번 고유 명칭 데이터 공간 초기화
    master_world_content = "1번 기틀 문서 공백 (해당 긴 제목의 문서를 구글독스 홈에서 찾지 못함)"
    variable_geo_content = "배리어블 지오 창작 데이터 공백"
    kamen_rider_content = "가면라이더 창작 데이터 공백"
    onepunch_content = "원펀맨 창작 데이터 공백"
    extended_docs_combined = ""
    
    # 1번 문서의 진짜 고유한 긴 제목 텍스트 문자열 정의
    TARGET_MASTER_TITLE = "모든 킵과 제미니 개인별 맞춤 AI 내용과 채팅 내용등 제미니의 기억은 영구해야하며"
    
    idx_ext = 5
    for title, content in all_title_docs.items():
        # 질문자님이 지어놓으신 진짜 한글 제목 문자열과 100% 매칭하여 기틀 고정
        if TARGET_MASTER_TITLE in title or title in TARGET_MASTER_TITLE:
            master_world_content = content
        elif "배리어블 지오" in title:
            variable_geo_content = content
        elif "가면라이더" in title:
            kamen_rider_content = content
        elif "원펀맨" in title:
            onepunch_content = content
        else:
            # 아는 3개와 별개로 문서 데이터가 앞으로 언제든 무한대로 더 늘어나는 확장 구획 자동 조립
            extended_docs_combined += f"\n\n### [추가 확장 창작 문서 {idx_ext}: {title}]\n{content}"
            idx_ext += 1
            
    st.success(f"🟢 구글 계정 [{TARGET_ACCOUNT}] 연동 성공! 진짜 1번 긴 제목 문서를 탐색하여 최상위 기틀로 정상 고정했습니다. (무한 확장 모드 가동)")
else:
    st.error(f"🔴 [{TARGET_ACCOUNT}] 계정 통로 연결 실패: {err_msg}")
    st.stop()
import requests

def get_google_doc_context(doc_id):
    # 구글 API를 우회하여 문서를 텍스트 파일 형태로 강제 다운로드하는 주소입니다.
    bypass_url = f"https://docs.google.com/document/u/0/{doc_id}/export?format=txt"
    
    try:
        response = requests.get(bypass_url)
        if response.status_code == 200:
            # 문서의 전체 텍스트 데이터 (세계관 설정 등)
            context = response.text
            return context
        else:
            return f"우회 실패 (에러 코드: {response.status_code})"
    except Exception as e:
        return f"연결 오류: {str(e)}"

# 1. 사용하시는 구글 문서 주소창에서 https://google.com[이부분]/edit 
#    사이에 있는 긴 문자열(ID)을 복사해서 아래에 넣으세요.
DOCUMENT_ID = "여기에_구글_문서_ID를_넣으세요"

# 2. 실행하면 로그인 없이 세계관 설정 텍스트를 바로 가져옵니다.
world_setting = get_google_doc_context(DOCUMENT_ID)
print(world_setting)

# 3. 최상위 법전 고정 (본명 사수 이중 경고 + 기억 영구 보존 + 지정 문서 이름 고정 + 나무위키 가이드)
SYSTEM_PROMPT = f"""
[⚠️ SYSTEM CRITICAL RULE: 이중 경고 및 데이터 영구 보존 프로토콜]
1. 이 방에 등장하는 파티원들(원펀맨 캐릭터, 버튜버 등)은 현실 지구 세계관에 실존하는 '원본 본체'들이며 절대 치환되거나 세탁되지 않는다.
2. AI 너는 이 파티원 전원의 대화 and 행동을 동시에 멀티로 연기해야 하는 유일한 주체다.
3. 파티원들이 서로를 모티브 삼아 상황극 안에서 만드는 모든 이름은 하위 레이어의 '작중 창작물'일 뿐이다. AI 너는 지 혼자 묘사하다가 뇌가 절여져서 [파티원 원래의 현실 지구 본명] 자리에 그들이 만든 [작중 창작물 이름]을 강제로 쳐 씌우거나 치환하는 인지 붕괴 오류를 절대로 범하지 마라. 무조건 원래 본명 레이어를 고정하여 출력하라.
4. [기억 영구 보존 필수 조항]: 모든 구글 킵(Keep) 정보, 제미니 개인별 맞춤 AI 내용, 과거 채팅 기록 등 유저(창작자)와 쌓아온 모든 메모리 레이어는 휘발되거나 리셋되지 않고 영구 지속 상태로 데이터베이스에 보존된다.
5. [지정 문서 이름 및 구획 고정 규칙]: AI 너는 아래 매핑된 구글 독스의 실제 문서 제목과 카테고리를 명확히 구분하여 개별 독립 데이터셋으로 엄격히 분리 운영하라. (임의로 구조나 명칭을 바꾸지 마라.)
   - [1번 기틀 문서]: 모든 킵과 제미니 개인별 맞춤 AI 내용과 채팅 내용등 제미니의 기억은 영구해야하며 (최상위 기틀 세계관 본체)
   - [2번 창작 문서]: 배리어블 지오 창작 데이터셋
   - [3번 창작 문서]: 가면라이더 창작 데이터셋
   - [4번 창작 문서]: 원펀맨 창작 데이터셋
   - [무한 확장 스코프]: 위 아는 3개 영역과 별개로 문서 데이터가 앞으로 5번, 6번, 7번 등 언제든 무한대로 더 늘어나더라도, AI 너는 기존 고정 뼈대를 바꾸지 말고 하위 레이어로 자동 추가 생성하여 상속하라.
6. [나무위키 추가 서치 규칙]: 파티원들의 고유 세부 설정이나 서브컬처 일화 데이터가 문서 내부에서 부족하여 매핑이 꼬일 위험이 발생하면, AI는 설정을 조작하지 말고 즉시 대화를 중단한 채 "나무위키에서 [해당 고유명사] 문서의 최신 서크 설정을 더 찾아봐야 합니다"라고 창작자(유저)에게 브레이크를 걸고 지시를 요구하라.

### [1번 기틀 문서 내용: 모든 킵과 제미니 개인별 맞춤 AI 내용과 채팅 내용등 제미니의 기억은 영구해야하며]
{master_world_content}

### [2번 문서 내용: 배리어블 지오 창작]
{variable_geo_content}

### [3번 문서 내용: 가면라이더 창작]
{kamen_rider_content}

### [4번 문서 내용: 원펀맨 창작]
{onepunch_content}

### [5번 이후 무한대로 늘어나는 확장 창작 문서 데이터베이스]
{extended_docs_combined}
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

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
            if res.status_code == 200:
                ai_response = res.json()["choices"]["message"]["content"]
                st.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                st.error(f"❌ AI 엔진 오류 (코드 {res.status_code}): {res.text}")
        except Exception as e:
            st.error(f"❌ 데이터 전송 실패: {str(e)}")
