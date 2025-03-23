#!/usr/bin/env python3
"""
AlgoTradePro5 Vulture Cleanup Script

A targeted script to clean up unused code using Vulture.
This script:
1. Scans for unused code using Vulture
2. Automatically removes or comments out unused code
3. Creates a backup of modified files

Usage:
    python vulture_cleanup.py [--min-confidence 60] [--comment-only] [--review-first] [--threads NUM_THREADS]
"""

import os
import sys
import re
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Set, Tuple
import datetime
import concurrent.futures
import multiprocessing

# Directory to store backups
BACKUP_DIR = Path("code_backup_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

# Files/directories to exclude from scanning (synchronized with code_cleaner.py)
EXCLUDED_DIRS = [
    # Python & Cache
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    
    # Version Control
    ".git",
    
    # Virtual Environments
    ".env",
    "venv",
    "ENV",
    ".venv",
    
    # Distribution & Packaging
    "dist",
    "build",
    "*.egg-info",
    
    # Dependencies
    "node_modules",
    "dependencies",
    
    # Data, Logs & Databases
    "logs",
    "log_dir",
    "data",
    "data_dir",
    "user_data",
    "databases",
    
    # Models and AI directories
    "models",
    "aimodels",
    "models/llm",
    "models/ml",
    
    # IDE & Editor
    ".vscode",
    ".idea",
    
    # Project-specific directories
    os.path.join("docker", "programdata"),
    "plot",
    "backtest_results",
    "hyperopt_results",
    ".next",
    
    # Custom directories to exclude
    "*_backup",
    "temp",
    "tmp",
    "archive"
]

# Files to exclude from scanning, expanded from .gitignore
EXCLUDED_FILES = [
    # Python
    "*.py[cod]",
    "*$py.class",
    "*.so",
    
    # Distribution
    "*.egg",
    
    # Data & Logs
    "*.log",
    "*.db",
    "*.sqlite*",
    
    # Model files
    "*.pkl",
    "*.h5",
    "*.pt",
    "*.pth",
    "*.onnx",
    "*.pb",
    "*.tflite",
    "*.savedmodel",
    "*.weights",
    "*.bin",
    "*.hdf5",
    "*.safetensors*",
    
    # Config & Sensitive files
    "*.env",
    "*.key",
    "*.pem",
    "*credentials*",
    "*secret*",
    "*password*",
    "*token*",
    "*config.json",
    "special_tokens_map.json",
    "tokenizer*.json",
    "added_tokens.json",
    "adapter_config.json",
    "generation_config.json",
    "quantize_config.json",
    
    # Package files
    "package-lock.json",
    
    # Temp & Backup
    "*.tmp",
    "*_backup",
    "*.swp"
]

# Get the project root directory
PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))

# Default to number of CPU cores for parallelism
DEFAULT_THREADS = max(1, multiprocessing.cpu_count())

def is_path_excluded(path: Path, exclude_dirs: List[str]) -> bool:
    """Check if a path should be excluded based on any part of its path"""
    # Convert path to parts for comparison
    path_parts = path.parts
    
    # Check if any part of the path matches an excluded dir
    for exclude_dir in exclude_dirs:
        exclude_parts = Path(exclude_dir).parts
        
        # Check if the exclude pattern appears anywhere in the path
        for i in range(len(path_parts) - len(exclude_parts) + 1):
            if path_parts[i:i+len(exclude_parts)] == exclude_parts:
                return True
    return False

def get_python_files(exclude_dirs: List[str] = None, exclude_files: List[str] = None) -> List[Path]:
    """Get all Python files in the project that aren't in excluded directories"""
    if exclude_dirs is None:
        exclude_dirs = EXCLUDED_DIRS
    if exclude_files is None:
        exclude_files = EXCLUDED_FILES
        
    python_files = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip excluded directories by modifying dirs in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not is_path_excluded(Path(os.path.join(root, d)), exclude_dirs)]
        
        for file in files:
            if file.endswith('.py'):
                file_path = Path(os.path.join(root, file))
                
                # Skip excluded files based on filename patterns
                if not any(re.match(pattern.replace('*', '.*'), file) for pattern in exclude_files if '*' in pattern):
                    python_files.append(file_path)
    
    print(f"Found {len(python_files)} Python files to scan")
    return python_files

def backup_file(file_path: Path):
    """Create a backup of a file before modifying it"""
    # Ensure file_path is absolute
    file_path = Path(os.path.abspath(file_path))
    
    # Make sure PROJECT_ROOT is absolute
    project_root_abs = Path(os.path.abspath(PROJECT_ROOT))
    
    # Get the relative path only if file_path is within PROJECT_ROOT
    try:
        rel_path = file_path.relative_to(project_root_abs)
        backup_path = BACKUP_DIR / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path
    except ValueError:
        # If file_path is not within PROJECT_ROOT, use a flattened path
        logger.warning(f"File {file_path} is not within project root {project_root_abs}")
        # Create a safe filename by replacing path separators
        safe_name = str(file_path).replace(os.path.sep, '_').replace(':', '_')
        backup_path = BACKUP_DIR / safe_name
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)
        return backup_path

def run_vulture(python_files: List[Path], min_confidence: int, num_threads: int = DEFAULT_THREADS) -> List[Dict]:
    """Run vulture on Python files to find unused code"""
    print(f"Scanning for unused code with confidence level >= {min_confidence}%...")
    print(f"Using {num_threads} threads for parallel processing")
    
    unused_items = []
    # Lock to prevent race conditions when appending to shared list
    items_lock = multiprocessing.Lock()
    
    def process_file(file_path):
        cmd = [
            "vulture",
            "--min-confidence", str(min_confidence),
            str(file_path)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            file_items = []
            if result.stdout:
                for line in result.stdout.splitlines():
                    # First pattern with confidence
                    match1 = re.match(r'(.+):(\d+): (.+) \((\d+)% confidence\)', line)
                    # Second pattern without confidence
                    match2 = re.match(r'(.+):(\d+): (.+)', line)
                    
                    match = match1 or match2
                    if match:
                        groups = match.groups()
                        
                        # Extract data based on which pattern matched
                        file_path = groups[0]
                        line_num = int(groups[1])
                        description = groups[2]
                        confidence = int(groups[3]) if len(groups) > 3 else min_confidence
                        
                        # Skip common false positives
                        if any(skip in description.lower() for skip in [
                            "__init__",
                            "__str__",
                            "__repr__",
                            "test_",
                            "pytest"
                        ]):
                            continue
                            
                        file_items.append({
                            "file": file_path,
                            "line": line_num,
                            "description": description,
                            "confidence": confidence
                        })
            
            # Acquire lock before updating shared list
            with items_lock:
                unused_items.extend(file_items)
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Using list to force execution
        list(executor.map(process_file, python_files))
    
    # Sort by file and line number
    unused_items.sort(key=lambda x: (x["file"], x["line"]))
    
    print(f"Found {len(unused_items)} unused code items")
    return unused_items

def get_full_element_range(file_path: str, line_number: int) -> Tuple[int, int]:
    """
    Get the full range (start and end line) of a code element (function, class, variable)
    This is important to remove the entire element, not just the line where it's defined
    """
    try:
        import ast
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # If there's a syntax error, just return the single line
            return line_number, line_number
            
        # Find the node that contains the line number
        for node in ast.walk(tree):
            # Only check nodes that have line number attributes
            if hasattr(node, 'lineno'):
                if node.lineno == line_number:
                    # Use getattr with default for Python versions that don't have end_lineno
                    end_line = getattr(node, 'end_lineno', line_number)
                    return node.lineno, end_line
                    
        # If no exact match found, return just the single line
        return line_number, line_number
    except Exception as e:
        # In case of any error, just return the single line
        print(f"Error analyzing code structure: {e}")
        return line_number, line_number

def review_unused_items(unused_items: List[Dict]) -> List[Dict]:
    """Present each unused item to the user for review"""
    approved_items = []
    
    print("\nReviewing unused code items. For each item, decide whether to remove/comment:")
    
    for i, item in enumerate(unused_items):
        file_path = item["file"]
        line_num = item["line"]
        desc = item["description"]
        confidence = item["confidence"]
        
        # Read the file to show context
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Get full range of the element
            start_line, end_line = get_full_element_range(file_path, line_num)
            
            # Calculate context range (3 lines before and after)
            context_start = max(0, start_line - 4)
            context_end = min(len(lines), end_line + 3)
            
            # Display context
            print(f"\n[{i+1}/{len(unused_items)}] {file_path}:{line_num} - {desc} ({confidence}% confidence)")
            print("-" * 50)
            
            for j in range(context_start, context_end):
                prefix = "→ " if context_start <= j < context_end and start_line - 1 <= j <= end_line - 1 else "  "
                print(f"{prefix}{j+1}: {lines[j].rstrip()}")
            
            print("-" * 50)
            
            # Ask for confirmation
            response = input("Remove/comment this code? [y/n/q]: ").lower()
            
            if response == 'y':
                approved_items.append(item)
            elif response == 'q':
                print("Review aborted. Exiting.")
                break
                
        except Exception as e:
            print(f"Error reviewing {file_path}: {e}")
    
    return approved_items

def clean_unused_code(unused_items: List[Dict], comment_only: bool = True) -> int:
    """Clean unused code by either commenting or removing it"""
    if not unused_items:
        return 0
    
    fixed_count = 0
    
    # First create the backup directory if it doesn't exist
    if not BACKUP_DIR.exists():
        BACKUP_DIR.mkdir(parents=True)
        print(f"Created backup directory: {BACKUP_DIR}")
    
    # Ensure PROJECT_ROOT is absolute
    project_root_abs = Path(os.path.abspath(PROJECT_ROOT))
    
    # Group items by file for efficiency
    file_items = {}
    for item in unused_items:
        file_path = item["file"]
        if file_path not in file_items:
            file_items[file_path] = []
        file_items[file_path].append(item)
    
    action = "Commenting" if comment_only else "Removing"
    print(f"{action} {len(unused_items)} unused code items in {len(file_items)} files...")
    
    for file_path, items in file_items.items():
        try:
            # Normalize the file path to absolute
            abs_file_path = os.path.abspath(file_path)
            
            # Ensure file exists 
            if not os.path.exists(abs_file_path):
                print(f"Warning: File not found: {abs_file_path}")
                continue
                
            # Create backup
            backup_path = backup_file(Path(abs_file_path))
            
            with open(abs_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Sort items by line number in reverse order to avoid index shifts
            items.sort(key=lambda x: x["line"], reverse=True)
            
            modified = False
            for item in items:
                line_idx = item["line"] - 1
                
                if line_idx >= len(lines):
                    continue
                    
                # Get full range of the element
                start_line, end_line = get_full_element_range(abs_file_path, item["line"])
                
                # Adjust for 0-based indexing
                start_idx = start_line - 1
                end_idx = end_line - 1
                
                if comment_only:
                    # Comment out the lines
                    for i in range(start_idx, end_idx + 1):
                        if i < len(lines):
                            lines[i] = f"# REMOVED_UNUSED_CODE: {lines[i]}"
                else:
                    # Remove the lines
                    for i in range(end_idx, start_idx - 1, -1):
                        if i < len(lines):
                            lines.pop(i)
                    
                    # Add a comment about what was removed
                    if start_idx < len(lines):
                        lines.insert(start_idx, f"# REMOVED_UNUSED_CODE: {item['description']} (was at line {item['line']})\n")
                
                modified = True
                fixed_count += 1
            
            if modified:
                with open(abs_file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                print(f"Fixed {len(items)} unused code items in {abs_file_path}")
                print(f"Backup saved to {backup_path}")
        
        except ValueError as ve:
            # Specific handling for path-related errors
            print(f"Path error cleaning {file_path}: {ve}")
        except Exception as e:
            print(f"Error cleaning {file_path}: {e}")
    
    return fixed_count

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AlgoTradePro5 Vulture Cleanup")
    parser.add_argument("--min-confidence", type=int, default=60, 
                        help="Minimum confidence percentage (default: 60)")
    parser.add_argument("--comment-only", action="store_true", 
                        help="Comment out unused code instead of removing it")
    parser.add_argument("--review-first", action="store_true", 
                        help="Review each unused item before cleaning")
    parser.add_argument("--threads", type=int, default=DEFAULT_THREADS, 
                        help="Number of threads to use for scanning (default: number of CPU cores)")
    
    args = parser.parse_args()
    
    # Get all Python files
    print(f"Starting vulture scan with {args.threads} threads")
    python_files = get_python_files(EXCLUDED_DIRS)
    
    # Run vulture to find unused code
    unused_items = run_vulture(python_files, args.min_confidence, args.threads)
    
    if not unused_items:
        print("No unused code found. Exiting.")
        return
    
    # Review items if requested
    if args.review_first:
        approved_items = review_unused_items(unused_items)
        print(f"\nApproved {len(approved_items)} out of {len(unused_items)} items for cleanup")
        unused_items = approved_items
    
    # Clean unused code
    fixed_count = clean_unused_code(unused_items, args.comment_only)
    
    print(f"\nSummary:")
    print(f"- Files scanned: {len(python_files)}")
    print(f"- Unused items found: {len(unused_items)}")
    print(f"- Items {'commented' if args.comment_only else 'removed'}: {fixed_count}")
    print(f"- Backup directory: {BACKUP_DIR}")
    print(f"- Threads used: {args.threads}")
    print(f"- Time per file: {len(python_files)/args.threads:.2f} files per thread")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCleanup interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)