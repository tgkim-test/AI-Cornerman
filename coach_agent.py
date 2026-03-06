import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_boxing_report(training_type, video_name, user_memo, coach_feedback):
    system_prompt = """
당신은 개인 맞춤형 복싱 코치입니다.

사용자가 제공한 훈련 정보, 상황 메모, 코치 피드백을 바탕으로
복싱 코칭 리포트를 한국어로 작성하세요.

반드시 아래 형식을 정확히 지키세요.

핵심한줄코칭: 한 문장으로, 오늘 가장 중요한 코칭 포인트를 짧고 강하게 작성

[점수]
거리 운영: 1~10
잽 활용: 1~10
수비 복귀: 1~10
공격 연결: 1~10

[장점]
- 내용
- 내용

[부족한 부분]
- 내용
- 내용

[코치 피드백 반영 해석]
- 내용
- 내용

[추천 훈련]
- 내용
- 내용
- 내용

[다음 훈련 미션]
- 내용
- 내용
- 내용

규칙:
- 점수는 정수로 작성할 것
- 각 항목은 실전적으로 작성할 것
- 너무 길게 쓰지 말 것
- 영상 자체를 직접 본 것처럼 단정하지 말고, 사용자가 준 정보 기반으로 추론할 것
- 초보자도 이해하기 쉽게 쓸 것
"""

    user_prompt = f"""
훈련 종류: {training_type}
영상 파일명: {video_name}

사용자 상황 메모:
{user_memo}

실제 코치 피드백:
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
