"""Select a grouped-CV model, calibrate intervals, then evaluate holdout once.

Run: OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python train.py
Optional: --source-csv '/path/to/Car details v3.csv' (verified Kaggle v4 bytes).
The calibration split never chooses a model, preprocessing rule or epoch budget.
"""
import argparse
import hashlib
import io
import json
import platform
import time
import zipfile
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from urllib.request import urlopen

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

from car_model import (FEATURES, GROUP_COLUMNS, clean_v3, conformal_quantile,
                       estimate, estimate_interval, intervals_from_log,
                       make_preprocessor, predicted_log_prices)
from build_manifest import write_manifest

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / 'artifacts'
SOURCE_PAGE = 'https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho'
DOWNLOAD = 'https://www.kaggle.com/api/v1/datasets/download/nehalbirla/vehicle-dataset-from-cardekho?datasetVersionNumber=4'
SOURCE_FILE = 'Car details v3.csv'
SOURCE_SHA256 = '1b2a30b2f36fd246366773fe5375399692f1a113890ad2a6d464b8c8deaadadb'
SEED = 42
COVERAGE = .8
LABELS = {'mlp': 'Mạng nơ-ron ANN (MLP)', 'random_forest': 'Random Forest',
          'hist_gradient_boosting': 'HistGradientBoosting'}
IMPLEMENTATIONS = {'mlp': 'sklearn.neural_network.MLPRegressor',
                   'random_forest': 'sklearn.ensemble.RandomForestRegressor',
                   'hist_gradient_boosting': 'sklearn.ensemble.HistGradientBoostingRegressor'}


def scores(actual, predicted):
    actual, predicted = np.asarray(actual, dtype=float), np.asarray(predicted, dtype=float)
    percentage = np.abs(actual - predicted) / actual * 100
    return {'n': int(len(actual)), 'mae_inr': float(mean_absolute_error(actual, predicted)),
            'rmse_inr': float(np.sqrt(mean_squared_error(actual, predicted))),
            'r2': float(r2_score(actual, predicted)) if len(actual) >= 2 else None,
            'mape_percent': float(np.mean(percentage)),
            'median_ape_percent': float(np.median(percentage))}


def group_hashes(frame):
    return pd.util.hash_pandas_object(frame[GROUP_COLUMNS], index=False).to_numpy(dtype=np.uint64)


def grouped_splits(data):
    groups = group_hashes(data)
    development_idx, test_idx = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=SEED).split(data, groups=groups))
    fit_local, calibration_local = next(GroupShuffleSplit(n_splits=1, test_size=.2, random_state=SEED + 1).split(
        data.iloc[development_idx], groups=groups[development_idx]))
    train_idx, calibration_idx = development_idx[fit_local], development_idx[calibration_local]
    group_sets = [set(groups[index]) for index in (train_idx, calibration_idx, test_idx)]
    if group_sets[0] & group_sets[1] or group_sets[0] & group_sets[2] or group_sets[1] & group_sets[2]:
        raise ValueError('Nhóm dữ liệu bị trùng giữa huấn luyện, hiệu chỉnh và kiểm tra.')
    return train_idx, calibration_idx, test_idx, groups


def new_model(name, seed):
    if name == 'mlp':
        return MLPRegressor(hidden_layer_sizes=(128, 64), activation='relu', solver='adam',
                            alpha=.01, learning_rate_init=.001, batch_size=64,
                            random_state=seed, max_iter=1, early_stopping=False)
    if name == 'random_forest':
        return RandomForestRegressor(n_estimators=220, max_depth=24, min_samples_leaf=2,
                                     max_features=.8, random_state=seed, n_jobs=2)
    return HistGradientBoostingRegressor(max_iter=220, learning_rate=.06, max_leaf_nodes=31,
                                        min_samples_leaf=20, l2_regularization=2.,
                                        early_stopping=False, random_state=seed)


def fit_transforms(frame):
    preprocessor = make_preprocessor()
    x = preprocessor.fit_transform(frame[FEATURES]).astype(np.float32)
    target_scaler = StandardScaler().fit(np.log1p(frame.selling_price).to_numpy().reshape(-1, 1))
    y = target_scaler.transform(np.log1p(frame.selling_price).to_numpy().reshape(-1, 1)).ravel()
    return preprocessor, target_scaler, x, y


def choose_mlp_epochs(frame, seed, history, context):
    """Only an inner grouped subset of the current fitting fold stops the ANN."""
    inner_train, inner_validation = next(GroupShuffleSplit(n_splits=1, test_size=.15, random_state=seed + 1000).split(
        frame, groups=group_hashes(frame)))
    train, validation = frame.iloc[inner_train], frame.iloc[inner_validation]
    prep, scaler, x_train, y_train = fit_transforms(train)
    x_validation = prep.transform(validation[FEATURES]).astype(np.float32)
    y_validation = scaler.transform(np.log1p(validation.selling_price).to_numpy().reshape(-1, 1)).ravel()
    model = new_model('mlp', seed)
    best_loss, best_epoch, stale = np.inf, 1, 0
    for epoch in range(1, 201):
        model.partial_fit(x_train, y_train)
        loss = float(mean_squared_error(y_validation, model.predict(x_validation)))
        history.append({'stage': 'mlp_inner_stop', 'context': context, 'epoch': epoch,
                        'train_loss': float(model.loss_), 'inner_validation_mse_scaled_log': loss})
        if loss < best_loss - 1e-5:
            best_loss, best_epoch, stale = loss, epoch, 0
        else:
            stale += 1
        if stale >= 20:
            break
    print(f'{context}: MLP inner grouped stop chose {best_epoch} epochs (ran {epoch})', flush=True)
    return best_epoch


def fit_candidate(name, frame, seed, history, context):
    started = time.monotonic()
    epochs = choose_mlp_epochs(frame, seed, history, context) if name == 'mlp' else None
    prep, scaler, x, y = fit_transforms(frame)
    model = new_model(name, seed)
    if name == 'mlp':
        for epoch in range(1, epochs + 1):
            model.partial_fit(x, y)
            history.append({'stage': 'mlp_refit', 'context': context, 'epoch': epoch,
                            'train_loss': float(model.loss_)})
    else:
        model.fit(x, y)
    history.append({'stage': 'fit_complete', 'context': context, 'model': name,
                    'fit_rows': len(frame), 'fit_seconds': time.monotonic() - started,
                    'epochs': epochs})
    return {'model': model, 'preprocessor': prep, 'target_scaler': scaler}, epochs


def cross_validate(train, history):
    groups = group_hashes(train)
    folds = list(GroupKFold(n_splits=5, shuffle=True, random_state=SEED).split(train, groups=groups))
    fold_ids = np.full(len(train), -1, dtype=np.int8)
    for fold, (fit_idx, validation_idx) in enumerate(folds):
        if set(groups[fit_idx]) & set(groups[validation_idx]):
            raise ValueError('Nhóm bị trùng trong cross-validation.')
        fold_ids[validation_idx] = fold
    models = {}
    for name, label in LABELS.items():
        results = []
        for fold, (fit_idx, validation_idx) in enumerate(folds):
            print(f'CV {label}: fold {fold + 1}/5', flush=True)
            fitted, epochs = fit_candidate(name, train.iloc[fit_idx], SEED + fold, history, f'cv_{name}_{fold + 1}')
            prediction = np.expm1(predicted_log_prices(fitted, train.iloc[validation_idx]))
            result = {'fold': fold + 1, 'fit_rows': len(fit_idx), 'validation_rows': len(validation_idx),
                      'fit_groups': len(set(groups[fit_idx])), 'validation_groups': len(set(groups[validation_idx])),
                      'group_overlap': 0, 'mlp_epochs': epochs, **scores(train.iloc[validation_idx].selling_price, prediction)}
            results.append(result)
            print(f'CV {name} fold {fold + 1}: MAE={result["mae_inr"]:.2f}, MAPE={result["mape_percent"]:.2f}%, R2={result["r2"]:.4f}', flush=True)
        metrics = ['mae_inr', 'rmse_inr', 'r2', 'mape_percent', 'median_ape_percent']
        models[name] = {'label': label, 'folds': results,
                        'mean': {metric: float(np.mean([row[metric] for row in results])) for metric in metrics},
                        'std': {metric: float(np.std([row[metric] for row in results], ddof=1)) for metric in metrics}}
    winner = min(models, key=lambda name: models[name]['mean']['mae_inr'])
    return winner, models, fold_ids


def price_segments(actual, prediction, low, high):
    masks = [('below_3_lakh', 'Dưới 3 lakh', actual < 300_000),
             ('3_to_6_lakh', '3–6 lakh', (actual >= 300_000) & (actual < 600_000)),
             ('6_to_10_lakh', '6–10 lakh', (actual >= 600_000) & (actual <= 1_000_000)),
             ('above_10_lakh', 'Trên 10 lakh', actual > 1_000_000)]
    return [{'segment': key, 'label': label, **scores(actual[mask], prediction[mask]),
             'coverage': float(np.mean((low[mask] <= actual[mask]) & (actual[mask] <= high[mask])))}
            for key, label, mask in masks if mask.any()]


def read_source(path=None):
    if path is not None:
        payload = Path(path).read_bytes()
    else:
        print('Downloading public Kaggle version 4…', flush=True)
        with urlopen(DOWNLOAD, timeout=60) as response:
            archive = response.read(10 * 1024 * 1024)
        with zipfile.ZipFile(io.BytesIO(archive)) as package:
            payload = package.read(SOURCE_FILE)
    if hashlib.sha256(payload).hexdigest() != SOURCE_SHA256:
        raise ValueError('SHA-256 của CSV không khớp Car details v3.csv, Kaggle dataset version 4.')
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-csv', type=Path, help='Tệp Kaggle v4 đã tải; kiểm tra SHA-256 trước huấn luyện.')
    args = parser.parse_args(argv)
    payload = read_source(args.source_csv)
    data, audit = clean_v3(pd.read_csv(io.BytesIO(payload)))
    train_idx, calibration_idx, test_idx, groups = grouped_splits(data)
    train = data.iloc[train_idx].copy()
    calibration = data.iloc[calibration_idx].copy()
    print('Fitting rows:', len(train), '; calibration rows:', len(calibration), '; reserved test rows:', len(test_idx), flush=True)
    history = []
    winner, cv_models, fold_ids = cross_validate(train, history)
    print('Selected using CV mean MAE only:', winner, flush=True)
    bundle, epochs = fit_candidate(winner, train, SEED, history, 'final_selected')
    calibration_log = predicted_log_prices(bundle, calibration)
    residuals = np.abs(np.log1p(calibration.selling_price.to_numpy()) - calibration_log)
    radius, rank = conformal_quantile(residuals, COVERAGE)
    bundle['conformal'] = {'nominal_coverage': COVERAGE, 'log_residual_quantile': radius,
                           'calibration_rows': len(calibration), 'quantile_rank': rank}

    # The selected model is fixed before this single final holdout evaluation.
    test = data.iloc[test_idx].copy()
    low, prediction, high = intervals_from_log(predicted_log_prices(bundle, test), radius)
    actual = test.selling_price.to_numpy(dtype=float)
    covered = (low <= actual) & (actual <= high)
    test_scores = scores(actual, prediction)
    report = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'source_url': SOURCE_PAGE, 'source_dataset_version': 4, 'source_file': SOURCE_FILE,
        'source_csv_sha256': hashlib.sha256(payload).hexdigest(),
        'dataset_listing_updated': '2023-01-14', 'observation_date': 'not available per listing',
        'currency': 'INR', 'price_unit_note': 'v3 selling_price is numeric INR; no lakh multiplication.',
        'license_name': 'Database: Open Database, Contents: Database Contents',
        'license_url': 'https://opendatacommons.org/licenses/dbcl/1.0/',
        'cleaning': audit,
        'split': {'seed': SEED, 'train_rows': len(train), 'validation_rows': len(calibration),
                  'test_rows': len(test), 'train_groups': len(set(groups[train_idx])),
                  'validation_groups': len(set(groups[calibration_idx])), 'test_groups': len(set(groups[test_idx])),
                  'group_columns': GROUP_COLUMNS, 'group_overlap': 0,
                  'validation_role': 'split-conformal calibration only; excluded from model/epoch selection'},
        'cross_validation': {'method': 'GroupKFold', 'n_splits': 5, 'seed': SEED,
                             'selection_data': '4423 fitting-development rows; calibration excluded',
                             'selection_metric': 'mean_mae_inr', 'std_ddof': 1,
                             'models': cv_models},
        'selected_model': {'name': winner, 'label': LABELS[winner], 'implementation': IMPLEMENTATIONS[winner],
                           'selection_metric': 'mean_cv_mae_inr',
                           'cv_mae_inr_mean': cv_models[winner]['mean']['mae_inr'],
                           'mlp_epochs': epochs, 'parameters': bundle['model'].get_params(),
                           'target': 'standardized log1p(INR)'},
        'test': test_scores,
        'conformal': {**bundle['conformal'], 'method': 'split conformal; absolute log1p(INR) residuals',
                      'test_coverage': float(np.mean(covered)),
                      'mean_width_inr': float(np.mean(high - low)),
                      'median_width_inr': float(np.median(high - low))},
        'price_segments': price_segments(actual, prediction, low, high),
        'median_baseline': scores(actual, np.full(len(test), train.selling_price.median())),
        'features': FEATURES,
        'limitations': [
            'Historical dataset through production year 2020; no listing observation dates or current-market prices.',
            'Conformal 80% is nominal marginal coverage under exchangeability, not a per-car probability guarantee.',
            'Grouped sampling, unobserved reposts and future distribution shift may affect interval coverage.',
            'Calibration labels do not choose preprocessing, model, hyperparameters or ANN epochs.',
            'Passenger classification is name/seats-based, not VIN-verified.',
        ],
        'versions': {package: version(package) for package in ['scikit-learn', 'numpy', 'pandas', 'joblib']},
        'python_version': platform.python_version(),
    }
    bundle['report'] = report
    ARTIFACTS.mkdir(exist_ok=True)
    joblib.dump(bundle, ARTIFACTS / 'ann_bundle.joblib', compress=('xz', 3))
    (ARTIFACTS / 'evaluation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    pd.DataFrame(history).to_csv(ARTIFACTS / 'training_history.csv', index=False)
    train[FEATURES + ['km_driven', 'selling_price']].to_csv(ARTIFACTS / 'reference.csv', index=False)
    result = test[['name', 'year', 'km_driven', 'selling_price']].copy()
    result['selected_prediction_inr'] = prediction
    result['interval_low_inr'], result['interval_high_inr'] = low, high
    result['interval_covered'] = covered
    result['absolute_error_inr'] = np.abs(actual - prediction)
    result['absolute_percentage_error_percent'] = np.abs(actual - prediction) / actual * 100
    result['original_clean_row'] = test_idx
    result.to_csv(ARTIFACTS / 'holdout_predictions.csv', index=False)
    np.savez_compressed(ARTIFACTS / 'split_indices.npz', train=train_idx, validation=calibration_idx,
                        test=test_idx, train_group_hash=groups[train_idx],
                        validation_group_hash=groups[calibration_idx], test_group_hash=groups[test_idx],
                        cv_fold=fold_ids)
    verification = {'created_utc': report['created_utc'], 'source_sha_verified': True,
                    'train_calibration_test_groups_disjoint': True,
                    'cv_fold_groups_disjoint': all(not set(group_hashes(train)[fold_ids == k]) & set(group_hashes(train)[fold_ids != k]) for k in range(5)),
                    'calibration_excluded_from_selection': True,
                    'interval_bounds_ordered': bool(np.all((0 <= low) & (low <= prediction) & (prediction <= high))),
                    'selected_model': winner, 'test_rows': len(test), 'test_metrics': test_scores,
                    'test_interval_coverage': float(np.mean(covered))}
    (ARTIFACTS / 'verification.json').write_text(json.dumps(verification, ensure_ascii=False, indent=2), encoding='utf-8')
    # Regenerate regression fixtures from the saved model; input examples are fixed.
    examples_path = ROOT / 'tests/prediction_examples.json'
    examples = json.loads(examples_path.read_text(encoding='utf-8'))
    saved_bundle = joblib.load(ARTIFACTS / 'ann_bundle.joblib')
    for example in examples:
        example['expected_prediction_inr'] = estimate(saved_bundle, example['inputs'])
        lower, central, upper = estimate_interval(saved_bundle, example['inputs'])
        example['expected_interval_inr'] = {'low': lower, 'central': central, 'high': upper}
    examples_path.write_text(json.dumps(examples, ensure_ascii=False, indent=2), encoding='utf-8')
    write_manifest(ARTIFACTS)
    print(json.dumps({'selected_model': report['selected_model'], 'test': test_scores,
                      'conformal': report['conformal'], 'price_segments': report['price_segments']}, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    with threadpool_limits(limits=2):
        main()
