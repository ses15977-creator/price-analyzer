import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="SellMetrics Pro | 시장 분석 대시보드",
    page_icon="📈",
    layout="wide"
)

# 타이틀 헤더
st.title("📈 SellMetrics Pro")
st.caption("초보 셀러를 위한 상품 시장 분석 및 마진/수익성 계산기")

st.divider()

# 사이드바 입력 정보
st.sidebar.header("⚙️ 상품 및 마진 설정")

product_name = st.sidebar.text_input("상품명", "샘플 상품")
cost_price = st.sidebar.number_input("원가 (원)", min_value=0, value=10000, step=500)
selling_price = st.sidebar.number_input("판매가 (원)", min_value=0, value=25000, step=1000)
shipping_fee = st.sidebar.number_input("배송비 (원)", min_value=0, value=3000, step=500)
platform_fee_rate = st.sidebar.slider("플랫폼 수수료율 (%)", min_value=0.0, max_value=30.0, value=10.0, step=0.5)

# 마진 및 이익 계산 logic
platform_fee = selling_price * (platform_fee_rate / 100)
total_cost = cost_price + shipping_fee + platform_fee
net_profit = selling_price - total_cost
margin_rate = (net_profit / selling_price * 100) if selling_price > 0 else 0

# 메인 화면 요약 지표
st.subheader(f"📦 {product_name} 수익성 분석 결과")

col1, col2, col3, col4 = st.columns(4)
col1.metric("판매가", f"{selling_price:,} 원")
col2.metric("총 비용", f"{int(total_cost):,} 원")
col3.metric("순이익", f"{int(net_profit):,} 원", delta=f"{int(net_profit):,} 원")
col4.metric("마진율", f"{margin_rate:.1f} %")

st.divider()

# 상세 비용 구조
st.subheader("💡 상세 비용 구조")

fee_df = pd.DataFrame({
    "항목": ["원가", "배송비", "플랫폼 수수료", "순이익"],
    "금액 (원)": [cost_price, shipping_fee, int(platform_fee), int(net_profit)]
})

st.table(fee_df)
