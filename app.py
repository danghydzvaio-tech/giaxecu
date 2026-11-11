"""Streamlit entrypoint: enter a passenger car and receive an ANN estimate."""
from pathlib import Path
import re
import base64
import json
import html
import streamlit.components.v1 as components

import pandas as pd
import streamlit as st

from service import load_assets, predict_vehicle
from photo_catalog import load_catalog, reference_car, photo_for_car

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='AutoValue India · Giá xe cũ', page_icon='🚗', layout='wide')


@st.cache_data(show_spinner=False, max_entries=16)
def embedded_photo_url(photo):
    # Keep this in the entrypoint: Cloud hot updates can retain older imported modules.
    filename = photo['filename']
    if Path(filename).name != filename:
        raise ValueError('Tên tệp ảnh không hợp lệ.')
    payload = (ROOT / 'static/cars' / filename).read_bytes()
    return 'data:image/webp;base64,' + base64.b64encode(payload).decode('ascii')


def fragment(name):
    document = (ROOT / 'index.html').read_text(encoding='utf-8')
    content = re.search(rf'<!-- av:{name} -->(.*?)<!-- /av:{name} -->', document, re.S).group(1)
    # st.html supports HTML images but strips inline SVG: preserve the artwork as a data image.
    def svg_image(match):
        class_name = re.search(r'class="([^"]+)"', match.group(0)).group(1)
        alt = 'Minh họa ô tô' if class_name == 'av-car' else ''
        return '<img class="' + class_name + '" alt="' + alt + '" decoding="async" src="data:image/svg+xml;base64,' + base64.b64encode(match.group(0).encode()).decode() + '">'
    content = re.sub(r'<svg\b[^>]*>.*?</svg>', svg_image, content, flags=re.S)
    for photo in load_catalog()['photos']:
        content = content.replace('src="static/cars/' + photo['filename'] + '"', 'src="' + embedded_photo_url(photo) + '" data-photo-id="' + photo['id'] + '"')
    return content


st.html('<style>' + (ROOT / 'style.css').read_text(encoding='utf-8') + '</style>')



@st.cache_resource
def assets():
    return load_assets()


try:
    bundle, reference = assets()
except (OSError, ValueError, KeyError) as exc:
    st.error('Không thể nạp mô hình. Hãy kiểm tra thư mục artifacts/ theo README của dự án.')
    with st.expander('Thông tin để sửa lỗi triển khai'):
        st.code(str(exc))
    st.stop()



def collection_html():
    photos = load_catalog()['photos']
    palette = ['#1c2d27', '#352020', '#202632', '#2b252f', '#1d2c2b', '#30281d']
    rows, credits = [], []
    for index, photo in enumerate(photos):
        car = reference_car(reference, photo)
        image = ''  # Populated from the unique embedded registry before motion/CDN loading.
        name = html.escape(str(car['name']).title())
        tag = html.escape(f"{car['brand'].title()} · {int(car['year'])}")
        price = f"₹{car['selling_price']:,.0f}"
        alt = html.escape(photo['photo_name'], quote=True)
        caption = html.escape(photo['photo_name'] + ' · ' + photo['author'] + ' · ' + photo['license'], quote=True)
        rows.append(f'''<button type="button" class="av-collection-row" data-color="{palette[index]}" data-index="{index}" data-image="{image}" data-photo-id="{photo['id']}" data-photo-alt="{alt}" data-photo-caption="{caption}" aria-expanded="false" aria-controls="av-row-extra-{index}">
          <span class="av-row-name">{name}</span><span class="av-row-tag">{tag}</span><span class="av-row-price">{price}</span>
          <span class="av-row-extra" id="av-row-extra-{index}" hidden><img class="av-row-image" data-photo-id="{photo['id']}" loading="lazy" alt="{alt}" width="{photo['width']}" height="{photo['height']}"><span>Giá nguồn lịch sử · {int(car['km_driven']):,} km</span><span class="av-photo-credit">{caption}</span></span></button>''')
        credits.append(f'''<li><a href="{html.escape(photo['source_page'], quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(photo['photo_name'])}</a> · {html.escape(photo['author'])} · <a href="{html.escape(photo['license_url'], quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(photo['license'])}</a></li>''')
    layers = ''.join(f'<div class="av-collection-background" data-layer="{i}" style="background:{c}"></div>' for i, c in enumerate(palette))
    # Hero bytes already exist once in the hero img; embed each remaining photo once.
    hero_id = load_catalog()['hero']
    registry = '<div class="av-photo-assets" data-photo-registry hidden aria-hidden="true">' + ''.join(
        '<span data-photo-key="' + photo['id'] + '" data-photo-src="' + embedded_photo_url(photo) + '"></span>'
        for photo in photos if photo['id'] != hero_id
    ) + '</div>'
    initial_id = photos[0]['id']
    return f'''<section id="collection" class="av-collection" aria-label="Xe trong dữ liệu tham chiếu">{layers}
      <div class="av-collection-copy"><p class="av-eyebrow">AUTOVALUE INDIA</p><h2>Đối chiếu với xe trong dữ liệu</h2><p>Giá nguồn lịch sử, không phải tin rao đang bán. Ảnh thật cùng dòng/thế hệ xe, không xác nhận chính chiếc xe hoặc mọi phiên bản động cơ trong dữ liệu.</p></div>
      <div class="av-collection-list">{''.join(rows)}</div><details class="av-image-credits"><summary>Nguồn và giấy phép ảnh</summary><ul>{''.join(credits)}</ul><p>Ảnh được giảm kích thước và chuyển WebP. Bản WebP giữ giấy phép của ảnh gốc.</p></details></section>
      {registry}<div class="av-preview" aria-hidden="true"><div class="av-preview-image"><img data-photo-id="{initial_id}" alt=""><img data-photo-id="{initial_id}" alt=""></div><span class="av-preview-caption">Ảnh thật cùng dòng xe</span></div>'''


report = bundle['report']
hero = fragment('hero')
for stat, count in [('usable', report['cleaning']['usable_rows']), ('test', report['split']['test_rows'])]:
    hero = re.sub(rf'(data-stat="{stat}" data-count=")\d+(">)[^<]+', lambda m: m.group(1) + str(count) + m.group(2) + f'{count:,}'.replace(',', '.'), hero)
st.html(hero)
with st.container(key='curtain'):
    st.html(collection_html())
    with st.container(key='intro-note'):
        st.caption('Ấn Độ · INR (₹) · 1 lakh = ₹100.000. Dữ liệu lịch sử có xe sản xuất đến 2020; kết quả chưa phải giá thị trường hiện tại.')

    BRAND_LABELS = {'bmw': 'BMW', 'mg': 'MG', 'land': 'Land Rover'}
    FUEL_LABELS = {'petrol': 'Xăng', 'diesel': 'Dầu diesel', 'cng': 'Khí CNG', 'lpg': 'Khí LPG'}
    GEAR_LABELS = {'manual': 'Số sàn', 'automatic': 'Số tự động'}
    OWNER_LABELS = {'first owner': 'Chủ thứ nhất', 'second owner': 'Chủ thứ hai', 'third owner': 'Chủ thứ ba',
                    'fourth & above owner': 'Chủ thứ tư trở lên', 'test drive car': 'Xe chạy thử'}
    SELLER_LABELS = {'individual': 'Cá nhân', 'dealer': 'Đại lý', 'trustmark dealer': 'Đại lý Trustmark'}

    st.html('<div id="prediction" tabindex="-1"></div>')
    with st.container(key='prediction-panel'):
        st.subheader('Thông tin ô tô')
        a, b = st.columns(2)
        brands = sorted(reference.brand.unique())
        brand = a.selectbox('Hãng xe', brands, index=brands.index('maruti') if 'maruti' in brands else 0,
                            format_func=lambda x: BRAND_LABELS.get(x, x.title()))
        names = sorted(reference.loc[reference.brand == brand, 'name'].unique())
        name = b.selectbox('Dòng xe / phiên bản', names,
                           index=names.index('maruti swift dzire vdi') if 'maruti swift dzire vdi' in names else 0,
                           format_func=str.title)
        peers = reference[reference.name == name]
        pairs = sorted(set(zip(peers.fuel, peers.transmission)))
        pair = st.selectbox('Nhiên liệu và hộp số', pairs,
                            format_func=lambda v: f'{FUEL_LABELS.get(v[0], v[0])} · {GEAR_LABELS.get(v[1], v[1])}')
        profile = peers[(peers.fuel == pair[0]) & (peers.transmission == pair[1])]


        def middle(column):
            values = profile[column].dropna()
            return float(values.median()) if len(values) else float(reference[column].median())


        def default_index(options, series):
            most_common = series.mode().iloc[0]
            return options.index(most_common)


        with st.form('vehicle'):
            a, b = st.columns(2)
            year = a.number_input('Năm sản xuất', min_value=int(report['cleaning']['year_min']),
                                  max_value=int(report['cleaning']['year_max']), value=int(middle('year')), step=1)
            km = b.number_input('Quãng đường đã đi (km)', min_value=0, max_value=3_000_000,
                                value=int(middle('km_driven')), step=1000)
            owners = sorted(reference.owner.unique())
            sellers = sorted(reference.seller_type.unique())
            owner = a.selectbox('Lịch sử sở hữu', owners, index=default_index(owners, profile.owner),
                                format_func=lambda v: OWNER_LABELS.get(v, v.title()))
            seller = b.selectbox('Người bán', sellers, index=default_index(sellers, profile.seller_type),
                                 format_func=lambda v: SELLER_LABELS.get(v, v.title()))
            with st.expander('Thông số kỹ thuật', expanded=True):
                st.caption('Đã điền gợi ý theo phiên bản. Hãy chỉnh lại cho đúng chiếc xe của bạn.')
                a, b, c = st.columns(3)
                engine = a.number_input('Dung tích động cơ (cc)', 400., 10_000., middle('engine_cc'), 1.)
                power = b.number_input('Công suất (bhp)', 10., 1000., middle('power_bhp'), .1)
                seats = c.number_input('Số ghế', 4, 9, int(middle('seats')), 1)
            submitted = st.form_submit_button('Dự đoán giá xe', type='primary', width='stretch')

    if submitted:
        row = dict(brand=brand, name=name, fuel=pair[0], transmission=pair[1], year=year,
                   km_driven=km, owner=owner, seller_type=seller, engine_cc=engine,
                   power_bhp=power, seats=seats)
        try:
            price, notes, matching = predict_vehicle(bundle, reference, row)
        except ValueError as exc:
            st.error(str(exc))
        else:
            with st.container(key='result-panel'):
                st.subheader('Giá tham khảo của bạn')
                st.write(f'**{name.title()} · {year} · {km:,} km**')
                a, b = st.columns(2)
                a.metric('Giá dự đoán', f'₹{price:,.0f}')
                b.metric('Tương đương', f'{price / 100_000:.2f} lakh')
                for note in notes:
                    st.warning(note)
                st.caption(f"Sai số tuyệt đối trung bình trên tập kiểm tra: khoảng ₹{report['ann']['mae_inr']:,.0f}. "
                           'Đây không phải biên sai số bảo đảm cho chiếc xe này.')
                download = pd.DataFrame([{'Xe': name.title(), 'Nam_san_xuat': year, 'Km': km,
                                          'Gia_du_doan_INR': round(price), 'Don_vi': 'INR',
                                          'Ghi_chu': 'Uoc tinh theo du lieu CarDekho lich su'}])
                st.download_button('Lưu kết quả (.csv)', download.to_csv(index=False).encode('utf-8-sig'),
                                    'ket_qua_gia_xe.csv', 'text/csv', on_click='ignore')
                with st.expander('Đối chiếu với xe trong dữ liệu'):
                    photo = photo_for_car(name, year)
                    if photo:
                        st.image(str(ROOT / 'static/cars' / photo['filename']), caption=photo['photo_name'] + ' · Ảnh tham khảo cùng dòng/thế hệ, không phải ảnh của chiếc xe trong dữ liệu.')
                        st.markdown(f"Ảnh: {photo['author']} · [Nguồn]({photo['source_page']}) · [{photo['license']}]({photo['license_url']})")
                    examples = matching.copy()
                    examples['distance'] = abs(examples.year - year) + abs(examples.km_driven - km) / 20_000
                    examples = examples.sort_values('distance').head(5)
                    st.dataframe(examples[['year', 'km_driven', 'selling_price']].rename(
                        columns={'year': 'Năm', 'km_driven': 'Số km', 'selling_price': 'Giá nguồn (₹)'}),
                        hide_index=True, width='stretch')
                    st.caption('Bản ghi lịch sử từ tập huấn luyện, không phải tin rao đang bán.')

    st.html('<div id="data" tabindex="-1"></div>')
    with st.container(key='about-panel'):
        with st.expander('Về dữ liệu và phạm vi dự đoán'):
            st.write('ANN đã được huấn luyện sẵn từ Car details v3.csv trên Kaggle, sau lọc còn 6.904 mẫu ô tô. '
                     'Website không yêu cầu bạn tải dữ liệu hoặc huấn luyện lại. Thông số gợi ý dựa trên trung vị các mẫu cùng phiên bản; '
                     'nếu phiên bản thiếu thông số thì dùng trung vị tập huấn luyện.')
            st.write('Giá tham khảo theo dữ liệu lịch sử, chưa tính tình trạng thực tế, tai nạn/ngập nước hoặc biến động thị trường. '
                     'Chỉ hỗ trợ các phiên bản có trong dữ liệu và năm sản xuất 1983–2020.')
            st.markdown('[Nguồn: Nehal Birla · CarDekho trên Kaggle](https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho) '
                        '· [Giấy phép dữ liệu](https://opendatacommons.org/licenses/odbl/1.0/)')

st.html(fragment('footer'))
# Streamlit sanitizes scripts out of st.html on some frontend versions.
# Use its supported same-origin HTML component to initialize our own UI script.
script_source = json.dumps((ROOT / 'script.js').read_text(encoding='utf-8')).replace('</', '<\\/')
components.html('<script>if(window.parent.__avMotion&&window.parent.__avMotion.version==="photo-inline-5"){window.parent.__avMotion.refresh();}else{const s=window.parent.document.createElement("script");s.textContent=' + script_source + ';window.parent.document.body.appendChild(s);}</script>', height=0, scrolling=False)
