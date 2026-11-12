"""Standalone UI demo. All prices are simulated; this file does not load an ANN."""
import base64
import csv
import html
import io
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st

BUILD = "PREMIUM-DEMO-2.0"
YEAR = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).year
st.set_page_config(page_title="AutoValue • Premium Demo", page_icon="🚘", layout="wide")

# 1. CSS — embedded here, not loaded from an external stylesheet.
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
:root{--bg:#17120F;--brown:#5B4632;--deep:#3A2C1F;--cream:#F4D9A0;--orange:#C8792C;--ink:#241A12;--line:rgba(244,217,160,.25);--glass:rgba(58,44,31,.55);--radius:24px;--shadow:0 24px 70px rgba(0,0,0,.25);--ease:cubic-bezier(.22,1,.36,1)}
html,body{background:var(--bg)!important;color:var(--cream)!important;color-scheme:dark}
.stApp{background:radial-gradient(ellipse at 90% 0%,rgba(200,121,44,.19),transparent 50%),linear-gradient(145deg,#17120F,#2C2118)!important;color:var(--cream)!important;font-family:Inter,system-ui,sans-serif!important}
[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:transparent!important}
#MainMenu,footer,[data-testid="stHeader"],[data-testid="stToolbar"]{display:none!important}
.stApp .block-container{max-width:1200px!important;padding:28px 32px 80px!important}
.stApp h1,.stApp h2,.stApp h3{font-family:Outfit,Inter,sans-serif!important;color:var(--cream)!important}
.stApp p,.stApp li{line-height:1.7!important}
.stApp [data-testid="stCaptionContainer"]{color:var(--cream)!important;opacity:1!important}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:24px;color:var(--cream)}
.wordmark{font-family:Outfit,sans-serif;font-size:18px;font-weight:700;letter-spacing:.12em}
.wordmark b{color:var(--orange)}.build{font-size:10px;letter-spacing:.1em;border:1px solid var(--line);padding:8px 12px;border-radius:99px;white-space:nowrap}
.hero{position:relative;overflow:hidden;display:grid;grid-template-columns:1.25fr .75fr;align-items:center;gap:32px;padding:36px 40px;margin-bottom:24px;border:1px solid var(--line);border-radius:var(--radius);background:linear-gradient(120deg,rgba(91,70,50,.45),rgba(58,44,31,.25));box-shadow:var(--shadow)}
.eyebrow{font-size:10px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;margin-bottom:14px;color:var(--cream)}
.hero h1{font-size:clamp(36px,4.4vw,60px)!important;line-height:1.06!important;letter-spacing:-.04em!important;margin:0 0 18px!important;padding:0!important}
.hero h1 span{background:linear-gradient(110deg,#FFF2D1,var(--cream),#D98C3D);-webkit-background-clip:text;background-clip:text;color:transparent!important}
.hero p{max-width:520px;font-size:14px;margin:0;color:var(--cream)}
.hero-art img{display:block;width:100%;height:auto;filter:drop-shadow(0 18px 28px rgba(200,121,44,.15));animation:float-car 7s ease-in-out infinite}
.hero-note{font-size:10px;text-align:center;letter-spacing:.15em;color:var(--cream);margin-top:12px}
/* GLASS: stable keyed containers, with a non-blur fallback. */
.st-key-vehicle-card,.st-key-empty-result,[class*="st-key-valuation-result-"]{padding:28px!important;border:1px solid var(--line)!important;border-radius:var(--radius)!important;background:var(--glass)!important;box-shadow:var(--shadow)!important;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.st-key-vehicle-card h2,[class*="st-key-valuation-result-"] h2{font-size:24px!important;letter-spacing:-.02em!important}
.step{display:flex;gap:10px;align-items:center;margin:10px 0 14px;font-size:12px;font-weight:600;letter-spacing:.03em}
.step b{display:grid;place-items:center;width:26px;height:26px;border:1px solid var(--line);border-radius:9px;font-size:10px;color:var(--cream)}
[data-testid="stForm"]{border:0!important;padding:0!important;background:transparent!important}
[data-testid="stWidgetLabel"] p{font-size:12px!important;font-weight:500!important;color:var(--cream)!important}
/* INPUT: React Aria in Streamlit 1.67 and the older BaseWeb selectors. */
[data-testid="stNumberInputContainer"],[data-testid="stSelectbox"] [role="group"],[data-baseweb="select"]>div{min-height:48px!important;border:1px solid rgba(244,217,160,.4)!important;border-radius:14px!important;background:rgba(23,18,15,.7)!important;box-shadow:none!important;transition:border-color .2s,box-shadow .2s!important}
[data-testid="stNumberInputContainer"]:focus-within,[data-testid="stSelectbox"] [role="group"]:focus-within,[data-baseweb="select"]:focus-within>div{border-color:var(--cream)!important;box-shadow:0 0 0 3px rgba(200,121,44,.2)!important}
.stApp input{color:var(--cream)!important;-webkit-text-fill-color:var(--cream)!important;caret-color:var(--cream)!important;background:transparent!important;font-family:Inter,sans-serif!important}
[data-testid="stNumberInputContainer"] button,[data-testid="stSelectbox"] button{color:var(--cream)!important;background:transparent!important}
[role="listbox"],[data-baseweb="popover"]>div{background:var(--deep)!important;color:var(--cream)!important}
[role="option"]{background:var(--deep)!important;color:var(--cream)!important}
[role="option"]:hover,[role="option"][aria-selected="true"],[role="option"][data-focused="true"]{background:var(--orange)!important;color:var(--ink)!important}
[data-testid="stExpander"]{border:1px solid var(--line)!important;border-radius:16px!important;background:rgba(23,18,15,.25)!important}
[data-testid="stSlider"]{padding-bottom:8px!important}
/* CTA: gradient, lift, glow and a light sweep on hover. */
[data-testid="stFormSubmitButton"] button{position:relative;overflow:hidden;width:100%!important;min-height:54px!important;margin-top:10px!important;border:1px solid rgba(244,217,160,.5)!important;border-radius:16px!important;background:linear-gradient(110deg,#C8792C,#F4D9A0)!important;color:var(--ink)!important;font-weight:700!important;box-shadow:0 10px 28px rgba(200,121,44,.24)!important;transition:transform .25s var(--ease),box-shadow .25s!important}
[data-testid="stFormSubmitButton"] button:hover{transform:translateY(-3px);box-shadow:0 16px 38px rgba(200,121,44,.4)!important;background:linear-gradient(110deg,#F4D9A0,#D98C3D)!important}
[data-testid="stFormSubmitButton"] button::after{content:'';position:absolute;inset:-100%;background:linear-gradient(100deg,transparent 42%,rgba(255,255,255,.35),transparent 58%);transform:translateX(-80%);transition:transform .65s;pointer-events:none}
[data-testid="stFormSubmitButton"] button:hover::after{transform:translateX(80%)}
[data-testid="stFormSubmitButton"] button p,[data-testid="stDownloadButton"] button p{color:inherit!important;font-weight:600!important}
[data-testid="stDownloadButton"] button{width:100%!important;min-height:44px!important;border:1px solid var(--line)!important;border-radius:14px!important;background:transparent!important;color:var(--cream)!important}
/* RESULT: a new container key restarts this animation only for a new estimate. */
[class*="st-key-valuation-result-"]{border-color:rgba(200,121,44,.65)!important;background:radial-gradient(ellipse at 100% 0%,rgba(200,121,44,.17),transparent 65%),rgba(35,26,18,.88)!important;box-shadow:0 0 0 1px rgba(244,217,160,.08),0 0 45px rgba(200,121,44,.16),var(--shadow)!important;animation:result-in .55s var(--ease) both}
.result-label{font-size:10px;letter-spacing:.14em;color:var(--cream);margin:18px 0 8px}
.price{font-family:Outfit,sans-serif;font-size:clamp(38px,4.8vw,64px);font-weight:700;line-height:1.15;letter-spacing:-.04em;color:#FFF0CD;overflow-wrap:anywhere}
.price-unit{font-size:12px;color:var(--cream);margin:8px 0 22px}.result-car{font-size:13px;margin:0 0 8px;color:var(--cream)}
.compare{padding:18px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:18px 0}
.compare-row{display:flex;justify-content:space-between;gap:12px;font-size:11px;margin-bottom:8px;color:var(--cream)}
.track{height:7px;background:rgba(244,217,160,.1);border-radius:10px;overflow:hidden;margin-bottom:14px}.track i{display:block;height:100%;border-radius:inherit;background:linear-gradient(90deg,var(--orange),var(--cream))}.track.reference i{background:rgba(244,217,160,.45)}
.empty-icon{display:grid;place-items:center;width:64px;height:64px;border:1px solid var(--line);border-radius:20px;margin-bottom:22px;color:var(--cream);font-size:28px;background:rgba(200,121,44,.08)}
.st-key-empty-result h3{font-size:24px!important}.st-key-empty-result p{font-size:13px;color:var(--cream)}
.demo-note{padding:12px 14px;border:1px solid var(--line);border-radius:12px;font-size:11px;line-height:1.7;color:var(--cream);background:rgba(23,18,15,.3);margin:20px 0 0}
.page-footer{display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-top:32px;padding-top:18px;border-top:1px solid var(--line);color:var(--cream);font-size:10px}
button:focus-visible,summary:focus-visible,a:focus-visible,input:focus-visible{outline:2px solid var(--cream)!important;outline-offset:4px!important}
@keyframes float-car{50%{transform:translateY(-8px)}}
@keyframes result-in{from{opacity:0;transform:translateY(16px) scale(.97)}to{opacity:1;transform:none}}
@media(max-width:760px){.stApp .block-container{padding:18px 16px 80px!important}.hero{grid-template-columns:1fr;padding:26px 22px;gap:20px}.hero-art{max-width:300px;margin:auto}.hero h1{font-size:40px!important}.hero p{font-size:13px}.st-key-vehicle-card,.st-key-empty-result,[class*="st-key-valuation-result-"]{padding:22px!important}.wordmark{font-size:14px}.build{font-size:8px;padding:7px 9px}.price{font-size:46px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>
"""

# 2. DEMO LOGIC — real ANN integration needs its complete validated input schema.
CATALOG = {
    "Maruti Suzuki": {"Swift": 750_000, "Baleno": 900_000},
    "Hyundai": {"Grand i10": 800_000, "i20": 1_050_000},
    "Honda": {"Amaze": 950_000, "City": 1_500_000},
}


def simulate_price(car):
    """Illustrative formula, NOT trained AI or actual market pricing."""
    base = CATALOG[car["brand"]][car["model"]]
    age = max(0, YEAR - car["year"])
    condition = {"Tốt": 1.0, "Trung bình": .88, "Cần sửa chữa": .72}[car["condition"]]
    gear = 1.08 if car["gear"] == "Số tự động" else 1.0
    value = base * (.91 ** age) * max(.55, 1 - car["km"] / 600_000)
    value *= condition * gear * (.95 ** (car["owners"] - 1))
    return round(max(base * .12, value) / 1000) * 1000, base


def clear_result():
    st.session_state.pop("demo_result", None)


def money(value):
    return f"₹{value:,.0f}"


def to_csv(record):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(record))
    writer.writeheader()
    writer.writerow(record)
    return stream.getvalue().encode("utf-8-sig")


# 3. LAYOUT — self-contained SVG, so no external image URL can break.
st.markdown(CSS, unsafe_allow_html=True)
st.markdown(f'<div class="topbar"><div class="wordmark">AUTO<b>VALUE</b></div><span class="build">{BUILD}</span></div>', unsafe_allow_html=True)
car_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 230" fill="none"><defs><linearGradient id="g" x2="1" y2="1"><stop stop-color="#F4D9A0"/><stop offset="1" stop-color="#C8792C"/></linearGradient></defs><ellipse cx="260" cy="195" rx="220" ry="16" fill="#C8792C" opacity=".12"/><path d="m58 132 53-18 66-65h141l80 66 58 20 13 38H44z" fill="#3A2C1F" stroke="url(#g)" stroke-width="3"/><path d="m140 112 48-48h117l59 48z" fill="#17120F" stroke="#F4D9A0" stroke-opacity=".5"/><path d="M250 65v47M58 143h45m298 0h49M160 149h179" stroke="#F4D9A0" stroke-width="3" stroke-linecap="round"/><circle cx="131" cy="171" r="33" fill="#17120F" stroke="#C8792C" stroke-width="4"/><circle cx="384" cy="171" r="33" fill="#17120F" stroke="#C8792C" stroke-width="4"/><circle cx="131" cy="171" r="14" stroke="#F4D9A0" stroke-width="3"/><circle cx="384" cy="171" r="14" stroke="#F4D9A0" stroke-width="3"/></svg>'
car_image = "data:image/svg+xml;base64," + base64.b64encode(car_svg.encode()).decode()
st.markdown(f'<section class="hero"><div><div class="eyebrow">PREMIUM INTERFACE • BẢN DEMO</div><h1>Định giá xe.<br><span>Trải nghiệm khác biệt.</span></h1><p>Nhập thông tin, khám phá giao diện mới và nhận kết quả mô phỏng ngay trong một màn hình.</p></div><div class="hero-art"><img src="{car_image}" alt="Minh họa ô tô cho bản demo giao diện"><div class="hero-note">BROWN · AMBER · LIQUID GLASS</div></div></section>', unsafe_allow_html=True)

left, right = st.columns([1.15, .85], gap="large")
with left:
    with st.container(key="vehicle-card"):
        st.subheader("Thông tin chiếc xe")
        st.caption("Điền thông tin để thử giao diện. Tất cả mức giá đều là giả lập.")
        st.markdown('<div class="step"><b>01</b> Nhận diện xe</div>', unsafe_allow_html=True)
        a, b = st.columns(2)
        brand = a.selectbox("Hãng xe", list(CATALOG), key="demo_brand", on_change=clear_result, icon=":material/directions_car:")
        model = b.selectbox("Dòng xe", list(CATALOG[brand]), key="demo_model", on_change=clear_result, icon=":material/local_offer:")
        with st.form("demo_vehicle"):
            st.markdown('<div class="step"><b>02</b> Lịch sử sử dụng</div>', unsafe_allow_html=True)
            a, b = st.columns(2)
            year = a.number_input("Năm sản xuất", 1995, YEAR, YEAR - 5, 1, icon=":material/calendar_month:")
            km = b.number_input("Quãng đường (km)", 0, 3_000_000, 65_000, 1000, icon=":material/speed:")
            a, b = st.columns(2)
            condition = a.selectbox("Tình trạng xe", ["Tốt", "Trung bình", "Cần sửa chữa"], icon=":material/verified:")
            gear = b.selectbox("Hộp số", ["Số sàn", "Số tự động"], icon=":material/settings:")
            with st.expander("Tùy chọn bổ sung", expanded=True):
                owners = st.slider("Số đời chủ", 1, 4, 1)
                st.caption("Các thông số chỉ được dùng trong công thức minh họa của bản demo.")
            submitted = st.form_submit_button("ĐỊNH GIÁ NGAY", type="primary", width="stretch")

# 4. CALCULATION + STATE — retain the input snapshot of the last submission.
if submitted:
    clear_result()
    if year is None or km is None:
        st.error("Vui lòng điền năm sản xuất và quãng đường trước khi tính.")
    else:
        car = dict(brand=brand, model=model, year=int(year), km=int(km), condition=condition, gear=gear, owners=owners)
        with st.spinner("Đang tính giá mô phỏng…"):
            price, base = simulate_price(car)
        run = st.session_state.get("demo_run", 0) + 1
        st.session_state.demo_run = run
        st.session_state.demo_result = dict(car=car.copy(), price=price, base=base, run=run)
        st.toast("Đã hoàn thành kết quả mô phỏng.", icon="✅")

# 5. RESULT — no confidence percentage or fictitious market range.
with right:
    result = st.session_state.get("demo_result")
    if not result:
        with st.container(key="empty-result"):
            st.markdown('<div class="empty-icon" aria-hidden="true">↗</div>', unsafe_allow_html=True)
            st.subheader("Giá trị bắt đầu từ thông tin.")
            st.write("Kết quả sẽ xuất hiện ở đây khi bạn bấm ĐỊNH GIÁ NGAY.")
            st.markdown('<div class="demo-note">DEMO GIAO DIỆN<br>Công thức minh họa được chạy ngay trên ứng dụng. Đây chưa phải kết quả của mô hình ANN.</div>', unsafe_allow_html=True)
    else:
        car, price, base = result["car"], result["price"], result["base"]
        with st.container(key=f'valuation-result-{result["run"]}'):
            st.markdown('<div class="eyebrow">KẾT QUẢ MÔ PHỎNG</div>', unsafe_allow_html=True)
            st.subheader("Một góc nhìn mới về chiếc xe.")
            name = html.escape(car["brand"] + " " + car["model"])
            st.markdown(f'<div class="result-label">GIÁ GIẢ LẬP · INR</div><div class="price">{money(price)}</div><div class="price-unit">{price / 100_000:.2f} lakh · 1 lakh = ₹100.000</div><div class="result-car">{name} · {car["year"]} · {car["km"]:,} km</div>', unsafe_allow_html=True)
            st.caption("Thông số của lần tính gần nhất. Bấm lại sau khi sửa thông tin.")
            scale = max(base, price)
            st.markdown(f'<div class="compare"><div class="compare-row"><span>Giá gốc giả định</span><b>{money(base)}</b></div><div class="track reference"><i style="width:{base / scale * 100:.1f}%"></i></div><div class="compare-row"><span>Kết quả công thức demo</span><b>{money(price)}</b></div><div class="track"><i style="width:{price / scale * 100:.1f}%"></i></div></div>', unsafe_allow_html=True)
            record = {**car, "simulated_price_INR": price, "demo_only": True, "build": BUILD}
            st.download_button("Tải kết quả demo CSV", to_csv(record), "autovalue_demo.csv", "text/csv", on_click="ignore", width="stretch")
            st.markdown('<div class="demo-note">CHỈ DÙNG KIỂM TRA GIAO DIỆN<br>Giá được tính bằng công thức giả lập, không phải mô hình ANN, báo giá thị trường hoặc khoảng tin cậy.</div>', unsafe_allow_html=True)

st.markdown(f'<div class="page-footer"><span>Người sáng lập: Trần Đăng Huy</span><span>Giao diện: {BUILD} · Demo độc lập</span></div>', unsafe_allow_html=True)
