import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from car_model import clean_v3
from service import load_assets, predict_vehicle


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle, cls.reference = load_assets(ROOT)
        cls.samples = json.loads((ROOT / 'tests/prediction_examples.json').read_text())

    def test_saved_model_predictions(self):
        for sample in self.samples:
            price, _, _ = predict_vehicle(self.bundle, self.reference, sample['inputs'])
            self.assertAlmostEqual(price, sample['expected_prediction_inr'], delta=2.0)

    def test_holdout_metrics_match_report(self):
        holdout = pd.read_csv(ROOT / 'artifacts/holdout_predictions.csv')
        report = self.bundle['report']
        self.assertEqual(len(holdout), report['split']['test_rows'])
        self.assertAlmostEqual(mean_absolute_error(holdout.selling_price, holdout.ann_prediction_inr),
                               report['ann']['mae_inr'], delta=1.)
        self.assertAlmostEqual(r2_score(holdout.selling_price, holdout.ann_prediction_inr),
                               report['ann']['r2'], delta=1e-5)
        self.assertLess(report['ann']['mae_inr'], report['median_baseline']['mae_inr'])

    def test_invalid_inputs_rejected(self):
        row = self.samples[0]['inputs']
        for key, value in [('year', 2026), ('km_driven', -10), ('engine_cc', float('nan')),
                           ('name', 'bajaj pulsar 150'), ('seats', 5.5)]:
            with self.subTest(key=key, value=value):
                invalid = {**row, key: value}
                with self.assertRaises(ValueError):
                    predict_vehicle(self.bundle, self.reference, invalid)

    def test_cleaning_rejects_motorcycle_and_truck(self):
        car = dict(name='Maruti Swift Dzire VDI', year=2014, selling_price=450000,
                   km_driven=145500, fuel='Diesel', seller_type='Individual',
                   transmission='Manual', owner='First Owner', engine='1248 CC',
                   max_power='74 bhp', seats=5.)
        rows = [car, car.copy(), {**car, 'name': 'Bajaj Pulsar 150', 'seats': 2.},
                {**car, 'name': 'Mahindra Bolero Pik-Up FB 1.7T', 'seats': 2.}]
        cleaned, audit = clean_v3(pd.DataFrame(rows))
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(audit['excluded_non_passenger_or_unverified_rows'], 2)
        self.assertEqual(audit['duplicate_rows_removed'], 1)

    def test_artifact_integrity_and_split(self):
        manifest = json.loads((ROOT / 'artifacts/manifest.json').read_text())
        for name, expected in manifest['sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT / 'artifacts' / name).read_bytes()).hexdigest(), expected)
        with np.load(ROOT / 'artifacts/split_indices.npz') as split:
            arrays = [split[key] for key in ['train', 'validation', 'test']]
        self.assertEqual(len(set(np.concatenate(arrays))), sum(map(len, arrays)))
        self.assertEqual(len(self.reference), self.bundle['report']['split']['train_rows'])


class WebTests(unittest.TestCase):
    def test_input_prediction_and_brand_switch(self):
        at = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=45).run()
        self.assertFalse(at.exception)
        self.assertFalse(at.metric)
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.metric), 1)
        self.assertTrue(at.metric[0].value.startswith('₹'))
        at.selectbox[0].select('honda').run()
        self.assertFalse(at.exception)
        at.button[0].click().run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.metric), 1)


if __name__ == '__main__':
    unittest.main()
