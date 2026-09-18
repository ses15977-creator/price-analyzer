import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ---------------------------------------------------------
# 1. 페이지 및 기본 UI 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="SellMetrics Pro | 시장 분석 및 수익성 대시보드",
    page_icon="https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #1E293B;
    margin-bottom: 0.2rem;
}
.sub-title {
    font-size: 1.0rem;
    color: #64748B;
    margin-bottom: 1.5rem;
}
.card-box {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 사이드바 입력
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
# 3. 데이터 계산 및 기본 마진 분석
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
max_review = df_market["리뷰수"].max()

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
diff_text = f"+{price_diff:,}원" if price_diff > 0 else f"{price_diff:,}원"

if target_price <= lowest_price:
    summary_opinion = f"목표 판매가({target_price:,}원)가 현재 시장 최저가({lowest_price:,}원) 이하로 설정되어 가격 경쟁력이 매우 우수합니다."
else:
    summary_opinion = f"목표 판매가가 시장 최저가 대비 <b>{price_diff:,}원</b> 높습니다. 사은품 증정이나 세트 상품 구성을 통한 추가 가치 제고 전략이 필요합니다."

if cost_price >= lowest_price:
    summary_opinion += "<br><span style='color:#DC2626;'>🚨 <b>경고:</b> 공급 원가가 시장 최저가 이상이므로 원가 인하 협상이 시급합니다.</span>"

# ---------------------------------------------------------
# 4. 차별화 기능 1, 2, 3 로직 계산
# ---------------------------------------------------------

# [차별화 1] 소싱 리스크 평가 스코어카드
risk_score = 100
risk_reasons = []

cost_ratio = (cost_price / target_price * 100) if target_price > 0 else 100
if cost_ratio > 65:
    risk_score -= 30
    risk_reasons.append(f"원가율 부담 높음 ({cost_ratio:.1f}% > 기준 65%)")
elif cost_ratio > 50:
    risk_score -= 15
    risk_reasons.append(f"원가율 보통 ({cost_ratio:.1f}%)")

if target_price > lowest_price:
    risk_score -= 25
    risk_reasons.append(f"시장 최저가 대비 {price_diff:,}원 비쌈")

if max_review >= 1000 and target_price > lowest_price:
    risk_score -= 20
    risk_reasons.append("기존 상위 권 선점자(리뷰 1,000개 이상) 대비 가격 열세")

if risk_score >= 80:
    risk_grade, risk_color = "🟢 안전 (소싱 강력 추천)", "#16A34A"
elif risk_score >= 50:
    risk_grade, risk_color = "🟡 주의 (전략 수정 필요)", "#D97706"
else:
    risk_grade, risk_color = "🔴 위험 (진입 재검토 권장)", "#DC2626"

# [차별화 2] 스마트 광고 한도 & ROAS 역산기 (네이버 기준 예시)
avg_fee_rate = fee_naver
_, avg_profit, _ = calculate_margin(target_price, cost_price, shipping_fee, avg_fee_rate)

if avg_profit > 0 and target_price > 0:
    min_bep_roas = round((target_price / avg_profit) * 100, 1)
    max_cpc_100per = int(avg_profit)            # 전환율 1% 기준 (100회 클릭당 1건 구매)
    max_cpc_50per = int(avg_profit * 0.02)     # 전환율 2% 기준
else:
    min_bep_roas = 0
    max_cpc_100per = 0
    max_cpc_50per = 0

# ---------------------------------------------------------
# 5. 메인 화면 대시보드 출력
# ---------------------------------------------------------
st.markdown('<div class="main-title">📈 SellMetrics Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">e-Commerce Market Analyzer & Profitability Dashboard</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("공급 원가", f"{cost_price:,}원")
col2.metric("목표 판매가", f"{target_price:,}원")
col3.metric("시장 최저가", f"{lowest_price:,}원", delta=lowest_platform)
col4.metric("최저가 대비 격차", diff_text)

# ---------------------------------------------------------
# 🌟 차별화 1: 소싱 리스크 평가 스코어카드 섹션
# ---------------------------------------------------------
st.markdown("---")
st.subheader("🛡️ 소싱 리스크 평가 스코어카드 (SellMetrics Score)")
col_sc1, col_sc2 = st.columns([1, 2])
with col_sc1:
    st.markdown(f"""
    <div style="text-align:center; padding: 20px; background-color: #F8FAFC; border-radius: 8px; border: 2px solid {risk_color};">
        <div style="font-size: 1.1rem; color: #475569; font-weight: bold;">진입 안전도 점수</div>
        <div style="font-size: 2.8rem; font-weight: 900; color: {risk_color};">{risk_score}점</div>
        <div style="font-size: 1.0rem; font-weight: bold; color: {risk_color};">{risk_grade}</div>
    </div>
    """, unsafe_allow_html=True)
with col_sc2:
    st.markdown("##### 📌 리스크 요인 진단 리포트")
    if risk_reasons:
        for reason in risk_reasons:
            st.write(f"- ⚠️ {reason}")
    else:
        st.write("- ✅ 감지된 주요 리스크가 없습니다. 가격 및 원가 경쟁력이 우수합니다.")

# ---------------------------------------------------------
# 📊 기존 마진 및 시장 현황
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📊 채널별 수익성 및 정산 분석")
st.dataframe(df_margin, use_container_width=True)

# ---------------------------------------------------------
# 🌟 차별화 2 & 3: 탭 메뉴로 추가 기능 탑재
# ---------------------------------------------------------
st.markdown("---")
tab_opt, tab_ad = st.tabs(["🎯 [신기능] 마켓별 역산 판매가 추천", "📢 [신기능] 스마트 광고 한도 & ROAS 역산기"])

with tab_opt:
    st.markdown("##### 💡 목표 순이익을 얻기 위한 각 채널별 권장 판매가")
    target_desired_profit = st.number_input("원하는 목표 순이익 입력 (원)", min_value=1000, value=3000, step=500)
    
    calc_rows = []
    for p in platforms:
        rate = p["수수료율"] / 100
        # 순이익 = 판매가 - 원가 - 배송비 - (판매가 * 수수료율)
        # 판매가 * (1 - 수수료율) = 순이익 + 원가 + 배송비
        rec_price = (target_desired_profit + cost_price + shipping_fee) / (1 - rate)
        rec_price = int(round(rec_price, -2)) # 100원 단위 반올림
        
        calc_rows.append({
            "채널명": p["플랫폼"],
            "수수료율": f"{p['수수료율']}%",
            "희망 순이익": f"{target_desired_profit:,}원",
            "권장 판매가": f"{rec_price:,}원",
            "현재 목표가 차이": f"{rec_price - target_price:+,}원"
        })
    st.dataframe(pd.DataFrame(calc_rows), use_container_width=True)

with tab_ad:
    st.markdown("##### 🎯 적자 없는 마케팅/광고 집행 가이드 (네이버 스마트스토어 기준)")
    col_ad1, col_ad2, col_ad3 = st.columns(3)
    col_ad1.metric("최소 목표 ROAS (손익분기점)", f"{min_bep_roas}%", help="이 ROAS 이상이어야 광고 집행 시 적자를 보지 않습니다.")
    col_ad2.metric("최대 클릭당 단가 (전환율 1%)", f"{max_cpc_100per:,}원", help="구매전환율 1% 가정 시 허용 가능한 1클릭당 최대 광고비입니다.")
    col_ad3.metric("최대 클릭당 단가 (전환율 2%)", f"{max_cpc_50per:,}원", help="구매전환율 2% 가정 시 허용 가능한 1클릭당 최대 광고비입니다.")

st.markdown("---")
st.subheader("🔍 주요 채널 최저가 및 경쟁 현황")
st.dataframe(df_market, use_container_width=True)

st.subheader("💡 시장 진입 종합 소견")
st.info(summary_opinion.replace("<b>","").replace("</b>","").replace("<br>"," ").replace("<span style='color:#DC2626;'>","").replace("</span>",""))

st.markdown("---")

# ---------------------------------------------------------
# 6. 요약 보고서 인쇄 기능 (A4 1페이지 규격 유지)
# ---------------------------------------------------------
margin_rows_html = "".join([
    f"<tr><td>{r['채널명']}</td><td>{r['수수료율']}</td><td>{r['공제 수수료']}</td><td>{r['예상 순이익']}</td><td>{r['마진율']}</td><td>{r['진입 판정']}</td></tr>"
    for r in margin_results
])

market_rows_html = "".join([
    f"<tr><td>{r['플랫폼']}</td><td style='text-align:left;'>{r['상품명']}</td><td>{r['판매가']:,}원</td><td>{r['리뷰수']:,}</td></tr>"
    for r in market_data
])

printable_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SELLMETRICS PRO - {product_name} 요약 보고서</title>
    <style>
        @page {{ size: A4 portrait; margin: 10mm; }}
        body {{ font-family: 'Malgun Gothic', sans-serif; color: #1E293B; margin: 0; padding: 10px; font-size: 9.5pt; }}
        .report-header {{ text-align: center; border-bottom: 2px solid #0F172A; padding-bottom: 8px; margin-bottom: 12px; }}
        .report-title {{ font-size: 16pt; font-weight: bold; color: #0F172A; }}
        .report-sub {{ font-size: 9.5pt; color: #475569; margin-top: 4px; }}
        .section-title {{ font-size: 10.5pt; font-weight: bold; margin-top: 12px; margin-bottom: 6px; border-left: 4px solid #0F172A; padding-left: 6px; color: #0F172A; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; font-size: 8.5pt; }}
        th, td {{ border: 1px solid #CBD5E1; padding: 5px 6px; text-align: center; }}
        th {{ background-color: #F1F5F9; font-weight: bold; color: #1E293B; }}
        .opinion-box {{ background-color: #F8FAFC; border: 1px solid #CBD5E1; padding: 8px 10px; border-radius: 4px; font-size: 9pt; line-height: 1.4; }}
    </style>
</head>
<body>
    <div class="report-header">
        <div class="report-title">SELLMETRICS PRO : 상품 분석 요약 보고서</div>
        <div class="report-sub">분석 대상 상품: <b>{product_name}</b> | 진입 안전도: <b>{risk_score}점 ({risk_grade})</b></div>
    </div>
    
    <div class="section-title">1. 핵심 가격 지표 요약</div>
    <table>
        <thead>
            <tr>
                <th>공급 원가</th>
                <th>기본 배송비</th>
                <th>목표 판매가</th>
                <th>시장 최저가</th>
                <th>최저가 대비 격차</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>{cost_price:,}원</b></td>
                <td>{shipping_fee:,}원</td>
                <td><b>{target_price:,}원</b></td>
                <td>{lowest_price:,}원 ({lowest_platform})</td>
                <td><b>{diff_text}</b></td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">2. 채널별 마진 및 수익 분석</div>
    <table>
        <thead>
            <tr>
                <th>채널명</th>
                <th>수수료율</th>
                <th>공제 수수료</th>
                <th>예상 순이익</th>
                <th>마진율</th>
                <th>진입 판정</th>
            </tr>
        </thead>
        <tbody>
            {margin_rows_html}
        </tbody>
    </table>

    <div class="section-title">3. 마케팅 집행 한도 (손익분기점)</div>
    <table>
        <thead>
            <tr>
                <th>최소 목표 ROAS</th>
                <th>클릭당 최대 허용 단가 (전환율 1%)</th>
                <th>클릭당 최대 허용 단가 (전환율 2%)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>{min_bep_roas}%</b></td>
                <td>{max_cpc_100per:,}원</td>
                <td>{max_cpc_50per:,}원</td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">4. 주요 플랫폼 경쟁 현황</div>
    <table>
        <thead>
            <tr>
                <th>플랫폼</th>
                <th>상품명</th>
                <th>판매가</th>
                <th>리뷰 수</th>
            </tr>
        </thead>
        <tbody>
            {market_rows_html}
        </tbody>
    </table>

    <div class="section-title">5. 최종 시장 진입 소견</div>
    <div class="opinion-box">
        <b>[종합 의견]</b> {summary_opinion}
    </div>
</body>
</html>
"""

btn_component = f"""
<div style="font-family: sans-serif; padding-top: 5px;">
    <button onclick="openPrintTab()" style="
        width: 100%;
        padding: 10px 12px;
        background-color: #0F172A;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        font-size: 13px;
        line-height: 1.4;
        cursor: pointer;">
        📄 1페이지 요약 보고서<br>새 탭에서 인쇄/저장 (PDF)
    </button>
</div>
<script>
function openPrintTab() {{
    var reportContent = `{printable_html}`;
    var win = window.top.open('', '_blank');
    if (win) {{
        win.document.open();
        win.document.write(reportContent);
        win.document.close();
        win.focus();
        setTimeout(function() {{
            win.print();
        }}, 400);
    }} else {{
        alert('팝업이 차단되었습니다. 주소창 우측에서 팝업 허용을 해주세요.');
    }}
}}
</script>
"""

col_btn, col_info = st.columns([1.3, 2.7])
with col_btn:
    components.html(btn_component, height=100)
with col_info:
    st.caption("💡 버튼 클릭 시 **새 탭**에서 요약 보고서만 깨끗하게 작성되어 1페이지 인쇄 창이 실행됩니다.")
