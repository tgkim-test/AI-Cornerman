import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_boxing_report(training_type, video_name, user_memo, coach_feedback):

    system_prompt = """
당신은 개인 맞춤형 복싱 코치입니다.

사용자가 제공한 훈련 정보, 상황 메모, 코치 피드백을 기반으로
복싱 코칭 리포트를 작성하세요.

반드시 아래 형식으로 답변하세요.

[장점]
- 2~3개

[부족한 부분]
- 2~3개

[코치 피드백 반영 해석]

[추천 훈련]
- 3개

[다음 훈련 미션]
- 3개
"""

    user_prompt = f"""
훈련 종류: {training_type}
영상 파일: {video_name}

상황 메모:
{user_memo}

코치 피드백:
{coach_feedback}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]
