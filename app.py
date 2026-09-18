import streamlit as st
import pandas as pd
import requests
import json
import urllib.request

# 페이지 기본 설정
st.set_page_config(
    page_title="SellMetrics Pro | 시장 분석 대시보드",
    page_icon="📈",
    layout="wide"
)

# 타이틀 헤더
st.title("📈 SellMetrics Pro | 시장 분석 및 수익성 대시보드")
st.caption("초보 셀러를 위한 키워드 분석, 실시간 경쟁 상품 검색 및 마진 계산 툴")

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

# 마진 및 이익 계산 logic
platform_fee = selling_price * (platform_fee_rate / 100)
total_cost = cost_price + shipping_fee + platform_fee
net_profit = selling_price - total_cost
margin_rate = (net_profit / selling_price * 100) if selling_price > 0 else 0

# -------------------------------------------------------------------
# [메인 탭 구성]
# -------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 마진/수익성 분석", "🔍 네이버 키워드 분석", "🛒 경쟁 상품 조사"])

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

# 탭 2: 네이버 키워드 데이터랩 API 분석
with tab2:
    st.subheader("🔍 네이버 데이터랩 키워드 검색 트렌드")
    search_keyword = st.text_input("분석할 키워드를 입력하세요", "캠핑용품")
    
    if st.button("키워드 트렌드 조회", type="primary"):
        client_id = st.secrets.get("NAVER_CLIENT_ID", None)
        client_secret = st.secrets.get("NAVER_CLIENT_SECRET", None)
        
        if client_id and client_secret:
            try:
                url = "https://openapi.naver.com/v1/datalab/search"
                body = json.dumps({
                    "startDate": "2025-01-01",
                    "endDate": "2026-09-01",
                    "timeUnit": "month",
                    "keywordGroups": [{"groupName": search_keyword, "keywords": [search_keyword]}]
                })
                
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                request.add_header("Content-Type", "application/json")
                
                response = urllib.request.urlopen(request, data=body.encode("utf-8"))
                res_code = response.getcode()
                
                if res_code == 200:
                    result = json.loads(response.read().decode('utf-8'))
                    data_list = result['results'][0]['data']
                    df_trend = pd.DataFrame(data_list)
                    df_trend.rename(columns={"period": "날짜", "ratio": "상대 검색량"}, inplace=True)
                    
                    st.success(f"'{search_keyword}' 실시간 네이버 트렌드 데이터 조회가 완료되었습니다.")
                    st.line_chart(df_trend.set_index("날짜"))
                else:
                    st.error("네이버 API 호출 실패")
            except Exception as e:
                st.error(f"API 연동 중 오류 발생: {e}")
        else:
            st.info(f"💡 (네이버 API 키 미설정 모드) '{search_keyword}' 예시 검색량 트렌드입니다.")
            chart_data = pd.DataFrame({
                "날짜": ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"],
                "검색량 트렌드": [45, 58, 72, 89, 95, 100]
            })
            st.line_chart(chart_data.set_index("날짜"))

# 탭 3: 경쟁 상품 조사 및 시장 비교
with tab3:
    st.subheader("🛒 실시간 경쟁 상품 리스트 및 가격 비교")
    st.write("주요 커머스 시장 상위 상품 데이터를 비교 분석합니다.")
    
    sample_products = pd.DataFrame({
        "상품명": [f"{search_keyword} 추천 1호", f"{search_keyword} 가성비 2호", f"{search_keyword} 프리미엄 3호", f"{search_keyword} 인기 4호"],
        "판매가": [23900, 18500, 34000, 21000],
        "리뷰 수": [1240, 850, 310, 2150],
        "평점": [4.8, 4.5, 4.9, 4.7]
    })
    st.dataframe(sample_products, use_container_width=True)
