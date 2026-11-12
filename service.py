"""Load the evaluated ANN and validate inputs independently of the web UI."""
import hashlib
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from car_model import estimate

ROOT = Path(__file__).resolve().parent


def load_assets(root=ROOT):
    folder = Path(root) / 'artifacts'
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    for filename, expected in manifest['sha256'].items():
        actual = hashlib.sha256((folder / filename).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'Tệp {filename} không khớp phiên bản mô hình. Hãy tải lại trọn bộ artifacts/.')
    bundle = joblib.load(folder / 'ann_bundle.joblib')
    reference = pd.read_csv(folder / 'reference.csv')
    if len(reference) != bundle['report']['split']['train_rows']:
        raise ValueError('Dữ liệu tham chiếu không khớp mô hình.')
    return bundle, reference


def predict_vehicle(bundle, reference, row):
    """Return a historical INR estimate, warnings and matching training references."""
    row = dict(row)
    for key in ['brand', 'name', 'fuel', 'transmission', 'owner', 'seller_type']:
        if not isinstance(row.get(key), str):
            raise ValueError(f'Thiếu thông tin: {key}.')
    limits = {
        'year': (bundle['report']['cleaning']['year_min'], bundle['report']['cleaning']['year_max']),
        'km_driven': (0, 3_000_000), 'engine_cc': (400, 10_000),
        'power_bhp': (10, 1_000), 'seats': (4, 9),
    }
    for key, (low, high) in limits.items():
        try:
            value = float(row[key])
        except (KeyError, TypeError, ValueError):
            raise ValueError(f'{key} phải là số hợp lệ.') from None
        if not np.isfinite(value) or not low <= value <= high:
            raise ValueError(f'{key} phải từ {low} đến {high}.')
        if key in ['year', 'seats'] and not value.is_integer():
            raise ValueError(f'{key} phải là số nguyên.')
        row[key] = value
    peers = reference[(reference.brand == row['brand']) & (reference.name == row['name'])
                      & (reference.fuel == row['fuel']) & (reference.transmission == row['transmission'])]
    if peers.empty:
        raise ValueError('Dữ liệu chưa hỗ trợ cấu hình xe này. Hãy chọn lại hãng, phiên bản, nhiên liệu và hộp số.')
    for key in ['owner', 'seller_type']:
        if row[key] not in set(reference[key]):
            raise ValueError(f'Giá trị {key} chưa được hỗ trợ.')
    warnings = []
    if len(peers) < 10:
        warnings.append('Cấu hình này có dưới 10 mẫu tham chiếu; kết quả có thể thiếu ổn định.')
    labels = {'year': 'Năm sản xuất', 'km_driven': 'Số km', 'engine_cc': 'Dung tích động cơ',
              'power_bhp': 'Công suất', 'seats': 'Số ghế'}
    for key, label in labels.items():
        known = peers[key].dropna()
        if len(known) and not known.min() <= row[key] <= known.max():
            warnings.append(f'{label} nằm ngoài phạm vi mẫu của phiên bản đã chọn.')
    if row['owner'] not in set(peers.owner) or row['seller_type'] not in set(peers.seller_type):
        warnings.append('Lịch sử sở hữu hoặc loại người bán ít được đại diện cho cấu hình này.')
    price = estimate(bundle, row)
    if not np.isfinite(price) or price <= 0:
        raise ValueError('Chưa thể dự đoán đáng tin cậy cho cấu hình này. Hãy kiểm tra thông số xe.')
    return price, warnings, peers
