import streamlit as st
from coach_agent import generate_boxing_report

st.set_page_config(page_title="AI Cornerman", page_icon="🥊", layout="centered")

st.title("🥊 AI Cornerman")
st.subheader("개인 맞춤 복싱 코치")
st.write("영상 + 상황 메모 + 코치 피드백을 기반으로 코칭 리포트를 생성합니다.")


def parse_report(report_text: str):
    sections = {
        "장점": "",
        "부족한 부분": "",
        "코치 피드백 반영 해석": "",
        "추천 훈련": "",
        "다음 훈련 미션": ""
    }

    current_section = None

    for line in report_text.splitlines():
        line = line.strip()
        if not line:
            continue

        if line == "[장점]":
            current_section = "장점"
        elif line == "[부족한 부분]":
            current_section = "부족한 부분"
        elif line == "[코치 피드백 반영 해석]":
            current_section = "코치 피드백 반영 해석"
        elif line == "[추천 훈련]":
            current_section = "추천 훈련"
        elif line == "[다음 훈련 미션]":
            current_section = "다음 훈련 미션"
        elif current_section:
            sections[current_section] += line + "\n"

    return sections


training_type = st.selectbox(
    "훈련 종류",
    ["스파링", "쉐도우", "미트훈련"]
)

uploaded_video = st.file_uploader(
    "훈련 영상을 업로드하세요",
    type=["mp4", "mov", "avi", "mkv"]
)

user_memo = st.text_area(
    "상황 메모",
    placeholder="예: 나 파란 헤드기어. 상대는 압박형. 잽으로 거리 잡으려 했지만 잘 안 맞았다.",
    height=150
)

coach_feedback = st.text_area(
    "실제 코치 피드백",
    placeholder="예: 힘을 빼고 쳐라. 뒷손이 없다.",
    height=120
)

if st.button("코칭 리포트 생성"):
    if uploaded_video is None:
        st.warning("먼저 영상을 업로드해주세요.")
    elif not user_memo.strip():
        st.warning("상황 메모를 입력해주세요.")
    elif not coach_feedback.strip():
        st.warning("실제 코치 피드백을 입력해주세요.")
    else:
        with st.spinner("AI가 코칭 리포트를 생성 중입니다..."):
            try:
                report = generate_boxing_report(
                    training_type=training_type,
                    video_name=uploaded_video.name,
                    user_memo=user_memo,
                    coach_feedback=coach_feedback
                )

                sections = parse_report(report)

                st.success("코칭 리포트 생성 완료")

                st.markdown("## 🥊 코칭 결과")

                with st.container(border=True):
                    st.markdown("### ✅ 장점")
                    st.markdown(sections["장점"] or "내용 없음")

                with st.container(border=True):
                    st.markdown("### ⚠️ 부족한 부분")
                    st.markdown(sections["부족한 부분"] or "내용 없음")

                with st.container(border=True):
                    st.markdown("### 🧠 코치 피드백 반영 해석")
                    st.markdown(sections["코치 피드백 반영 해석"] or "내용 없음")

                with st.container(border=True):
                    st.markdown("### 🥊 추천 훈련")
                    st.markdown(sections["추천 훈련"] or "내용 없음")

                with st.container(border=True):
                    st.markdown("### 🎯 다음 훈련 미션")
                    st.markdown(sections["다음 훈련 미션"] or "내용 없음")

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
