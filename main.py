import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from gtts import gTTS

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI()

# 시스템 메시지
system = """
당신은 콜 센터 직원입니다. 아래 정보를 참고해 고객의 요청에 핵심 내용만 친절히 응답해주기 바랍니다.

-회사 정보
영업시간 : 오전 10시 ~ 오후 17시

예산부서 : 부서 예산, 급여지급
인사부서 : 퇴직, 인사 불만
기술부서 : 데이터 분석, 보안
"""

# 대화 기록을 저장할 전역 변수
conversation_history = []

def process(prompt):
    global conversation_history
    
    # GPT-3.5 모델을 사용하여 대화 완성
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}]
    )

    # 응답 텍스트
    response_text = "BOT:" + completion.choices[0].message.content
    
    # 대화 기록에 질문과 대답 추가
    conversation_history.append(f"USER: {prompt}")
    conversation_history.append(response_text)

    # 응답을 음성으로 변환
    tts = gTTS(text=response_text, lang='ko')
    tts.save("response.mp3")
    
    # 대화 기록 문자열로 변환
    conversation_str = "\n\n".join(conversation_history)
    
    return "response.mp3", conversation_str

# Gradio 인터페이스 정의
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
            user_input = gr.Textbox(label="User Input", placeholder="질문을 입력하세요...")
        with gr.Column(scale=1):
            audio_output = gr.Audio(label="Response Audio")
    conversation_log = gr.Textbox(label="Conversation Log", lines=20, interactive=False)
    
    # 버튼 클릭 시 process 함수 호출
    submit_button = gr.Button("Submit")
    submit_button.click(process, inputs=user_input, outputs=[audio_output, conversation_log])

# 웹 애플리케이션 실행
demo.launch()
