"""Download Kaggle v4, train an ANN and evaluate untouched holdout groups.

Run: OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python train.py
Never uses the uploaded Excel. No key needed for this public Kaggle download.
"""
import copy
import hashlib
import io
import json
import platform
import zipfile
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from urllib.request import urlopen

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

from car_model import FEATURES, GROUP_COLUMNS, clean_v3, make_preprocessor
from build_manifest import write_manifest

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / 'artifacts'
SOURCE_PAGE = 'https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho'
DOWNLOAD = 'https://www.kaggle.com/api/v1/datasets/download/nehalbirla/vehicle-dataset-from-cardekho?datasetVersionNumber=4'
SOURCE_FILE = 'Car details v3.csv'
SEED = 42


def scores(actual, predicted):
    return {'mae_inr': float(mean_absolute_error(actual, predicted)),
            'rmse_inr': float(np.sqrt(mean_squared_error(actual, predicted))),
            'r2': float(r2_score(actual, predicted))}


def main():
    ARTIFACTS.mkdir(exist_ok=True)
    print('Downloading public Kaggle version 4…', flush=True)
    with urlopen(DOWNLOAD, timeout=60) as response:
        archive = response.read(10 * 1024 * 1024)
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        payload = z.read(SOURCE_FILE)
    data, audit = clean_v3(pd.read_csv(io.BytesIO(payload)))
    print('Cleaning:', json.dumps(audit, ensure_ascii=False), flush=True)
    groups = pd.util.hash_pandas_object(data[GROUP_COLUMNS], index=False)
    development_idx, test_idx = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=SEED).split(data, groups=groups))
    development = data.iloc[development_idx]
    train_local, val_local = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=SEED + 1).split(development, groups=groups.iloc[development_idx]))
    train_idx, val_idx = development_idx[train_local], development_idx[val_local]
    train, val, test = data.iloc[train_idx], data.iloc[val_idx], data.iloc[test_idx]
    group_sets = [set(groups.iloc[idx]) for idx in (train_idx, val_idx, test_idx)]
    assert not (group_sets[0] & group_sets[1] or group_sets[0] & group_sets[2] or group_sets[1] & group_sets[2])
    prep = make_preprocessor()
    x_train = prep.fit_transform(train[FEATURES]).astype(np.float32)
    x_val = prep.transform(val[FEATURES]).astype(np.float32)
    x_test = prep.transform(test[FEATURES]).astype(np.float32)
    target_scaler = StandardScaler().fit(np.log1p(train.selling_price).to_numpy().reshape(-1, 1))
    y_train = target_scaler.transform(np.log1p(train.selling_price).to_numpy().reshape(-1, 1)).ravel()
    y_val = target_scaler.transform(np.log1p(val.selling_price).to_numpy().reshape(-1, 1)).ravel()
    ann = MLPRegressor(hidden_layer_sizes=(128, 64), activation='relu', solver='adam',
                       alpha=.01, learning_rate_init=.001, batch_size=64,
                       random_state=SEED, max_iter=1, early_stopping=False)
    best_loss, best_model, best_epoch, stale, history = np.inf, None, 0, 0, []
    # Explicit validation groups; no internal random-row validation split.
    for epoch in range(1, 401):
        ann.partial_fit(x_train, y_train)
        validation_loss = float(mean_squared_error(y_val, ann.predict(x_val)))
        history.append({'epoch': epoch, 'train_loss': float(ann.loss_),
                        'validation_mse_scaled_log': validation_loss})
        if validation_loss < best_loss - 1e-5:
            best_loss, best_model, best_epoch, stale = validation_loss, copy.deepcopy(ann), epoch, 0
        else:
            stale += 1
        if epoch % 25 == 0:
            print(f'ANN epoch {epoch}: validation loss={validation_loss:.5f}, best epoch={best_epoch}', flush=True)
        if stale >= 30:
            break
    def inverse(scaled):
        return np.maximum(0, np.expm1(target_scaler.inverse_transform(np.asarray(scaled).reshape(-1, 1)).ravel()))
    ann_predictions = inverse(best_model.predict(x_test))
    print('Training Random Forest comparator…', flush=True)
    forest = RandomForestRegressor(n_estimators=220, max_depth=24, min_samples_leaf=2,
                                   max_features=.8, random_state=SEED, n_jobs=2)
    forest.fit(x_train, y_train)
    forest_predictions = inverse(forest.predict(x_test))
    median_predictions = np.full(len(test), train.selling_price.median())
    report = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'source_url': SOURCE_PAGE, 'source_dataset_version': 4, 'source_file': SOURCE_FILE,
        'source_csv_sha256': hashlib.sha256(payload).hexdigest(),
        'dataset_listing_updated': '2023-01-14', 'observation_date': 'not available per listing',
        'currency': 'INR', 'price_unit_note': 'v3 selling_price is treated as numeric INR; no lakh multiplication.',
        'license_name': 'Database: Open Database, Contents: Database Contents',
        'license_url': 'https://opendatacommons.org/licenses/dbcl/1.0/',
        'cleaning': audit,
        'split': {'seed': SEED, 'train_rows': len(train), 'validation_rows': len(val), 'test_rows': len(test),
                  'train_groups': len(group_sets[0]), 'validation_groups': len(group_sets[1]), 'test_groups': len(group_sets[2]),
                  'group_columns': GROUP_COLUMNS, 'group_overlap': 0},
        'ann': {'implementation': 'sklearn.neural_network.MLPRegressor', 'hidden_layers': [128, 64],
                'activation': 'relu', 'optimizer': 'adam', 'l2_alpha': .01,
                'learning_rate': .001, 'batch_size': 64, 'epochs_run': len(history),
                'best_epoch': best_epoch, 'patience': 30,
                'target': 'standardized log1p(INR)', **scores(test.selling_price, ann_predictions)},
        'random_forest': scores(test.selling_price, forest_predictions),
        'median_baseline': scores(test.selling_price, median_predictions),
        'features': FEATURES,
        'limitations': [
            'Historical dataset; no verified current-market prices or individual listing dates.',
            'One held-out grouped split is not a guarantee across future samples or unseen car models.',
            'Grouping reduces duplicate leakage, but no VIN/listing ID exists to rule out all reposts.',
            'No calibrated prediction intervals; test MAE is not a per-car error bound.',
            'Rows with missing seats are kept only for recognized car makes; classification is name-based, not VIN-verified.',
        ],
        'versions': {p: version(p) for p in ['scikit-learn', 'numpy', 'pandas', 'joblib']},
        'python_version': platform.python_version(),
    }
    joblib.dump({'model': best_model, 'preprocessor': prep, 'target_scaler': target_scaler,
                 'report': report}, ARTIFACTS / 'ann_bundle.joblib', compress=3)
    (ARTIFACTS / 'evaluation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    pd.DataFrame(history).to_csv(ARTIFACTS / 'training_history.csv', index=False)
    train[FEATURES + ['km_driven', 'selling_price']].to_csv(ARTIFACTS / 'reference.csv', index=False)
    results = test[['name', 'year', 'km_driven', 'selling_price']].copy()
    results['ann_prediction_inr'] = ann_predictions
    results['random_forest_prediction_inr'] = forest_predictions
    results['original_clean_row'] = test_idx
    results.to_csv(ARTIFACTS / 'holdout_predictions.csv', index=False)
    np.savez_compressed(ARTIFACTS / 'split_indices.npz', train=train_idx, validation=val_idx, test=test_idx)
    write_manifest(ARTIFACTS)
    print(json.dumps({'split': report['split'], 'ann': report['ann'],
                      'random_forest': report['random_forest'], 'median_baseline': report['median_baseline']}, indent=2), flush=True)
    print('Saved evaluated ANN and training-only references to', ARTIFACTS, flush=True)


if __name__ == '__main__':
    with threadpool_limits(limits=2):
        main()
