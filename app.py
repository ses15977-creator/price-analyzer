import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 페이지 설정 및 테마 디자인 (CSS)
# ---------------------------------------------------------
st.set_page_config(
    page_title="SellMetrics Pro | 시장 분석 및 수익성 대시보드",
    page_icon="📈",
    layout="wide"
)

# 인쇄 전용 CSS 및 카드형 고급 UI 스타일링
st.markdown("""
<style>
    /* 기본 폰트 및 스타일 */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }
    .kpi-title { font-size: 0.9rem; color: #64748B; font-weight: 600; }
    .kpi-value { font-size: 1.6rem; color: #0F172A; font-weight: 700; margin-top: 4px; }
    
    /* PDF 인쇄 전용 CSS (1페이지 요약 스타일링) */
    @media print {
        [data-testid="stSidebar"], .no-print, header, footer {
            display: none !important;
        }
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        .print-header {
            display: block !important;
            text-align: center;
            border-bottom: 2px solid #0F172A;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        .stDataFrame { font-size: 10pt !important; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 헤더 섹션
# ---------------------------------------------------------
st.markdown('<div class="main-title">📈 SellMetrics Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">e-Commerce Market Analyzer & Profitability Dashboard</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 사이드바: 파라미터 입력
# ---------------------------------------------------------
st.sidebar.header("🎯 분석 대상 상품 설정")
product_name = st.sidebar.text_input("상품명 / 키워드", "키스틱")
cost_price = st.sidebar.number_input("공급 원가 (원)", min_value=0, value=11300, step=500)
shipping_fee = st.sidebar.number_input("기본 배송비 (원)", min_value=0, value=2900, step=500)
target_price = st.sidebar.number_input("목표 판매가 (원)", min_value=0, value=19900, step=500)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ 플랫폼 수수료율 설정 (%)")
fee_naver = st.sidebar.number_input("네이버 스마트스토어", value=5.8)
fee_always = st.sidebar.number_input("올웨이즈", value=5.5)
fee_kakao = st.sidebar.number_input("카카오톡 쇼핑하기", value=10.0)
fee_coupang = st.sidebar.number_input("쿠팡 (위탁/수수료)", value=10.8)
fee_11st = st.sidebar.number_input("11번가", value=13.0)
fee_gmarket = st.sidebar.number_input("G마켓 / 옥션", value=13.0)

# ---------------------------------------------------------
# 분석 데이터 처리 로직
# ---------------------------------------------------------
market_data = [
    {"플랫폼": "쿠팡", "상품명": f"{product_name} 고급형", "판매가": 17500, "리뷰수": 1205},
    {"플랫폼": "네이버", "상품명": f"{product_name} 본사직영", "판매가": 17900, "리뷰수": 142},
    {"플랫폼": "올웨이즈", "상품명": f"[팀구매] {product_name}", "판매가": 17800, "리뷰수": 512},
    {"플랫폼": "카카오쇼핑", "상품명": f"{product_name} 톡딜세트", "판매가": 18200, "리뷰수": 89},
    {"플랫폼": "G마켓", "상품명": f"[무료배송] {product_name}", "판매가": 18500, "리뷰수": 38},
    {"플랫폼": "11번가", "상품명": f"{product_name} 특가", "판매가": 19000, "리뷰수": 12},
]

df_market = pd.DataFrame(market_data)
lowest_price = df_market["판매가"].min()
lowest_platform = df_market.loc[df_market["판매가"].idxmin()]["플랫폼"]

def calculate_margin(price, cost, shipping, fee_rate):
    fee = price * (fee_rate / 100)
    net_profit = price - cost - shipping - fee
    margin_rate = (net_profit / price) * 100 if price > 0 else 0
    return int(fee), int(net_profit), round(margin_rate, 1)

platforms = [
    {"플랫폼": "네이버 스마트스토어", "수수료율": fee_naver},
    {"플랫폼": "올웨이즈", "수수료율": fee_always},
    {"플랫폼": "카카오톡 쇼핑하기", "수수료율": fee_kakao},
    {"플랫폼": "쿠팡", "수수료율": fee_coupang},
    {"플랫폼": "11번가", "수수료율": fee_11st},
    {"플랫폼": "G마켓 / 옥션", "수수료율": fee_gmarket},
]

margin_results = []
for p in platforms:
    fee, profit, rate = calculate_margin(target_price, cost_price, shipping_fee, p["수수료율"])
    margin_results.append({
        "채널명": p["플랫폼"],
        "수수료율": f"{p['수수료율']}%",
        "공제 수수료": f"{fee:,}원",
        "예상 순이익": f"{profit:,}원",
        "마진율(%)": f"{rate}%",
        "진입 판정": "✅ 가능" if profit > 0 else "❌ 마진 부족"
    })

df_margin = pd.DataFrame(margin_results)
price_diff = target_price - lowest_price

# ---------------------------------------------------------
# 메인 요약 대시보드 (KPI Cards)
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">공급 원가</div><div class="kpi-value">{cost_price:,}원</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">목표 판매가</div><div class="kpi-value">{target_price:,}원</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">시장 최저가</div><div class="kpi-value">{lowest_price:,}원 <span style="font-size:0.8rem; color:#64748B;">({lowest_platform})</span></div></div>', unsafe_allow_html=True)
with col4:
    diff_color = "#EF4444" if price_diff > 0 else "#10B981"
    diff_sign = f"+{price_diff:,}" if price_diff > 0 else f"{price_diff:,}"
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">최저가 대비 격차</div><div class="kpi-value" style="color:{diff_color};">{diff_sign}원</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 본문 분석 결과
# ---------------------------------------------------------
st.subheader("📊 채널별 수익성 및 정산 분석")
st.dataframe(df_margin, use_container_width=True)

st.subheader("🔍 주요 채널 최저가 및 경쟁 현황")
st.dataframe(df_market, use_container_width=True)

st.subheader("💡 시장 진입 종합 소견")
if target_price <= lowest_price:
    st.success(f"**[가격 경쟁력 우수]** 목표 판매가({target_price:,}원)가 시장 최저가({lowest_price:,}원) 이하로 포지셔닝되어 초기 진입 시 상위 노출에 유리합니다.")
else:
    st.warning(f"**[가격 재조정 권장]** 목표 판매가가 시장 최저가 대비 **{price_diff:,}원** 높습니다. 증정품 구성 또는 전용 세트 상품 구성을 권장합니다.")

if cost_price >= lowest_price:
    st.error("**[진입 위험]** 공급 원가가 시장 최저가보다 높거나 같습니다. 공급처와의 원가 재협상이 필수적입니다.")

# ---------------------------------------------------------
# 1페이지 전용 PDF 보고서 출력 버튼
# ---------------------------------------------------------
st.markdown("---")
col_btn, col_info = st.columns([1, 3])

with col_btn:
    if st.button("📄 1페이지 요약 보고서 저장 (PDF)", use_container_width=True):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)

with col_info:
    st.caption("💡 버튼을 누른 후 인쇄 창에서 **[대상 -> PDF로 저장]**을 선택하면 1장 짜리 완벽한 분석 보고서 파일로 저장됩니다.")
