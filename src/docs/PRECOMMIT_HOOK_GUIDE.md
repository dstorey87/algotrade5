# AlgoTradePro5 Pre-commit Hook System

This document explains how to use the AlgoTradePro5 pre-commit hook system, which is designed to help GitHub Copilot maintain state between sessions, track changes, update documentation, and log progress.

## Overview

The pre-commit hook system provides the following key features:

1. **Session State Tracking** - Maintains the context and state between Copilot sessions, particularly useful when hitting rate limits
2. **Change Logging** - Records all changes made to the codebase with timestamps
3. **Documentation Updates** - Automates updating documentation files with changes
4. **Task Management** - Tracks development tasks and their status
5. **Journal Maintenance** - Automatically updates the development journal with timestamps

## Installation

To install the pre-commit hook, run:

```bash
python src/hooks/install_hook.py
```

This will:
1. Create a Git pre-commit hook in your `.git/hooks` directory
2. Set up the necessary directory structure
3. Initialize the logging system
4. Backup any existing pre-commit hook

## Core Components

The system consists of the following components:

- `pre_commit_hook.py` - The main pre-commit hook implementation
- `task_manager.py` - Task tracking and management
- `automation_cli.py` - Command-line interface for interacting with the system
- `install_hook.py` - Installation script for the Git hook
- `run_pre_commit.py` - Runner script invoked by Git

## Using the Automation CLI

The `automation_cli.py` script provides a command-line interface for interacting with the pre-commit hook system. Here are some common usage examples:

### Managing Session State

```bash
# Update session state with current context
python src/hooks/automation_cli.py session --active-components "WebSocket,Frontend" --current-phase "Frontend Development" --active-branch "feature/websocket" --last-component "WebSocketProvider"

# Update next actions
python src/hooks/automation_cli.py session --pending-tasks "Implement error handling,Add authentication" --priority "Error Handling"
```

### Logging Changes

```bash
# Log changes made to the codebase
python src/hooks/automation_cli.py log --components "WebSocket,Frontend" --changes "Implemented WebSocket client,Added real-time updates" --next-actions "Add error handling,Implement authentication"
```

### Updating Documentation

```bash
# Update the journal
python src/hooks/automation_cli.py journal --title "WebSocket Implementation" --content "Implemented WebSocket client with reconnection logic and error handling."

# Update the frontend plan
python src/hooks/automation_cli.py frontend --section "Real-time Components" --content "- WebSocketProvider\n- DataStreamHook\n- RealtimeChartComponent"

# Update the architecture analysis
python src/hooks/automation_cli.py architecture --section "WebSocket Integration" --content "The WebSocket integration provides real-time data streaming..."
```

### Managing Tasks

```bash
# Add a new task
python src/hooks/automation_cli.py task-add --category frontend --name "Implement Error Handling" --description "Add error handling to WebSocket client" --priority high

# Update task status
python src/hooks/automation_cli.py task-update --task-id fe-001 --status in_progress

# Set current focus
python src/hooks/automation_cli.py task-focus --category frontend --task-id fe-001

# List tasks
python src/hooks/automation_cli.py task-list
```

## Recovering from Copilot Rate Limits

When GitHub Copilot hits rate limits, the pre-commit hook system helps maintain state and continue development seamlessly. Here's the recommended workflow:

### Before Rate Limit

Always make sure to update the session state and log changes before you might hit a rate limit:

```bash
# Update session state
python src/hooks/automation_cli.py session --active-components "WebSocket" --last-component "WebSocketClient" --current-phase "Error Handling"

# Log changes
python src/hooks/automation_cli.py log --components "WebSocket" --changes "Implemented reconnection logic" --next-actions "Add error handling"
```

### After Rate Limit

When starting a new Copilot session after a rate limit, use these commands to recover context:

```bash
# Check current session state
cat src/docs/copilot_session.md

# List current tasks
python src/hooks/automation_cli.py task-list

# Check change log
cat src/docs/changes.log
```

This will give you the context needed to continue development from where you left off.

## Best Practices for Copilot

### Logging Context

- Always update the session state after completing major changes
- Log all changes with detailed descriptions
- Update the progress tracker regularly

### Documentation Updates

- Keep the journal updated with timestamped entries
- Update the frontend plan when design changes occur
- Update the architecture documentation when system design changes

### Task Management

- Keep the task list updated with current status
- Set the current focus to the task being worked on
- Mark tasks as completed when finished

## File Locations

The system maintains several important files:

- `src/docs/copilot_session.md` - Current session state and context
- `src/docs/changes.log` - Log of all changes made to the codebase
- `src/docs/journal.md` - Development journal with timestamped entries
- `src/docs/FRONTEND_DEV_PLAN.md` - Frontend development plan
- `src/docs/ARCHITECTURE_ANALYSIS.md` - Architecture analysis and documentation
- `src/docs/tasks.json` - Task definitions and status
- `src/docs/progress.md` - Human-readable progress report

## Automation Command Reference

### Session Management

```
python src/hooks/automation_cli.py session [options]
  --active-components COMPONENTS    Comma-separated list of active components
  --pending-tasks TASKS             Comma-separated list of pending tasks
  --completed-tasks TASKS           Comma-separated list of completed tasks
  --priority PRIORITY               Next priority task
  --dependencies DEPENDENCIES       Comma-separated list of dependencies
  --current-phase PHASE             Current development phase
  --active-branch BRANCH            Active git branch
  --last-component COMPONENT        Last component worked on
```

### Change Logging

```
python src/hooks/automation_cli.py log [options]
  --components COMPONENTS           Comma-separated list of modified components
  --changes CHANGES                 Comma-separated list of changes made
  --next-actions ACTIONS            Comma-separated list of next actions
```

### Documentation Updates

```
python src/hooks/automation_cli.py journal [options]
  --title TITLE                     Entry title
  --content CONTENT                 Entry content
  --content-file FILE               File containing entry content

python src/hooks/automation_cli.py frontend [options]
  --section SECTION                 Section to update
  --content CONTENT                 Section content
  --content-file FILE               File containing section content

python src/hooks/automation_cli.py architecture [options]
  --section SECTION                 Section to update
  --content CONTENT                 Section content
  --content-file FILE               File containing section content
```

### Task Management

```
python src/hooks/automation_cli.py task-add [options]
  --category CATEGORY               Task category
  --name NAME                       Task name
  --description DESCRIPTION         Task description
  --priority PRIORITY               Task priority (low, medium, high)
  --dependencies DEPENDENCIES       Comma-separated list of task dependencies

python src/hooks/automation_cli.py task-update [options]
  --task-id ID                      Task ID
  --status STATUS                   Task status (pending, in_progress, completed, blocked)

python src/hooks/automation_cli.py task-focus [options]
  --category CATEGORY               Task category
  --task-id ID                      Task ID

python src/hooks/automation_cli.py task-list [options]
  --count COUNT                     Number of tasks to list (default: 5)
```

## Running the Pre-commit Hook Manually

You can run the pre-commit hook manually with:

```bash
python src/hooks/automation_cli.py run-hook
```

This will execute the pre-commit hook, updating all documentation and logging changes.

## Summary

This pre-commit hook system provides a robust way for GitHub Copilot to maintain development context between sessions, especially when rate limits are hit. By regularly updating the session state, logging changes, and tracking tasks, development can continue seamlessly even after interruptions.