#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task Manager for AlgoTradePro5.

This module manages development tasks and tracks progress between Copilot sessions.
It serves as a continuation point when Copilot sessions are interrupted due to rate limits.
"""

import os
import json
import datetime
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/task_manager.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("task_manager")

class TaskManager:
    """Task Manager for AlgoTradePro5 development."""
    
    def __init__(self, root_dir: str = None):
        """Initialize the task manager.
        
        Args:
            root_dir: Root directory of the project
        """
        self.root_dir = root_dir or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.task_file = os.path.join(self.root_dir, "src", "docs", "tasks.json")
        self.progress_file = os.path.join(self.root_dir, "src", "docs", "progress.md")
        
        # Create log directory if it doesn't exist
        os.makedirs(os.path.join(self.root_dir, "logs"), exist_ok=True)
        
        # Create docs directory if it doesn't exist
        os.makedirs(os.path.join(self.root_dir, "src", "docs"), exist_ok=True)
        
        # Load or create tasks
        self.tasks = self._load_or_create_tasks()
    
    def _load_or_create_tasks(self) -> Dict[str, Any]:
        """Load tasks or create them if they don't exist."""
        if os.path.exists(self.task_file):
            try:
                with open(self.task_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Error decoding task file {self.task_file}")
                return self._create_default_tasks()
        else:
            return self._create_default_tasks()
    
    def _create_default_tasks(self) -> Dict[str, Any]:
        """Create default tasks."""
        default_tasks = {
            "last_update": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "categories": {
                "frontend": {
                    "name": "Frontend Development",
                    "tasks": [
                        {
                            "id": "fe-001",
                            "name": "Implement WebSocket Client",
                            "description": "Create WebSocket client for real-time data",
                            "status": "pending",
                            "priority": "high",
                            "dependencies": []
                        },
                        {
                            "id": "fe-002",
                            "name": "Create Real-time Dashboard",
                            "description": "Implement real-time trading dashboard",
                            "status": "pending",
                            "priority": "high",
                            "dependencies": ["fe-001"]
                        }
                    ]
                },
                "backend": {
                    "name": "Backend Development",
                    "tasks": [
                        {
                            "id": "be-001",
                            "name": "Implement WebSocket Server",
                            "description": "Create WebSocket server for real-time data",
                            "status": "pending",
                            "priority": "high",
                            "dependencies": []
                        },
                        {
                            "id": "be-002",
                            "name": "Create Data Processing Pipeline",
                            "description": "Implement data processing pipeline",
                            "status": "pending",
                            "priority": "medium",
                            "dependencies": ["be-001"]
                        }
                    ]
                },
                "documentation": {
                    "name": "Documentation",
                    "tasks": [
                        {
                            "id": "doc-001",
                            "name": "Update Architecture Documentation",
                            "description": "Update architecture documentation with real-time components",
                            "status": "pending",
                            "priority": "medium",
                            "dependencies": []
                        },
                        {
                            "id": "doc-002",
                            "name": "Update Frontend Plan",
                            "description": "Update frontend development plan",
                            "status": "pending",
                            "priority": "medium",
                            "dependencies": []
                        }
                    ]
                }
            },
            "current_focus": {
                "category": "frontend",
                "task_id": "fe-001"
            },
            "completed_tasks": []
        }
        
        # Save default tasks
        with open(self.task_file, 'w') as f:
            json.dump(default_tasks, f, indent=2)
        
        # Create initial progress file
        self._update_progress_file()
        
        return default_tasks
    
    def _save_tasks(self):
        """Save tasks to the task file."""
        try:
            # Update timestamp
            self.tasks["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save tasks
            with open(self.task_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
            
            # Update progress file
            self._update_progress_file()
            
            logger.info(f"Saved tasks to {self.task_file}")
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")
    
    def _update_progress_file(self):
        """Update the progress file with current task status."""
        try:
            # Create a markdown file with task status
            content = "# AlgoTradePro5 Development Progress\n\n"
            content += f"Last updated: {self.tasks['last_update']}\n\n"
            
            # Current focus
            current_category = self.tasks["current_focus"]["category"]
            current_task_id = self.tasks["current_focus"]["task_id"]
            
            # Find current task
            current_task = None
            for task in self.tasks["categories"][current_category]["tasks"]:
                if task["id"] == current_task_id:
                    current_task = task
                    break
            
            if current_task:
                content += f"## Current Focus: {current_task['name']}\n\n"
                content += f"**Description**: {current_task['description']}\n"
                content += f"**Priority**: {current_task['priority']}\n"
                content += f"**Status**: {current_task['status']}\n\n"
            
            # Tasks by category
            content += "## Tasks by Category\n\n"
            
            for category_id, category in self.tasks["categories"].items():
                content += f"### {category['name']}\n\n"
                
                # Create a table of tasks
                content += "| ID | Name | Description | Status | Priority |\n"
                content += "|---|---|---|---|---|\n"
                
                for task in category["tasks"]:
                    content += f"| {task['id']} | {task['name']} | {task['description']} | {task['status']} | {task['priority']} |\n"
                
                content += "\n"
            
            # Completed tasks
            content += "## Completed Tasks\n\n"
            
            if self.tasks["completed_tasks"]:
                content += "| ID | Name | Completion Date |\n"
                content += "|---|---|---|\n"
                
                for completed_task in self.tasks["completed_tasks"]:
                    content += f"| {completed_task['id']} | {completed_task['name']} | {completed_task['completed_at']} |\n"
            else:
                content += "No tasks completed yet.\n"
            
            # Write to file
            with open(self.progress_file, 'w') as f:
                f.write(content)
            
            logger.info(f"Updated progress file at {self.progress_file}")
        except Exception as e:
            logger.error(f"Error updating progress file: {e}")
    
    def add_task(self, category: str, name: str, description: str, priority: str = "medium", 
                 dependencies: List[str] = None) -> str:
        """Add a new task.
        
        Args:
            category: Category of the task
            name: Name of the task
            description: Description of the task
            priority: Priority of the task (low, medium, high)
            dependencies: List of task IDs that this task depends on
            
        Returns:
            str: ID of the newly created task
        """
        try:
            # Check if category exists
            if category not in self.tasks["categories"]:
                # Create new category
                self.tasks["categories"][category] = {
                    "name": category.capitalize(),
                    "tasks": []
                }
            
            # Generate task ID
            category_prefix = category[:2].lower()
            task_count = len(self.tasks["categories"][category]["tasks"]) + 1
            task_id = f"{category_prefix}-{task_count:03d}"
            
            # Create task
            task = {
                "id": task_id,
                "name": name,
                "description": description,
                "status": "pending",
                "priority": priority,
                "dependencies": dependencies or []
            }
            
            # Add task
            self.tasks["categories"][category]["tasks"].append(task)
            
            # Save tasks
            self._save_tasks()
            
            logger.info(f"Added task {task_id}: {name}")
            
            return task_id
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            return None
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """Update the status of a task.
        
        Args:
            task_id: ID of the task
            status: New status (pending, in_progress, completed, blocked)
            
        Returns:
            bool: True if the task was updated, False otherwise
        """
        try:
            # Find the task
            for category_id, category in self.tasks["categories"].items():
                for task in category["tasks"]:
                    if task["id"] == task_id:
                        # Update status
                        old_status = task["status"]
                        task["status"] = status
                        
                        # If task is completed, move it to completed_tasks
                        if status == "completed" and old_status != "completed":
                            # Add to completed_tasks
                            self.tasks["completed_tasks"].append({
                                "id": task_id,
                                "name": task["name"],
                                "completed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                        
                        # Save tasks
                        self._save_tasks()
                        
                        logger.info(f"Updated task {task_id} status to {status}")
                        
                        return True
            
            logger.warning(f"Task {task_id} not found")
            return False
        except Exception as e:
            logger.error(f"Error updating task status: {e}")
            return False
    
    def set_current_focus(self, category: str, task_id: str) -> bool:
        """Set the current focus task.
        
        Args:
            category: Category of the task
            task_id: ID of the task
            
        Returns:
            bool: True if the focus was set, False otherwise
        """
        try:
            # Check if category and task exist
            if category not in self.tasks["categories"]:
                logger.warning(f"Category {category} not found")
                return False
            
            # Check if task exists in category
            task_exists = False
            for task in self.tasks["categories"][category]["tasks"]:
                if task["id"] == task_id:
                    task_exists = True
                    break
            
            if not task_exists:
                logger.warning(f"Task {task_id} not found in category {category}")
                return False
            
            # Set current focus
            self.tasks["current_focus"] = {
                "category": category,
                "task_id": task_id
            }
            
            # Save tasks
            self._save_tasks()
            
            logger.info(f"Set current focus to {category}/{task_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error setting current focus: {e}")
            return False
    
    def get_current_focus(self) -> Dict[str, Any]:
        """Get the current focus task.
        
        Returns:
            Dict: Current focus task details
        """
        try:
            # Get current focus
            current_category = self.tasks["current_focus"]["category"]
            current_task_id = self.tasks["current_focus"]["task_id"]
            
            # Find current task
            for task in self.tasks["categories"][current_category]["tasks"]:
                if task["id"] == current_task_id:
                    return {
                        "category": current_category,
                        "task": task
                    }
            
            logger.warning(f"Current focus task {current_category}/{current_task_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error getting current focus: {e}")
            return None
    
    def get_next_tasks(self, count: int = 3) -> List[Dict[str, Any]]:
        """Get the next tasks to work on based on dependencies and priority.
        
        Args:
            count: Number of tasks to return
            
        Returns:
            List[Dict]: List of tasks to work on next
        """
        try:
            next_tasks = []
            
            # Get all pending and in_progress tasks
            all_tasks = []
            for category_id, category in self.tasks["categories"].items():
                for task in category["tasks"]:
                    if task["status"] in ["pending", "in_progress"]:
                        all_tasks.append({
                            "category": category_id,
                            "task": task
                        })
            
            # Get completed task IDs
            completed_task_ids = [task["id"] for task in self.tasks["completed_tasks"]]
            
            # Filter tasks that have all dependencies completed
            available_tasks = []
            for task_info in all_tasks:
                task = task_info["task"]
                
                # Check if all dependencies are completed
                dependencies_met = True
                for dependency in task["dependencies"]:
                    if dependency not in completed_task_ids:
                        dependencies_met = False
                        break
                
                if dependencies_met:
                    available_tasks.append(task_info)
            
            # Sort by priority (high, medium, low)
            priority_order = {"high": 0, "medium": 1, "low": 2}
            available_tasks.sort(key=lambda x: priority_order.get(x["task"]["priority"], 99))
            
            # Get the next 'count' tasks
            next_tasks = available_tasks[:count]
            
            return next_tasks
        except Exception as e:
            logger.error(f"Error getting next tasks: {e}")
            return []


def main():
    """Main function to demonstrate task manager usage."""
    task_manager = TaskManager()
    
    # Add some sample tasks if running directly
    if not os.path.exists(task_manager.task_file):
        # Add frontend tasks
        task_manager.add_task(
            category="frontend",
            name="Implement WebSocket Client",
            description="Create WebSocket client for real-time data",
            priority="high"
        )
        
        task_manager.add_task(
            category="frontend",
            name="Create Real-time Dashboard",
            description="Implement real-time trading dashboard",
            priority="high",
            dependencies=["fe-001"]
        )
        
        # Add backend tasks
        task_manager.add_task(
            category="backend",
            name="Implement WebSocket Server",
            description="Create WebSocket server for real-time data",
            priority="high"
        )
        
        task_manager.add_task(
            category="backend",
            name="Create Data Processing Pipeline",
            description="Implement data processing pipeline",
            priority="medium",
            dependencies=["be-001"]
        )
        
        # Set current focus
        task_manager.set_current_focus("frontend", "fe-001")
        
        print("Created sample tasks and set current focus to WebSocket Client")
    else:
        # Show current focus
        current_focus = task_manager.get_current_focus()
        if current_focus:
            print(f"Current focus: {current_focus['task']['name']} ({current_focus['task']['id']})")
        
        # Show next tasks
        next_tasks = task_manager.get_next_tasks()
        print("\nNext tasks to work on:")
        for i, task_info in enumerate(next_tasks):
            task = task_info["task"]
            print(f"{i+1}. {task['name']} ({task['id']}) - {task['priority']} priority")


if __name__ == "__main__":
    main()