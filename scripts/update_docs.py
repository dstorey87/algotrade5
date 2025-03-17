#!/usr/bin/env python3
import os
import sys
from datetime import datetime
import json
import re
from pathlib import Path

def update_frontend_dev_plan(changed_files):
    """Update FRONTEND_DEV_PLAN.md based on frontend changes"""
    frontend_plan_path = Path("frontend/FRONTEND_DEV_PLAN.md")
    if not frontend_plan_path.exists():
        return
    
    with open(frontend_plan_path, 'r') as f:
        content = f.read()
    
    # Update current status section
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_changes = f"\n## Latest Updates - {timestamp}\n"
    for file in changed_files:
        if file.startswith('frontend/'):
            new_changes += f"- Updated {file}\n"
    
    # Insert new changes before ## Current Status section
    if "## Current Status" in content:
        content = content.replace("## Current Status", new_changes + "\n## Current Status")
    else:
        content += new_changes
    
    with open(frontend_plan_path, 'w') as f:
        f.write(content)

def update_architecture_analysis(changed_files):
    """Update ARCHITECTURE_ANALYSIS.md based on architectural changes"""
    arch_path = Path("src/docs/ARCHITECTURE_ANALYSIS.md")
    if not arch_path.exists():
        return
    
    with open(arch_path, 'r') as f:
        content = f.read()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_changes = f"\n### Architecture Updates - {timestamp}\n"
    for file in changed_files:
        if any(p in file for p in ['src/', 'config/', 'data/']):
            new_changes += f"- Modified {file}\n"
    
    # Add to Future Architecture section
    if "## Future Architecture" in content:
        content = content.replace("## Future Architecture", new_changes + "\n## Future Architecture")
    else:
        content += new_changes
    
    with open(arch_path, 'w') as f:
        f.write(content)

def update_development_journal(changed_files):
    """Update journal.md with latest changes"""
    journal_path = Path("src/docs/journal.md")
    if not journal_path.exists():
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    with open(journal_path, 'a') as f:
        f.write(f"\n## Development Update - {timestamp}\n\n")
        f.write("### Changes Made\n")
        for file in changed_files:
            f.write(f"- Modified {file}\n")

def update_copilot_session(changed_files):
    """Update copilot_interface.md with latest context"""
    interface_path = Path("copilot_interface.md")
    if not interface_path.exists():
        return
    
    with open(interface_path, 'r') as f:
        content = f.read()
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Update Recent Changes table
    changes_table = "\n### Recent Changes\n| Date       | Component    | Status    |\n|------------|-------------|-----------|"
    for file in changed_files:
        component = file.split('/')[0]
        changes_table += f"\n| {timestamp} | {component:<11} | Updated   |"
    
    # Replace or append changes table
    if "### Recent Changes" in content:
        pattern = r"### Recent Changes.*?(?=\n##|\Z)"
        content = re.sub(pattern, changes_table, content, flags=re.DOTALL)
    else:
        content += "\n" + changes_table
    
    with open(interface_path, 'w') as f:
        f.write(content)

def main():
    """Main function to update all documentation files"""
    # Get changed files from git
    import subprocess
    result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                          capture_output=True, text=True)
    changed_files = result.stdout.splitlines()
    
    if not changed_files:
        return 0
    
    try:
        update_frontend_dev_plan(changed_files)
        update_architecture_analysis(changed_files)
        update_development_journal(changed_files)
        update_copilot_session(changed_files)
        
        # Stage the updated documentation files
        docs_to_stage = [
            'frontend/FRONTEND_DEV_PLAN.md',
            'src/docs/ARCHITECTURE_ANALYSIS.md',
            'src/docs/journal.md',
            'copilot_interface.md'
        ]
        for doc in docs_to_stage:
            if Path(doc).exists():
                subprocess.run(['git', 'add', doc])
        
        return 0
    except Exception as e:
        print(f"Error updating documentation: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())