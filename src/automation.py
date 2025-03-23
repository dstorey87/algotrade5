#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AlgoTradePro5 Automation System.

This script serves as the main entry point for the automation system,
coordinating pre-commit hooks, task management, and documentation updates.
It's designed to be run by GitHub Copilot to automate development tasks.
"""

import argparse
import datetime
import logging
import os
import sys
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("automation")

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from src.pre_commit_hook import PreCommitHook
from src.task_manager import TaskManager


def setup_env():
    """Set up the environment for automation."""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Create src/docs directory if it doesn't exist
    os.makedirs("src/docs", exist_ok=True)


def run_pre_commit_hook():
    """Run the pre-commit hook manually."""
    hook = PreCommitHook()
    success = hook.run_pre_commit_hook()
    
    if success:
        logger.info("Pre-commit hook ran successfully")
    else:
        logger.error("Pre-commit hook failed")
        sys.exit(1)


def update_documentation(args):
    """Update project documentation."""
    hook = PreCommitHook()
    
    if args.architecture:
        # Update architecture documentation
        section = args.architecture
        content = args.content or ""
        
        if not content and not args.file:
            logger.error("Either content or file must be specified for architecture updates")
            sys.exit(1)
        
        if args.file:
            try:
                with open(args.file, 'r') as f:
                    content = f.read()
            except Exception as e:
                logger.error(f"Error reading file {args.file}: {e}")
                sys.exit(1)
        
        hook.update_architecture(section, content)
        logger.info(f"Updated architecture documentation section '{section}'")
    
    if args.frontend:
        # Update frontend plan
        if not args.content and not args.file:
            logger.error("Either content or file must be specified for frontend plan updates")
            sys.exit(1)
            
        updates = {}
        
        if args.file:
            try:
                import json
                with open(args.file, 'r') as f:
                    updates = json.load(f)
            except Exception as e:
                logger.error(f"Error reading file {args.file}: {e}")
                sys.exit(1)
        elif args.content:
            try:
                import json
                updates = json.loads(args.content)
            except Exception as e:
                logger.error(f"Error parsing JSON content: {e}")
                sys.exit(1)
        
        hook.update_frontend_plan(updates)
        logger.info("Updated frontend development plan")
    
    if args.journal:
        # Update journal
        section_title = args.journal
        
        if not args.content and not args.file:
            logger.error("Either content or file must be specified for journal updates")
            sys.exit(1)
            
        entries = []
        
        if args.file:
            try:
                import json
                with open(args.file, 'r') as f:
                    entries = json.load(f)
            except Exception as e:
                logger.error(f"Error reading file {args.file}: {e}")
                sys.exit(1)
        elif args.content:
            try:
                import json
                entries = json.loads(args.content)
            except Exception as e:
                logger.error(f"Error parsing JSON content: {e}")
                sys.exit(1)
        
        hook.update_journal(section_title, entries)
        logger.info(f"Updated journal with section '{section_title}'")
    
    if args.log_changes:
        # Log changes
        components = args.components.split(',') if args.components else []
        changes = args.changes.split(',') if args.changes else []
        next_actions = args.next_actions.split(',') if args.next_actions else []
        
        hook.log_changes(components, changes, next_actions)
        logger.info("Logged changes")


def manage_tasks(args):
    """Manage development tasks."""
    task_manager = TaskManager()
    
    if args.add:
        # Add a new task
        category = args.category or "general"
        name = args.name
        description = args.description or ""
        priority = args.priority or "medium"
        dependencies = args.dependencies.split(',') if args.dependencies else []
        
        task_id = task_manager.add_task(category, name, description, priority, dependencies)
        
        if task_id:
            logger.info(f"Added task {task_id}: {name}")
        else:
            logger.error("Failed to add task")
            sys.exit(1)
    
    if args.update:
        # Update task status
        task_id = args.task_id
        status = args.status
        
        success = task_manager.update_task_status(task_id, status)
        
        if success:
            logger.info(f"Updated task {task_id} status to {status}")
        else:
            logger.error(f"Failed to update task {task_id}")
            sys.exit(1)
    
    if args.focus:
        # Set current focus
        category = args.category
        task_id = args.task_id
        
        success = task_manager.set_current_focus(category, task_id)
        
        if success:
            logger.info(f"Set current focus to {category}/{task_id}")
        else:
            logger.error(f"Failed to set focus to {category}/{task_id}")
            sys.exit(1)
    
    if args.list:
        # List tasks
        current_focus = task_manager.get_current_focus()
        next_tasks = task_manager.get_next_tasks(count=5)
        
        if current_focus:
            print(f"Current focus: {current_focus['task']['name']} ({current_focus['task']['id']})")
            print(f"Description: {current_focus['task']['description']}")
            print(f"Status: {current_focus['task']['status']}")
            print(f"Priority: {current_focus['task']['priority']}")
        else:
            print("No current focus task")
        
        print("\nNext tasks to work on:")
        if next_tasks:
            for i, task_info in enumerate(next_tasks):
                task = task_info["task"]
                print(f"{i+1}. {task['name']} ({task['id']}) - {task['priority']} priority")
        else:
            print("No tasks available")


def update_session_state(args):
    """Update the Copilot session state."""
    hook = PreCommitHook()
    
    active_components = args.active_components.split(',') if args.active_components else None
    pending_tasks = args.pending_tasks.split(',') if args.pending_tasks else None
    completed_tasks = args.completed_tasks.split(',') if args.completed_tasks else None
    
    hook.update_session_state(
        active_components=active_components,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        priority=args.priority,
        dependencies=args.dependencies.split(',') if args.dependencies else None,
        current_phase=args.current_phase,
        active_branch=args.active_branch,
        last_component=args.last_component
    )
    
    logger.info("Updated Copilot session state")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='AlgoTradePro5 Automation System')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Pre-commit hook command
    pre_commit_parser = subparsers.add_parser('pre-commit', help='Run pre-commit hook')
    
    # Documentation command
    docs_parser = subparsers.add_parser('docs', help='Update documentation')
    docs_parser.add_argument('--architecture', help='Architecture documentation section to update')
    docs_parser.add_argument('--frontend', action='store_true', help='Update frontend development plan')
    docs_parser.add_argument('--journal', help='Journal section title to add')
    docs_parser.add_argument('--log-changes', action='store_true', help='Log changes')
    docs_parser.add_argument('--content', help='Content to update with (JSON for frontend/journal)')
    docs_parser.add_argument('--file', help='File containing content to update with')
    docs_parser.add_argument('--components', help='Comma-separated list of components modified')
    docs_parser.add_argument('--changes', help='Comma-separated list of changes made')
    docs_parser.add_argument('--next-actions', help='Comma-separated list of next actions')
    
    # Task management command
    tasks_parser = subparsers.add_parser('tasks', help='Manage tasks')
    tasks_parser.add_argument('--add', action='store_true', help='Add a new task')
    tasks_parser.add_argument('--update', action='store_true', help='Update task status')
    tasks_parser.add_argument('--focus', action='store_true', help='Set current focus')
    tasks_parser.add_argument('--list', action='store_true', help='List tasks')
    tasks_parser.add_argument('--category', help='Task category')
    tasks_parser.add_argument('--name', help='Task name')
    tasks_parser.add_argument('--description', help='Task description')
    tasks_parser.add_argument('--priority', help='Task priority (low, medium, high)')
    tasks_parser.add_argument('--dependencies', help='Comma-separated list of task dependencies')
    tasks_parser.add_argument('--task-id', help='Task ID')
    tasks_parser.add_argument('--status', help='Task status (pending, in_progress, completed, blocked)')
    
    # Session state command
    session_parser = subparsers.add_parser('session', help='Update Copilot session state')
    session_parser.add_argument('--active-components', help='Comma-separated list of active components')
    session_parser.add_argument('--pending-tasks', help='Comma-separated list of pending tasks')
    session_parser.add_argument('--completed-tasks', help='Comma-separated list of completed tasks')
    session_parser.add_argument('--priority', help='Next priority task')
    session_parser.add_argument('--dependencies', help='Comma-separated list of dependencies')
    session_parser.add_argument('--current-phase', help='Current development phase')
    session_parser.add_argument('--active-branch', help='Active git branch')
    session_parser.add_argument('--last-component', help='Last component being worked on')
    
    return parser.parse_args()


def main():
    """Main entry point for the automation system."""
    setup_env()
    args = parse_args()
    
    if args.command == 'pre-commit':
        run_pre_commit_hook()
    elif args.command == 'docs':
        update_documentation(args)
    elif args.command == 'tasks':
        manage_tasks(args)
    elif args.command == 'session':
        update_session_state(args)
    else:
        print("No command specified. Use --help for usage information.")
        sys.exit(1)


if __name__ == "__main__":
    main()