#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Script for AlgoTradePro5 Pre-commit Hook System.

This script tests the functionality of the pre-commit hook system,
verifying that it correctly maintains state, logs changes, and updates documentation.
"""

import os
import sys
import datetime
import json
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from hooks.pre_commit_hook import PreCommitHook
from hooks.task_manager import TaskManager

def test_session_state():
    """Test updating and maintaining session state."""
    print("Testing Session State Management...")
    
    # Create PreCommitHook instance
    hook = PreCommitHook()
    
    # Update session state
    hook.update_session_state(
        active_components=["WebSocket", "Frontend"],
        pending_tasks=["Implement error handling", "Add authentication"],
        completed_tasks=["Basic WebSocket setup"],
        priority="Error Handling",
        dependencies=["Socket.IO", "React"],
        current_phase="Frontend Development",
        active_branch="feature/websocket",
        last_component="WebSocketProvider"
    )
    
    # Verify session state was updated
    if os.path.exists(hook.session_file):
        print("✅ Session state file created successfully")
    else:
        print("❌ Failed to create session state file")
        return False
    
    print("Session state updated successfully")
    return True

def test_change_logging():
    """Test logging changes."""
    print("\nTesting Change Logging...")
    
    # Create PreCommitHook instance
    hook = PreCommitHook()
    
    # Log changes
    hook.log_changes(
        components_modified=["WebSocket", "Frontend"],
        changes=[
            "Implemented WebSocket client with reconnection logic",
            "Added real-time updates to dashboard",
            "Implemented error handling for WebSocket connections"
        ],
        next_actions=[
            "Add authentication to WebSocket connections",
            "Implement unit tests for WebSocket client",
            "Add documentation for WebSocket API"
        ]
    )
    
    # Verify changes log was updated
    if os.path.exists(hook.changes_log):
        print("✅ Changes log file created/updated successfully")
    else:
        print("❌ Failed to create/update changes log file")
        return False
    
    print("Changes logged successfully")
    return True

def test_journal_update():
    """Test updating the journal."""
    print("\nTesting Journal Updates...")
    
    # Create PreCommitHook instance
    hook = PreCommitHook()
    
    # Update journal
    hook.update_journal(
        entry_title="WebSocket Implementation Progress",
        entry_content="""
### Components Implemented
- WebSocketProvider component for managing connections
- useWebSocket hook for React integration
- Reconnection logic with exponential backoff
- Error handling and connection status tracking

### Next Steps
1. Add authentication to WebSocket connections
2. Implement unit tests for WebSocket client
3. Add documentation for WebSocket API
"""
    )
    
    # Verify journal was updated
    if os.path.exists(hook.journal_file):
        print("✅ Journal file created/updated successfully")
    else:
        print("❌ Failed to create/update journal file")
        return False
    
    print("Journal updated successfully")
    return True

def test_frontend_plan_update():
    """Test updating the frontend plan."""
    print("\nTesting Frontend Plan Updates...")
    
    # Create PreCommitHook instance
    hook = PreCommitHook()
    
    # Update frontend plan
    hook.update_frontend_plan(
        section="Real-time Components",
        content="""
- WebSocketProvider - Manages WebSocket connections
- useWebSocket - React hook for WebSocket integration
- RealtimeChart - Real-time chart component
- StreamingDataGrid - Real-time data grid

### Implementation Status
- WebSocketProvider: Completed
- useWebSocket: Completed
- RealtimeChart: In Progress
- StreamingDataGrid: Pending

### Next Steps
1. Complete RealtimeChart component
2. Implement StreamingDataGrid component
3. Add unit tests for all components
"""
    )
    
    # Verify frontend plan was updated
    if os.path.exists(hook.frontend_plan):
        print("✅ Frontend plan file created/updated successfully")
    else:
        print("❌ Failed to create/update frontend plan file")
        return False
    
    print("Frontend plan updated successfully")
    return True

def test_architecture_update():
    """Test updating the architecture analysis."""
    print("\nTesting Architecture Analysis Updates...")
    
    # Create PreCommitHook instance
    hook = PreCommitHook()
    
    # Update architecture analysis
    hook.update_architecture(
        section="WebSocket Integration",
        content="""
The WebSocket integration provides real-time data streaming between the server and the client.

### Components
- **WebSocketServer**: Manages WebSocket connections on the server
- **WebSocketClient**: Manages WebSocket connections on the client
- **MessageHandler**: Processes WebSocket messages
- **ConnectionManager**: Handles connection lifecycle

### Implementation Details
- Socket.IO is used for WebSocket implementation
- Reconnection logic with exponential backoff
- Authentication via JWT
- Message compression for efficient data transfer

### Performance Considerations
- Connection pooling for efficient resource usage
- Message batching for reduced network overhead
- Binary message format for reduced payload size
"""
    )
    
    # Verify architecture analysis was updated
    if os.path.exists(hook.arch_file):
        print("✅ Architecture analysis file created/updated successfully")
    else:
        print("❌ Failed to create/update architecture analysis file")
        return False
    
    print("Architecture analysis updated successfully")
    return True

def test_task_management():
    """Test task management functionality."""
    print("\nTesting Task Management...")
    
    # Create TaskManager instance
    task_manager = TaskManager()
    
    # Add tasks
    print("Adding tasks...")
    fe_task1 = task_manager.add_task(
        category="frontend",
        name="Implement WebSocket Client",
        description="Create WebSocket client with reconnection logic",
        priority="high"
    )
    
    fe_task2 = task_manager.add_task(
        category="frontend",
        name="Create Real-time Dashboard",
        description="Implement real-time dashboard with data streaming",
        priority="high",
        dependencies=[fe_task1]
    )
    
    be_task1 = task_manager.add_task(
        category="backend",
        name="Implement WebSocket Server",
        description="Create WebSocket server with authentication",
        priority="high"
    )
    
    # Update task status
    print("Updating task status...")
    task_manager.update_task_status(fe_task1, "in_progress")
    
    # Set current focus
    print("Setting current focus...")
    task_manager.set_current_focus("frontend", fe_task1)
    
    # Get current focus
    current_focus = task_manager.get_current_focus()
    if current_focus and current_focus["task"]["id"] == fe_task1:
        print(f"✅ Current focus set to: {current_focus['task']['name']}")
    else:
        print("❌ Failed to set current focus")
        return False
    
    # Get next tasks
    next_tasks = task_manager.get_next_tasks()
    if next_tasks:
        print(f"✅ Next tasks retrieved successfully: {len(next_tasks)} tasks")
    else:
        print("❌ Failed to retrieve next tasks")
        return False
    
    # Verify task files were created
    if os.path.exists(task_manager.task_file) and os.path.exists(task_manager.progress_file):
        print("✅ Task files created successfully")
    else:
        print("❌ Failed to create task files")
        return False
    
    print("Task management tests completed successfully")
    return True

def test_pre_commit_hook():
    """Test running the pre-commit hook."""
    print("\nTesting Pre-commit Hook Execution...")
    
    # Create PreCommitHook instance
    hook = PreCommitHook()
    
    # Run pre-commit hook
    success = hook.run_pre_commit_hook()
    
    if success:
        print("✅ Pre-commit hook executed successfully")
    else:
        print("❌ Pre-commit hook execution failed")
        return False
    
    print("Pre-commit hook test completed successfully")
    return True

def main():
    """Main entry point."""
    print("=== AlgoTradePro5 Pre-commit Hook System Test ===\n")
    
    # Run tests
    tests = [
        test_session_state,
        test_change_logging,
        test_journal_update,
        test_frontend_plan_update,
        test_architecture_update,
        test_task_management,
        test_pre_commit_hook
    ]
    
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("src/docs", exist_ok=True)
    
    # Run tests
    results = []
    for test in tests:
        results.append(test())
    
    # Print summary
    print("\n=== Test Summary ===")
    success_count = sum(1 for result in results if result)
    print(f"Tests passed: {success_count}/{len(tests)}")
    
    if all(results):
        print("\n✅ All tests passed!")
        print("\nThe pre-commit hook system is working correctly.")
        print("You can now use it to maintain state between Copilot sessions.")
    else:
        print("\n❌ Some tests failed.")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()