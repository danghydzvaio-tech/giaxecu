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

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='AutoValue India · Giá xe cũ', page_icon='🚗', layout='wide')
def fragment(name):
    document = (ROOT / 'index.html').read_text(encoding='utf-8')
    content = re.search(rf'<!-- av:{name} -->(.*?)<!-- /av:{name} -->', document, re.S).group(1)
    # st.html supports HTML images but strips inline SVG: preserve the artwork as a data image.
    def svg_image(match):
        class_name = re.search(r'class="([^"]+)"', match.group(0)).group(1)
        alt = 'Minh họa ô tô' if class_name == 'av-car' else ''
        return '<img class="' + class_name + '" alt="' + alt + '" decoding="async" src="data:image/svg+xml;base64,' + base64.b64encode(match.group(0).encode()).decode() + '">'
    content = re.sub(r'<svg\b[^>]*>.*?</svg>', svg_image, content, flags=re.S)
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
    source = (ROOT / 'index.html').read_text(encoding='utf-8')
    svg = re.search(r'<svg\b[^>]*class="av-car".*?</svg>', source, re.S).group(0)
    image = 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()
    palette = ['#dbe8dc', '#e9dfd3', '#dcdff0', '#e8dce3', '#d5e8e6', '#eee4cc']
    rows = []
    paint = [('#E8F0DC','#99AF99','#42645B'),('#EEDDD2','#B29A8B','#68574F'),('#E0E5F3','#9AAAC2','#45556F'),('#ECDDDE','#B49AA4','#705362'),('#E0F1EE','#87B7AD','#396D64'),('#F0E9D6','#BCAD82','#746442')]
    for index, brand_name in enumerate(['maruti', 'honda', 'hyundai', 'toyota', 'ford', 'renault']):
        subset = reference[reference.brand == brand_name]
        popular = subset.name.value_counts().index[0]
        selected = subset[subset.name == popular].sort_values('selling_price')
        car = selected.iloc[len(selected) // 2]
        light, middle_color, dark = paint[index]
        colored_svg = svg.replace('#DFEFEE', light).replace('#8CA7AE', middle_color).replace('#34515F', dark)
        image = 'data:image/svg+xml;base64,' + base64.b64encode(colored_svg.encode()).decode()
        name = html.escape(str(car['name']).title())
        tag = html.escape(f"{brand_name.title()} · {int(car['year'])}")
        price = f"₹{car['selling_price']:,.0f}"
        rows.append(f'''<button type="button" class="av-collection-row" data-color="{palette[index]}" data-index="{index}" data-image="{image}" aria-expanded="false" aria-controls="av-row-extra-{index}">
          <span class="av-row-name">{name}</span><span class="av-row-tag">{tag}</span><span class="av-row-price">{price}</span>
          <span class="av-row-extra" id="av-row-extra-{index}" hidden><img class="av-row-image" src="{image}" loading="lazy" alt="Minh họa ô tô, không phải ảnh xe thực tế"><span>Giá nguồn lịch sử · {int(car['km_driven']):,} km · Minh họa ô tô</span></span></button>''')
    layers = ''.join(f'<div class="av-collection-background" data-layer="{i}" style="background:{c}"></div>' for i, c in enumerate(palette))
    return f'''<section id="collection" class="av-collection" aria-label="Xe trong dữ liệu tham chiếu">{layers}
      <div class="av-collection-copy"><p class="av-eyebrow">AUTOVALUE INDIA</p><h2>Đối chiếu với xe trong dữ liệu</h2><p>Giá nguồn lịch sử, không phải tin rao đang bán. Hình xe là minh họa SVG tự vẽ.</p></div>
      <div class="av-collection-list">{''.join(rows)}</div></section>
      <div class="av-preview" aria-hidden="true"><div class="av-preview-image"><img src="{image}" alt=""><img src="{image}" alt=""></div><span class="av-preview-caption">Minh họa ô tô</span></div>'''


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
components.html('<script>if(window.parent.__avMotion&&window.parent.__avMotion.version==="creative-3"){window.parent.__avMotion.refresh();}else{const s=window.parent.document.createElement("script");s.textContent=' + script_source + ';window.parent.document.body.appendChild(s);}</script>', height=0, scrolling=False)
