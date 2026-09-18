import streamlit as st
import pandas as pd
import requests
import json

# 페이지 기본 설정
st.set_page_config(
    page_title="SellMetrics Pro | 시장 분석 대시보드",
    page_icon="📈",
    layout="wide"
)

# 타이틀 헤더
st.title("📈 SellMetrics Pro | 시장 분석 및 수익성 대시보드")
st.caption("초보 셀러를 위한 키워드 분석, 상품 검색 및 마진 계산 툴")

st.divider()

# -------------------------------------------------------------------
# [사이드바] 마진 계산기 입력
# -------------------------------------------------------------------
st.sidebar.header("⚙️ 마진 계산기")
product_name = st.sidebar.text_input("상품명", "샘플 상품")
cost_price = st.sidebar.number_input("원가 (원)", min_value=0, value=10000, step=500)
selling_price = st.sidebar.number_input("판매가 (원)", min_value=0, value=25000, step=1000)
shipping_fee = st.sidebar.number_input("배송비 (원)", min_value=0, value=3000, step=500)
platform_fee_rate = st.sidebar.slider("플랫폼 수수료율 (%)", min_value=0.0, max_value=30.0, value=10.0, step=0.5)

# 마진 및 이익 계산
platform_fee = selling_price * (platform_fee_rate / 100)
total_cost = cost_price + shipping_fee + platform_fee
net_profit = selling_price - total_cost
margin_rate = (net_profit / selling_price * 100) if selling_price > 0 else 0

# -------------------------------------------------------------------
# [메인 탭 구성]
# -------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 마진/수익성 분석", "🔍 키워드/시장 분석", "🛒 경쟁 상품 조사"])

# 탭 1: 마진 및 수익성 분석
with tab1:
    st.subheader(f"📦 {product_name} 수익성 분석 결과")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("판매가", f"{selling_price:,} 원")
    col2.metric("총 비용", f"{int(total_cost):,} 원")
    col3.metric("순이익", f"{int(net_profit):,} 원", delta=f"{int(net_profit):,} 원")
    col4.metric("마진율", f"{margin_rate:.1f} %")
    
    st.divider()
    
    st.subheader("💡 상세 비용 구조")
    fee_df = pd.DataFrame({
        "항목": ["원가", "배송비", "플랫폼 수수료", "순이익"],
        "금액 (원)": [cost_price, shipping_fee, int(platform_fee), int(net_profit)]
    })
    st.table(fee_df)

# 탭 2: 키워드 분석
with tab2:
    st.subheader("🔍 네이버/쿠팡 키워드 검색량 분석")
    search_keyword = st.text_input("분석할 키워드를 입력하세요", "캠핑용품")
    
    if st.button("키워드 분석 실행", type="primary"):
        st.info(f"'{search_keyword}' 키워드에 대한 트렌드 분석 결과입니다.")
        
        # 샘플 키워드 트렌드 데이터 시각화
        chart_data = pd.DataFrame({
            "날짜": pd.date_range(start="2026-01-01", periods=6, freq="M").strftime("%Y-%m"),
            "검색량 트렌드": [35, 42, 68, 85, 92, 100]
        })
        st.line_chart(chart_data.set_index("날짜"))

# 탭 3: 경쟁 상품 조사
with tab3:
    st.subheader("🛒 실시간 경쟁 상품 리스트")
    st.write("시장 내 상위 판매 상품의 가격대 및 사양을 비교합니다.")
    
    sample_products = pd.DataFrame({
        "상품명": [f"{search_keyword} 추천 1호", f"{search_keyword} 가성비 2호", f"{search_keyword} 프리미엄 3호"],
        "판매가": [23900, 18500, 34000],
        "리뷰 수": [1240, 850, 310],
        "평점": [4.8, 4.5, 4.9]
    })
    st.dataframe(sample_products, use_container_width=True)
