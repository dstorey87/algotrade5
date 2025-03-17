#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pre-commit hook for AlgoTradePro5.

This module implements a pre-commit hook that:
1. Logs changes made to files
2. Updates documentation based on changes
3. Maintains state between Copilot sessions
4. Tracks pending tasks to pick up where left off
5. Updates journal.md with timestamps
"""

import os
import sys
import json
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/pre_commit.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("pre_commit_hook")

class PreCommitHook:
    """Main pre-commit hook handler for AlgoTradePro5."""
    
    def __init__(self, root_dir: str = None):
        """Initialize the pre-commit hook system.
        
        Args:
            root_dir: Root directory of the project
        """
        self.root_dir = root_dir or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.session_file = os.path.join(self.root_dir, "src", "docs", "copilot_session.md")
        self.changes_log = os.path.join(self.root_dir, "src", "docs", "changes.log")
        self.journal_file = os.path.join(self.root_dir, "src", "docs", "journal.md")
        self.arch_file = os.path.join(self.root_dir, "src", "docs", "ARCHITECTURE_ANALYSIS.md")
        self.frontend_plan = os.path.join(self.root_dir, "src", "docs", "FRONTEND_DEV_PLAN.md")
        self.config_file = os.path.join(self.root_dir, "config", "pre-commit-config.json")
        
        # Create log directory if it doesn't exist
        os.makedirs(os.path.join(self.root_dir, "logs"), exist_ok=True)
        
        # Load or create configuration
        self.config = self._load_or_create_config()
        
        # Load current session state
        self.session_state = self._load_session_state()

    def _load_or_create_config(self) -> Dict[str, Any]:
        """Load configuration or create it if it doesn't exist."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Error decoding config file {self.config_file}")
                return self._create_default_config()
        else:
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create a default configuration."""
        default_config = {
            "code_quality": {
                "frontend": {
                    "tools": ["eslint", "prettier"],
                    "ignore_patterns": ["node_modules", "dist"]
                },
                "backend": {
                    "tools": ["pylint", "mypy"],
                    "ignore_patterns": ["__pycache__", "*.pyc"]
                }
            },
            "documentation": {
                "auto_update": True,
                "files": {
                    "frontend_plan": self.frontend_plan,
                    "architecture": self.arch_file,
                    "journal": self.journal_file,
                    "copilot_session": self.session_file
                }
            },
            "pending_tasks": [
                "Implement real-time trading dashboard",
                "Complete documentation system"
            ],
            "next_priority": "Documentation System",
            "dependencies": []
        }
        
        # Ensure config directory exists
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        # Save default config
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def _load_session_state(self) -> Dict[str, Any]:
        """Load the current session state from the session file."""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    content = f.read()
                    # Extract JSON from markdown code block
                    import re
                    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                    if json_match:
                        try:
                            return json.loads(json_match.group(1))
                        except json.JSONDecodeError:
                            logger.error("Failed to parse session JSON")
                            return self._create_default_session()
                    else:
                        return self._create_default_session()
            except Exception as e:
                logger.error(f"Error loading session file: {e}")
                return self._create_default_session()
        else:
            return self._create_default_session()
    
    def _create_default_session(self) -> Dict[str, Any]:
        """Create a default session state."""
        return {
            "last_update": datetime.datetime.now().strftime("%Y-%m-%d"),
            "current_context": {
                "active_components": [],
                "pending_tasks": self.config.get("pending_tasks", []),
                "completed_tasks": []
            },
            "next_session_requirements": {
                "priority": self.config.get("next_priority", ""),
                "dependencies": self.config.get("dependencies", []),
                "context_preservation": {
                    "current_phase": "",
                    "active_branch": "",
                    "last_component": ""
                }
            }
        }
    
    def update_session_state(self, 
                             active_components: Optional[List[str]] = None,
                             pending_tasks: Optional[List[str]] = None,
                             completed_tasks: Optional[List[str]] = None,
                             priority: Optional[str] = None,
                             dependencies: Optional[List[str]] = None,
                             current_phase: Optional[str] = None,
                             active_branch: Optional[str] = None,
                             last_component: Optional[str] = None) -> None:
        """Update the session state with new information.
        
        Args:
            active_components: List of components being worked on
            pending_tasks: List of tasks to be completed
            completed_tasks: List of completed tasks
            priority: Next priority task
            dependencies: List of dependencies for the next priority
            current_phase: Current development phase
            active_branch: Active git branch
            last_component: Last component being worked on
        """
        # Update the session state
        if active_components is not None:
            self.session_state["current_context"]["active_components"] = active_components
        
        if pending_tasks is not None:
            self.session_state["current_context"]["pending_tasks"] = pending_tasks
        
        if completed_tasks is not None:
            self.session_state["current_context"]["completed_tasks"] = completed_tasks
        
        if priority is not None:
            self.session_state["next_session_requirements"]["priority"] = priority
        
        if dependencies is not None:
            self.session_state["next_session_requirements"]["dependencies"] = dependencies
        
        if current_phase is not None:
            self.session_state["next_session_requirements"]["context_preservation"]["current_phase"] = current_phase
        
        if active_branch is not None:
            self.session_state["next_session_requirements"]["context_preservation"]["active_branch"] = active_branch
        
        if last_component is not None:
            self.session_state["next_session_requirements"]["context_preservation"]["last_component"] = last_component
        
        # Update timestamp
        self.session_state["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Save session state
        self._save_session_state()
    
    def _save_session_state(self) -> None:
        """Save the current session state to the session file."""
        os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
        
        try:
            # Format as markdown with JSON code block
            content = f"""# Copilot Development Session Tracker

## Current Session State
```json
{json.dumps(self.session_state, indent=2)}
```

## Session Recovery Instructions
1. Load last known state from current_context
2. Check pending_tasks for next priority
3. Verify completed_tasks for context
4. Continue development from last_component

## Branch Management
- Current: {self.session_state["next_session_requirements"]["context_preservation"]["active_branch"] or "N/A"}
- Last Commit: {self.session_state["next_session_requirements"]["context_preservation"]["last_component"] or "N/A"}
- Next Priority: {self.session_state["next_session_requirements"]["priority"] or "N/A"}
"""
            
            with open(self.session_file, 'w') as f:
                f.write(content)
            
            logger.info(f"Updated session state in {self.session_file}")
        except Exception as e:
            logger.error(f"Error saving session state: {e}")
    
    def log_changes(self, components_modified: List[str], changes: List[str], 
                    next_actions: List[str]) -> None:
        """Log changes to the changes log file.
        
        Args:
            components_modified: List of components that were modified
            changes: List of changes made
            next_actions: List of next actions to be taken
        """
        os.makedirs(os.path.dirname(self.changes_log), exist_ok=True)
        
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Format components as a list
            components_str = "\n".join([f"- {component}" for component in components_modified])
            
            # Format changes as a numbered list
            changes_str = "\n".join([f"{i+1}. {change}" for i, change in enumerate(changes)])
            
            # Format next actions as a numbered list
            next_actions_str = "\n".join([f"{i+1}. {action}" for i, action in enumerate(next_actions)])
            
            # Create entry
            entry = f"""
[{timestamp}] SYSTEM UPDATE
Components Modified:
{components_str}

Changes:
{changes_str}

Next Actions Required:
{next_actions_str}
"""
            
            # Append to the changes log
            with open(self.changes_log, 'a') as f:
                f.write(entry)
            
            logger.info(f"Logged changes to {self.changes_log}")
        except Exception as e:
            logger.error(f"Error logging changes: {e}")
    
    def update_journal(self, entry_title: str, entry_content: str) -> None:
        """Update the development journal with a new entry.
        
        Args:
            entry_title: Title of the entry
            entry_content: Content of the entry
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Create entry
            entry = f"""
## {entry_title} - {timestamp}

{entry_content}
"""
            
            # Append to the journal
            with open(self.journal_file, 'a') as f:
                f.write(entry)
            
            logger.info(f"Updated journal in {self.journal_file}")
        except Exception as e:
            logger.error(f"Error updating journal: {e}")
    
    def update_frontend_plan(self, section: str, content: str) -> None:
        """Update the frontend development plan.
        
        Args:
            section: Section to update
            content: Content to update the section with
        """
        try:
            if os.path.exists(self.frontend_plan):
                with open(self.frontend_plan, 'r') as f:
                    frontend_content = f.read()
                
                # Find the section in the frontend plan
                import re
                section_pattern = re.compile(f"## {section}[^#]*", re.DOTALL)
                section_match = section_pattern.search(frontend_content)
                
                if section_match:
                    # Replace the section with the new content
                    updated_content = f"## {section}\n{content}\n"
                    frontend_content = frontend_content.replace(section_match.group(0), updated_content)
                else:
                    # Add the section to the end of the file
                    frontend_content += f"\n\n## {section}\n{content}\n"
            else:
                # Create a new frontend plan
                frontend_content = f"# Frontend Development Plan\n\n## {section}\n{content}\n"
            
            # Save the updated frontend plan
            os.makedirs(os.path.dirname(self.frontend_plan), exist_ok=True)
            with open(self.frontend_plan, 'w') as f:
                f.write(frontend_content)
            
            logger.info(f"Updated frontend plan in {self.frontend_plan}")
        except Exception as e:
            logger.error(f"Error updating frontend plan: {e}")
    
    def update_architecture(self, section: str, content: str) -> None:
        """Update the architecture analysis document.
        
        Args:
            section: Section to update
            content: Content to update the section with
        """
        try:
            if os.path.exists(self.arch_file):
                with open(self.arch_file, 'r') as f:
                    arch_content = f.read()
                
                # Find the section in the architecture file
                import re
                section_pattern = re.compile(f"## {section}[^#]*", re.DOTALL)
                section_match = section_pattern.search(arch_content)
                
                if section_match:
                    # Replace the section with the new content
                    updated_content = f"## {section}\n\n{content}\n\n"
                    arch_content = arch_content.replace(section_match.group(0), updated_content)
                else:
                    # Add the section to the end of the file
                    arch_content += f"\n\n## {section}\n\n{content}\n\n"
            else:
                # Create a new architecture file
                arch_content = f"# AlgoTradPro5 Architecture Analysis\n\n## {section}\n\n{content}\n\n"
            
            # Save the updated architecture file
            os.makedirs(os.path.dirname(self.arch_file), exist_ok=True)
            with open(self.arch_file, 'w') as f:
                f.write(arch_content)
            
            logger.info(f"Updated architecture analysis in {self.arch_file}")
        except Exception as e:
            logger.error(f"Error updating architecture analysis: {e}")
    
    def run_pre_commit_hook(self) -> bool:
        """Run the pre-commit hook.
        
        Returns:
            bool: True if the hook succeeded, False otherwise
        """
        logger.info("Running pre-commit hook")
        
        try:
            # 1. Update session state
            self._save_session_state()
            
            # 2. Log the operation
            self.log_changes(
                components_modified=["Pre-commit hook system"],
                changes=["Ran pre-commit hook"],
                next_actions=["Verify documentation updates", "Check session state"]
            )
            
            logger.info("Pre-commit hook completed successfully")
            return True
        except Exception as e:
            logger.error(f"Pre-commit hook failed: {e}")
            return False


def main():
    """Main entry point for the pre-commit hook."""
    try:
        hook = PreCommitHook()
        success = hook.run_pre_commit_hook()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Pre-commit hook failed with exception: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()