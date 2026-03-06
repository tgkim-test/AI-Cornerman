import re
import streamlit as st
from coach_agent import generate_boxing_report

st.set_page_config(page_title="AI Cornerman", page_icon="🥊", layout="wide")

# -----------------------------
# 스타일
# -----------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1180px;
}

.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}

.sub-title {
    color: #666;
    margin-bottom: 1.5rem;
}

.hero-card {
    background: linear-gradient(135deg, #fff4e6 0%, #ffe0b2 100%);
    border-radius: 20px;
    padding: 22px 24px;
    margin-bottom: 20px;
    border: 1px solid #f3c98b;
}

.hero-label {
    font-size: 0.95rem;
    color: #7a4b00;
    font-weight: 700;
    margin-bottom: 8px;
}

.hero-text {
    font-size: 1.45rem;
    font-weight: 800;
    color: #2d1b00;
    line-height: 1.5;
}

.score-card {
    border-radius: 18px;
    padding: 18px;
    border: 1px solid #ececec;
    background: #ffffff;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    text-align: center;
    margin-bottom: 10px;
}

.score-label {
    font-size: 0.95rem;
    color: #666;
    font-weight: 700;
    margin-bottom: 6px;
}

.score-value {
    font-size: 2rem;
    font-weight: 900;
    margin-bottom: 6px;
}

.score-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
}

.badge-good {
    background: #e8f7ec;
    color: #1f7a37;
}

.badge-mid {
    background: #fff6dd;
    color: #946200;
}

.badge-low {
    background: #fdeaea;
    color: #b42318;
}

.footer-note {
    color: #777;
    font-size: 0.9rem;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 도우미 함수
# -----------------------------
def get_status(score: int):
    if score >= 8:
        return "🟢 좋음", "badge-good"
    elif score >= 6:
        return "🟡 보통", "badge-mid"
    else:
        return "🔴 보완 필요", "badge-low"


def render_score_card(label: str, score: int):
    status_text, badge_class = get_status(score)
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-label">{label}</div>
            <div class="score-value">{score}/10</div>
            <span class="score-badge {badge_class}">{status_text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_list(items):
    if not items:
        st.write("내용 없음")
        return
    for item in items:
        st.markdown(f"- {item}")


def parse_report(report_text: str):
    sections = {
        "핵심한줄코칭": "",
        "점수": {
            "거리 운영": 0,
            "잽 활용": 0,
            "수비 복귀": 0,
            "공격 연결": 0,
        },
        "장점": [],
        "부족한 부분": [],
        "코치 피드백 반영 해석": [],
        "추천 훈련": [],
        "다음 훈련 미션": [],
    }

    current_section = None

    for raw_line in report_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("핵심한줄코칭:"):
            sections["핵심한줄코칭"] = line.replace("핵심한줄코칭:", "").strip()
            current_section = None
            continue

        if line == "[점수]":
            current_section = "점수"
            continue
        elif line == "[장점]":
            current_section = "장점"
            continue
        elif line == "[부족한 부분]":
            current_section = "부족한 부분"
            continue
        elif line == "[코치 피드백 반영 해석]":
            current_section = "코치 피드백 반영 해석"
            continue
        elif line == "[추천 훈련]":
            current_section = "추천 훈련"
            continue
        elif line == "[다음 훈련 미션]":
            current_section = "다음 훈련 미션"
            continue

        if current_section == "점수":
            match = re.match(r"^(거리 운영|잽 활용|수비 복귀|공격 연결)\s*:\s*(\d+)", line)
            if match:
                key = match.group(1)
                value = int(match.group(2))
                value = max(1, min(10, value))
                sections["점수"][key] = value

        elif current_section in ["장점", "부족한 부분", "코치 피드백 반영 해석", "추천 훈련", "다음 훈련 미션"]:
            cleaned = line.lstrip("-").strip()
            if cleaned:
                sections[current_section].append(cleaned)

    return sections


# -----------------------------
# 헤더
# -----------------------------
st.markdown('<div class="main-title">🥊 AI Cornerman</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">복싱 영상 + 상황 메모 + 실제 코치 피드백을 바탕으로 개인 맞춤 코칭 리포트를 생성합니다.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# 입력 영역
# -----------------------------
with st.container(border=True):
    st.markdown("### 훈련 정보 입력")

    col1, col2 = st.columns(2)

    with col1:
        training_type = st.selectbox(
            "훈련 종류",
            ["스파링", "쉐도우", "미트훈련"]
        )

    with col2:
        training_focus = st.selectbox(
            "오늘 특히 신경 쓴 포인트",
            ["선택 안 함", "잽", "거리 유지", "가드", "바디 공격", "뒷손", "카운터 대응", "스텝"]
        )

    uploaded_video = st.file_uploader(
        "훈련 영상을 업로드하세요",
        type=["mp4", "mov", "avi", "mkv"]
    )

    user_memo = st.text_area(
        "상황 메모",
        placeholder="예: 나 파란 헤드기어. 상대는 아웃복싱 스타일. 잽으로 거리 잡으려 했지만 잘 맞지 않았고, 바디잽 들어가다 카운터도 맞았다.",
        height=150
    )

    coach_feedback = st.text_area(
        "실제 코치 피드백",
        placeholder="예: 힘을 빼고 쳐라. 뒷손이 없다. 공격 후 멈추지 마라.",
        height=120
    )

    analyze_clicked = st.button("코칭 리포트 생성", use_container_width=True)

# -----------------------------
# 결과 생성
# -----------------------------
if analyze_clicked:
    if uploaded_video is None:
        st.warning("먼저 영상을 업로드해주세요.")
    elif not user_memo.strip():
        st.warning("상황 메모를 입력해주세요.")
    elif not coach_feedback.strip():
        st.warning("실제 코치 피드백을 입력해주세요.")
    else:
        with st.spinner("AI가 코칭 리포트를 생성 중입니다..."):
            try:
                combined_memo = user_memo
                if training_focus != "선택 안 함":
                    combined_memo += f"\n\n오늘 특히 신경 쓴 포인트: {training_focus}"

                report = generate_boxing_report(
                    training_type=training_type,
                    video_name=uploaded_video.name,
                    user_memo=combined_memo,
                    coach_feedback=coach_feedback
                )

                sections = parse_report(report)

                st.success("코칭 리포트 생성 완료")

                # 핵심 한줄 코칭
                st.markdown(
                    f"""
                    <div class="hero-card">
                        <div class="hero-label">오늘의 핵심 한줄 코칭</div>
                        <div class="hero-text">{sections["핵심한줄코칭"] or "잽을 던진 뒤 바로 복귀하는 동작을 가장 먼저 안정시키세요."}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # 점수 카드 4개
                st.markdown("### 📊 오늘의 코칭 스코어")
                score_cols = st.columns(4)
                score_labels = ["거리 운영", "잽 활용", "수비 복귀", "공격 연결"]

                for col, label in zip(score_cols, score_labels):
                    with col:
                        render_score_card(label, sections["점수"].get(label, 0) or 0)

                # 메인 결과 카드
                top_col1, top_col2 = st.columns(2)

                with top_col1:
                    with st.container(border=True):
                        st.markdown("### ✅ 장점")
                        st.caption("이번 훈련에서 유지할 점")
                        render_list(sections["장점"])

                with top_col2:
                    with st.container(border=True):
                        st.markdown("### ⚠️ 부족한 부분")
                        st.caption("우선 교정이 필요한 부분")
                        render_list(sections["부족한 부분"])

                with st.container(border=True):
                    st.markdown("### 🧠 코치 피드백 반영 해석")
                    st.caption("실제 코치 피드백을 이번 훈련 맥락에서 해석")
                    render_list(sections["코치 피드백 반영 해석"])

                bottom_col1, bottom_col2 = st.columns(2)

                with bottom_col1:
                    with st.container(border=True):
                        st.markdown("### 🥊 추천 훈련")
                        st.caption("다음 훈련에 바로 적용할 드릴")
                        render_list(sections["추천 훈련"])

                with bottom_col2:
                    with st.container(border=True):
                        st.markdown("### 🎯 다음 훈련 미션")
                        st.caption("다음 스파링/훈련에서 집중할 3가지")
                        render_list(sections["다음 훈련 미션"])

                with st.expander("원본 리포트 보기"):
                    st.text(report)

                st.markdown(
                    '<div class="footer-note">다음 단계 추천: 훈련 기록 저장 → 이전 스파링 비교 → 반복 약점 자동 추적</div>',
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
