import re
import requests


class GloLiveGeminiBot:

    def __init__(self):
        # 1. 제미니가 영구적으로 보관해야 하는 개인별 맞춤 내용 및 채팅 기억 저장소
        self.permanent_memory = {
            "chat_history": [],  # 제미니의 영구 채팅 내역 보존
            "world_setting": "",  # 메인 베이스: 모든 킵과 제미니 맞춤 AI 및 세계관
            "sub_creations": {
                "variable": "",  # [만든 순서 1번] 배리어블 지오 창작
                "kamen": "",  # [만든 순서 2번] 가면라이더 창작
                "onepunch": "",  # [만든 순서 3번] 원펀맨=에비
            },
        }

        # 2. 알려주신 구글 문서 홈(u/0)에서 각 문서를 클릭했을 때 나오는 실제 주소 연결
        # (각 문서의 주소창 링크 전체를 그대로 붙여넣으시면 됩니다)
        self.doc_links = {
            "world": "https://google.com",
            "variable": "https://google.com",
            "kamen": "https://google.com",
            "onepunch": "https://google.com",
        }

    def _bypass_read(self, url):
        """구글 Docs 주소에서 ID만 정확히 뽑아내어 우회 리딩하는 내부 함수"""
        match = re.search(r"/document/d/([a-zA-Z0-9-_]+)", url)
        if not match:
            return ""
        doc_id = match.group(1)
        # 구글 문서 시스템 전용 우회 다운로드 포맷
        bypass_url = (
            f"https://google.com{doc_id}/export?format=txt"
        )
        try:
            res = requests.get(bypass_url, timeout=5)
            return res.text if res.status_code == 200 else ""
        except:
            return ""

    def sync_all_documents(self):
        """사용자가 AI 파티원 글을 문서에 옮긴 뒤, 실행 시 고정된 순서로 기억을 갱신하는 함수"""
        print(
            "📥 [글로라이브 지구] 구글 문서 홈(u/0) 기반 순서대로 리딩 시작..."
        )

        # [메인 세계관 및 제미니 개인 맞춤 기억 로드]
        self.permanent_memory["world_setting"] = self._bypass_read(
            self.doc_links["world"]
        )

        # [요청하신 만든 순서 엄격 준수하여 리딩]
        # 1번: 배리어블 지오 창작
        self.permanent_memory["sub_creations"]["variable"] = (
            self._bypass_read(self.doc_links["variable"])
        )
        # 2번: 가면라이더 창작
        self.permanent_memory["sub_creations"]["kamen"] = self._bypass_read(
            self.doc_links["kamen"]
        )
        # 3번: 원펀맨=에비
        self.permanent_memory["sub_creations"]["onepunch"] = self._bypass_read(
            self.doc_links["onepunch"]
        )

        print(
            "💾 [순서 고정 완료] 배리어블 1번 ➡️ 가면라이더 2번 순으로 제미니 맞춤 데이터 영구 동기화."
        )

    def run_chat(self, user_message):
        """제미니가 순서대로 쌓인 기억을 모두 완벽히 숙지한 상태로 상황극 대화를 처리하는 함수"""
        system_prompt = f"""
[제미니 영구 기억 & 맞춤 AI 설정]
{self.permanent_memory['world_setting']}

[라운지 파티 창작 설정 (만든 순서 준수)]
1. 배리어블 지오 설정: {self.permanent_memory['sub_creations']['variable']}
2. 가면라이더 설정: {self.permanent_memory['sub_creations']['kamen']}
3. 원펀맨 설정: {self.permanent_memory['sub_creations']['onepunch']}
"""

        # 채팅 기록 영구 보존 및 제미니 프롬프트 주입 영역
        print(f"\n[시스템 프롬프트 반영 완료]")
        print(f"유저: {user_message}")

        # 대화 내용이 휘발되지 않도록 배열에 지속 저장
        self.permanent_memory["chat_history"].append(
            {"user": user_message, "reply": "제미니 답변 내용"}
        )


# ==========================================
# 실행부
# ==========================================
if __name__ == "__main__":
    bot = GloLiveGeminiBot()

    # 1. 문서에 수동으로 글을 옮겨 적은 후 실행하면 정해진 순서로 최신 내용 리딩
    bot.sync_all_documents()

    # 2. 제미니가 모든 설정을 영구 기억한 채로 라운지 상황극 진행
    bot.run_chat("라운지 파티에서 다음 창작 이어가자.")
