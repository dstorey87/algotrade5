#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AlgoTradePro5 Automation CLI.

This module provides a command-line interface for the automation system,
allowing for easier interaction with the pre-commit hooks, task management,
and documentation updates.
"""

import os
import sys
import argparse
import logging
import datetime
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from hooks.pre_commit_hook import PreCommitHook
from hooks.task_manager import TaskManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/automation_cli.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("automation_cli")


def ensure_directories_exist():
    """Ensure that necessary directories exist."""
    os.makedirs("logs", exist_ok=True)
    os.makedirs("src/docs", exist_ok=True)


def handle_session_update(args):
    """Handle session state updates."""
    hook = PreCommitHook()
    
    # Parse active components
    active_components = args.active_components.split(',') if args.active_components else None
    
    # Parse pending tasks
    pending_tasks = args.pending_tasks.split(',') if args.pending_tasks else None
    
    # Parse completed tasks
    completed_tasks = args.completed_tasks.split(',') if args.completed_tasks else None
    
    # Parse dependencies
    dependencies = args.dependencies.split(',') if args.dependencies else None
    
    # Update session state
    hook.update_session_state(
        active_components=active_components,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        priority=args.priority,
        dependencies=dependencies,
        current_phase=args.current_phase,
        active_branch=args.active_branch,
        last_component=args.last_component
    )
    
    logger.info("Updated session state")
    print("Session state updated successfully")


def handle_log_changes(args):
    """Handle logging changes."""
    hook = PreCommitHook()
    
    # Parse components
    components = args.components.split(',') if args.components else []
    
    # Parse changes
    changes = args.changes.split(',') if args.changes else []
    
    # Parse next actions
    next_actions = args.next_actions.split(',') if args.next_actions else []
    
    # Log changes
    hook.log_changes(components, changes, next_actions)
    
    logger.info("Logged changes")
    print("Changes logged successfully")


def handle_journal_update(args):
    """Handle journal updates."""
    hook = PreCommitHook()
    
    # Check if content is from a file
    if args.content_file:
        try:
            with open(args.content_file, 'r') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            print(f"Error reading file: {e}")
            return
    else:
        content = args.content
    
    # Update journal
    hook.update_journal(args.title, content)
    
    logger.info("Updated journal")
    print("Journal updated successfully")


def handle_frontend_plan_update(args):
    """Handle frontend plan updates."""
    hook = PreCommitHook()
    
    # Check if content is from a file
    if args.content_file:
        try:
            with open(args.content_file, 'r') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            print(f"Error reading file: {e}")
            return
    else:
        content = args.content
    
    # Update frontend plan
    hook.update_frontend_plan(args.section, content)
    
    logger.info("Updated frontend plan")
    print("Frontend plan updated successfully")


def handle_architecture_update(args):
    """Handle architecture analysis updates."""
    hook = PreCommitHook()
    
    # Check if content is from a file
    if args.content_file:
        try:
            with open(args.content_file, 'r') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            print(f"Error reading file: {e}")
            return
    else:
        content = args.content
    
    # Update architecture analysis
    hook.update_architecture(args.section, content)
    
    logger.info("Updated architecture analysis")
    print("Architecture analysis updated successfully")


def handle_task_add(args):
    """Handle adding a new task."""
    task_manager = TaskManager()
    
    # Parse dependencies
    dependencies = args.dependencies.split(',') if args.dependencies else None
    
    # Add task
    task_id = task_manager.add_task(
        category=args.category,
        name=args.name,
        description=args.description,
        priority=args.priority,
        dependencies=dependencies
    )
    
    if task_id:
        logger.info(f"Added task {task_id}")
        print(f"Task {task_id} added successfully")
    else:
        logger.error("Failed to add task")
        print("Failed to add task")


def handle_task_update(args):
    """Handle updating a task."""
    task_manager = TaskManager()
    
    # Update task
    success = task_manager.update_task_status(
        task_id=args.task_id,
        status=args.status
    )
    
    if success:
        logger.info(f"Updated task {args.task_id} to {args.status}")
        print(f"Task {args.task_id} updated successfully")
    else:
        logger.error(f"Failed to update task {args.task_id}")
        print(f"Failed to update task {args.task_id}")


def handle_task_focus(args):
    """Handle setting task focus."""
    task_manager = TaskManager()
    
    # Set focus
    success = task_manager.set_current_focus(
        category=args.category,
        task_id=args.task_id
    )
    
    if success:
        logger.info(f"Set focus to {args.category}/{args.task_id}")
        print(f"Focus set to {args.category}/{args.task_id} successfully")
    else:
        logger.error(f"Failed to set focus to {args.category}/{args.task_id}")
        print(f"Failed to set focus to {args.category}/{args.task_id}")


def handle_task_list(args):
    """Handle listing tasks."""
    task_manager = TaskManager()
    
    # Get current focus
    current_focus = task_manager.get_current_focus()
    
    # Get next tasks
    next_tasks = task_manager.get_next_tasks(count=args.count)
    
    # Print current focus
    if current_focus:
        print(f"Current Focus: {current_focus['task']['name']} ({current_focus['task']['id']})")
        print(f"Description: {current_focus['task']['description']}")
        print(f"Status: {current_focus['task']['status']}")
        print(f"Priority: {current_focus['task']['priority']}")
    else:
        print("No current focus")
    
    # Print next tasks
    print("\nNext Tasks:")
    if next_tasks:
        for i, task_info in enumerate(next_tasks):
            task = task_info["task"]
            print(f"{i+1}. [{task['id']}] {task['name']} - {task['priority']} priority")
            print(f"   Status: {task['status']}")
            print(f"   Description: {task['description']}")
            if task['dependencies']:
                print(f"   Dependencies: {', '.join(task['dependencies'])}")
            print()
    else:
        print("No tasks available")


def handle_run_hook(args):
    """Handle running the pre-commit hook."""
    hook = PreCommitHook()
    
    # Run hook
    success = hook.run_pre_commit_hook()
    
    if success:
        logger.info("Pre-commit hook ran successfully")
        print("Pre-commit hook ran successfully")
    else:
        logger.error("Pre-commit hook failed")
        print("Pre-commit hook failed")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="AlgoTradePro5 Automation CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Session Update Command
    session_parser = subparsers.add_parser("session", help="Update session state")
    session_parser.add_argument("--active-components", help="Comma-separated list of active components")
    session_parser.add_argument("--pending-tasks", help="Comma-separated list of pending tasks")
    session_parser.add_argument("--completed-tasks", help="Comma-separated list of completed tasks")
    session_parser.add_argument("--priority", help="Next priority")
    session_parser.add_argument("--dependencies", help="Comma-separated list of dependencies")
    session_parser.add_argument("--current-phase", help="Current development phase")
    session_parser.add_argument("--active-branch", help="Active git branch")
    session_parser.add_argument("--last-component", help="Last component worked on")
    session_parser.set_defaults(func=handle_session_update)
    
    # Log Changes Command
    log_parser = subparsers.add_parser("log", help="Log changes")
    log_parser.add_argument("--components", help="Comma-separated list of modified components")
    log_parser.add_argument("--changes", help="Comma-separated list of changes")
    log_parser.add_argument("--next-actions", help="Comma-separated list of next actions")
    log_parser.set_defaults(func=handle_log_changes)
    
    # Journal Update Command
    journal_parser = subparsers.add_parser("journal", help="Update journal")
    journal_parser.add_argument("--title", required=True, help="Entry title")
    journal_parser.add_argument("--content", help="Entry content")
    journal_parser.add_argument("--content-file", help="File containing entry content")
    journal_parser.set_defaults(func=handle_journal_update)
    
    # Frontend Plan Update Command
    frontend_parser = subparsers.add_parser("frontend", help="Update frontend plan")
    frontend_parser.add_argument("--section", required=True, help="Section to update")
    frontend_parser.add_argument("--content", help="Section content")
    frontend_parser.add_argument("--content-file", help="File containing section content")
    frontend_parser.set_defaults(func=handle_frontend_plan_update)
    
    # Architecture Update Command
    arch_parser = subparsers.add_parser("architecture", help="Update architecture analysis")
    arch_parser.add_argument("--section", required=True, help="Section to update")
    arch_parser.add_argument("--content", help="Section content")
    arch_parser.add_argument("--content-file", help="File containing section content")
    arch_parser.set_defaults(func=handle_architecture_update)
    
    # Task Add Command
    task_add_parser = subparsers.add_parser("task-add", help="Add a new task")
    task_add_parser.add_argument("--category", required=True, help="Task category")
    task_add_parser.add_argument("--name", required=True, help="Task name")
    task_add_parser.add_argument("--description", help="Task description")
    task_add_parser.add_argument("--priority", choices=["low", "medium", "high"], default="medium", help="Task priority")
    task_add_parser.add_argument("--dependencies", help="Comma-separated list of task dependencies")
    task_add_parser.set_defaults(func=handle_task_add)
    
    # Task Update Command
    task_update_parser = subparsers.add_parser("task-update", help="Update a task")
    task_update_parser.add_argument("--task-id", required=True, help="Task ID")
    task_update_parser.add_argument("--status", required=True, choices=["pending", "in_progress", "completed", "blocked"], help="Task status")
    task_update_parser.set_defaults(func=handle_task_update)
    
    # Task Focus Command
    task_focus_parser = subparsers.add_parser("task-focus", help="Set task focus")
    task_focus_parser.add_argument("--category", required=True, help="Task category")
    task_focus_parser.add_argument("--task-id", required=True, help="Task ID")
    task_focus_parser.set_defaults(func=handle_task_focus)
    
    # Task List Command
    task_list_parser = subparsers.add_parser("task-list", help="List tasks")
    task_list_parser.add_argument("--count", type=int, default=5, help="Number of tasks to list")
    task_list_parser.set_defaults(func=handle_task_list)
    
    # Run Hook Command
    hook_parser = subparsers.add_parser("run-hook", help="Run pre-commit hook")
    hook_parser.set_defaults(func=handle_run_hook)
    
    return parser.parse_args()


def main():
    """Main entry point."""
    ensure_directories_exist()
    args = parse_arguments()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        print("Please specify a command. Use --help for more information.")


if __name__ == "__main__":
    main()