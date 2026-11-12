"""AutoValue India: premium Streamlit UI; prediction service remains unchanged."""
from pathlib import Path
import base64
import html
import importlib
import json

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

try:
    from service import load_assets, predict_vehicle, prediction_interval, historical_reference
except ImportError:
    # Community Cloud can retain the previous imported modules during a hot update.
    import car_model
    importlib.reload(car_model)
    import service
    importlib.reload(service)
    from service import load_assets, predict_vehicle, prediction_interval, historical_reference
from photo_catalog import load_catalog, reference_car, photo_for_car
from price_format import format_inr, format_price_units, indian_axis_expr

ROOT = Path(__file__).resolve().parent
PALETTE = {'brown': '#5B4632', 'deep': '#3A2C1F', 'cream': '#F4D9A0', 'orange': '#C8792C'}
st.set_page_config(page_title='AutoValue India · Định giá xe cũ', page_icon='🚘', layout='wide')


def load_css():
    files = ['assets/theme.css', 'ui_effects.css', 'navbar.css']
    css = '\n'.join((ROOT / filename).read_text(encoding='utf-8') for filename in files)
    st.markdown('<style>' + css + '</style>', unsafe_allow_html=True)


def money(value):
    return format_inr(value)


def percent(value):
    return f'{value:.1f}'.replace('.', ',') + '%'


def clear_result():
    st.session_state.pop('valuation_result', None)


@st.cache_resource
def assets(manifest_version):
    # A regenerated manifest also invalidates the cached model after deployment.
    return load_assets(ROOT)


@st.cache_data(show_spinner=False)
def hero_photo():
    photo = next(p for p in load_catalog()['photos'] if p['id'] == load_catalog()['hero'])
    path = ROOT / 'static/cars' / photo['filename']
    return 'data:image/webp;base64,' + base64.b64encode(path.read_bytes()).decode('ascii')


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
st.markdown((ROOT / 'navbar.html').read_text(encoding='utf-8'), unsafe_allow_html=True)
image = hero_photo()
hero = next(p for p in load_catalog()['photos'] if p['id'] == load_catalog()['hero'])
art = ('<figure class="hero-image"><img src="' + image + '" alt="' + html.escape(hero['photo_name'], quote=True) + '" width="' + str(hero['width']) + '" height="' + str(hero['height']) + '">'
       '<figcaption>Ảnh: ' + html.escape(hero['author']) + ' · <a href="' + html.escape(hero['source_page'], quote=True) + '" target="_blank" rel="noopener noreferrer">Nguồn ảnh</a> · <a href="' + html.escape(hero['license_url'], quote=True) + '" target="_blank" rel="noopener noreferrer">' + html.escape(hero['license']) + '</a></figcaption></figure>')
st.markdown('<section class="hero"><div>'
            '<h1>Dự đoán giá xe<br><span class="gradient">bằng thuật toán AI</span></h1>'
            '<p>Chọn phiên bản, kiểm tra thông số và nhận giá tham khảo bằng mô hình AI đã được huấn luyện sẵn.</p>'
            '<div class="badges"><span class="badge">✦ Mô hình AI</span><span class="badge">◉ Dữ liệu CarDekho</span><span class="badge">↗ Kết quả bằng INR</span></div></div>' + art + '</section>', unsafe_allow_html=True)
st.markdown('<p class="scope">Giá tham khảo thị trường xe cũ Ấn Độ (INR), dựa trên dữ liệu lịch sử CarDekho đến năm 2020, không phải giá rao bán hiện tại.</p>', unsafe_allow_html=True)
try:
    manifest_version = (ROOT / 'artifacts/manifest.json').read_text(encoding='utf-8')
    bundle, reference = assets(manifest_version)
except (OSError, ValueError, KeyError):
    st.error('Không thể nạp mô hình. Hãy kiểm tra đầy đủ thư mục artifacts/ theo README của dự án.')
    st.stop()
report = bundle['report']
if st.session_state.get('model_manifest') != manifest_version:
    clear_result()
    st.session_state.model_manifest = manifest_version
model_label = report['selected_model']['label']
BRAND_LABELS = {'bmw': 'BMW', 'mg': 'MG', 'land': 'Land Rover'}
FUEL_LABELS = {'petrol': 'Xăng', 'diesel': 'Dầu diesel', 'cng': 'Khí CNG', 'lpg': 'Khí LPG'}
GEAR_LABELS = {'manual': 'Số sàn', 'automatic': 'Số tự động'}
OWNER_LABELS = {'first owner': 'Chủ thứ nhất', 'second owner': 'Chủ thứ hai', 'third owner': 'Chủ thứ ba', 'fourth & above owner': 'Chủ thứ tư trở lên', 'test drive car': 'Xe chạy thử'}
SELLER_LABELS = {'individual': 'Cá nhân', 'dealer': 'Đại lý', 'trustmark dealer': 'Đại lý Trustmark'}
with st.container(key='valuation-section'):
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
                interval_low, price, interval_high = prediction_interval(bundle, row)
            st.session_state.valuation_result = dict(row=row, price=price, notes=notes, matching=matching,
                                                     interval_low=interval_low, interval_high=interval_high)
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
            st.markdown(f'<div class="estimate"><div class="label">GIÁ DỰ ĐOÁN · INR</div><div class="price">{money(price)}</div><div class="unit">Ước tính bằng {html.escape(model_label)}</div></div>', unsafe_allow_html=True)
            st.markdown(f'**Khoảng {money(result["interval_low"])} – {money(result["interval_high"])} · độ tin cậy mục tiêu 80%**')
            st.caption(f'Split conformal trên dữ liệu lịch sử; độ phủ thực tế trên tập kiểm tra: {percent(report["conformal"]["test_coverage"] * 100)}. Mức phủ này không bảo đảm riêng cho từng chiếc xe.')
            st.metric('Tương đương', format_price_units(price))
            st.caption('1 lakh = ₹1,00,000; 1 crore = 100 lakh')
            for note in result['notes']:
                st.warning(note)
            st.caption(f'Sai số phần trăm tuyệt đối trung bình (MAPE): {percent(report["test"]["mape_percent"])}; trung vị: {percent(report["test"]["median_ape_percent"])} trên tập kiểm tra.')
            with st.expander('Khoảng giá của các mẫu lịch sử cùng cấu hình'):
                nearby, fallback = historical_reference(matching, r['year'])
                low, high = float(nearby.selling_price.min()), float(nearby.selling_price.max())
                domain_low, domain_high = min(low, price), max(high, price)
                span = max(domain_high - domain_low, 1.0)
                start, band, marker = (low - domain_low) / span * 100, (high - low) / span * 100, (price - domain_low) / span * 100
                st.markdown(f'<div class="history-track" role="img" aria-label="Khoảng giá lịch sử {money(low)} đến {money(high)}; vạch giá dự đoán {money(price)}"><i style="left:{start:.3f}%;width:{band:.3f}%"></i><b style="left:{marker:.3f}%"></b></div><div class="range-ends"><span>Thấp nhất lịch sử<br><b>{money(low)}</b></span><span>Giá dự đoán<br><b>{money(price)}</b></span><span>Cao nhất lịch sử<br><b>{money(high)}</b></span></div>', unsafe_allow_html=True)
                st.caption(f'{len(nearby):,} mẫu cùng phiên bản, nhiên liệu và hộp số. ' + ('Có dưới 5 mẫu trong khoảng ±2 năm; đang dùng toàn bộ các năm của cấu hình này.' if fallback else 'Chỉ lấy năm sản xuất trong khoảng ±2 năm so với xe nhập vào.'))
                st.caption('Dải màu là giá lịch sử, vạch sáng là giá dự đoán; đây là phần đối chiếu riêng với khoảng dự đoán conformal phía trên.')
            download = pd.DataFrame([{'Xe': r['name'].title(), 'Nam_san_xuat': r['year'], 'Km': r['km_driven'], 'Gia_du_doan_INR': round(price), 'Khoang_thap_INR': round(result['interval_low']), 'Khoang_cao_INR': round(result['interval_high']), 'Muc_phu_muc_tieu': .8, 'Don_vi': 'INR', 'Ghi_chu': 'Uoc tinh theo du lieu CarDekho lich su'}])
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
                shown = examples.sort_values('distance').head(5)[['year', 'km_driven', 'selling_price']].rename(columns={'year': 'Năm', 'km_driven': 'Số km', 'selling_price': 'Giá nguồn (₹)'})
                st.dataframe(shown.style.format({'Giá nguồn (₹)': money}), hide_index=True, width='stretch')
                st.caption('Bản ghi lịch sử từ tập huấn luyện, không phải tin rao đang bán.')

# A stateful expander skips generating image bytes until the user opens it.
gallery = st.expander('Những chiếc xe trong dữ liệu', expanded=False, key='gallery', on_change='rerun')
if gallery.open:
    with gallery:
        show_sample_gallery(reference)

with st.container(key='reference-section'):
    with st.container(key='reference-card'):
        st.markdown('<p class="section-kicker">GÓC NHÌN TỪ DỮ LIỆU LỊCH SỬ</p>', unsafe_allow_html=True)
        st.subheader('Hiểu dữ liệu trước khi đọc mức giá')
        st.caption('Tất cả biểu đồ dùng tập huấn luyện CarDekho tại Ấn Độ. Không phải thống kê thị trường hiện tại.')
        cards = [('Mẫu ô tô sau xử lý', f"{report['cleaning']['usable_rows']:,}"), ('Mẫu kiểm tra độc lập', f"{report['split']['test_rows']:,}"), ('MAPE · tập kiểm tra', percent(report['test']['mape_percent']))]
        st.markdown('<div class="mini-grid">' + ''.join(f'<div class="mini-card"><small>{label}</small><strong>{value}</strong></div>' for label, value in cards) + '</div>', unsafe_allow_html=True)
        st.markdown('### Giá trung vị theo năm sản xuất')
        st.caption(f'{name.title()} · {FUEL_LABELS.get(pair[0], pair[0])} · {GEAR_LABELS.get(pair[1], pair[1])}. Mỗi điểm là trung vị các mẫu lịch sử, không phải dự báo khấu hao của một chiếc xe.')
        trend = profile.groupby('year', as_index=False).agg(price=('selling_price', 'median'), samples=('selling_price', 'size'))
        if len(trend) >= 2:
            plot = trend.rename(columns={'year': 'Năm sản xuất', 'price': 'Giá trung vị (INR)'})[['Năm sản xuất', 'Giá trung vị (INR)']]
            plot['Giá hiển thị'] = plot['Giá trung vị (INR)'].map(money)
            # Preserve Streamlit's line/hover/zoom behavior; format only the year.
            base = alt.Chart(plot, width=0, height=280).mark_line().encode(
                x=alt.X('Năm sản xuất:Q', title='Năm sản xuất', scale=alt.Scale(),
                        axis=alt.Axis(grid=False, tickMinStep=1, format='d')),
                y=alt.Y('Giá trung vị (INR):Q', title='Giá trung vị (INR)',
                        scale=alt.Scale(), axis=alt.Axis(grid=True, labelExpr=indian_axis_expr())),
                color=alt.value(PALETTE['orange']),
                tooltip=[alt.Tooltip('Năm sản xuất:Q', format='d'),
                         alt.Tooltip('Giá hiển thị:N', title='Giá trung vị (INR)')],
            )
            nearest = alt.selection_point(nearest=True, on='mousemove',
                                          fields=['Năm sản xuất'], empty=False, clear='mouseleave')
            chart = alt.layer(
                base,
                base.mark_point(opacity=0).add_params(nearest),
                base.mark_point(filled=True, size=65).transform_filter(nearest),
            ).configure_legend(symbolType='stroke').properties(width=0, height=280).interactive()
            st.altair_chart(chart, width='stretch', height=280)
        else:
            st.info('Cấu hình này chưa có đủ năm sản xuất để vẽ đường giá. Xem các mẫu trong bảng bên dưới.')
        shown_trend = trend.rename(columns={'year': 'Năm sản xuất', 'price': 'Giá trung vị (INR)', 'samples': 'Số mẫu'})
        st.dataframe(shown_trend.style.format({'Giá trung vị (INR)': money}), hide_index=True, width='stretch')
        st.markdown('### Số mẫu tham chiếu theo nhiên liệu')
        fuels = reference.fuel.map(lambda x: FUEL_LABELS.get(x, x)).value_counts().rename_axis('Nhiên liệu').reset_index(name='Số mẫu')
        st.bar_chart(fuels, x='Nhiên liệu', y='Số mẫu', horizontal=True, color=PALETTE['cream'], height=240)
        st.caption('Biểu đồ mô tả dữ liệu. Không thể suy ra mức ảnh hưởng riêng của nhiên liệu lên giá từ số mẫu này.')

with st.container(key='about-section'):
    with st.container(key='about-card'):
        st.markdown('<p class="section-kicker">MINH BẠCH VỀ PHẠM VI SỬ DỤNG</p>', unsafe_allow_html=True)
        st.subheader('AI hỗ trợ tham khảo. Bạn quyết định.')
        st.write(f'Mô hình {model_label} được chọn bằng GroupKFold 5 lần giữa MLPRegressor, RandomForestRegressor và HistGradientBoostingRegressor trên phần dữ liệu huấn luyện. Tập validation được giữ riêng cho hiệu chỉnh conformal; tập kiểm tra chỉ dùng để báo cáo cuối. Dữ liệu là Car details v3.csv trên Kaggle.')
        st.write('Website dùng mô hình đã huấn luyện sẵn. Thông số gợi ý là trung vị các mẫu cùng cấu hình; khi thiếu thì dùng trung vị tập huấn luyện.')
        st.write(f"Chỉ hỗ trợ các phiên bản có trong dữ liệu, năm sản xuất {report['cleaning']['year_min']}–{report['cleaning']['year_max']}. Giá bằng rupee Ấn Độ (INR); 1 lakh = ₹1,00,000; 1 crore = 100 lakh.")
        st.warning('Giá chưa tính tình trạng thực tế, tai nạn/ngập nước hoặc biến động thị trường. Không dùng kết quả này như báo giá giao dịch hiện tại.')
        st.write(f'Khoảng dự đoán được hiệu chỉnh bằng split conformal trên phần dư log của tập validation, với mục tiêu phủ 80%. Độ phủ đo được trên tập kiểm tra là {percent(report["conformal"]["test_coverage"] * 100)}; mức này áp dụng cho tổng thể dữ liệu tương tự, không phải xác suất bảo đảm cho từng xe hoặc từng hãng.')
        st.markdown('[Nguồn: Nehal Birla · CarDekho trên Kaggle](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho) · [Giấy phép dữ liệu ODbL](https://opendatacommons.org/licenses/odbl/1.0/)')

st.markdown('<div class="page-footer"><span class="founder-credit">Người sáng lập: Trần Đăng Huy</span><span><a href="https://github.com/danghydzvaio-tech/giaxecu" target="_blank" rel="noopener noreferrer">GitHub ↗</a> · Giá trị tham khảo từ dữ liệu lịch sử</span></div>', unsafe_allow_html=True)

# One zero-height bootstrap for our trusted scripts; each controller reuses its
# observers across reruns. st.html sanitizes scripts in the deployed frontend.
effects = json.dumps((ROOT / 'ui_effects.js').read_text(encoding='utf-8') + '\n' + (ROOT / 'navbar.js').read_text(encoding='utf-8')).replace('</', '<\\/')
components.html('<script>const p=window.parent;if(p.__avGlass?.version==="glass-2"&&p.__avNav?.version==="nav-1"){p.__avGlass.refresh();p.__avNav.refresh();}else{const s=p.document.createElement("script");s.textContent=' + effects + ';p.document.body.appendChild(s);s.remove();}</script>', height=0, scrolling=False)
