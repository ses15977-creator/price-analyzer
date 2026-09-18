import streamlit.components.v1 as components

# ---------------------------------------------------------
# [1번 방법] 새 브라우저 탭 팝업을 통한 1페이지 전용 인쇄 시스템
# ---------------------------------------------------------

# 1. 인쇄용 표 HTML 생성
margin_rows_html = "".join([
    f"<tr><td>{r['채널명']}</td><td>{r['수수료율']}</td><td>{r['공제 수수료']}</td><td>{r['예상 순이익']}</td><td>{r['마진율']}</td><td>{r['진입 판정']}</td></tr>"
    for r in margin_results
])

market_rows_html = "".join([
    f"<tr><td>{r['플랫폼']}</td><td style='text-align:left;'>{r['상품명']}</td><td>{r['판매가']:,}원</td><td>{r['리뷰수']:,}</td></tr>"
    for r in market_data
])

# 2. 새 탭에 보여줄 순수 Pure HTML 문서 작성 (외부 UI 완전히 배제)
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
        <div class="report-sub">분석 대상 상품: <b>{product_name}</b></div>
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
    
    <div class="section-title">3. 주요 플랫폼 경쟁 현황</div>
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
    
    <div class="section-title">4. 최종 시장 진입 소견</div>
    <div class="opinion-box">
        <b>[종합 의견]</b> {summary_opinion}
    </div>
</body>
</html>
"""

# 3. 새 탭을 열어 HTML을 주입하고 인쇄를 호출하는 자바스크립트 버튼
btn_component = f"""
<div style="font-family: sans-serif;">
    <button onclick="openPrintTab()" style="
        width: 100%;
        padding: 12px;
        background-color: #0F172A;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
        cursor: pointer;">
        📄 1페이지 요약 보고서 새 탭에서 인쇄/저장 (PDF)
    </button>
</div>

<script>
function openPrintTab() {{
    var reportContent = `{printable_html}`;
    // 부모 창(top) 기준으로 완전히 새로운 브라우저 탭 생성
    var win = window.top.open('', '_blank');
    if (win) {{
        win.document.open();
        win.document.write(reportContent);
        win.document.close();
        win.focus();
        // 문서 로딩 후 인쇄 창 실행
        setTimeout(function() {{
            win.print();
        }}, 400);
    }} else {{
        alert('팝업이 차단되었습니다. 브라우저 주소창 우측에서 팝업 허용을 해주세요.');
    }}
}}
</script>
"""

col_btn, col_info = st.columns([1.2, 2.8])
with col_btn:
    components.html(btn_component, height=65)

with col_info:
    st.caption("💡 버튼 클릭 시 **새 탭**에서 깔끔한 요약 보고서만 작성되어 인쇄 창이 바로 나타납니다.")
