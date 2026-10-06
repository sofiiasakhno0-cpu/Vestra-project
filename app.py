import streamlit as st
import json, hashlib
from pathlib import Path
from data.company import COMPANIES
from data.market import get_market_snapshot, get_price_history
from data.fundamentals import get_fundamentals
from data.automotive import get_automotive_metrics
from data.xstocks import get_xstock_price, prepare_investment
from analytics.score import calculate_vestra_score
from analytics.shield import simulate_shield

st.set_page_config(page_title="Vestra", page_icon="V", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu,footer,header{visibility:hidden}.stApp{background:#000;color:#f5f5f5}
[data-testid="stHeader"], [data-testid="stToolbar"], section[data-testid="stSidebar"]{display:none}
.block-container{max-width:1500px;padding:2rem 3rem 4rem}
.vestra-title{font-size:2.7rem;font-weight:700;letter-spacing:-.04em}
.vestra-subtitle,.muted{color:#888}.section-title{font-size:1.35rem;font-weight:650;margin:1.3rem 0 .75rem}
.card{background:#080808;border:1px solid #242424;border-radius:16px;padding:18px 20px;height:100%}
.metric-label{color:#888;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em}
.metric-value{font-size:1.4rem;font-weight:650;margin-top:5px}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{background:#080808!important;border-color:#303030!important}
input{color:#fff!important}.stButton>button{background:#101010;color:#fff;border:1px solid #343434;border-radius:10px}
.small-source{font-size:.72rem;color:#777;margin-top:7px}.invest-box{border:1px solid #343434;border-radius:16px;padding:18px;background:#080808}
</style>
""", unsafe_allow_html=True)

DATA=Path(".vestra"); DATA.mkdir(exist_ok=True); USERS=DATA/"users.json"
def load_users():
    try: return json.loads(USERS.read_text(encoding="utf-8")) if USERS.exists() else {}
    except: return {}
def save_users(x): USERS.write_text(json.dumps(x,indent=2),encoding="utf-8")
def ph(x): return hashlib.sha256(x.encode()).hexdigest()
if "user" not in st.session_state: st.session_state.user=None

with st.expander("Account", expanded=st.session_state.user is None):
    if st.session_state.user:
        st.write(f"Signed in as **{st.session_state.user}**")
        if st.button("Log out"): st.session_state.user=None; st.rerun()
    else:
        mode=st.radio("Account",["Log in","Create account"],horizontal=True,label_visibility="collapsed")
        email=st.text_input("Email"); password=st.text_input("Password",type="password")
        if mode=="Create account":
            if st.button("Create account"):
                users=load_users()
                if not email or not password: st.error("Enter email and password.")
                elif email.lower() in users: st.error("Account already exists.")
                else:
                    users[email.lower()]={"password":ph(password)}; save_users(users)
                    st.session_state.user=email.lower(); st.rerun()
        elif st.button("Log in"):
            r=load_users().get(email.lower())
            if r and r.get("password")==ph(password): st.session_state.user=email.lower(); st.rerun()
            else: st.error("Incorrect email or password.")

st.markdown("<div class='vestra-title'>Vestra</div><div class='vestra-subtitle'>Invest smarter. Drive further. · Automotive investment intelligence</div>",unsafe_allow_html=True)

c1,c2,c3=st.columns([2.2,1,1])
with c1: ticker=st.selectbox("Company",list(COMPANIES),format_func=lambda x:f"{x} · {COMPANIES[x]['name']}")
with c2: period=st.selectbox("Market period",["1mo","3mo","6mo","1y","2y"],index=3)
with c3: shield=st.selectbox("Vestra Shield",[0,25,50],index=2,format_func=lambda x:f"{x}%")
company=COMPANIES[ticker]; snap=get_market_snapshot(ticker); hist=get_price_history(ticker,period); fund=get_fundamentals(ticker); score=calculate_vestra_score(snap,fund)
ai=get_automotive_metrics(ticker,fund)

st.markdown("<div class='section-title'>Market Intelligence</div>",unsafe_allow_html=True)
cols=st.columns(4)
for col,label,value in zip(cols,["Price","Previous close","Market cap","Vestra Score"],[snap.get("price","—"),snap.get("previous_close","—"),snap.get("market_cap","—"),f"{score:.1f}"]):
    with col: st.markdown(f"<div class='card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>",unsafe_allow_html=True)
if hist is not None and not hist.empty: st.line_chart(hist["Close"])

# Working live-data token card: public xStocks pricing requires no API key.
token=company.get("tokenized")
xq=get_xstock_price(token)
if token and not token.startswith("Not "):
    st.markdown("<div class='section-title'>Tokenized Investment</div>",unsafe_allow_html=True)
    a,b=st.columns([2,1])
    with a:
        px=xq.get("price")
        px_text=f"${px:,.4f}" if px is not None else "Unavailable"
        st.markdown(f"<div class='invest-box'><div class='metric-label'>{token} · Solana</div><div class='metric-value'>{px_text}</div><div class='small-source'>{xq.get('status','')}</div></div>",unsafe_allow_html=True)
    with b:
        if st.button("Invest",use_container_width=True): st.session_state.show_invest=True
    if st.session_state.get("show_invest",False):
        st.markdown("### Investment order")
        st.caption("The token price below is fetched from the public xStocks API. The prototype prepares an order but does not sign or submit a securities transaction.")
        qty=st.number_input("Token quantity",min_value=0.0001,value=1.0,step=0.1)
        wallet=st.text_input("Solana wallet (optional)",placeholder="Your wallet public address")
        if st.button("Prepare investment"):
            try:
                order=prepare_investment(token,qty,wallet)
                st.success(f"Order prepared: {order['quantity']} {order['token']} · estimated notional ${order['estimated_notional']:,.2f}")
                st.json(order)
            except Exception as exc: st.error(str(exc))
        st.caption("Actual purchase/signing requires an eligible user, a compliant execution provider, wallet signing and applicable KYC/AML checks; those are intentionally not executed by this school/demo build.")

st.markdown("<div class='section-title'>Automotive Intelligence</div>",unsafe_allow_html=True)
st.caption(f"Latest available operating data · {ai.get('period','Latest available')}")
fields=[("Vehicle sales","vehicle_sales"),("Deliveries","deliveries"),("Registrations","registrations"),("Market share","market_share"),("EV penetration","ev_penetration"),("Dealer inventory","dealer_inventory"),("Incentives","incentives"),("Recalls","recalls"),("Battery prices","battery_prices"),("Production guidance","production_guidance"),("Margins","margins"),("CAPEX","capex"),("Cash burn","cash_burn")]
cols=st.columns(4)
for i,(label,key) in enumerate(fields):
    val=ai.get(key,"Unavailable")
    if isinstance(val,float): val=f"${val/1e9:.2f}B" if abs(val)>=1e9 else f"${val/1e6:.1f}M"
    if isinstance(val,int): val=f"{val:,}"
    with cols[i%4]: st.markdown(f"<div class='card' style='margin-bottom:12px'><div class='metric-label'>{label}</div><div style='margin-top:6px;font-weight:600'>{val}</div></div>",unsafe_allow_html=True)
st.caption(f"Primary operating source: {ai.get('source','Company investor relations')} · Battery source: {ai.get('battery_source','Our World in Data')}")

st.markdown("<div class='section-title'>Financial Intelligence</div>",unsafe_allow_html=True)
cols=st.columns(4)
for col,label,key in zip(cols,["Revenue","Net income","Operating cash flow","Free cash flow"],["revenue","net_income","operating_cash_flow","free_cash_flow"]):
    value=fund.get(key)
    if isinstance(value,(int,float)): value=f"${value/1e9:.2f}B" if abs(value)>=1e9 else f"${value/1e6:.1f}M"
    with col: st.markdown(f"<div class='card'><div class='metric-label'>{label}</div><div class='metric-value'>{value if value is not None else 'Unavailable'}</div></div>",unsafe_allow_html=True)
st.caption(f"Financial source: {fund.get('source','Public financial filings')}")

st.markdown("<div class='section-title'>Company Profile</div>",unsafe_allow_html=True)
a,b=st.columns([2,1])
with a: st.markdown(f"<div class='card'><h3>{company['name']}</h3><p class='muted'>{company.get('description','')}</p></div>",unsafe_allow_html=True)
with b: st.markdown(f"<div class='card'><div class='metric-label'>Official source</div><a href='{company.get('official_url','#')}' target='_blank'>Investor relations</a></div>",unsafe_allow_html=True)

st.markdown("<div class='section-title'>Vestra Shield</div>",unsafe_allow_html=True)
a,b=st.columns([1,2])
with a:
    investment=st.number_input("Investment (USD)",100.0,1000000.0,1000.0,100.0)
    ref=st.number_input("Reference price",0.01,100000.0,float(snap.get("price") or 100),1.0)
with b:
    result=simulate_shield(investment,float(snap.get("price") or ref),ref,shield)
    st.markdown(f"<div class='card'><div class='metric-label'>Protected value — simulation</div><div class='metric-value'>${result.get('protected_value',0):,.2f}</div><p class='muted'>Shield {shield}%. Scenario calculation only; not an insurance or compensation contract.</p></div>",unsafe_allow_html=True)
