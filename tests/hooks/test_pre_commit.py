import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path

# Add hooks directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / '.git' / 'hooks'))
from pre_commit import PreCommitHook

class TestPreCommitHook(unittest.TestCase):
    def setUp(self):
        self.hook = PreCommitHook()
        
    def test_code_quality_checks(self):
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            self.assertTrue(self.hook.run_code_quality_checks())
            
    def test_documentation_updates(self):
        self.hook.changes = [{
            'type': 'frontend',
            'component': 'Dashboard',
            'description': 'Added new feature'
        }]
        
        with patch('builtins.open', MagicMock()):
            self.hook.update_frontend_plan()
            self.hook.update_architecture_docs()
            self.hook.update_journal()
            self.hook.update_copilot_session()

if __name__ == '__main__':
    unittest.main()
