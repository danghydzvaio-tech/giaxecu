"""The Kaggle archive must be complete, including archives larger than 10 MiB."""
import hashlib
import io
import unittest
import zipfile
from unittest.mock import MagicMock, patch

import train


class SourceDownloadTests(unittest.TestCase):
    def response(self, archive, length):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = archive
        response.headers = {'Content-Length': str(length)}
        return response

    def test_archive_larger_than_old_limit_is_not_truncated(self):
        payload = b'name,year\nSynthetic unit-test fixture,2020\n'
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED) as package:
            package.writestr(train.SOURCE_FILE, payload)
            package.writestr('padding.bin', b'0' * (10 * 1024 * 1024 + 1))
        archive = output.getvalue()
        response = self.response(archive, len(archive))
        with patch('train.urlopen', return_value=response), patch('train.SOURCE_SHA256', hashlib.sha256(payload).hexdigest()):
            self.assertEqual(train.read_source(), payload)

    def test_truncated_response_has_a_clear_error(self):
        response = self.response(b'incomplete', 100)
        with patch('train.urlopen', return_value=response):
            with self.assertRaisesRegex(ValueError, 'chưa đầy đủ'):
                train.read_source()


if __name__ == '__main__':
    unittest.main()
