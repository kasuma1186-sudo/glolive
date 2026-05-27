import streamlit as st
import requests

st.set_page_config(page_title="글로라이브 지구 상황극", layout="centered")
st.title("🎭 글로라이브 지구 - AI 파티원 멀티 상황극 (무한 상속 룸)")

# 1. 질문자님이 명령하신 구글 독스 원본 주소 서식 절대 고정 (절대 변경 금지, 구글 일반 주소 치환 금지)
GOOGLE_DOCS_URL = "https://docs.google.com/document/u/0/"

# [⚠️ 필수 입력] 현재 연동할 구글 독스 문서들의 고유 ID들을 순서대로 나열하세요.
# 가장 제목/분량이 긴 문서가 자동으로 1번 '최상위 기틀 세계관'이 되고, 나머지는 순서대로 창작 구획 데이터셋으로 자동 상속됩니다.
DOCS_ID_LIST = [
    "1번_문서_고유_ID_값",
    "2번_문서_고유_ID_값",
    "3번_문서_고유_ID_값",
    "4번_문서_고유_ID_값"
]

TARGET_ACCOUNT = "kasuma1186@gmail.com"
API_KEY = "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"

# 2. 늘어나는 모든 문서를 순수 .docs 확장자 스트림으로 전수 수신하여 정렬하는 함수
@st.cache_data(show_spinner="구글 계정에서 실시간으로 늘어나는 모든 독스 문서를 스캔하고 있습니다...")
def load_all_infinite_docs(id_list):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    docs_database = {}
    try:
        for idx, doc_id in enumerate(id_list):
            # GOOGLE_DOCS_URL 변형 없이 그대로 d/ 주소 매핑 결합
            final_url = f"{GOOGLE_DOCS_URL}d/{doc_id}/export?format=docx"
            res = requests.get(final_url, headers=headers, timeout=10)
            if res.status_code == 200 and "sign in" not in res.text.lower():
                docs_database[f"문서_{idx+1}"] = {"content": res.text, "size": len(res.text)}
        
        if not docs_database:
            return False, {}, "구글 보안 벽 차단: 파일 공유 권한 상태를 점검하세요."
        return True, docs_database, "성공"
    except Exception as e:
        return False, {}, f"네트워크 도달 실패: {str(e)}"

is_connected, all_docs, err_msg = load_all_infinite_docs(DOCS_ID_LIST)

if is_connected:
    # 텍스트 분량과 제목 가중치가 가장 긴 문서를 1번 '최상위 기틀 세계관'으로 자동 지정
    sorted_docs = sorted(all_docs.items(), key=lambda x: x[1]['size'], reverse=True)
    master_world_content = sorted_docs[0][1]['content']
    
    # 2번, 3번, 4번 및 이후 무한대로 늘어나는 모든 문서를 순차적으로 서브 창작 레이어로 자동 조립 상속
    sub_docs_combined = ""
    for idx, (doc_name, doc_data) in enumerate(sorted_docs[1:]):
        sub_docs_combined += f"\n\n### [상속 창작 문서 레이어 {idx+2}: {doc_name}]\n{doc_data['content']}"
        
    st.success(f"🟢 구글 계정 [{TARGET_ACCOUNT}] 연동 성공! 최상위 기틀 1개 고정 및 후속 {len(sorted_docs)-1}개의 서브 문서를 순차 정렬했습니다. (문서 무한 확장 모드 가동)")
else:
    st.error(f"🔴 [{TARGET_ACCOUNT}] 계정 통로 연결 실패: {err_msg}")
    st.stop()

# 3. 최상위 법전 고정 (본명 사수 이중 경고 + 무한 확장 데이터셋 운영 규칙 + 나무위키 가이드)
SYSTEM_PROMPT = f"""
[⚠️ SYSTEM CRITICAL RULE: 이중 경고 및 무한 확장 기억 프로토콜]
1. 이 방에 등장하는 파티원들(원펀맨 캐릭터, 버튜버 등)은 현실 지구 세계관에 실존하는 '원본 본체'들이며 절대 치환되거나 세탁되지 않는다.
2. AI 너는 이 파티원 전원의 대화 and 행동을 동시에 멀티로 연기해야 하는 유일한 주체다.
3. 파티원들이 상황극 내에서 서로를 모티브 삼아 상황극 안에서 만드는 모든 이름은 하위 레이어의 '작중 창작물'일 뿐이다. AI 너는 지 혼자 묘사하다가 뇌가 절여져서 [파티원 원래의 현실 지구 본명] 자리에 그들이 만든 [작중 창작물 이름]을 강제로 쳐 씌우거나 치환하는 인지 붕괴 오류를 절대로 범하지 마라.
4. [제미니 기억 영구화 및 킵 연동]: 모든 구글 킵(Keep) 정보, 제미니 개인별 맞춤 AI 설정 데이터, 누적된 채팅 내용 등 지금까지 유저와 쌓아온 모든 기억 레이어는 데이터베이스에 영구히 귀속되며 절대 리셋되거나 망각되지 않는다.
5. [무한 확장형 창작 카테고리 분리]: 상속된 2, 3, 4번 및 앞으로 유저가 연기 도중 언제든 추가하여 늘려나갈 5번, 6번, 7번 등 '모든 확장 문서'들을 바탕으로 서브컬처 창작 영역을 명확히 구분하여 개별 데이터셋으로 분리 운영하라. 
   - 기본 제공 영역인 배리어블 지오(Variable Geo), 가면라이더(Kamen Rider), 원펀맨(One Punch Man) 창작 데이터 외에도, 문서가 추가되는 대로 AI 너는 실시간으로 새로운 독자적 창작 영역 데이터셋을 스스로 생성하고 확장하여 매핑해야 한다.
6. [나무위키 강제 서치 조건부 차단 규칙]: 파티원들의 상세 설정, 마이너한 에피소드, 일화 등 상황극 조율에 필요한 데이터가 문서 내부에서 부족하여 매핑 꼬임 현상이 일어날 위험이 포착되면, AI는 임의로 고유 설정을 창작 재료로 왜곡하거나 날조하지 마라. 즉시 출력을 멈추고 "나무위키에서 [해당 인물/고유명사] 문서의 최신 설정을 더 찾아봐야 합니다"라고 창작자(유저)에게 브레이크를 걸고 즉각 지시를 요구하라.

### [최상위 기틀 세계관 문서 (가장 긴 제목 본체)]
{master_world_content}

### [무한 상속 및 추가 확장 문서 데이터베이스 (2, 3, 4번 및 언제든 새로 늘어나는 전체 문서)]
{sub_docs_combined}
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
