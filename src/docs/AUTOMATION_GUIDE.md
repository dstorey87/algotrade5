# AlgoTradePro5 Automation System Guide

This document explains how to use the automation system for AlgoTradePro5, particularly for GitHub Copilot to maintain development state between sessions when rate limits are hit.

## Overview

The automation system consists of several components:

1. **Pre-commit Hook** - Automatically validates and updates documentation before each commit
2. **Task Manager** - Tracks development tasks and progress
3. **Session Tracker** - Maintains state between Copilot sessions
4. **Documentation Updater** - Automates updates to documentation files

## Getting Started

### Installation

1. Install the pre-commit hook:

```bash
python src/install_pre_commit.py
```

2. Verify the installation:

```bash
python src/test_pre_commit.py
```

## Using the Automation System

The main entry point for the automation system is `src/automation.py`. This script provides a command-line interface for all automation tasks.

### Managing Tasks

```bash
# Add a new task
python src/automation.py tasks --add --category frontend --name "Implement WebSocket Client" --description "Create WebSocket client for real-time data" --priority high

# Update task status
python src/automation.py tasks --update --task-id fe-001 --status in_progress

# Set current focus
python src/automation.py tasks --focus --category frontend --task-id fe-001

# List tasks
python src/automation.py tasks --list
```

### Updating Documentation

```bash
# Update architecture documentation
python src/automation.py docs --architecture "Real-time Data System" --file real_time_docs.md

# Update frontend plan
python src/automation.py docs --frontend --content '{"Real-time Components": {"Core Components": ["WebSocketProvider"]}}'

# Add journal entry
python src/automation.py docs --journal "WebSocket Implementation" --file journal_entry.json

# Log changes
python src/automation.py docs --log-changes --components "WebSocket,Frontend" --changes "Added WebSocket implementation" --next-actions "Implement error handling"
```

### Maintaining Session State

```bash
# Update session state
python src/automation.py session --active-components "WebSocket,Frontend" --pending-tasks "Implement error handling" --priority "Error Handling" --current-phase "Frontend Development"
```

## For GitHub Copilot: Maintaining State Between Sessions

When GitHub Copilot hits rate limits, it's essential to preserve the development context. The automation system helps with this through two key mechanisms:

### 1. Session State Management

The session state is stored in `src/docs/copilot_session.md`. This file contains:

- Active components being worked on
- Pending tasks
- Completed tasks
- Next priority
- Dependencies
- Current phase
- Active branch
- Last component worked on

GitHub Copilot should update this file before ending a session, and read it at the start of a new session.

Example session state update:

```bash
python src/automation.py session --active-components "WebSocket,Frontend" --pending-tasks "Error handling,Authentication" --completed-tasks "Basic WebSocket setup" --priority "Error Handling" --current-phase "Frontend Development" --active-branch "feature/websocket" --last-component "WebSocketProvider"
```

### 2. Task Management

The task management system keeps track of all development tasks in `src/docs/tasks.json` and provides a human-readable view in `src/docs/progress.md`.

GitHub Copilot should:
1. Check the current focus task at the start of a session
2. Update task status as work progresses
3. Set the focus to the next task when the current one is completed

```bash
# Check current tasks
python src/automation.py tasks --list

# Mark task as in progress
python src/automation.py tasks --update --task-id fe-001 --status in_progress

# Mark task as completed
python src/automation.py tasks --update --task-id fe-001 --status completed

# Focus on next task
python src/automation.py tasks --focus --category frontend --task-id fe-002
```

### 3. Logging Changes

All changes should be logged to maintain a clear history of development:

```bash
python src/automation.py docs --log-changes --components "WebSocket" --changes "Implemented reconnection logic" --next-actions "Add error handling"
```

### 4. Updating Documentation

Documentation should be kept up-to-date with each development session:

```bash
# Update journal
python src/automation.py docs --journal "WebSocket Implementation" --content '[{"type": "subsection", "title": "Reconnection Logic", "items": ["Implemented exponential backoff", "Added connection state management"], "completed": true}]'

# Update architecture docs
python src/automation.py docs --architecture "Real-time Data System" --content "Updated WebSocket implementation with reconnection logic"

# Update frontend plan
python src/automation.py docs --frontend --content '{"Real-time Components": {"Implementation Status": "In Progress"}}'
```

## Best Practices for GitHub Copilot

1. **Start Each Session with Context**:
   ```bash
   python src/automation.py tasks --list
   ```

2. **Update Session State Regularly**:
   ```bash
   python src/automation.py session --active-components "..." --current-phase "..." --last-component "..."
   ```

3. **Log All Changes**:
   ```bash
   python src/automation.py docs --log-changes --components "..." --changes "..." --next-actions "..."
   ```

4. **Update Task Status**:
   ```bash
   python src/automation.py tasks --update --task-id "..." --status "..."
   ```

5. **End Each Session with Clear Continuation Point**:
   ```bash
   python src/automation.py session --priority "Next task to work on" --last-component "Last component worked on"
   ```

By following these practices, GitHub Copilot can maintain development context even when sessions are interrupted by rate limits, ensuring smooth and continuous development of AlgoTradePro5.