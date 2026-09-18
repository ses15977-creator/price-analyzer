import streamlit as st
import pandas as pd
from supabase import create_client, Client
import json
import urllib.request

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

# Direct REST API를 통한 회원가입 함수 (인코딩 에러 완전 우회)
def direct_signup(email, password):
    url = f"{st.secrets['SUPABASE_URL']}/auth/v1/signup"
    headers = {
        "apikey": st.secrets["SUPABASE_KEY"],
        "Content-Type": "application/json"
    }
    data = json.dumps({"email": email, "password": password}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    with urllib.request.urlopen(req) as response:
        res_body = response.read().decode("utf-8")
        return json.loads(res_body)

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

    # 2. 회원가입 탭 (Direct REST API 사용으로 ASCII 오류 완전 해결)
    with tab2:
        st.subheader("신규 셀러 회원가입")
        with st.form("signup_form"):
            new_email = st.text_input("이메일 주소")
            new_pw = st.text_input("비밀번호", type="password")
            submit_signup = st.form_submit_button("회원가입 완료", type="primary", use_container_width=True)
            
            if submit_signup:
                email_val = new_email.strip()
                pw_val = new_pw.strip()
                
                if email_val and pw_val:
                    try:
                        direct_signup(email_val, pw_val)
                        st.success("회원가입이 완료되었습니다! 🔑 로그인 탭으로 이동해서 로그인해 주세요.")
                    except urllib.error.HTTPError as e:
                        err_msg = e.read().decode("utf-8")
                        st.error(f"회원가입 실패: {err_msg}")
                    except Exception as e:
                        st.error(f"회원가입 실패: {e}")
                else:
                    st.warning("이메일과 비밀번호를 모두 입력해 주세요.")

# -------------------------------------------------------------------
# [메인 대시보드 화면] 로그인 성공 시
# -------------------------------------------------------------------
else:
    st.sidebar.title(f"👤 {st.session_state.user.email} 님")
    
    if st.sidebar.button("로그아웃"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

    st.title("📊 시장 분석 및 수익성 대시보드")
    st.write("SellMetrics Pro에 오신 것을 환영합니다! 아래에서 상품 시장 분석을 시작하세요.")
    st.info("대시보드 기능 및 데이터 분석 툴이 준비되어 있습니다.")
