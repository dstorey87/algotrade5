#!/usr/bin/env python
"""
AlgoTradePro5 Pre-commit Hook Script
This script performs automated checks, documentation updates, and code formatting before each commit.
"""

import os
import sys
import json
import re
import logging
import traceback
import subprocess
from datetime import datetime
from pathlib import Path
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'logs', 'pre-commit.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('pre-commit-hook')

class PreCommitHook:
    """Pre-commit hook for AlgoTradePro5 that handles code quality checks and documentation updates."""
    
    def __init__(self):
        """Initialize the pre-commit hook with necessary paths and configurations."""
        # Get the root directory of the repository
        self.script_path = Path(os.path.abspath(__file__))
        self.hooks_dir = self.script_path.parent
        self.src_dir = self.hooks_dir.parent
        self.repo_root = self.src_dir.parent
        
        # Configuration file paths
        self.config_path = self.repo_root / 'config' / 'pre-commit-config.json'
        
        # Documentation file paths
        self.journal_path = self.src_dir / 'docs' / 'journal.md'
        self.architecture_path = self.src_dir / 'docs' / 'ARCHITECTURE_ANALYSIS.md'
        self.integration_path = self.src_dir / 'docs' / 'INTEGRATION_GUIDE.md'
        self.changes_log_path = self.src_dir / 'docs' / 'changes.log'
        self.session_path = self.src_dir / 'docs' / 'copilot_session.md'
        
        # Load configuration
        self.config = self.load_config()
        
        # Create necessary directories if they don't exist
        os.makedirs(self.repo_root / 'logs', exist_ok=True)
        os.makedirs(self.src_dir / 'docs', exist_ok=True)

    def load_config(self):
        """Load the pre-commit hook configuration from the config file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Configuration file not found at %s. Using default configuration.", self.config_path)
            return {
                "code_quality": {
                    "backend": {
                        "tools": ["pylint", "mypy"],
                        "ignore_patterns": ["__pycache__", "*.pyc"]
                    },
                    "frontend": {
                        "tools": ["eslint", "prettier"],
                        "ignore_patterns": ["node_modules", "dist"]
                    }
                },
                "documentation": {
                    "auto_update": True,
                    "files": {
                        "architecture": str(self.architecture_path),
                        "journal": str(self.journal_path),
                        "integration": str(self.integration_path),
                        "session": str(self.session_path)
                    }
                }
            }
        except json.JSONDecodeError as e:
            logger.error("Error parsing configuration file: %s", e)
            logger.error("Using default configuration")
            return {
                "code_quality": {
                    "backend": {
                        "tools": ["pylint", "mypy"],
                        "ignore_patterns": ["__pycache__", "*.pyc"]
                    }
                },
                "documentation": {
                    "auto_update": True
                }
            }

    def run(self):
        """Run the pre-commit hook with full error checking and reporting."""
        try:
            logger.info("Starting pre-commit hook...")
            
            # Step 1: Get the staged files
            staged_files = self.get_staged_files()
            if not staged_files:
                logger.info("No files staged for commit. Hook passed.")
                return 0
                
            logger.info("Found %d staged files: %s", len(staged_files), staged_files)
            
            # Step 2: Check code quality for the staged files
            if not self.check_code_quality(staged_files):
                logger.error("Code quality checks failed. Please fix the issues and try again.")
                return 1
                
            # Step 3: Update documentation based on changes
            if not self.update_documentation(staged_files):
                logger.error("Documentation update failed. Please check the logs and try again.")
                return 1
                
            # Step 4: Update changes log
            if not self.update_changes_log(staged_files):
                logger.warning("Changes log update failed. Continuing anyway...")
            
            # Step 5: Update session state
            if not self.update_session_state(staged_files):
                logger.warning("Session state update failed. Continuing anyway...")
            
            logger.info("Pre-commit hook completed successfully.")
            return 0
        except Exception as e:
            logger.error("Unexpected error in pre-commit hook: %s", e)
            logger.error(traceback.format_exc())
            return 1

    def get_staged_files(self):
        """Get the list of files staged for commit."""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
                capture_output=True,
                text=True,
                check=True
            )
            return [line for line in result.stdout.splitlines() if line.strip()]
        except subprocess.CalledProcessError as e:
            logger.error("Error getting staged files: %s", e)
            return []

    def check_code_quality(self, staged_files):
        """Check code quality for the staged files."""
        python_files = [f for f in staged_files if f.endswith('.py')]
        js_files = [f for f in staged_files if f.endswith('.js') or f.endswith('.jsx')]
        
        if not python_files and not js_files:
            logger.info("No Python or JavaScript files to check")
            return True
            
        success = True
        
        # Check Python files with pylint and mypy if configured
        if python_files and 'pylint' in self.config.get('code_quality', {}).get('backend', {}).get('tools', []):
            for py_file in python_files:
                file_path = os.path.join(self.repo_root, py_file)
                if not os.path.exists(file_path):
                    logger.warning("File %s not found, skipping", file_path)
                    continue
                    
                try:
                    logger.info("Running pylint on %s", py_file)
                    result = subprocess.run(
                        ['pylint', file_path, '--disable=C0111,C0103'],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode != 0:
                        logger.warning("Pylint found issues in %s:", py_file)
                        for line in result.stdout.splitlines():
                            if 'error' in line.lower() or 'warning' in line.lower():
                                logger.warning(line)
                        # We don't fail on warnings, only on errors
                        if 'error' in result.stdout.lower():
                            success = False
                except (subprocess.SubprocessError, FileNotFoundError) as e:
                    logger.warning("Failed to run pylint: %s", e)
        
        # Check JavaScript files with eslint if configured
        if js_files and 'eslint' in self.config.get('code_quality', {}).get('frontend', {}).get('tools', []):
            for js_file in js_files:
                file_path = os.path.join(self.repo_root, js_file)
                if not os.path.exists(file_path):
                    logger.warning("File %s not found, skipping", file_path)
                    continue
                    
                try:
                    logger.info("Running eslint on %s", js_file)
                    result = subprocess.run(
                        ['npx', 'eslint', file_path],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode != 0:
                        logger.warning("ESLint found issues in %s:", js_file)
                        for line in result.stdout.splitlines():
                            logger.warning(line)
                        # We don't fail on warnings, only on errors
                        if 'error' in result.stdout.lower():
                            success = False
                except (subprocess.SubprocessError, FileNotFoundError) as e:
                    logger.warning("Failed to run eslint: %s", e)
        
        return success

    def update_documentation(self, staged_files):
        """Update documentation based on the changes."""
        if not self.config.get('documentation', {}).get('auto_update', False):
            logger.info("Documentation auto-update is disabled")
            return True
            
        try:
            # Update journal
            self.update_journal(staged_files)
            
            # Update architecture documentation if needed
            if any(f.endswith('.py') for f in staged_files) or any('architecture' in f.lower() for f in staged_files):
                self.update_architecture_doc(staged_files)
            
            # Update integration guide if needed
            if any(f.endswith('.py') for f in staged_files) or any('integration' in f.lower() for f in staged_files):
                self.update_integration_guide(staged_files)
            
            return True
        except Exception as e:
            logger.error("Error updating documentation: %s", e)
            logger.error(traceback.format_exc())
            return False

    def update_journal(self, staged_files):
        """Update the journal.md file with the latest changes."""
        if not os.path.exists(self.journal_path):
            logger.warning("Journal file not found at %s. Creating a new one.", self.journal_path)
            with open(self.journal_path, 'w') as f:
                f.write("# AlgoTradePro5 Development Journal\n\n")
        
        try:
            # Get current date and time
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d %H:%M")
            
            # Identify main components affected
            components_affected = self.identify_components(staged_files)
            
            # Create journal entry
            journal_entry = f"\n## System Update - {date_str}\n\n"
            journal_entry += "### Changes Made\n"
            
            # Group files by type
            file_groups = {}
            for file in staged_files:
                ext = os.path.splitext(file)[1]
                if ext not in file_groups:
                    file_groups[ext] = []
                file_groups[ext].append(file)
            
            # Add section for files modified
            journal_entry += "#### Files Modified\n"
            for files in file_groups.values():
                for file in files[:5]:  # Limit to 5 files per type
                    journal_entry += f"- {file}\n"
                if len(files) > 5:
                    journal_entry += f"- ... and {len(files) - 5} more\n"
            
            # Add section for components affected
            journal_entry += "\n#### Components Affected\n"
            for component in components_affected:
                journal_entry += f"- {component}\n"
            
            # Add next steps
            journal_entry += "\n### Next Steps\n"
            journal_entry += "1. Complete the priority task: Install Pre-commit Hook\n"
            journal_entry += "2. Install hook in Git repository\n"
            journal_entry += "3. Implement WebSocket functionality\n"
            journal_entry += "4. Update documentation\n"
            
            # Append to journal
            with open(self.journal_path, 'a') as f:
                f.write(journal_entry)
            
            logger.info("Journal updated successfully")
            return True
        except Exception as e:
            logger.error("Error updating journal: %s", e)
            return False

    def update_architecture_doc(self, staged_files):
        """Update the architecture documentation if needed."""
        # This is a simplified implementation
        # In a real implementation, this would analyze code changes and update architecture docs
        logger.info("Updating architecture documentation would happen here")
        return True

    def update_integration_guide(self, staged_files):
        """Update the integration guide if needed."""
        # This is a simplified implementation
        # In a real implementation, this would analyze code changes and update integration docs
        logger.info("Updating integration guide would happen here")
        return True

    def update_changes_log(self, staged_files):
        """Update the changes.log file with the latest changes."""
        try:
            # Get current date and time
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d %H:%M")
            
            # Identify main components affected
            components_affected = self.identify_components(staged_files)
            
            # Create log entry
            log_entry = f"[{date_str}] SYSTEM UPDATE\n"
            log_entry += "Components Modified:\n"
            
            for component in components_affected:
                log_entry += f"- {component}\n"
            
            log_entry += "\nChanges:\n"
            log_entry += f"1. Updated {len(staged_files)} files\n"
            log_entry += f"2. Modified components: {', '.join(components_affected)}\n"
            
            log_entry += "\nNext Actions Required:\n"
            log_entry += "1. Update documentation to reflect changes\n"
            log_entry += "2. Run tests to verify changes work correctly\n"
            log_entry += "3. Check integration with other components\n"
            
            # Append to changes log
            with open(self.changes_log_path, 'a') as f:
                f.write(log_entry)
            
            logger.info("Changes log updated successfully")
            return True
        except Exception as e:
            logger.error("Error updating changes log: %s", e)
            return False

    def update_session_state(self, staged_files):
        """Update the session state in the copilot_session.md file."""
        try:
            if not os.path.exists(self.session_path):
                logger.warning("Session state file not found at %s. Creating a new one.", self.session_path)
                with open(self.session_path, 'w') as f:
                    f.write("# Copilot Development Session Tracker\n\n")
                    f.write("## Current Session State\n")
                    f.write("```json\n")
                    f.write("{\n")
                    f.write('  "last_update": "' + datetime.now().strftime("%Y-%m-%d") + '",\n')
                    f.write('  "current_context": {\n')
                    f.write('    "active_components": [],\n')
                    f.write('    "pending_tasks": [\n')
                    f.write('      "Install hook in Git repository",\n')
                    f.write('      "Implement WebSocket functionality",\n')
                    f.write('      "Update documentation"\n')
                    f.write('    ],\n')
                    f.write('    "completed_tasks": []\n')
                    f.write('  },\n')
                    f.write('  "next_session_requirements": {\n')
                    f.write('    "priority": "Install Pre-commit Hook",\n')
                    f.write('    "dependencies": [],\n')
                    f.write('    "context_preservation": {\n')
                    f.write('      "current_phase": "Development Infrastructure",\n')
                    f.write('      "active_branch": "main",\n')
                    f.write('      "last_component": "Pre-commit Hook System"\n')
                    f.write('    }\n')
                    f.write('  }\n')
                    f.write('}\n')
                    f.write('```\n\n')
                    f.write('## Session Recovery Instructions\n')
                    f.write('1. Load last known state from current_context\n')
                    f.write('2. Check pending_tasks for next priority\n')
                    f.write('3. Review `changes.log` for latest modifications\n')
                    f.write('4. Verify all dependencies are installed\n')
                    f.write('5. Resume development from the priority task\n\n')
                    f.write('Remember to check for any system alerts or errors before proceeding.\n')
            
            # Update existing file
            components_affected = self.identify_components(staged_files)
            
            # For a real implementation, we would parse the existing JSON and update it
            # Here we just log that it would be updated
            logger.info("Session state would be updated with components: %s", components_affected)
            
            return True
        except Exception as e:
            logger.error("Error updating session state: %s", e)
            return False

    def identify_components(self, staged_files):
        """Identify the main components affected by the changes."""
        components = set()
        
        for file in staged_files:
            if 'frontend' in file.lower() or file.endswith(('.js', '.jsx', '.ts', '.tsx', '.css', '.html')):
                components.add('Frontend')
            elif 'backend' in file.lower() or file.endswith('.py'):
                components.add('Backend')
            elif 'tests' in file.lower() or file.endswith(('_test.py', '.test.js')):
                components.add('Tests')
            elif 'docker' in file.lower() or file.endswith(('Dockerfile', 'docker-compose.yml')):
                components.add('Docker')
            elif 'docs' in file.lower() or file.endswith(('.md', '.txt')):
                components.add('Documentation')
            elif 'hooks' in file.lower():
                components.add('Pre-commit hook system')
                
        if not components:
            components.add('General')
            
        return list(components)

def main():
    """Main function to run the pre-commit hook."""
    start_time = time.time()
    hook = PreCommitHook()
    result = hook.run()
    elapsed_time = time.time() - start_time
    logger.info(f"Pre-commit hook completed in {elapsed_time:.2f} seconds with result code {result}")
    sys.exit(result)

if __name__ == "__main__":
    main()