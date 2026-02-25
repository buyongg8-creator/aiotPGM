import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# 1. 환경 설정 및 API 연결
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# 기록을 저장할 파일 이름
LOG_FILE = "chat_history.txt"

# 2. 파일 관리 함수 (저장 및 불러오기)
def load_history():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    return []

def save_history(user_q, ai_ans):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"USER: {user_q}\n")
        f.write(f"AI: {ai_ans}\n")

# 3. 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# 4. UI 구성 (심플한 레이아웃)
st.title("📄 AI 대화 어시스턴트")
st.subheader("대화 기록이 자동으로 파일에 저장됩니다.")

# 질문 입력창
with st.container():
    question = st.text_input("질문을 입력하세요", placeholder="무엇을 도와드릴까요?")
    col1, col2 = st.columns([1, 5])
    
    with col1:
        send_btn = st.button("보내기")
    with col2:
        if st.button("기록 전체 삭제"):
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
            st.session_state.messages = []
            st.rerun()

# 5. 로직 실행
if send_btn and question:
    with st.spinner("답변 생성 중..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", # 또는 사용 가능한 모델명
                contents=question
            )
            ans_text = response.text
            
            # 파일에 즉시 저장
            save_history(question, ans_text)
            
            # 세션 업데이트 (화면 표시용)
            st.session_state.messages.append(f"USER: {question}")
            st.session_state.messages.append(f"AI: {ans_text}")
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 6. 대화 기록 화면 출력
st.divider()
for msg in reversed(st.session_state.messages):
    if msg.startswith("USER:"):
        st.info(msg.replace("USER:", "👤 나: "))
    else:
        st.success(msg.replace("AI:", "🤖 AI: "))