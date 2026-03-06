import streamlit as st
from coach_agent import generate_boxing_report

st.set_page_config(page_title="AI Cornerman", page_icon="🥊", layout="centered")

st.title("🥊 AI Cornerman")
st.subheader("개인 맞춤 복싱 코치")
st.write("영상 + 상황 메모 + 코치 피드백을 기반으로 코칭 리포트를 생성합니다.")

with st.form("boxing_form"):
    training_type = st.selectbox(
        "훈련 종류",
        ["스파링", "쉐도우", "미트훈련"]
    )

    uploaded_video = st.file_uploader(
        "훈련 영상 업로드",
        type=["mp4", "mov", "avi", "mkv"]
    )

    user_memo = st.text_area(
        "상황 메모",
        placeholder="예: 상대는 압박형이었고, 잽을 많이 쓰려고 했다. 2라운드부터 체력이 떨어졌다.",
        height=150
    )

    coach_feedback = st.text_area(
        "실제 코치 피드백",
        placeholder="예: 잽 후 오른손 가드가 내려간다. 공격 후 멈추는 습관이 있다.",
        height=150
    )

    submitted = st.form_submit_button("코칭 리포트 생성")

if submitted:
    if uploaded_video is None:
        st.warning("먼저 영상을 업로드해주세요.")
    elif not user_memo.strip():
        st.warning("상황 메모를 입력해주세요.")
    elif not coach_feedback.strip():
        st.warning("코치 피드백을 입력해주세요.")
    else:
        with st.spinner("AI가 코칭 리포트를 생성하는 중입니다..."):
            try:
                report = generate_boxing_report(
                    training_type=training_type,
                    video_name=uploaded_video.name,
                    user_memo=user_memo,
                    coach_feedback=coach_feedback,
                )

                st.success("코칭 리포트 생성 완료")
                st.markdown("## 분석 결과")
                st.markdown(report)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
