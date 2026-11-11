import hashlib
import unittest
from pathlib import Path

import pandas as pd
from PIL import Image

from photo_catalog import ROOT, load_catalog, reference_car, photo_for_car, public_photo_url


class PhotoCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()
        cls.reference = pd.read_csv(ROOT / 'artifacts/reference.csv')

    def test_each_photo_matches_its_named_training_record(self):
        expected = {
            'dzire': ('maruti swift dzire vdi', 2013),
            'city': ('honda city i vtec vx', 2014),
            'eon': ('hyundai eon era plus', 2014),
            'etios': ('toyota etios gd', 2012),
            'figo': ('ford figo diesel titanium', 2011),
            'kwid': ('renault kwid rxt', 2015),
        }
        self.assertEqual(set(expected), {p['id'] for p in self.catalog['photos']})
        for photo in self.catalog['photos']:
            with self.subTest(photo=photo['id']):
                car = reference_car(self.reference, photo)
                self.assertEqual((car['name'], int(car['year'])), expected[photo['id']])
                self.assertEqual(car['selling_price'], photo['dataset_price'])
                self.assertEqual(photo_for_car(car['name'], car['year'])['id'], photo['id'])

    def test_local_real_photos_have_license_and_verified_bytes(self):
        for photo in self.catalog['photos']:
            path = ROOT / 'static/cars' / photo['filename']
            with self.subTest(photo=photo['id']):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), photo['sha256'])
                with Image.open(path) as image:
                    self.assertEqual(image.format, 'WEBP')
                    self.assertEqual(image.size, (photo['width'], photo['height']))
                for key in ['author', 'license', 'license_url', 'source_page', 'match_note']:
                    self.assertTrue(photo[key])
                self.assertTrue(photo['source_page'].startswith('https://commons.wikimedia.org/wiki/File:'))
                self.assertEqual(public_photo_url(photo), '/app/static/cars/' + photo['filename'])

    def test_unknown_model_or_generation_never_gets_a_random_photo(self):
        for name, year in [('bmw 320d', 2015), ('maruti swift vdi', 2013),
                           ('toyota etios liva gd', 2012), ('honda city i vtec vx', 2010),
                           ('renault kwid rxt', 2020)]:
            self.assertIsNone(photo_for_car(name, year), (name, year))


if __name__ == '__main__':
    unittest.main()
