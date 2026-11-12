"""Passenger-car data rules and inference shared by training and Streamlit."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC = ['year', 'log_km', 'engine_cc', 'power_bhp', 'seats']
CATEGORICAL = ['brand', 'name', 'fuel', 'transmission', 'owner', 'seller_type']
FEATURES = NUMERIC + CATEGORICAL
GROUP_COLUMNS = ['name', 'year', 'km_driven', 'fuel', 'transmission']
BRANDS = {
    'maruti', 'hyundai', 'mahindra', 'tata', 'toyota', 'honda', 'ford', 'chevrolet',
    'renault', 'volkswagen', 'bmw', 'skoda', 'nissan', 'jaguar', 'volvo', 'datsun',
    'mercedes-benz', 'fiat', 'audi', 'lexus', 'jeep', 'mitsubishi', 'land', 'force',
    'isuzu', 'ambassador', 'kia', 'mg', 'daewoo', 'opel', 'peugeot',
}


def numeric_prefix(values):
    return pd.to_numeric(values.astype('string').str.extract(r'(\d+(?:\.\d+)?)', expand=False), errors='coerce')


def clean_v3(raw):
    required = {'name', 'year', 'selling_price', 'km_driven', 'fuel', 'seller_type',
                'transmission', 'owner', 'engine', 'max_power', 'seats'}
    if not required.issubset(raw.columns):
        raise ValueError('Cần đúng tệp Car details v3.csv từ nguồn Kaggle đã ghi trong README.')
    d = raw.copy()
    audit = {'raw_rows': len(d)}
    for col in ['name', 'fuel', 'transmission', 'owner', 'seller_type']:
        d[col] = d[col].astype('string').str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)
    d['brand'] = d.name.str.split().str[0]
    commercial = d.name.str.contains(r'pik[ -]?up|pick[ -]?up|truck|ambulance|\bwinger\b', regex=True, na=False)
    seats = pd.to_numeric(d.seats, errors='coerce')
    passenger = d.brand.isin(BRANDS) & ~commercial & (seats.isna() | seats.between(4, 9))
    audit['excluded_non_passenger_or_unverified_rows'] = int((~passenger).sum())
    audit['excluded_names'] = sorted(d.loc[~passenger, 'name'].dropna().unique().tolist())
    d = d[passenger].copy()
    for col in ['year', 'selling_price', 'km_driven', 'seats']:
        d[col] = pd.to_numeric(d[col], errors='coerce')
    valid = (d.year.between(1980, 2020) & (d.year % 1 == 0)
             & np.isfinite(d.km_driven) & d.km_driven.between(0, 3_000_000)
             & d.selling_price.between(10_000, 200_000_000)
             & d[['name', 'fuel', 'transmission', 'owner', 'seller_type']].notna().all(axis=1))
    audit['invalid_required_rows'] = int((~valid).sum())
    d = d[valid].copy()
    audit['duplicate_rows_removed'] = int(d.duplicated().sum())
    d = d.drop_duplicates().reset_index(drop=True)
    d['engine_cc'] = numeric_prefix(d.engine).where(lambda s: s.between(400, 10_000))
    d['power_bhp'] = numeric_prefix(d.max_power).where(lambda s: s.between(10, 1_000))
    d['seats'] = d.seats.where(d.seats.between(4, 9))
    d['log_km'] = np.log1p(d.km_driven)
    audit['missing_engine_cc'] = int(d.engine_cc.isna().sum())
    audit['missing_power_bhp'] = int(d.power_bhp.isna().sum())
    audit['missing_seats'] = int(d.seats.isna().sum())
    audit['usable_rows'] = len(d)
    audit['year_min'] = int(d.year.min())
    audit['year_max'] = int(d.year.max())
    audit['brands'] = sorted(d.brand.unique().tolist())
    return d, audit


def make_preprocessor():
    return ColumnTransformer([
        ('numeric', Pipeline([('fill', SimpleImputer(strategy='median')),
                              ('scale', StandardScaler())]), NUMERIC),
        ('category', OneHotEncoder(handle_unknown='infrequent_if_exist', min_frequency=3,
                                   sparse_output=False, dtype=np.float32), CATEGORICAL),
    ])


def prediction_frame(row):
    row = dict(row)
    row['log_km'] = np.log1p(row['km_driven'])
    return pd.DataFrame([row])[FEATURES]


def estimate(bundle, row):
    transformed = bundle['preprocessor'].transform(prediction_frame(row))
    scaled_log_price = bundle['model'].predict(transformed)
    log_price = bundle['target_scaler'].inverse_transform(scaled_log_price.reshape(-1, 1)).ravel()
    return float(np.maximum(0, np.expm1(log_price))[0])
