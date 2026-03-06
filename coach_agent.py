import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_boxing_report(training_type: str, video_name: str, user_memo: str, coach_feedback: str) -> str:
    system_prompt = """
당신은 개인 맞춤형 복싱 코치입니다.
사용자가 업로드한 훈련 영상 정보, 사용자 메모, 실제 코치 피드백을 바탕으로
한국어 코칭 리포트를 작성하세요.

반드시 아래 형식으로 답변하세요.

[장점]
- 2~3개

[부족한 부분]
- 2~3개

[코치 피드백 반영 해석]
- 코치 피드백이 현재 훈련에서 어떤 의미인지 설명

[추천 훈련]
- 3개
- 구체적으로

[다음 스파링/훈련 미션]
- 3개
- 짧고 실전적으로

주의:
- 과장하지 말 것
- 영상 자체를 직접 본 것처럼 단정하지 말 것
- 사용자가 제공한 정보 기반으로 추론할 것
- 문장은 쉽게, 실전적으로 쓸 것
"""

    user_prompt = f"""
훈련 종류: {training_type}
업로드한 영상 파일명: {video_name}

사용자 상황 메모:
{user_memo}

실제 코치 피드백:
{coach_feedback}
"""

    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content
