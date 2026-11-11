"""Verified local car photos and exact gallery-to-training-row matching."""
from functools import lru_cache
import json
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent


@lru_cache(maxsize=1)
def load_catalog():
    return json.loads((ROOT / 'static/cars/catalog.json').read_text(encoding='utf-8'))


def reference_car(reference, photo):
    selected = reference[(reference.name == photo['dataset_name']) & (reference.year == photo['dataset_year'])]
    if 'dataset_price' in photo:
        selected = selected[selected.selling_price == photo['dataset_price']]
    if selected.empty:
        raise ValueError(f"Không có bản ghi train khớp ảnh: {photo['dataset_name']} / {photo['dataset_year']}")
    selected = selected.sort_values('selling_price')
    return selected.iloc[len(selected) // 2]


def photo_for_car(name, year):
    name = str(name).strip().lower()
    for photo in load_catalog()['photos']:
        if name.startswith(photo['match_prefix']) and photo['min_year'] <= int(year) <= photo['max_year']:
            return photo
    return None


def public_photo_url(photo, base_path=''):
    prefix = '/' + base_path.strip('/') if base_path.strip('/') else ''
    return prefix + '/app/static/cars/' + photo['filename']


@lru_cache(maxsize=16)
def _embedded_photo(filename):
    if Path(filename).name != filename:
        raise ValueError('Tên tệp ảnh không hợp lệ.')
    payload = (ROOT / 'static/cars' / filename).read_bytes()
    return 'data:image/webp;base64,' + base64.b64encode(payload).decode('ascii')


def embedded_photo_url(photo):
    """Embed verified repository bytes; no static route/proxy/CDN dependency."""
    return _embedded_photo(photo['filename'])
