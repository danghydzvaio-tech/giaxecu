"""AutoValue India: premium Streamlit UI; prediction service remains unchanged."""
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import base64
import html

import pandas as pd
import streamlit as st

from service import load_assets, predict_vehicle
from photo_catalog import load_catalog, reference_car, photo_for_car

ROOT = Path(__file__).resolve().parent
PALETTE = {'brown': '#5B4632', 'deep': '#3A2C1F', 'cream': '#F4D9A0', 'orange': '#C8792C'}
st.set_page_config(page_title='AutoValue India · Định giá xe cũ', page_icon='🚘', layout='wide')


def load_css():
    st.markdown('''<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700;800&display=swap');
    /* 01. Palette, page and typography */
    :root{--brown:#5B4632;--deep:#3A2C1F;--cream:#F4D9A0;--orange:#C8792C;--button-ink:#281E15;--card:#473525;--field:var(--deep);--bg:var(--brown);--ink:var(--cream);--muted:var(--cream);--accent:var(--orange);--line:rgba(244,217,160,.42);--control-line:rgba(244,217,160,.65);--glow:rgba(200,121,44,.22);--shadow:rgba(40,30,21,.32);--gradient:linear-gradient(110deg,var(--cream),var(--orange));--title-font:'Cormorant Garamond',Georgia,'Times New Roman',serif;--page-glow:radial-gradient(ellipse at 92% 8%,rgba(200,121,44,.22),transparent 55%);--page-gradient:linear-gradient(135deg,var(--brown),var(--deep) 82%)}
    html,body{background:var(--deep);color:var(--ink);color-scheme:dark}
    .stApp{background:var(--page-glow),var(--page-gradient);color:var(--ink);font-family:Inter,sans-serif}
    #MainMenu,footer,[data-testid="stHeader"]{display:none}
    .block-container{max-width:1240px;padding:2rem 2rem 1rem}
    h1,h2,h3{font-family:Sora,Inter,sans-serif;letter-spacing:-.02em;color:var(--ink)}
    h2{font-size:1.6rem!important}h3{font-size:1.1rem!important}
    p,li,[data-testid="stCaptionContainer"]{line-height:1.7}
    [data-testid="stCaptionContainer"]{color:var(--muted);opacity:1}
    a{color:var(--cream);text-decoration-color:var(--orange)}a:hover{color:var(--orange);background-color:var(--button-ink)}a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible{outline:3px solid var(--cream)!important;outline-offset:4px}
    .brandbar{display:flex;align-items:center;justify-content:space-between;margin:0 0 24px;gap:16px;font-size:11px;letter-spacing:.15em;font-weight:700}
    .brandbar{background:var(--brown);color:var(--cream)}.brandbar span{color:var(--muted);letter-spacing:.1em;font-weight:500}.brand-dot{color:var(--cream)}
    /* 02. Hero: CSS-only motion, no JavaScript or animation CDN */
    .hero{display:grid;grid-template-columns:1.05fr 1fr;gap:32px;align-items:center;position:relative;overflow:hidden;isolation:isolate;border:1px solid var(--line);border-radius:28px;padding:44px;background:radial-gradient(ellipse at 100% 0%,rgba(200,121,44,.1),transparent 65%),var(--deep);animation:appear .6s ease both}
    .hero:before{content:'';position:absolute;z-index:-1;left:30%;top:-100px;width:350px;height:350px;border-radius:50%;background:radial-gradient(circle,rgba(244,217,160,.06),transparent 70%);animation:drift 25s ease-in-out infinite alternate;pointer-events:none}
    .eyebrow{font-size:10px;letter-spacing:.17em;color:var(--cream);font-weight:700;margin:0 0 18px}
    .hero h1{font-family:var(--title-font);font-size:clamp(32px,3.7vw,52px);font-weight:700;line-height:1.2;margin:0 0 20px;padding:0;text-shadow:0 2px 18px rgba(244,217,160,.1)}
    .hero h1,.gradient{background:var(--gradient);background-clip:text;-webkit-background-clip:text;color:transparent}
    .hero p{font-size:14px;color:var(--muted);margin:0 0 22px;max-width:470px}
    .badges{display:flex;flex-wrap:wrap;gap:8px}.badge{font-size:10px;color:var(--cream);background:transparent;border:1px solid var(--line);border-radius:100px;padding:7px 10px}
    .hero-image{margin:0;animation:float 7s ease-in-out infinite}.hero-image img{display:block;width:100%;height:clamp(240px,26vw,360px);object-fit:cover;object-position:53% center;border-radius:20px;border:1px solid var(--line);box-shadow:0 24px 60px var(--shadow)}.hero-image figcaption{font-size:9px;color:var(--muted);margin:10px 0 0;text-align:right}.hero-image a{color:var(--cream)}.hero-image a:hover{color:var(--orange)}
    .scope{font-size:12px;color:var(--muted);margin:18px 2px 24px}
    /* 03. Tabs and cards */
    [data-baseweb="tab-list"]{gap:24px;border-bottom:1px solid var(--line);margin-bottom:20px;overflow-x:auto}
    button[data-baseweb="tab"]{font-family:Inter,sans-serif;white-space:nowrap;height:52px;color:var(--muted);padding:0 4px}
    [role="tab"][aria-selected="true"]{color:var(--cream)!important}
    [data-baseweb="tab-highlight"]{height:3px;background:var(--gradient);border-radius:8px}
    .st-key-input-card,.st-key-result-card,.st-key-reference-card,.st-key-about-card{padding:28px;border:1px solid var(--line);background:linear-gradient(150deg,var(--card),var(--deep));border-radius:20px;box-shadow:0 16px 50px var(--shadow);animation:appear .45s ease both}
    .st-key-result-card{margin-top:24px;border-color:var(--orange);animation-delay:.1s}
    .section-kicker{font-size:10px;letter-spacing:.15em;font-weight:700;color:var(--cream);margin:0 0 8px}
    .card-intro{color:var(--muted);font-size:13px;margin:0 0 20px}
    .mini-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:16px 0 24px}
    .mini-card{padding:20px;background:var(--deep);border:1px solid var(--line);border-radius:16px;transition:transform .2s,box-shadow .2s,border-color .2s}
    .mini-card:hover{transform:translateY(-6px);border-color:var(--orange);box-shadow:0 16px 36px var(--shadow)}
    .mini-card small{display:block;color:var(--muted);font-size:11px;margin-bottom:10px}.mini-card strong{font-family:Sora,sans-serif;font-size:clamp(17px,2vw,24px);color:var(--ink)}
    /* 04. Accessible native input controls */
    [data-testid="stForm"]{border:0;padding:0}
    [data-testid="stWidgetLabel"] p{font-size:12px;color:var(--cream);font-weight:500}
    [data-testid="stNumberInputContainer"],[data-baseweb="select"]>div,[data-testid="stSelectbox"] [role="group"]{border-radius:12px!important;background:var(--field)!important;border-color:var(--control-line)!important;transition:border-color .2s,box-shadow .2s}
    [data-testid="stNumberInputContainer"]:focus-within,[data-baseweb="select"]:focus-within>div,[data-testid="stSelectbox"] [role="group"]:focus-within{border-color:var(--cream)!important;box-shadow:0 0 0 3px var(--glow)}
    [data-testid="stNumberInputContainer"]{min-height:48px}
    [data-testid="stSelectbox"] input[role="combobox"]{min-height:46px}
    [data-testid="stExpander"]{border-radius:14px;border-color:var(--line);background:var(--deep)}
    [data-testid="stFormSubmitButton"] button{min-height:54px;width:100%;border:1px solid var(--cream);border-radius:999px;background:transparent;color:var(--cream);font-weight:700;transition:transform .2s,box-shadow .2s,background-color .2s,color .2s}
    [data-testid="stFormSubmitButton"] button:hover{transform:translateY(-2px);box-shadow:0 8px 30px var(--glow);background:var(--orange);color:var(--button-ink);border-color:var(--cream)}
    [data-testid="stFormSubmitButton"] button:active{transform:scale(.98)}
    [data-testid="stDownloadButton"] button,[data-testid="stButton"] button{border-radius:999px;min-height:44px;border:1px solid var(--cream);background:transparent;color:var(--cream)}
    [data-testid="stDownloadButton"] button:hover,[data-testid="stButton"] button:hover{background:var(--orange);color:var(--button-ink);border-color:var(--cream)}
    [data-testid="stAlert"]{border-radius:14px;border:1px solid var(--line);background:var(--deep);color:var(--cream)}
    /* 05. Result and historical reference range */
    .estimate{padding:26px;border:1px solid var(--line);background:radial-gradient(ellipse at 100% 0%,var(--glow),transparent 65%),var(--deep);border-radius:18px;margin:12px 0 18px}
    .estimate .label{color:var(--cream);font-size:12px}.price{font-family:Sora,sans-serif;font-size:clamp(48px,6vw,80px);line-height:1.2;font-weight:700;letter-spacing:-.04em;color:var(--cream);overflow-wrap:anywhere;margin:14px 0}.estimate .unit{font-size:12px;color:var(--muted)}
    [data-testid="stMetric"]{background:var(--deep);padding:18px;border:1px solid var(--line);border-radius:14px}[data-testid="stMetricValue"]{font-family:Sora,sans-serif;font-size:24px;color:var(--cream)}
    .range-track{height:10px;background:var(--gradient);border-radius:10px;margin:18px 0 10px}.range-ends{display:flex;justify-content:space-between;gap:20px;font-size:12px;color:var(--cream)}
    .page-footer{border-top:1px solid var(--line);margin:40px 0 0;padding:24px 0;background:var(--brown);color:var(--muted);font-size:11px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
    /* Vehicle gallery: keep the verified photos and their historical records. */
    .sample-gallery{margin:28px 0 32px}.sample-gallery h2{margin:0 0 8px}.sample-intro{font-size:13px;color:var(--muted);max-width:760px;margin:0 0 20px}
    .sample-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
    .sample-car{overflow:hidden;border:1px solid var(--line);border-radius:20px;background:var(--card);transition:transform .2s,border-color .2s,box-shadow .2s}
    .sample-car:hover{transform:translateY(-6px);border-color:var(--orange);box-shadow:0 16px 36px var(--shadow)}
    .sample-car>img{display:block;width:100%;height:190px;object-fit:cover;background:var(--deep)}
    .sample-body{padding:20px}.sample-car h3{font-size:16px!important;line-height:1.5;margin:0 0 8px;padding:0}.sample-meta{font-size:12px;color:var(--muted);margin:0 0 12px}
    .sample-price{font-family:Sora,sans-serif;font-size:25px;font-weight:600;color:var(--cream)}.sample-price-label{font-size:10px;color:var(--muted);margin-top:4px}
    .sample-car details{margin-top:16px;font-size:11px;color:var(--muted);line-height:1.7}.sample-car summary{cursor:pointer;color:var(--cream)}.sample-car details p{margin:8px 0 0}.sample-car details a{color:var(--cream)}.sample-car details a:hover{color:var(--orange)}
    /* Theme native Streamlit controls and their portalled dropdowns as well. */
    [data-testid="stAppViewContainer"],[data-testid="stMain"]{background:transparent}
    .stApp :is(p,li,h2,h3,label,summary),[data-testid="stCaptionContainer"],[data-testid="stMetricLabel"]{color:var(--cream)}
    .brandbar,.eyebrow,.section-kicker,.hero p,.scope,.sample-intro,.card-intro,.sample-meta,.sample-price-label,.page-footer{ text-transform:uppercase;letter-spacing:.08em }
    [role="tab"] p{font-size:12px;letter-spacing:.08em;text-transform:uppercase}
    [role="tab"]:hover{color:var(--cream);background:var(--deep)}
    [role="tab"] .react-aria-SelectionIndicator{background:var(--gradient)}
    [data-testid="stNumberInputContainer"] input,[data-testid="stSelectbox"] input,[data-baseweb="select"] input{background:transparent!important;color:var(--cream)!important;caret-color:var(--cream);-webkit-text-fill-color:var(--cream)}
    [data-testid="stNumberInputContainer"] button,[data-testid="stSelectbox"] button{color:var(--cream);background:transparent}
    [data-testid="stNumberInputContainer"] button:hover,[data-testid="stSelectbox"] button:hover{color:var(--button-ink);background:var(--orange)}
    [role="listbox"],[data-baseweb="popover"]>div{background:var(--deep)!important;color:var(--cream)!important;border-color:var(--line)!important}
    [role="option"]{background:var(--deep)!important;color:var(--cream)!important}
    [role="option"]:hover,[role="option"][aria-selected="true"],[role="option"][data-focused="true"]{background:var(--orange)!important;color:var(--button-ink)!important}
    [data-testid="stFormSubmitButton"] button p,[data-testid="stDownloadButton"] button p,[data-testid="stButton"] button p{color:inherit}
    [data-testid="stTooltipIcon"]{color:var(--cream)}[data-testid="stTooltipIcon"]:hover{color:var(--orange)}
    [role="tooltip"],[data-testid="stTooltipContent"]{background:var(--button-ink)!important;color:var(--cream)!important}
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"],[data-testid="stAlert"] svg{color:var(--cream)}
    .hero-image a:hover,.sample-car details a:hover,.page-footer a:hover{background:var(--button-ink)}
    ::selection{background:var(--orange);color:var(--button-ink)}
    @media(forced-colors:active){.hero h1,.gradient{background:none;color:CanvasText;text-shadow:none}}
    @media(max-width:1000px){.sample-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
    @media(max-width:600px){.sample-grid{grid-template-columns:1fr}.sample-car>img{height:210px}}
    /* 06. Motion and small screens */
    @keyframes appear{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
    @keyframes float{50%{transform:translateY(-6px)}}@keyframes drift{to{transform:translate(70px,90px)}}
    @media(max-width:760px){.block-container{padding:1.2rem 1rem}.hero{grid-template-columns:1fr;padding:24px;gap:24px}.hero h1{font-size:36px}.hero-image img{height:200px;aspect-ratio:16/9}.brandbar{font-size:10px}.brandbar span{font-size:9px}.st-key-input-card,.st-key-result-card,.st-key-reference-card,.st-key-about-card{padding:20px}.mini-grid{grid-template-columns:1fr}.mini-card{padding:16px}.mini-card strong{font-size:22px}[data-baseweb="tab-list"]{gap:14px}.price{font-size:clamp(38px,10vw,60px)}.estimate{padding:18px}}
    @media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
    </style>''', unsafe_allow_html=True)


def money(value):
    return f'₹{value:,.0f}'


def clear_result():
    st.session_state.pop('valuation_result', None)


@st.cache_resource
def assets():
    return load_assets(ROOT)


@st.cache_data(show_spinner=False)
def hero_photo():
    path = ROOT / 'static/cars/—Pngtree—black bmw car in close-up_15181512.png'
    if not path.is_file():
        return ''
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode('ascii')


@st.cache_data(show_spinner=False, max_entries=16)
def sample_photo(filename):
    if Path(filename).name != filename:
        raise ValueError('Tên tệp ảnh không hợp lệ.')
    return 'data:image/webp;base64,' + base64.b64encode((ROOT / 'static/cars' / filename).read_bytes()).decode('ascii')


def show_sample_gallery(reference):
    cards = []
    for photo in load_catalog()['photos']:
        car = reference_car(reference, photo)
        name = html.escape(str(car['name']).title())
        alt = html.escape(photo['photo_name'], quote=True)
        author = html.escape(photo['author'])
        source = html.escape(photo['source_page'], quote=True)
        license_url = html.escape(photo['license_url'], quote=True)
        license_name = html.escape(photo['license'])
        cards.append(
            f'<article class="sample-car"><img src="{sample_photo(photo["filename"])}" alt="{alt}" loading="lazy" width="{photo["width"]}" height="{photo["height"]}">'
            f'<div class="sample-body"><h3>{name}</h3><p class="sample-meta">{int(car["year"])} · {int(car["km_driven"]):,} km</p>'
            f'<div class="sample-price">{money(car["selling_price"])}</div><div class="sample-price-label">GIÁ NGUỒN LỊCH SỬ · INR</div>'
            f'<details><summary>Thông tin ảnh &amp; nguồn</summary><p>{alt} · Ảnh: {author} · '
            f'<a href="{source}" target="_blank" rel="noopener noreferrer">Nguồn ảnh</a> · '
            f'<a href="{license_url}" target="_blank" rel="noopener noreferrer">{license_name}</a></p>'
            '<p>Ảnh tham khảo cùng dòng/thế hệ, không xác nhận chính chiếc xe hoặc mọi phiên bản động cơ. Ảnh được giảm kích thước và chuyển WebP, giữ giấy phép gốc.</p></details></div></article>'
        )
    st.markdown('<section class="sample-gallery" aria-label="Xe mẫu trong dữ liệu"><p class="eyebrow">KHÁM PHÁ BỘ SƯU TẬP</p>'
                '<h2>Những chiếc xe trong dữ liệu</h2><p class="sample-intro">Ảnh thật cùng dòng/thế hệ xe. Giá lấy từ bản ghi lịch sử tương ứng trong tập huấn luyện, không phải giá rao bán hiện tại hoặc kết quả dự đoán.</p>'
                '<div class="sample-grid">' + ''.join(cards) + '</div></section>', unsafe_allow_html=True)


load_css()
st.markdown('<div class="brandbar"><div><b class="brand-dot">◈</b> AUTOVALUE INDIA</div><span>ẤN ĐỘ · INR (₹)</span></div>', unsafe_allow_html=True)
image = hero_photo()
art = ('<figure class="hero-image"><img src="' + image + '" alt="Cận cảnh xe BMW màu đen" width="2912" height="1632">'
       '<figcaption>Ảnh minh họa · <a href="https://vi.pngtree.com/freebackground/black-bmw-car-in-close-up-photo-photo_15181512.html" target="_blank" rel="noopener noreferrer">Pngtree</a></figcaption></figure>') if image else ''
st.markdown('<section class="hero"><div><div class="eyebrow">DỮ LIỆU LỊCH SỬ. GÓC NHÌN RÕ RÀNG HƠN.</div>'
            '<h1>Khám phá giá trị<br><span class="gradient">chiếc xe của bạn.</span></h1>'
            '<p>Chọn phiên bản, kiểm tra thông số và nhận giá tham khảo bằng mô hình AI đã được huấn luyện sẵn.</p>'
            '<div class="badges"><span class="badge">✦ Mô hình ANN</span><span class="badge">◉ Dữ liệu CarDekho</span><span class="badge">↗ Kết quả bằng INR</span></div></div>' + art + '</section>', unsafe_allow_html=True)
st.markdown('<p class="scope">Giá lịch sử tại Ấn Độ · 1 lakh = ₹100.000 · Không phải giá thị trường Việt Nam hoặc giá giao dịch hiện tại.</p>', unsafe_allow_html=True)
try:
    bundle, reference = assets()
except (OSError, ValueError, KeyError):
    st.error('Không thể nạp mô hình. Hãy kiểm tra đầy đủ thư mục artifacts/ theo README của dự án.')
    st.stop()
report = bundle['report']
show_sample_gallery(reference)
BRAND_LABELS = {'bmw': 'BMW', 'mg': 'MG', 'land': 'Land Rover'}
FUEL_LABELS = {'petrol': 'Xăng', 'diesel': 'Dầu diesel', 'cng': 'Khí CNG', 'lpg': 'Khí LPG'}
GEAR_LABELS = {'manual': 'Số sàn', 'automatic': 'Số tự động'}
OWNER_LABELS = {'first owner': 'Chủ thứ nhất', 'second owner': 'Chủ thứ hai', 'third owner': 'Chủ thứ ba', 'fourth & above owner': 'Chủ thứ tư trở lên', 'test drive car': 'Xe chạy thử'}
SELLER_LABELS = {'individual': 'Cá nhân', 'dealer': 'Đại lý', 'trustmark dealer': 'Đại lý Trustmark'}
valuation, market, about = st.tabs(['🚘 Định giá', '📊 Dữ liệu tham chiếu', 'ℹ️ Giới thiệu'])

with valuation:
    with st.container(key='input-card'):
        st.markdown('<p class="section-kicker">01 / THÔNG TIN CHIẾC XE</p>', unsafe_allow_html=True)
        st.subheader('Bắt đầu với chiếc xe của bạn')
        st.markdown('<p class="card-intro">Chọn đúng phiên bản để nhận thông số gợi ý phù hợp.</p>', unsafe_allow_html=True)
        a, b = st.columns(2)
        brands = sorted(reference.brand.unique())
        brand = a.selectbox('🚗 Hãng xe', brands, index=brands.index('maruti') if 'maruti' in brands else 0,
                            format_func=lambda x: BRAND_LABELS.get(x, x.title()), help='Các hãng có trong tập huấn luyện.', on_change=clear_result)
        names = sorted(reference.loc[reference.brand == brand, 'name'].unique())
        name = b.selectbox('🏷️ Dòng xe / phiên bản', names, index=names.index('maruti swift dzire vdi') if 'maruti swift dzire vdi' in names else 0,
                           format_func=str.title, help='Chọn đúng phiên bản động cơ của xe.', on_change=clear_result)
        peers = reference[reference.name == name]
        pairs = sorted(set(zip(peers.fuel, peers.transmission)))
        pair = st.selectbox('⛽ Nhiên liệu và hộp số', pairs,
                            format_func=lambda v: f'{FUEL_LABELS.get(v[0], v[0])} · {GEAR_LABELS.get(v[1], v[1])}',
                            help='Chỉ hiển thị các cấu hình có trong dữ liệu.', on_change=clear_result)
        profile = peers[(peers.fuel == pair[0]) & (peers.transmission == pair[1])]

        def middle(column):
            values = profile[column].dropna()
            return float(values.median()) if len(values) else float(reference[column].median())

        def default_index(options, series):
            return options.index(series.mode().iloc[0])

        with st.form('vehicle'):
            st.markdown('### Tình trạng & lịch sử sử dụng')
            a, b = st.columns(2)
            year = a.number_input('📅 Năm sản xuất', min_value=int(report['cleaning']['year_min']), max_value=int(report['cleaning']['year_max']), value=int(middle('year')), step=1, help='Năm sản xuất trong phạm vi dữ liệu huấn luyện.')
            km = b.number_input('🛣️ Quãng đường đã đi (km)', min_value=0, max_value=3_000_000, value=int(middle('km_driven')), step=1000, help='Tổng số km trên đồng hồ, từ 0 đến 3.000.000 km.')
            owners, sellers = sorted(reference.owner.unique()), sorted(reference.seller_type.unique())
            owner = a.selectbox('🔑 Lịch sử sở hữu', owners, index=default_index(owners, profile.owner), format_func=lambda v: OWNER_LABELS.get(v, v.title()), help='Số đời chủ mà xe đã trải qua.')
            seller = b.selectbox('🤝 Người bán', sellers, index=default_index(sellers, profile.seller_type), format_func=lambda v: SELLER_LABELS.get(v, v.title()), help='Cá nhân hoặc loại đại lý bán xe.')
            with st.expander('⚙️ Thông số kỹ thuật', expanded=True):
                st.caption('Đã điền gợi ý theo phiên bản. Hãy chỉnh lại cho đúng chiếc xe của bạn.')
                a, b, c = st.columns(3)
                engine = a.number_input('Dung tích động cơ (cc)', 400., 10_000., middle('engine_cc'), 1., help='Dung tích xi-lanh, đơn vị cc; xem giấy đăng ký xe.')
                power = b.number_input('Công suất (bhp)', 10., 1000., middle('power_bhp'), .1, help='Công suất động cơ tính bằng bhp, không phải kW.')
                seats = c.number_input('Số ghế', 4, 9, int(middle('seats')), 1, help='Tổng số ghế theo đăng ký, gồm ghế lái.')
            submitted = st.form_submit_button('Dự đoán giá xe ↗', type='primary', width='stretch')
    if submitted:
        row = dict(brand=brand, name=name, fuel=pair[0], transmission=pair[1], year=year, km_driven=km, owner=owner, seller_type=seller, engine_cc=engine, power_bhp=power, seats=seats)
        clear_result()
        try:
            with st.spinner('Đang đối chiếu thông số và ước tính giá xe…'):
                price, notes, matching = predict_vehicle(bundle, reference, row)
            st.session_state.valuation_result = dict(row=row, price=price, notes=notes, matching=matching)
        except ValueError as exc:
            st.error(str(exc))
    result = st.session_state.get('valuation_result')
    if result:
        r, price, matching = result['row'], result['price'], result['matching']
        with st.container(key='result-card'):
            st.markdown('<p class="section-kicker">02 / KẾT QUẢ CỦA BẠN</p>', unsafe_allow_html=True)
            st.subheader('Giá tham khảo của bạn')
            st.write(f"**{r['name'].title()} · {r['year']} · {r['km_driven']:,} km**")
            st.caption('Kết quả cho thông số ở lần bấm Dự đoán gần nhất. Bấm lại sau khi chỉnh thông số.')
            st.markdown(f'<div class="estimate"><div class="label">GIÁ DỰ ĐOÁN · INR</div><div class="price">{money(price)}</div><div class="unit">{price / 100_000:.2f} lakh · Ước tính bằng mô hình ANN</div></div>', unsafe_allow_html=True)
            a, b = st.columns(2)
            a.metric('Giá dự đoán', money(price))
            b.metric('Tương đương', f'{price / 100_000:.2f} lakh')
            for note in result['notes']:
                st.warning(note)
            st.caption(f"Sai số tuyệt đối trung bình trên tập kiểm tra: khoảng {money(report['ann']['mae_inr'])}. Đây không phải biên sai số bảo đảm cho chiếc xe này.")
            with st.expander('Khoảng giá của các mẫu lịch sử cùng cấu hình'):
                low, high = matching.selling_price.min(), matching.selling_price.max()
                st.markdown(f'<div class="range-track" aria-hidden="true"></div><div class="range-ends"><span>Thấp nhất<br><b>{money(low)}</b></span><span>Cao nhất<br><b>{money(high)}</b></span></div>', unsafe_allow_html=True)
                st.caption(f'{len(matching):,} mẫu cùng phiên bản, nhiên liệu và hộp số, có thể khác năm và tình trạng. Đây không phải khoảng dự đoán hoặc mức độ tin cậy.')
            download = pd.DataFrame([{'Xe': r['name'].title(), 'Nam_san_xuat': r['year'], 'Km': r['km_driven'], 'Gia_du_doan_INR': round(price), 'Don_vi': 'INR', 'Ghi_chu': 'Uoc tinh theo du lieu CarDekho lich su'}])
            a, b = st.columns(2)
            a.download_button('↓ Tải kết quả CSV', download.to_csv(index=False).encode('utf-8-sig'), 'ket_qua_gia_xe.csv', 'text/csv', on_click='ignore', width='stretch')
            b.button('↻ Dự đoán lại', on_click=clear_result, width='stretch', help='Ẩn kết quả hiện tại; giữ các thông số để bạn chỉnh và dự đoán tiếp.')
            with st.expander('Đối chiếu với xe trong dữ liệu'):
                photo = photo_for_car(r['name'], r['year'])
                if photo:
                    st.image(str(ROOT / 'static/cars' / photo['filename']), caption=photo['photo_name'] + ' · Ảnh tham khảo cùng dòng/thế hệ, không phải ảnh của chiếc xe trong dữ liệu.')
                    st.markdown(f"Ảnh: {photo['author']} · [Nguồn]({photo['source_page']}) · [{photo['license']}]({photo['license_url']})")
                examples = matching.copy()
                examples['distance'] = abs(examples.year - r['year']) + abs(examples.km_driven - r['km_driven']) / 20_000
                st.dataframe(examples.sort_values('distance').head(5)[['year', 'km_driven', 'selling_price']].rename(columns={'year': 'Năm', 'km_driven': 'Số km', 'selling_price': 'Giá nguồn (₹)'}), hide_index=True, width='stretch')
                st.caption('Bản ghi lịch sử từ tập huấn luyện, không phải tin rao đang bán.')

with market:
    with st.container(key='reference-card'):
        st.markdown('<p class="section-kicker">GÓC NHÌN TỪ DỮ LIỆU LỊCH SỬ</p>', unsafe_allow_html=True)
        st.subheader('Hiểu dữ liệu trước khi đọc mức giá')
        st.caption('Tất cả biểu đồ dùng tập huấn luyện CarDekho tại Ấn Độ. Không phải thống kê thị trường hiện tại.')
        cards = [('Mẫu ô tô sau xử lý', f"{report['cleaning']['usable_rows']:,}"), ('Mẫu kiểm tra độc lập', f"{report['split']['test_rows']:,}"), ('Sai số trung bình · tập kiểm tra', money(report['ann']['mae_inr']))]
        st.markdown('<div class="mini-grid">' + ''.join(f'<div class="mini-card"><small>{label}</small><strong>{value}</strong></div>' for label, value in cards) + '</div>', unsafe_allow_html=True)
        st.markdown('### Giá trung vị theo năm sản xuất')
        st.caption(f'{name.title()} · {FUEL_LABELS.get(pair[0], pair[0])} · {GEAR_LABELS.get(pair[1], pair[1])}. Mỗi điểm là trung vị các mẫu lịch sử, không phải dự báo khấu hao của một chiếc xe.')
        trend = profile.groupby('year', as_index=False).agg(price=('selling_price', 'median'), samples=('selling_price', 'size'))
        if len(trend) >= 2:
            st.line_chart(trend.rename(columns={'year': 'Năm sản xuất', 'price': 'Giá trung vị (INR)'}), x='Năm sản xuất', y='Giá trung vị (INR)', color=PALETTE['orange'], height=280)
        else:
            st.info('Cấu hình này chưa có đủ năm sản xuất để vẽ đường giá. Xem các mẫu trong bảng bên dưới.')
        st.dataframe(trend.rename(columns={'year': 'Năm sản xuất', 'price': 'Giá trung vị (INR)', 'samples': 'Số mẫu'}), hide_index=True, width='stretch')
        st.markdown('### Số mẫu tham chiếu theo nhiên liệu')
        fuels = reference.fuel.map(lambda x: FUEL_LABELS.get(x, x)).value_counts().rename_axis('Nhiên liệu').reset_index(name='Số mẫu')
        st.bar_chart(fuels, x='Nhiên liệu', y='Số mẫu', horizontal=True, color=PALETTE['cream'], height=240)
        st.caption('Biểu đồ mô tả dữ liệu. Không thể suy ra mức ảnh hưởng riêng của nhiên liệu lên giá từ số mẫu này.')

with about:
    with st.container(key='about-card'):
        st.markdown('<p class="section-kicker">MINH BẠCH VỀ PHẠM VI SỬ DỤNG</p>', unsafe_allow_html=True)
        st.subheader('AI hỗ trợ tham khảo. Bạn quyết định.')
        st.write('Mô hình ANN được huấn luyện sẵn từ Car details v3.csv trên Kaggle. Website không yêu cầu tải dữ liệu hoặc huấn luyện lại. Thông số gợi ý là trung vị các mẫu cùng cấu hình; khi thiếu thì dùng trung vị tập huấn luyện.')
        st.write(f"Chỉ hỗ trợ các phiên bản có trong dữ liệu, năm sản xuất {report['cleaning']['year_min']}–{report['cleaning']['year_max']}. Giá bằng rupee Ấn Độ (INR); 1 lakh = ₹100.000.")
        st.warning('Giá chưa tính tình trạng thực tế, tai nạn/ngập nước hoặc biến động thị trường. Không dùng kết quả này như báo giá giao dịch hoặc định giá xe tại Việt Nam.')
        st.write('Mô hình hiện chưa có khoảng dự đoán được hiệu chỉnh, điểm tin cậy cho từng xe hoặc phân tích mức ảnh hưởng riêng của từng yếu tố. Vì vậy ứng dụng không hiển thị các chỉ số này.')
        st.markdown('[Nguồn: Nehal Birla · CarDekho trên Kaggle](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho) · [Giấy phép dữ liệu ODbL](https://opendatacommons.org/licenses/odbl/1.0/)')

current_year = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).year
st.markdown(f'<div class="page-footer"><span>© {current_year} Đặng Huy · AutoValue India</span><span><a href="https://github.com/danghydzvaio-tech/giaxecu" target="_blank" rel="noopener noreferrer">GitHub ↗</a> · Giá trị tham khảo từ dữ liệu lịch sử</span></div>', unsafe_allow_html=True)
