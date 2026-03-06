import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_boxing_report(training_type, video_name, user_memo, coach_feedback):

    system_prompt = """
당신은 개인 맞춤형 복싱 코치입니다.

사용자가 제공한 훈련 정보, 상황 메모, 코치 피드백을 기반으로
복싱 코칭 리포트를 한국어로 작성하세요.

반드시 아래 형식을 정확히 지키세요.

[장점]
- 내용
- 내용

[부족한 부분]
- 내용
- 내용

[코치 피드백 반영 해석]
- 내용

[추천 훈련]
- 내용
- 내용
- 내용

[다음 훈련 미션]
- 내용
- 내용
- 내용

주의:
- 각 섹션 제목은 반드시 그대로 쓸 것
- 각 항목은 짧고 실전적으로 쓸 것
- 영상 자체를 직접 본 것처럼 단정하지 말고, 사용자 입력을 바탕으로 추론할 것
"""

    user_prompt = f"""
훈련 종류: {training_type}
영상 파일: {video_name}

상황 메모:
{user_memo}

코치 피드백:
{coach_feedback}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content
