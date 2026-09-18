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

# 고급 UI 스타일링 및 1페이지 전용 보고서 인쇄 CSS
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.0rem; color: #64748B; margin-bottom: 1.5rem; }
    
    .kpi-container { display: flex; gap: 10px; margin-bottom: 20px; }
    .kpi-card {
        flex: 1;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .kpi-title { font-size: 0.85rem; color: #64748B; font-weight: 600; }
    .kpi-value { font-size: 1.4rem; color: #0F172A; font-weight: 700; margin-top: 2px; }

    /* 인쇄 시 화면의 일반 대시보드는 숨기고 'Print Report' 전용 요약 영역만 1페이지로 출력 */
    @media screen {
        .print-only-report { display: none !important; }
    }
    
    @media print {
        /* 웹 UI 요소 완전히 제거 */
        [data-testid="stSidebar"], .no-print, header, footer, .stButton, .screen-only {
            display: none !important;
        }
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        
        /* 1페이지 보고서 출력 설정 */
        .print-only-report {
            display: block !important;
            padding: 20px;
            font-family: Arial, sans-serif;
            color: #1E293B;
        }
        .report-header {
            text-align: center;
            border-bottom: 2px solid #0F172A;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        .report-title { font-size: 20pt; font-weight: bold; }
        .report-sub { font-size: 10pt; color: #475569; }
        .section-title { font-size: 12pt; font-weight: bold; margin-top: 15px; margin-bottom: 5px; border-left: 4px solid #0F172A; padding-left: 8px; }
        
        table { width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 9pt; }
        th, td { border: 1px solid #CBD5E1; padding: 6px 8px; text-align: left; }
        th { background-color: #F1F5F9; font-weight: bold; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 사이드바 입력 설정
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
# 데이터 계산 및 처리
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
        "마진율": f"{rate}%",
        "진입 판정": "✅ 가능" if profit > 0 else "❌ 불가"
    })

df_margin = pd.DataFrame(margin_results)
price_diff = target_price - lowest_price

# 진입 소견 텍스트 생성
if target_price <= lowest_price:
    summary_opinion = f"목표 판매가({target_price:,}원)가 시장 최저가({lowest_price:,}원) 이하로 포지셔닝되어 가격 경쟁력이 우수합니다."
else:
    summary_opinion = f"목표 판매가가 시장 최저가 대비 {price_diff:,}원 높습니다. 증정품 구성 또는 세트 상품 구성을 통한 가치 제고가 필요합니다."

if cost_price >= lowest_price:
    summary_opinion += " (🚨 공급 원가가 최저가 이상이므로 원가 재협상이 필수적입니다.)"

# ---------------------------------------------------------
# [웹 화면 전용] 대시보드 출력
# ---------------------------------------------------------
st.markdown('<div class="screen-only">', unsafe_allow_html=True)
st.markdown('<div class="main-title">📈 SellMetrics Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">e-Commerce Market Analyzer & Profitability Dashboard</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("공급 원가", f"{cost_price:,}원")
col2.metric("목표 판매가", f"{target_price:,}원")
col3.metric("시장 최저가", f"{lowest_price:,}원 ({lowest_platform})")
diff_text = f"+{price_diff:,}원" if price_diff > 0 else f"{price_diff:,}원"
col4.metric("최저가 대비 격차", diff_text)

st.subheader("📊 채널별 수익성 및 정산 분석")
st.dataframe(df_margin, use_container_width=True)

st.subheader("🔍 주요 채널 최저가 및 경쟁 현황")
st.dataframe(df_market, use_container_width=True)

st.subheader("💡 시장 진입 종합 소견")
st.info(summary_opinion)

st.markdown("---")
col_btn, col_info = st.columns([1, 3])
with col_btn:
    if st.button("📄 1페이지 요약 보고서 저장 (PDF)", use_container_width=True):
        st.components.v1.html("<script>window.parent.print();</script>", height=0)
with col_info:
    st.caption("💡 버튼 클릭 후 인쇄 창에서 **[대상 -> PDF로 저장]**을 선택하면 요약된 1장짜리 보고서로 출력됩니다.")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# [PDF 인쇄 전용] 1페이지 요약 보고서 레이아웃 (Print-Only)
# ---------------------------------------------------------
st.markdown(f"""
<div class="print-only-report">
    <div class="report-header">
        <div class="report-title">SELLMETRICS PRO : 상품 분석 요약 보고서</div>
        <div class="report-sub">분석 대상 상품: <b>{product_name}</b></div>
    </div>
    
    <div class="section-title">1. 핵심 가격 지표 요약</div>
    <table>
        <tr>
            <th>공급 원가</th>
            <th>기본 배송비</th>
            <th>목표 판매가</th>
            <th>시장 최저가</th>
            <th>최저가 대비 격차</th>
        </tr>
        <tr>
            <td>{cost_price:,}원</td>
            <td>{shipping_fee:,}원</td>
            <td>{target_price:,}원</td>
            <td>{lowest_price:,}원 ({lowest_platform})</td>
            <td>{diff_text}</td>
        </tr>
    </table>
    
    <div class="section-title">2. 채널별 마진 및 수익 분석</div>
    {df_margin.to_html(index=False)}
    
    <div class="section-title">3. 주요 플랫폼 경쟁 현황</div>
    {df_market.to_html(index=False)}
    
    <div class="section-title">4. 최종 시장 진입 소견</div>
    <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; padding: 10px; border-radius: 4px; font-size: 9.5pt;">
        <b>종합 의견:</b> {summary_opinion}
    </div>
</div>
""", unsafe_allow_html=True)
