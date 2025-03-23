"""Unit tests for the pre-commit hook functionality."""
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add hooks directory to path before imports
HOOKS_PATH = str(Path(__file__).parent.parent.parent / '.git' / 'hooks')
if HOOKS_PATH not in sys.path:
    sys.path.insert(0, HOOKS_PATH)

try:
    from pre_commit import PreCommitHook
except ImportError:
    print("Warning: pre-commit hook not found in path")
    PreCommitHook = None

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
