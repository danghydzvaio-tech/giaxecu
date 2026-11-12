"""Leakage, finite-sample interval and honest-reporting regression checks."""
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

from car_model import conformal_quantile, intervals_from_log
from service import historical_reference, load_assets, predict_vehicle

ROOT = Path(__file__).resolve().parents[1]


class ConformalMathTests(unittest.TestCase):
    def test_finite_sample_order_statistic_not_interpolated(self):
        q, rank = conformal_quantile(np.arange(1, 11) / 10, .8)
        self.assertEqual(rank, 9)
        self.assertAlmostEqual(q, .9)
        q, rank = conformal_quantile(np.arange(1101, dtype=float), .8)
        self.assertEqual(rank, 882)
        self.assertEqual(q, 881.)
        self.assertEqual(conformal_quantile([.1, .2, .3, .4], .8), (.4, 4))

    def test_insufficient_or_invalid_calibration_fails(self):
        for residuals, coverage in [([], .8), ([.1, .2, .3], .8), ([np.nan] * 5, .8),
                                    ([-1] * 5, .8), ([.1] * 5, 1), ([.1] * 5, 0)]:
            with self.subTest(residuals=residuals, coverage=coverage):
                with self.assertRaises(ValueError):
                    conformal_quantile(residuals, coverage)

    def test_log_intervals_are_multiplicative_and_nonnegative(self):
        low, central, high = intervals_from_log(np.log1p([0, 100, 1_000_000]), .5)
        np.testing.assert_allclose(central, [0, 100, 1_000_000])
        self.assertTrue(np.all((0 <= low) & (low <= central) & (central <= high)))
        self.assertAlmostEqual(low[1], 101 * np.exp(-.5) - 1)
        self.assertAlmostEqual(high[1], 101 * np.exp(.5) - 1)


class EvaluatedModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle, cls.reference = load_assets(ROOT)
        cls.report = cls.bundle['report']
        cls.examples = json.loads((ROOT / 'tests/prediction_examples.json').read_text())

    def test_selected_model_minimizes_only_cross_validation_mae(self):
        cv = self.report['cross_validation']
        self.assertEqual(cv['method'], 'GroupKFold')
        self.assertEqual(cv['n_splits'], 5)
        self.assertEqual(set(cv['models']), {'mlp', 'random_forest', 'hist_gradient_boosting'})
        for model in cv['models'].values():
            self.assertEqual(len(model['folds']), 5)
            self.assertEqual([f['fold'] for f in model['folds']], [1, 2, 3, 4, 5])
            for metric in ['mae_inr', 'mape_percent', 'r2']:
                values = [row[metric] for row in model['folds']]
                self.assertAlmostEqual(np.mean(values), model['mean'][metric], places=7)
                self.assertAlmostEqual(np.std(values, ddof=1), model['std'][metric], places=7)
        selected = min(cv['models'], key=lambda key: cv['models'][key]['mean']['mae_inr'])
        self.assertEqual(self.report['selected_model']['name'], selected)

    def test_fitting_calibration_test_and_cv_groups_are_disjoint(self):
        with np.load(ROOT / 'artifacts/split_indices.npz') as split:
            sets = [set(split[key]) for key in ['train_group_hash', 'validation_group_hash', 'test_group_hash']]
            self.assertFalse(sets[0] & sets[1] or sets[0] & sets[2] or sets[1] & sets[2])
            groups, folds = split['train_group_hash'], split['cv_fold']
            self.assertEqual(len(folds), len(self.reference))
            self.assertEqual(set(folds), set(range(5)))
            for fold in range(5):
                self.assertFalse(set(groups[folds == fold]) & set(groups[folds != fold]))
        self.assertEqual(self.report['split']['group_overlap'], 0)
        self.assertIn('excluded', self.report['cross_validation']['selection_data'])

    def test_test_coverage_and_price_segment_errors_recompute(self):
        holdout = pd.read_csv(ROOT / 'artifacts/holdout_predictions.csv')
        covered = ((holdout.interval_low_inr <= holdout.selling_price)
                   & (holdout.selling_price <= holdout.interval_high_inr))
        self.assertAlmostEqual(covered.mean(), self.report['conformal']['test_coverage'], places=10)
        self.assertTrue((holdout.interval_low_inr <= holdout.selected_prediction_inr).all())
        self.assertTrue((holdout.selected_prediction_inr <= holdout.interval_high_inr).all())
        self.assertEqual(self.report['conformal']['nominal_coverage'], .8)
        n = self.report['split']['validation_rows']
        self.assertEqual(self.report['conformal']['quantile_rank'], int(np.ceil((n + 1) * .8)))
        masks = {'below_3_lakh': holdout.selling_price < 300_000,
                 '3_to_6_lakh': holdout.selling_price.between(300_000, 600_000, inclusive='left'),
                 '6_to_10_lakh': holdout.selling_price.between(600_000, 1_000_000),
                 'above_10_lakh': holdout.selling_price > 1_000_000}
        self.assertEqual(sum(row['n'] for row in self.report['price_segments']), len(holdout))
        for segment in self.report['price_segments']:
            rows = holdout[masks[segment['segment']]]
            self.assertEqual(len(rows), segment['n'])
            error = np.abs(rows.selling_price - rows.selected_prediction_inr)
            self.assertAlmostEqual(error.mean(), segment['mae_inr'], places=6)
            self.assertAlmostEqual((error / rows.selling_price * 100).mean(), segment['mape_percent'], places=6)
            self.assertAlmostEqual(covered[masks[segment['segment']]].mean(), segment['coverage'], places=10)

    def test_low_confidence_warns_for_small_brand_and_expensive_car(self):
        row = self.examples[0]['inputs']
        peers = self.reference[(self.reference.name == row['name'])
                               & (self.reference.fuel == row['fuel'])
                               & (self.reference.transmission == row['transmission'])].head(5)
        self.assertGreater(len(peers), 0)
        # A rare-brand fixture must still satisfy the service's categorical validation.
        row = {**row, 'owner': peers.iloc[0].owner, 'seller_type': peers.iloc[0].seller_type}
        with patch('service.estimate', return_value=250_000):
            _, notes, _ = predict_vehicle(self.bundle, peers, row)
        self.assertTrue(any('độ tin cậy thấp' in note.lower() and 'hãng' in note.lower() for note in notes))
        with patch('service.estimate', return_value=1_000_001):
            _, notes, _ = predict_vehicle(self.bundle, self.reference, row)
        self.assertTrue(any('độ tin cậy thấp' in note.lower() and '10 lakh' in note for note in notes))
        with patch('service.estimate', return_value=1_000_000):
            _, notes, _ = predict_vehicle(self.bundle, self.reference, row)
        self.assertFalse(any('giá dự đoán trên 10 lakh' in note for note in notes))


class HistoricalRangeTests(unittest.TestCase):
    def test_window_includes_boundary_years_and_fallback_below_five(self):
        peers = pd.DataFrame({'year': [2001, 2002, 2003, 2004, 2005, 2010],
                              'selling_price': [100_000] * 6})
        nearby, fallback = historical_reference(peers, 2003)
        self.assertFalse(fallback)
        self.assertEqual(nearby.year.tolist(), [2001, 2002, 2003, 2004, 2005])
        nearby, fallback = historical_reference(peers, 2010)
        self.assertTrue(fallback)
        pd.testing.assert_frame_equal(nearby, peers)


if __name__ == '__main__':
    unittest.main()
