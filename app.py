import streamlit as st
import pandas as pd

st.set_page_config(page_title="상품 판매성 및 마진 분석기", layout="wide")

st.title("📊 1인 셀러 전용 상품 분석 및 마진 계산기")
st.caption("공급가, 목표가, 온라인 최저가를 비교하고 1페이지 보고서를 생성합니다.")

st.sidebar.header("📥 분석 상품 정보 입력")
product_name = st.sidebar.text_input("상품명 / 키워드", "무선 미니 가습기")
cost_price = st.sidebar.number_input("원가 (공급가, 원)", min_value=0, value=10000, step=500)
shipping_fee = st.sidebar.number_input("배송비 (원)", min_value=0, value=3000, step=500)
target_price = st.sidebar.number_input("목표 판매가 (원)", min_value=0, value=18000, step=500)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ 플랫폼별 수수료 설정 (%)")
fee_naver = st.sidebar.number_input("네이버 스마트스토어", value=5.8)
fee_coupang = st.sidebar.number_input("쿠팡 (위탁/수수료)", value=10.8)
fee_gmarket = st.sidebar.number_input("G마켓 / 옥션", value=13.0)

market_data = [
    {"플랫폼": "쿠팡", "상품명": f"{product_name} 고급형", "판매가": 17500, "리뷰수": 1205},
    {"플랫폼": "네이버", "상품명": f"{product_name} 본사직영", "판매가": 17900, "리뷰수": 142},
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
    {"플랫폼": "네이버 스토어", "수수료율": fee_naver},
    {"플랫폼": "쿠팡", "수수료율": fee_coupang},
    {"플랫폼": "G마켓", "수수료율": fee_gmarket},
]

margin_results = []
for p in platforms:
    fee, profit, rate = calculate_margin(target_price, cost_price, shipping_fee, p["수수료율"])
    margin_results.append({
        "플랫폼": p["플랫폼"],
        "수수료율(%)": f"{p['수수료율']}%",
        "수수료(원)": f"{fee:,}원",
        "예상 순이익(원)": f"{profit:,}원",
        "마진율(%)": f"{rate}%",
        "판매가능여부": "✅ 가능" if profit > 0 else "❌ 마진보장 불가"
    })

df_margin = pd.DataFrame(margin_results)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("입력 공급가", f"{cost_price:,}원")
col2.metric("목표 판매가", f"{target_price:,}원")
col3.metric("온라인 최저가", f"{lowest_price:,}원 ({lowest_platform})")

price_diff = target_price - lowest_price
diff_text = f"{price_diff:+,}원" if price_diff != 0 else "최저가와 동일"
col4.metric("최저가 대비 차이", diff_text, delta_color="inverse")

st.subheader("📌 1. 플랫폼별 마진율 계산")
st.dataframe(df_margin, use_container_width=True)

st.subheader("📌 2. 온라인 최저가 및 경쟁 상품 현황")
st.dataframe(df_market, use_container_width=True)

st.subheader("📌 3. 최종 진입 경쟁력 요약")
if target_price <= lowest_price:
    st.success(f"👍 **경쟁력 있음:** 목표 판매가({target_price:,}원)가 현재 시장 최저가({lowest_price:,}원) 이하입니다.")
else:
    st.warning(f"⚠️ **가격 경쟁 필요:** 목표가가 시장 최저가보다 {price_diff:,}원 높습니다. 사은품 구성이나 세트 판매 전략이 필요합니다.")

if cost_price >= lowest_price:
    st.error("🚨 **진입 불가:** 공급가가 시장 최저가보다 높거나 같습니다. 원가 인하 협상이 필요합니다.")

st.info("💡 Tip: 브라우저 인쇄기능(Ctrl + P 또는 Cmd + P)을 누르면 이 화면 그대로 1장 PDF 보고서로 저장할 수 있습니다.")
