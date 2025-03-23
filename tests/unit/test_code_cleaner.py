import unittest
from unittest.mock import MagicMock, patch

import code_cleaner


class TestCodeCleaner(unittest.TestCase):
    @patch('code_cleaner.vulture')
    def test_unused_code_detection(self, mock_vulture):
        mock_vulture.return_value = []
        result = code_cleaner.check_unused_code()
        self.assertEqual(result, [])

    @patch('code_cleaner.check_circular_imports')
    def test_circular_import_detection(self, mock_check):
        mock_check.side_effect = OSError("Filename or extension too long")
        with self.assertRaises(OSError):
            code_cleaner.check_circular_imports()

if __name__ == '__main__':
    unittest.main()