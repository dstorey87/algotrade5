"""Unit tests for the pre-commit hook functionality."""
import sys
from pathlib import Path

# Add hooks directory to path before imports
hooks_path = str(Path(__file__).parent.parent.parent / '.git' / 'hooks')
if hooks_path not in sys.path:
    sys.path.insert(0, hooks_path)

import unittest
from unittest.mock import patch, MagicMock
from pre_commit import PreCommitHook

class TestPreCommitHook(unittest.TestCase):
    """Test suite for the PreCommitHook class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.hook = PreCommitHook()

    def test_code_quality_checks(self):
        """Test that code quality checks run correctly."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            self.assertTrue(self.hook.run_code_checks('test.py'))

    def test_documentation_updates(self):
        """Test that documentation files are updated correctly."""
        self.hook.changes = [{
            'type': 'frontend',
            'component': 'Dashboard',
            'description': 'Added new feature'
        }]

        with patch('builtins.open', MagicMock()):
            self.hook.update_frontend_plan(['frontend/test.tsx'])
            self.hook.update_architecture_doc(['src/api/test.py'])
            self.hook.update_journal(['frontend/test.tsx'])
            self.hook.update_copilot_session(['frontend/test.tsx'])

if __name__ == '__main__':
    unittest.main()
