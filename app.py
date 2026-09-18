import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="SellMetrics Pro | 시장 분석 대시보드",
    page_icon="📈",
    layout="wide"
)

# -------------------------------------------------------------------
# [메인 대시보드 화면] 인증 없이 바로 진입
# -------------------------------------------------------------------
st.title("📊 SellMetrics Pro | 시장 분석 및 수익성 대시보드")
st.caption("회원 인증 없이 바로 이용 가능한 대시보드 모드입니다.")

st.divider()

# 사이드바 설정
st.sidebar.title("📈 SellMetrics Pro")
st.sidebar.info("서비스 메뉴")

# 메인 콘텐츠 영역
st.subheader("Welcome to SellMetrics Pro")
st.write("아래에서 상품 시장 분석 및 수익성 계산 기능을 활용하세요.")

st.info("💡 분석 도구 및 데이터 시각화 기능 구현 준비 완료!")
