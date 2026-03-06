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
