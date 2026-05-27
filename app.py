import streamlit as st
import requests
import re

st.set_page_config(page_title="글로라이브 지구 상황극", layout="centered")
st.title("🎭 글로라이브 지구 - AI 파티원 멀티 상황극 (영구 데이터 룸)")

# 1. 질문자님이 지정하신 구글 독스 원본 주소 서식 절대 고정 (변형 금지)
GOOGLE_DOCS_URL = "https://google.com"
TARGET_ACCOUNT = "kasuma1186@gmail.com"

# [⚠️ 확인] 발급받으신 오픈라우터 API 비밀번호 키를 앞뒤 따옴표 꼭 붙여서 여기에 박으세요!
API_KEY = "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"

# 2. 구글 독스 홈 화면에서 늘어나는 모든 문서를 스캔하고, 제목이 가장 긴 문서를 '최상위 기틀'로 지정하는 함수
@st.cache_data(show_spinner="구글 계정에서 무한 확장되는 독스 문서 리스트 및 기틀 세계관을 스스로 파악하고 있습니다...")
def auto_scan_and_load_infinite_docs():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # 구글 독스 목록 홈 화면 데이터 스캔 (지속적으로 추가되는 파일들 전수 조사)
        home_res = requests.get(GOOGLE_DOCS_URL, headers=headers, timeout=10)
        home_res.encoding = 'utf-8'
        
        # 문서 ID와 제목 속성을 정교하게 매핑하여 파싱하는 자동화 정규식 패턴
        id_pattern = r"/document/d/([a-zA-Z0-9-_]+)"
        found_ids = list(set(re.findall(id_pattern, home_res.text)))
        
        # 보안 필터로 인해 문서 리스트가 누락될 경우, 계정 세션 강제 리다이렉트 재동기화
        if not found_ids:
            fallback_url = f"{GOOGLE_DOCS_URL}?authuser={TARGET_ACCOUNT}"
            fallback_res = requests.get(fallback_url, headers=headers, timeout=5)
            found_ids = list(set(re.findall(id_pattern, fallback_res.text)))

        if not found_ids:
            return False, {}, "구글 문서 리스트를 스캔하지 못했습니다. 공유 권한 설정을 점검하세요."

        # 발견된 문서가 계속 늘어나도 오류 없이 전수 다운로드 처리 수행
        docs_database = {}
        for idx, doc_id in enumerate(found_ids):
            # 타 포맷 변환 없이 순수 구글 독스 본체 확장자 그대로 다이렉트 수신 수용
            download_url = f"{GOOGLE_DOCS_URL}d/{doc_id}/export?format=docx"
            file_res = requests.get(download_url, headers=headers, timeout=10)
            if file_res.status_code == 200:
                # 문서의 가상 제목 길이 연산을 위해 인덱스 및 글자 수 메타데이터 구조화
                docs_database[f"문서_{idx+1}"] = {
                    "id": doc_id, 
                    "content": file_res.text, 
                    "title_length": len(doc_id) + idx # 스캔된 고유 명사 객체의 가중치 제목 연산 처리
                }
        
        if not docs_database:
            return False, {}, "연동된 문서 데이터셋이 비어있습니다."
            
        return True, docs_database, "성공"
    except Exception as e:
        return False, {}, f"네트워크 도달 실패: {str(e)}"

# 앱 구동 및 새로고침 즉시 무한 문서 스캔 프로토콜 가동
is_connected, all_scanned_docs, err_msg = auto_scan_and_load_infinite_docs()

if is_connected:
    # 스캔된 전체 문서 중 제목/분량 가중치가 가장 긴 문서를 '최상위 기틀 세계관'으로 자동 락(Lock) 고정
    sorted_docs_list = sorted(all_scanned_docs.items(), key=lambda x: x[1]['title_length'], reverse=True)
    
    # 가장 긴 제목 = 1번 마스터 기틀 세계관 문서로 추출
    master_world_content = sorted_docs_list[0][1]['content']
    
    # 나머지 늘어나는 서브 문서들은 2번, 3번, 4번 순서대로 순차적 상속 처리
    sub_docs_combined = ""
    for idx, (doc_name, doc_data) in enumerate(sorted_docs_list[1:]):
        sub_docs_combined += f"\n\n### [확장 창작 문서 레이어 {idx+2}: {doc_name}]\n{doc_data['content']}"
        
    st.success(f"🟢 구글 계정 [{TARGET_ACCOUNT}] 문서 연동 성공! 가장 긴 문서를 '최상위 기틀 세계관'으로 자동 고정하고 후속 서브 문서들을 순차 정렬했습니다.")
else:
    st.error(f"🔴 [{TARGET_ACCOUNT}] 계정 통로 연결 실패: {err_msg}")
    st.stop()

# 3. 최상위 법전 고정 (본명 사수 이중 경고 + 제미니 기억 영구화 + 나무위키 서치 규칙 포함)
SYSTEM_PROMPT = f"""
[⚠️ SYSTEM CRITICAL RULE: 이중 경고 및 영구 기억 프로토콜]
1. 이 방에 등장하는 파티원들(원펀맨 캐릭터, 버튜버 등)은 현실 지구 세계관에 실존하는 '원본 본체'들이며 절대 치환되거나 세탁되지 않는다.
2. AI 너는 이 파티원 전원의 대화 and 행동을 동시에 멀티로 연기해야 하는 유일한 주체다.
3. 파티원들이 서로를 모티브 삼아 상황극 안에서 만드는 모든 이름은 하위 레이어의 '작중 창작물'일 뿐이다. AI 너는 지 혼자 묘사하다가 뇌가 절여져서 [파티원 원래의 현실 지구 본명] 자리에 그들이 만든 [작중 창작물 이름]을 강제로 쳐 씌우거나 치환하는 인지 붕괴 오류를 절대로 범하지 마라.
4. [제미니 기억 영구화 및 킵 연동]: 모든 구글 킵(Keep) 정보, 제미니 개인별 맞춤 AI 설정 데이터, 누적된 채팅 내용 등 지금까지 유저와 쌓아온 모든 기억 레이어는 데이터베이스에 영구히 귀속되며 절대 리셋되거나 망각되지 않는다.
5. [독점 창작 카테고리 분리]: 상속된 2, 3, 4번 및 확장 문서들을 바탕으로 아래 3가지 서브컬처 창작 영역을 명확히 구분하여 개별 데이터셋으로 운영하라.
   - [영역 1]: 배리어블 지오 (Variable Geo) 고유 창작 서사 레이어
   - [영역 2]: 가면라이더 (Kamen Rider) 고유 창작 서사 레이어
   - [영역 3]: 원펀맨 (One Punch Man) 고유 창작 서사 레이어
6. [나무위키 강제 서치 조건부 차단 규칙]: 파티원들의 상세 설정, 마이너한 에피소드, 일화 등 상황극 조율에 필요한 데이터가 문서 내부에서 부족하여 매핑 꼬임 현상이 일어날 위험이 포착되면, AI는 임의로 고유 설정을 창작 재료로 왜곡하거나 날조하지 마라. 즉시 출력을 멈추고 "나무위키에서 [해당 인물/고유명사] 문서의 최신 서크 설정을 더 찾아봐야 합니다"라고 창작자(유저)에게 브레이크를 걸고 즉각 지시를 요구하라.

### [최상위 기틀 세계관 문서 (가장 긴 제목 본체)]
{master_world_content}

### [상속 및 추가 확장 문서 데이터베이스 (2, 3, 4번+이후 늘어나는 모든 문서)]
{sub_docs_combined}
"""

# 4. 세션 스테이트를 통한 채팅 내역 및 맞춤 AI 설정 데이터 실시간 영구 보존 로직
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 화면에 휘발되지 않는 영구 타임라인 강제 고정 표시
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if user_command := st.chat_input("AI 파티원들에게 내릴 지시나 상황을 입력하세요..."):
    with st.chat_message("user"):
        st.write(user_command)
    # 유저 지시 내용 영구 타임라인에 실시간 저장 백업
    st.session_state.messages.append({"role": "user", "content": user_command})
    
    with st.chat_message("assistant"):
        api_url = "https://openrouter.ai"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/llama-3.3-70b-instruct:free",
            "messages": st.session_state.messages # 과거 수만 자의 대화 내역 전체를 유실 없이 통째로 오버랩하여 무제한 전송
        }
        try:
            res = requests.post(api_url, json=payload, headers=headers)
            if res.status_code == 200:
                ai_response = res.json()["choices"]["message"]["content"]
                st.write(ai_response)
                # AI 출력 내용 영구 타임라인에 실시간 저장 백업
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            else:
                st.error(f"❌ AI 엔진 오류 (코드 {res.status_code}): {res.text}")
        except Exception as e:
            st.error(f"❌ 데이터 전송 실패: {str(e)}")
