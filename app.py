import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="내 증상 건강 가이드",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 내 증상에 맞는 병원 방문 가이드")
st.write("현재 증상을 입력하면 의료기관 방문에 관한 일반적인 안내를 제공합니다.")
st.warning("이 프로그램은 의학적 진단을 내리지 않습니다. 증상이 걱정되면 보호자와 의료진에게 상담하세요.")

# ==========================================
# [핵심 요소 1] 리스트 (list)
# ==========================================
symptoms = ["두통", "복통", "목 통증", "기침", "발열", "어지러움", "기타"]

danger_signs = [
    "호흡곤란",
    "의식 변화",
    "갑작스럽고 심한 두통",
    "심한 가슴 통증",
    "갑작스러운 마비 또는 말하기 어려움"
]

normal_signs = ["발열", "구토", "어지러움", "심한 피로"]

# 리스트 덧셈(+)을 이용해 전체 선택지 리스트 생성
all_other_signs = danger_signs + normal_signs + ["없음"]


# ==========================================
# [핵심 요소 2] 함수 (def)
# ==========================================
def check_symptom(symptom, pain_level, duration, signs):
    
    # ------------------------------------------
    # [핵심 요소 3] 반복구조 (for문)
    # 사용자가 선택한 동반 증상(signs) 리스트를 하나씩 꺼내어 위험 신호인지 반복 검사
    # ------------------------------------------
    for sign in signs:
        if sign in danger_signs:
            return (
                "응급 의료 도움 필요",
                f"위험 신호('{sign}')가 확인되었습니다. 즉시 보호자에게 알리고 119 또는 응급실의 도움을 받으세요."
            )

    # ------------------------------------------
    # [핵심 요소 4] 선택구조 (if - elif - else)
    # 통증 정도, 지속 기간, 동반 증상 조건에 따라 결과를 분기
    # ------------------------------------------
    if pain_level >= 8:
        return (
            "빠른 의료진 상담 필요",
            "통증이 매우 심합니다. 보호자에게 알리고 신속하게 병원에서 진료를 받으세요."
        )
    elif duration == "4일 이상":
        return (
            "병원 진료 권장",
            "증상이 여러 날 지속되고 있습니다. 병원에서 정확한 원인을 확인하는 것이 좋습니다."
        )
    elif pain_level >= 5:
        return (
            "병원 진료 권장",
            "통증이 비교적 큰 편입니다. 보호자와 상의하여 병원에서 진료받으세요."
        )
    elif "발열" in signs or "구토" in signs:
        return (
            "증상 관찰 및 진료 상담",
            "발열이나 구토 등 다른 증상이 동반되었습니다. 보호자에게 알리고 의료진과 상담하세요."
        )
    else:
        return (
            "건강 상태 관찰",
            "특별한 위험 신호가 없습니다. 충분히 쉬면서 상태를 관찰하고, 증상이 악화되면 병원을 방문하세요."
        )


# 2. 사용자 입력 화면
st.subheader("① 현재 증상 입력")
symptom = st.selectbox("어떤 증상이 있나요?", symptoms)
pain_level = st.slider("통증 정도를 선택하세요. (1: 약함 ~ 10: 매우 심함)", 1, 10, 3)
duration = st.radio("증상이 얼마나 지속되었나요?", ["하루 미만", "1~3일", "4일 이상"])

st.subheader("② 동반 증상 선택")
signs = st.multiselect("함께 나타나는 증상을 선택하세요.", all_other_signs)

# 3. 분석 버튼 클릭 시 실행 (선택구조 활용)
if st.button("증상 분석하기"):

    # '없음'과 다른 증상을 동시에 골랐는지 확인하는 선택구조 (if-else)
    if "없음" in signs and len(signs) > 1:
        st.error("⚠️ '없음'과 다른 동반 증상을 동시에 선택할 수 없습니다. 다시 선택해 주세요.")
    else:
        # 정의한 함수(check_symptom) 호출
        result, message = check_symptom(symptom, pain_level, duration, signs)

        st.subheader("③ 분석 결과")

        # 결과에 따라 알림창 색상을 다르게 출력하는 선택구조 (if-elif-else)
        if result == "응급 의료 도움 필요":
            st.error(result)
        elif result in ["빠른 의료진 상담 필요", "병원 진료 권장"]:
            st.warning(result)
        else:
            st.info(result)

        st.write(message)

        # 입력 정보 표로 정리
        data = {
            "항목": ["증상 종류", "통증 정도", "지속 기간", "동반 증상"],
            "입력 결과": [
                symptom,
                f"{pain_level}점",
                duration,
                ", ".join(signs) if signs else "선택 없음"
            ]
        }
        df = pd.DataFrame(data)

        st.subheader("④ 입력 정보 확인")
        st.table(df)

st.divider()
st.caption("본 프로그램은 학습용 건강 정보 안내 프로그램이며 의료진의 진단을 대신할 수 없습니다.")
