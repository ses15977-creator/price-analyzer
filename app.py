import streamlit as st
import pandas as pd
from supabase import create_client, Client
import urllib.parse

# 페이지 기본 설정
st.set_page_config(
    page_title="SellMetrics Pro | 시장 분석 대시보드",
    page_icon="📈",
    layout="wide"
)

# Supabase 연동 설정
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# 세션 상태 초기화
if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------------------------------------------------
# [인증 화면] 로그인 / 회원가입
# -------------------------------------------------------------------
if st.session_state.user is None:
    st.title("📈 SellMetrics Pro")
    st.caption("서비스 이용을 위해 로그인 또는 회원가입을 해주세요.")
    
    tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])
    
    # 1. 로그인 탭
    with tab1:
        st.subheader("셀러 로그인")
        with st.form("login_form"):
            login_email = st.text_input("이메일 주소")
            login_pw = st.text_input("비밀번호", type="password")
            submit_login = st.form_submit_button("로그인 완료", type="primary", use_container_width=True)
            
            if submit_login:
                if login_email.strip() and login_pw.strip():
                    try:
                        res = supabase.auth.sign_in_with_password({
                            "email": login_email.strip(),
                            "password": login_pw.strip()
                        })
                        st.session_state.user = res.user
                        st.success("로그인 성공!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"로그인 실패: {e}")
                else:
                    st.warning("이메일과 비밀번호를 모두 입력해 주세요.")

    # 2. 회원가입 탭 (한글 ASCII 인코딩 에러 완전 보완)
    with tab2:
        st.subheader("신규 셀러 회원가입")
        with st.form("signup_form"):
            new_email = st.text_input("이메일 주소")
            new_pw = st.text_input("비밀번호", type="password")
            user_name = st.text_input("성함 / 셀러명")
            submit_signup = st.form_submit_button("회원가입 완료", type="primary", use_container_width=True)
            
            if submit_signup:
                email_val = new_email.strip()
                pw_val = new_pw.strip()
                name_val = user_name.strip()
                
                if email_val and pw_val and name_val:
                    try:
                        # 한글 인코딩 오류 방지 (URL 인코딩 변환)
                        safe_name = urllib.parse.quote(name_val)
                        
                        res = supabase.auth.sign_up({
                            "email": email_val,
                            "password": pw_val,
                            "options": {
                                "data": {
                                    "name": safe_name
                                }
                            }
                        })
                        st.success("회원가입이 성공적으로 완료되었습니다! 🔑 로그인 탭으로 이동해서 로그인해 주세요.")
                    except Exception as e:
                        st.error(f"회원가입 실패: {e}")
                else:
                    st.warning("모든 항목을 입력해 주세요.")

# -------------------------------------------------------------------
# [메인 대시보드 화면] 로그인 성공 시
# -------------------------------------------------------------------
else:
    user_data = st.session_state.user.user_metadata or {}
    encoded_name = user_data.get("name", "")
    
    # URL 인코딩된 이름을 다시 원래 한글로 디코딩
    try:
        display_name = urllib.parse.unquote(encoded_name) if encoded_name else st.session_state.user.email
    except:
        display_name = st.session_state.user.email
    
    st.sidebar.title(f"👤 {display_name} 님")
    st.sidebar.caption(f"계정: {st.session_state.user.email}")
    
    if st.sidebar.button("로그아웃"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

    st.title("📊 시장 분석 및 수익성 대시보드")
    st.write("SellMetrics Pro에 오신 것을 환영합니다! 아래에서 상품 시장 분석을 시작하세요.")
    st.info("대시보드 기능 및 데이터 분석 툴이 준비되어 있습니다.")
