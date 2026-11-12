"""Behavior checks for saved results and optional browser number fields."""
from pathlib import Path
import unittest
from streamlit.testing.v1 import AppTest
ROOT = Path(__file__).resolve().parents[1]
class PremiumUITests(unittest.TestCase):
    def test_result_survives_rerun_and_can_be_cleared(self):
        app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=45).run()
        app.button[0].click().run()
        price = app.metric[0].value
        app.run()
        self.assertEqual(app.metric[0].value, price)
        next(b for b in app.button if 'Dự đoán lại' in b.label).click().run()
        self.assertFalse(app.metric)
        self.assertFalse(app.exception)
    def test_empty_numeric_field_recovers_default_without_crashing(self):
        app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=45).run()
        app.number_input[0].set_value(None)
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertIsNotNone(app.number_input[0].value)
        self.assertTrue(app.metric)
if __name__ == '__main__':
    unittest.main()
