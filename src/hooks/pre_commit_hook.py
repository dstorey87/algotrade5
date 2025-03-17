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
6. Updates architecture plans in ARCHITECTURE_ANALYSIS.md
7. Creates a summary of next actions for Copilot
"""

import os
import sys
import json
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import re
import subprocess

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
        self.next_actions_file = os.path.join(self.root_dir, "src", "docs", "COPILOT_NEXT_ACTIONS.md")
        
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
            # Ensure the journal file exists
            os.makedirs(os.path.dirname(self.journal_file), exist_ok=True)
            if not os.path.exists(self.journal_file):
                with open(self.journal_file, 'w') as f:
                    f.write("# AlgoTradePro5 Development Journal\n\n")
            
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
            # Ensure the architecture file directory exists
            os.makedirs(os.path.dirname(self.arch_file), exist_ok=True)
            
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
            with open(self.arch_file, 'w') as f:
                f.write(arch_content)
            
            logger.info(f"Updated architecture analysis in {self.arch_file}")
        except Exception as e:
            logger.error(f"Error updating architecture analysis: {e}")
    
    def _get_git_changes(self) -> Tuple[List[str], List[str]]:
        """Get the files changed in the current git staged changes.
        
        Returns:
            Tuple containing:
                - List of components modified based on file paths
                - List of change descriptions
        """
        try:
            # Get the files that have been staged for commit
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Extract the file paths
            file_paths = result.stdout.strip().split('\n')
            file_paths = [f for f in file_paths if f]  # Remove empty strings
            
            # Determine the components modified based on file paths
            components_modified = []
            for file_path in file_paths:
                if file_path.startswith("src/hooks"):
                    if "Pre-commit hook system" not in components_modified:
                        components_modified.append("Pre-commit hook system")
                elif file_path.startswith("frontend"):
                    if "Frontend" not in components_modified:
                        components_modified.append("Frontend")
                elif file_path.startswith("src/backend"):
                    if "Backend" not in components_modified:
                        components_modified.append("Backend")
                elif file_path.startswith("src/docs"):
                    if "Documentation" not in components_modified:
                        components_modified.append("Documentation")
                elif file_path.startswith("src/ai"):
                    if "AI Models" not in components_modified:
                        components_modified.append("AI Models")
                elif file_path.startswith("src/quantum"):
                    if "Quantum Computing" not in components_modified:
                        components_modified.append("Quantum Computing")
                elif file_path.startswith("src/tests") or file_path.startswith("tests"):
                    if "Tests" not in components_modified:
                        components_modified.append("Tests")
            
            # Get more detailed changes
            result = subprocess.run(
                ["git", "diff", "--cached", "--stat"],
                capture_output=True,
                text=True,
                check=True
            )
            
            changes = [
                f"Updated {len(file_paths)} files",
                "Modified components: " + ", ".join(components_modified)
            ]
            
            return components_modified, changes
        except subprocess.SubprocessError as e:
            logger.error(f"Error getting git changes: {e}")
            return ["Unknown"], ["Unknown changes"]
    
    def _get_active_branch(self) -> str:
        """Get the name of the active git branch.
        
        Returns:
            str: Name of the active branch
        """
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            
            return result.stdout.strip()
        except subprocess.SubprocessError as e:
            logger.error(f"Error getting active branch: {e}")
            return "unknown-branch"
    
    def create_next_actions_summary(self) -> None:
        """Create a summary of what Copilot needs to do next.
        
        This is critical for when Copilot sessions need to be reset.
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.next_actions_file), exist_ok=True)
            
            # Get the current priority task
            priority_task = self.session_state["next_session_requirements"]["priority"]
            
            # Get the pending tasks
            pending_tasks = self.session_state["current_context"]["pending_tasks"]
            
            # Get the active components
            active_components = self.session_state["current_context"]["active_components"]
            
            # Get the last component worked on
            last_component = self.session_state["next_session_requirements"]["context_preservation"]["last_component"]
            
            # Get the current phase
            current_phase = self.session_state["next_session_requirements"]["context_preservation"]["current_phase"]
            
            # Create the summary content
            content = f"""# Copilot Next Actions Summary

## CRITICAL: Resume Point for Copilot After Reset

### Current State Summary
- **Current Phase**: {current_phase or "N/A"}
- **Active Branch**: {self._get_active_branch()}
- **Last Component Modified**: {last_component or "N/A"}
- **Active Components**: {', '.join(active_components) if active_components else "N/A"}

### Priority Task
{priority_task or "No priority task set"}

### Pending Tasks
{os.linesep.join([f"- {task}" for task in pending_tasks]) if pending_tasks else "No pending tasks"}

### Current Context
The development is currently focused on {current_phase or "development"} with emphasis on {last_component or "the system"}. 
The next priority is to work on {priority_task or "the next task in the pending list"}.

### Technical Dependencies
{os.linesep.join([f"- {dep}" for dep in self.session_state["next_session_requirements"]["dependencies"]]) if self.session_state["next_session_requirements"]["dependencies"] else "No specific dependencies"}

### Resumption Instructions
1. Review the `ARCHITECTURE_ANALYSIS.md` file for system design context
2. Check `journal.md` for recent changes and progress
3. Focus first on completing the priority task: {priority_task or "Check pending tasks"}
4. Then continue with remaining pending tasks in order
5. Update documentation as changes are made

*Last Updated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
            
            # Write the content to the file
            with open(self.next_actions_file, 'w') as f:
                f.write(content)
            
            logger.info(f"Created next actions summary in {self.next_actions_file}")
        except Exception as e:
            logger.error(f"Error creating next actions summary: {e}")

    def auto_update_architecture(self) -> None:
        """Automatically update the architecture analysis document based on recent changes.
        
        This ensures the architecture documentation is always kept up-to-date.
        """
        try:
            # Get the files that have been staged for commit
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Extract the file paths
            file_paths = result.stdout.strip().split('\n')
            file_paths = [f for f in file_paths if f]  # Remove empty strings
            
            # Check if there are files that would affect architecture
            architecture_updates = []
            
            # Check for frontend changes
            frontend_files = [f for f in file_paths if f.startswith("frontend/") or f.startswith("src/frontend/")]
            if frontend_files:
                architecture_updates.append(("Frontend Components", "Frontend architecture has been updated with new components or modifications to existing ones."))
            
            # Check for backend changes
            backend_files = [f for f in file_paths if f.startswith("src/backend/")]
            if backend_files:
                architecture_updates.append(("Backend Services", "Backend services have been modified or new ones have been added."))
            
            # Check for AI model changes
            ai_files = [f for f in file_paths if f.startswith("src/ai/") or f.startswith("models/")]
            if ai_files:
                architecture_updates.append(("AI Models Integration", "AI model integration has been updated or new models have been added."))
            
            # Check for quantum computing changes
            quantum_files = [f for f in file_paths if f.startswith("src/quantum/")]
            if quantum_files:
                architecture_updates.append(("Quantum Computing Layer", "Quantum computing components have been modified or enhanced."))
            
            # Check for database changes
            db_files = [f for f in file_paths if "database" in f.lower() or "db" in f.lower() or f.endswith(".sql")]
            if db_files:
                architecture_updates.append(("Data Storage Architecture", "Database schema or data access layer has been updated."))
            
            # Update the architecture document for each affected section
            for section, description in architecture_updates:
                # Get the file content to analyze what was changed
                section_content = f"""
{description}

### Updated Components
"""
                for file_path in file_paths:
                    if ((section == "Frontend Components" and (file_path.startswith("frontend/") or file_path.startswith("src/frontend/"))) or
                        (section == "Backend Services" and file_path.startswith("src/backend/")) or
                        (section == "AI Models Integration" and (file_path.startswith("src/ai/") or file_path.startswith("models/"))) or
                        (section == "Quantum Computing Layer" and file_path.startswith("src/quantum/")) or
                        (section == "Data Storage Architecture" and ("database" in file_path.lower() or "db" in file_path.lower() or file_path.endswith(".sql")))):
                        section_content += f"- {file_path}\n"
                
                section_content += "\n### Integration Impact\n"
                section_content += "These changes may affect system integration and should be tested thoroughly.\n"
                
                # Update the architecture document
                self.update_architecture(section, section_content)
                
            if not architecture_updates:
                logger.info("No architecture-related changes detected")
                
        except Exception as e:
            logger.error(f"Error auto-updating architecture: {e}")
    
    def auto_update_journal(self) -> None:
        """Automatically update the journal with information about the current commit.
        
        This ensures the journal.md is always maintained with proper timestamps.
        """
        try:
            # Get the staged files
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True, 
                text=True,
                check=True
            )
            
            # Extract the file paths
            file_paths = result.stdout.strip().split('\n')
            file_paths = [f for f in file_paths if f]  # Remove empty strings
            
            if not file_paths:
                logger.info("No files staged for commit, skipping journal update")
                return
            
            # Get the components modified
            components_modified, _ = self._get_git_changes()
            
            # Generate the entry title
            if len(components_modified) == 1:
                entry_title = f"{components_modified[0]} Update"
            else:
                entry_title = "System Update"
            
            # Generate the entry content
            entry_content = "### Changes Made\n"
            
            # Add information about the files changed
            entry_content += "#### Files Modified\n"
            for file_path in file_paths[:10]:  # Limit to 10 files to avoid excessively long entries
                entry_content += f"- {file_path}\n"
            
            if len(file_paths) > 10:
                entry_content += f"- ... and {len(file_paths) - 10} more files\n"
            
            # Add information about the components affected
            entry_content += "\n#### Components Affected\n"
            for component in components_modified:
                entry_content += f"- {component}\n"
            
            # Add next steps
            entry_content += "\n### Next Steps\n"
            
            # Add the priority task first
            priority_task = self.session_state["next_session_requirements"]["priority"]
            if priority_task:
                entry_content += f"1. Complete the priority task: {priority_task}\n"
            
            # Add the pending tasks
            pending_tasks = self.session_state["current_context"]["pending_tasks"]
            for i, task in enumerate(pending_tasks[:3]):  # Limit to 3 tasks
                offset = 2 if priority_task else 1
                entry_content += f"{i + offset}. {task}\n"
            
            # Update the journal
            self.update_journal(entry_title, entry_content)
            
        except Exception as e:
            logger.error(f"Error auto-updating journal: {e}")
    
    def enhance_architecture_update(self) -> None:
        """Analyze changes more deeply to ensure all architecture plans are properly updated in ARCHITECTURE_ANALYSIS.md.
        
        This specialized method ensures that any architectural changes are always documented properly,
        following step 3 of the pre-commit requirements.
        """
        try:
            # Get the files that have been staged for commit
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Extract the file paths
            file_paths = result.stdout.strip().split('\n')
            file_paths = [f for f in file_paths if f]  # Remove empty strings
            
            if not file_paths:
                logger.info("No files staged for commit, skipping architecture enhancement")
                return
            
            # Check for architecture-related file content
            architecture_related_terms = [
                "architecture", "system design", "component", "integration", 
                "interface", "pattern", "framework", "infrastructure",
                "module", "service", "api", "database schema", "model", "class",
                "dependency", "workflow", "pipeline", "websocket"
            ]
            
            # Look for architectural changes by examining file content
            architectural_changes = []
            
            for file_path in file_paths:
                # Skip binary files and certain file types
                if (file_path.endswith('.png') or file_path.endswith('.jpg') or
                    file_path.endswith('.pdf') or file_path.endswith('.zip') or
                    '/node_modules/' in file_path or '/__pycache__/' in file_path):
                    continue
                    
                try:
                    # Get the diff content to analyze actual changes
                    diff_result = subprocess.run(
                        ["git", "diff", "--cached", file_path],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    
                    diff_content = diff_result.stdout.lower()
                    
                    # Check if the diff contains architecture-related terms
                    has_architecture_terms = any(term in diff_content for term in architecture_related_terms)
                    
                    if has_architecture_terms:
                        # Determine the component or module type
                        component_type = "General Architecture"
                        
                        if file_path.startswith("frontend/") or file_path.startswith("src/frontend/"):
                            component_type = "Frontend Architecture"
                        elif file_path.startswith("src/backend/"):
                            component_type = "Backend Services"
                        elif file_path.startswith("src/ai/") or file_path.startswith("models/"):
                            component_type = "AI Architecture"
                        elif file_path.startswith("src/quantum/"):
                            component_type = "Quantum Computing Architecture"
                        elif "database" in file_path.lower() or "db" in file_path.lower() or file_path.endswith(".sql"):
                            component_type = "Data Storage Architecture"
                        elif "api" in file_path.lower() or "rest" in file_path.lower() or "http" in file_path.lower():
                            component_type = "API Architecture"
                        elif "test" in file_path.lower():
                            component_type = "Testing Framework"
                        
                        # Add to architectural changes if not already present
                        if not any(change[0] == component_type for change in architectural_changes):
                            architectural_changes.append((component_type, file_path))
                
                except Exception as e:
                    logger.warning(f"Error analyzing diff for {file_path}: {e}")
                    continue
            
            # If we found architectural changes, update the architecture document
            for component_type, example_file in architectural_changes:
                # Prepare a more detailed description based on the component type
                if component_type == "Frontend Architecture":
                    description = "Frontend architecture has been updated with new components or modifications to existing UI elements, improving the user experience and real-time data visualization."
                elif component_type == "Backend Services":
                    description = "Backend service architecture has been enhanced to improve performance, reliability, or add new functionality. These changes affect the core system behavior."
                elif component_type == "AI Architecture":
                    description = "AI model architecture has been modified, potentially affecting prediction accuracy, training pipeline, or inference capabilities."
                elif component_type == "Quantum Computing Architecture":
                    description = "Quantum computing components have been updated to improve simulation performance or enhance trading algorithm precision."
                elif component_type == "Data Storage Architecture":
                    description = "Database schema or data access layer has been updated to optimize queries, improve data integrity, or support new features."
                elif component_type == "API Architecture":
                    description = "API interfaces have been modified, affecting how system components communicate with each other or external services."
                elif component_type == "Testing Framework":
                    description = "Testing infrastructure has been enhanced to improve code quality, reliability, and maintainability."
                else:
                    description = "Core architectural components have been modified, affecting the overall system design and behavior."
                
                # Create content for the architecture document
                content = f"""
{description}

### Architectural Impact
- **Component Type**: {component_type}
- **Primary Files**: {example_file}
- **Scope**: This change affects how the system is structured and how components interact.
- **Integration Considerations**: Test thoroughly to ensure compatibility with existing components.

### Implementation Details
The architecture has been updated to improve system design, component interaction, or user experience.
All architecture plans are now properly documented in ARCHITECTURE_ANALYSIS.md, following step 3
of the pre-commit requirements.

### Related Components
"""
                # Add related files to the content
                for file_path in file_paths:
                    if ((component_type == "Frontend Architecture" and (file_path.startswith("frontend/") or file_path.startswith("src/frontend/"))) or
                        (component_type == "Backend Services" and file_path.startswith("src/backend/")) or
                        (component_type == "AI Architecture" and (file_path.startswith("src/ai/") or file_path.startswith("models/"))) or
                        (component_type == "Quantum Computing Architecture" and file_path.startswith("src/quantum/")) or
                        (component_type == "Data Storage Architecture" and ("database" in file_path.lower() or "db" in file_path.lower() or file_path.endswith(".sql"))) or
                        (component_type == "API Architecture" and ("api" in file_path.lower() or "rest" in file_path.lower() or "http" in file_path.lower())) or
                        (component_type == "Testing Framework" and "test" in file_path.lower())):
                        content += f"- {file_path}\n"
                
                # Update the architecture document with this enhanced description
                self.update_architecture(component_type, content)
                logger.info(f"Enhanced architecture documentation for {component_type}")
                
            if not architectural_changes:
                logger.info("No architectural changes detected that require documentation")
                
        except Exception as e:
            logger.error(f"Error enhancing architecture documentation: {e}")

    def run_pre_commit_hook(self) -> bool:
        """Run the pre-commit hook.
        
        Returns:
            bool: True if the hook succeeded, False otherwise
        """
        logger.info("Running pre-commit hook")
        
        try:
            # 1. Get information about staged changes
            components_modified, changes = self._get_git_changes()
            
            # 2. Update the active branch in session state
            active_branch = self._get_active_branch()
            self.update_session_state(
                active_branch=active_branch,
                active_components=components_modified
            )
            
            # 3. Generate next actions based on current state
            next_actions = [
                "Update documentation to reflect changes",
                "Run tests to verify changes work correctly",
                "Check integration with other components"
            ]
            
            # 4. Log the changes
            self.log_changes(
                components_modified=components_modified,
                changes=changes,
                next_actions=next_actions
            )
            
            # 5. Auto-update the architecture analysis if needed
            self.auto_update_architecture()
            
            # 6. ENHANCED: Apply specialized architecture updates to ARCHITECTURE_ANALYSIS.md
            self.enhance_architecture_update()
            
            # 7. Auto-update the journal with committed changes
            self.auto_update_journal()
            
            # 8. Create a summary of what Copilot needs to do next
            self.create_next_actions_summary()
            
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