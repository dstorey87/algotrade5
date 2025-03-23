#!/usr/bin/env python3
"""
AlgoTradePro5 Code Cleaner

A comprehensive tool to continuously monitor and clean the codebase:
1. Find and remove unused code (Vulture)
2. Detect and prevent circular imports (pydeps)
3. Find duplicate code
4. Format imports (isort)
5. Check code quality (pylint)
6. Run continuously (watchdog)

Usage:
    python code_cleaner.py [--clean] [--watch]
"""

import os
import sys
import time
import re
import argparse
import subprocess
import shutil
import glob
import logging
from pathlib import Path
import importlib
from typing import List, Set, Dict, Tuple, Optional
import ast
import hashlib

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("code_cleaner.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("CodeCleaner")

# Project configuration
PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = PROJECT_ROOT / ".env"

# Directories to exclude from scanning
EXCLUDED_DIRS = [
    ".git", 
    ".venv", 
    "venv",
    "env",
    "__pycache__", 
    "node_modules",
    "models",
    "log_dir",docker-compose up -d --build freqai
PS C:\AlgoTradPro5> docker-compose up -d --build freqai
WARNING: Error parsing config file (C:\Users\darre\.docker\config.json): json: cannot unmarshal number into Go value of type configfile.ConfigFile
Compose now can delegate build to bake for better performances
Just set COMPOSE_BAKE=true
#0 building with "default" instance using docker driver

#1 [freqai internal] load build definition from Dockerfile.freqai
#1 transferring dockerfile: 603B 0.1s done
#1 DONE 0.1s

#2 [freqai internal] load metadata for docker.io/library/python:3.11-slim
#2 ...

#3 [freqai auth] library/python:pull token for registry-1.docker.io
#3 DONE 0.0s

#2 [freqai internal] load metadata for docker.io/library/python:3.11-slim
#2 DONE 1.7s

#4 [freqai internal] load .dockerignore
#4 transferring context: 3.27kB done
#4 DONE 0.0s

#5 [freqai 1/7] FROM docker.io/library/python:3.11-slim@sha256:7029b00486ac40bed03e36775b864d3f3d39dcbdf19cd45e6a52d541e6c178f0
#5 DONE 0.0s

#6 [freqai 2/7] WORKDIR /app
#6 CACHED

#7 [freqai internal] load build context
#7 transferring context: 45B 0.0s done
#7 DONE 0.1s

#8 [freqai 3/7] RUN apt-get update && apt-get install -y     build-essential     git     && rm -rf /var/lib/apt/lists/*
#8 ...

#9 [freqai 4/7] COPY requirements-freqai.txt .
#9 CACHED

#10 [freqai 5/7] RUN pip install -r requirements-freqai.txt
#10 CACHED

#11 [freqai 7/7] COPY ./src/freqai_service.py /app/src/
#11 ERROR: failed to calculate checksum of ref 6e04d618-cb39-4ea9-998e-192d09f8966d::cnwoa9n4it35nkcpjj2knc8xk: "/src/freqai_service.py": not found

#12 [freqai 6/7] COPY ./src/freqai_interface.py /app/src/
#12 ERROR: failed to calculate checksum of ref 6e04d618-cb39-4ea9-998e-192d09f8966d::cnwoa9n4it35nkcpjj2knc8xk: "/src/freqai_interface.py": not found

#8 [freqai 3/7] RUN apt-get update && apt-get install -y     build-essential     git     && rm -rf /var/lib/apt/lists/*
#8 CANCELED
------
 > [freqai 6/7] COPY ./src/freqai_interface.py /app/src/:
------
------
 > [freqai 7/7] COPY ./src/freqai_service.py /app/src/:
------
failed to solve: failed to compute cache key: failed to calculate checksum of ref 6e04d618-cb39-4ea9-998e-192d09f8966d::cnwoa9n4it35nkcpjj2knc8xk: "/src/freqa
i_service.py": not found                                                                                                                                      
    "docker/programdata",
    "site-packages",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache"
]

# Files to exclude from scanning
EXCLUDED_FILES = [
    "*.pyc", 
    "*.pyo", 
    "*.mo", 
    "*.o", 
    "*.so", 
    "*.egg", 
    "*.log", 
    "*.db",
    "*.pkl",
    "*.model",
    "*.pt",
    "*.bin",
    "*.h5",
    "*.hdf5",
    "*.feather",
    "*.parquet",
    ".DS_Store",
    "Thumbs.db",
    "*.lock"
]

# Global counters for statistics
STATS = {
    "unused_code": 0,
    "circular_imports": 0,
    "duplicate_code": 0,
    "import_issues": 0,
    "quality_issues": 0,
    "files_scanned": 0
}

def load_environment_vars():
    """Load environment variables from .env file"""
    if not ENV_FILE.exists():
        return
    
    with open(ENV_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)
            os.environ[key.strip()] = value.strip().strip('"\'')

def get_python_files(exclude_dirs: List[str] = None, exclude_files: List[str] = None) -> List[Path]:
    """Get all Python files in the project, respecting exclusions"""
    if exclude_dirs is None:
        exclude_dirs = EXCLUDED_DIRS
    if exclude_files is None:
        exclude_files = EXCLUDED_FILES
    
    python_files = []
    
    # Build the exclude pattern for glob
    exclude_patterns = []
    for pattern in exclude_files:
        exclude_patterns.append(f"**/{pattern}")
        
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.py'):
                file_path = Path(os.path.join(root, file))
                
                # Check if file matches any exclude pattern
                exclude = False
                for pattern in exclude_patterns:
                    if file_path.match(pattern):
                        exclude = True
                        break
                
                if not exclude:
                    python_files.append(file_path)
    
    return python_files

def check_unused_code(python_files: List[Path], min_confidence: int = 80) -> List[Dict]:
    """Use Vulture to find unused code"""
    logger.info("Checking for unused code with Vulture...")
    unused_items = []
    
    # Create a temporary file with all Python file paths
    temp_file = PROJECT_ROOT / "temp_files.txt"
    with open(temp_file, 'w') as f:
        for file_path in python_files:
            f.write(f"{file_path}\n")
    
    try:
        # Run vulture with the file containing paths
        result = subprocess.run(
            ["vulture", "--min-confidence", str(min_confidence), f"@{temp_file}"],
            capture_output=True,
            text=True
        )
        
        # Parse vulture output
        if result.stdout:
            for line in result.stdout.splitlines():
                match = re.match(r'(.+):(\d+): (.+) \((\d+)% confidence\)', line)
                if match:
                    file_path, line_num, description, confidence = match.groups()
                    unused_items.append({
                        "file": file_path,
                        "line": int(line_num),
                        "description": description,
                        "confidence": int(confidence)
                    })
        
        STATS["unused_code"] = len(unused_items)
        logger.info(f"Found {len(unused_items)} unused code items")
    except Exception as e:
        logger.error(f"Error checking unused code: {e}")
    finally:
        # Clean up temporary file
        if temp_file.exists():
            temp_file.unlink()
    
    return unused_items

def read_file_with_fallback_encoding(file_path: Path) -> str:
    """Read a file with fallback encodings if UTF-8 fails"""
    encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, skip the file
    raise UnicodeDecodeError(f"Failed to decode {file_path} with any encoding")

def detect_circular_imports(python_files: List[Path]) -> List[Dict]:
    """Detect circular imports using a custom implementation"""
    logger.info("Checking for circular imports...")
    circular_imports = []
    
    # Build import graph
    graph = {}
    
    for file_path in python_files:
        try:
            # Use short relative paths to avoid Windows path length issues
            rel_path = file_path.relative_to(PROJECT_ROOT)
            module_name = str(rel_path).replace('\\', '.').replace('/', '.').replace('.py', '')
            
            try:
                file_content = read_file_with_fallback_encoding(file_path)
                tree = ast.parse(file_content)
            except UnicodeDecodeError:
                logger.warning(f"Skipping {file_path} due to encoding issues")
                continue
            except Exception as e:
                logger.error(f"Error parsing {file_path}: {e}")
                continue
            
            # Track imports for this module
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)
            
            graph[module_name] = imports
            
        except Exception as e:
            logger.error(f"Error analyzing imports in {file_path}: {e}")
            continue
    
    # Find cycles using DFS
    def find_cycle(node: str, visited: Set[str], path: List[str]) -> Optional[List[str]]:
        if node in path:
            # Found a cycle
            cycle_start = path.index(node)
            return path[cycle_start:]
        
        if node in visited:
            return None
        
        visited.add(node)
        path.append(node)
        
        if node in graph:
            for neighbor in graph[node]:
                cycle = find_cycle(neighbor, visited, path.copy())
                if cycle:
                    return cycle
        
        return None
    
    # Check each node for cycles
    visited = set()
    for node in graph:
        if node not in visited:
            cycle = find_cycle(node, visited, [])
            if cycle:
                circular_imports.append({
                    "modules": cycle,
                    "description": " -> ".join(cycle)
                })
    
    STATS["circular_imports"] = len(circular_imports)
    logger.info(f"Found {len(circular_imports)} circular import chains")
    return circular_imports

def check_import_issues(python_files: List[Path]) -> List[Dict]:
    """Check for import issues (missing imports, unused imports)"""
    logger.info("Checking for import issues...")
    import_issues = []
    
    for file_path in python_files:
        try:
            # First validate file syntax
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    ast.parse(f.read())
            except SyntaxError:
                logger.warning(f"Skipping {file_path} due to syntax errors")
                continue
            
            # Increased timeout to 30 seconds per file
            timeout_seconds = 30
            
            # Run isort check with timeout
            try:
                result = subprocess.run(
                    ["isort", "--check", "--diff", str(file_path)],
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds
                )
                
                if result.returncode != 0:
                    import_issues.append({
                        "file": str(file_path),
                        "type": "unsorted_imports",
                        "description": "Imports are not properly sorted"
                    })
            except subprocess.TimeoutExpired:
                logger.warning(f"isort check timed out for {file_path}")
            except Exception as e:
                logger.error(f"Error running isort on {file_path}: {e}")
            
            # Check for unused imports with pyflakes (with timeout)
            try:
                result = subprocess.run(
                    ["python", "-m", "pyflakes", str(file_path)],
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds
                )
                
                for line in result.stdout.splitlines():
                    if "imported but unused" in line or "undefined name" in line:
                        match = re.match(r'(.+?):(\d+):(\d+): (.*)', line)
                        if match:
                            _, line_num, _, message = match.groups()
                            import_issues.append({
                                "file": str(file_path),
                                "line": int(line_num),
                                "type": "import_issue",
                                "description": message
                            })
            except subprocess.TimeoutExpired:
                logger.warning(f"pyflakes check timed out for {file_path}")
            except Exception as e:
                logger.error(f"Error running pyflakes on {file_path}: {e}")
                
        except Exception as e:
            logger.error(f"Error checking import issues in {file_path}: {e}")
            continue
    
    STATS["import_issues"] = len(import_issues)
    logger.info(f"Found {len(import_issues)} import issues")
    return import_issues

def find_duplicate_code(python_files: List[Path], min_lines: int = 3) -> List[Dict]:
    """Find duplicate code blocks using a simple token-based approach"""
    logger.info(f"Finding duplicate code (minimum {min_lines} lines)...")
    duplicate_blocks = []
    
    # Store code blocks by their hash
    hashes = {}
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file with AST to avoid comments and whitespace
            tree = ast.parse(content)
            
            # Get line numbers for each node
            code_blocks = []
            for node in ast.walk(tree):
                if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                    # Only consider blocks of sufficient size
                    if node.end_lineno - node.lineno + 1 >= min_lines:
                        lines = content.splitlines()[node.lineno-1:node.end_lineno]
                        block_content = '\n'.join(lines)
                        
                        # Skip very small blocks
                        if len(block_content) < 30:
                            continue
                        
                        # Create a hash of the code block
                        block_hash = hashlib.md5(block_content.encode()).hexdigest()
                        
                        code_blocks.append({
                            "file": str(file_path),
                            "start_line": node.lineno,
                            "end_line": node.end_lineno,
                            "content": block_content,
                            "hash": block_hash
                        })
            
            # Add blocks to the hash dictionary
            for block in code_blocks:
                if block["hash"] in hashes:
                    hashes[block["hash"]].append(block)
                else:
                    hashes[block["hash"]] = [block]
                    
        except Exception as e:
            logger.error(f"Error finding duplicate code in {file_path}: {e}")
    
    # Find duplicates
    for block_hash, blocks in hashes.items():
        if len(blocks) > 1:
            # Only report each set of duplicates once
            duplicate_blocks.append({
                "hash": block_hash,
                "instances": blocks,
                "size": len(blocks[0]["content"].splitlines())
            })
    
    STATS["duplicate_code"] = len(duplicate_blocks)
    logger.info(f"Found {len(duplicate_blocks)} sets of duplicate code")
    return duplicate_blocks

def clean_unused_code(unused_items: List[Dict], auto_fix: bool = False) -> int:
    """Clean unused code found by Vulture"""
    if not unused_items:
        return 0
    
    fixed_count = 0
    logger.info(f"{'Auto-fixing' if auto_fix else 'Would fix'} {len(unused_items)} unused code items")
    
    # Group by file for efficiency
    file_items = {}
    for item in unused_items:
        file_path = item["file"]
        if file_path not in file_items:
            file_items[file_path] = []
        file_items[file_path].append(item)
    
    for file_path, items in file_items.items():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Sort items by line number in reverse order to avoid index shifts
            items.sort(key=lambda x: x["line"], reverse=True)
            
            modified = False
            for item in items:
                line_idx = item["line"] - 1
                if line_idx < len(lines):
                    # For now, just comment out the line
                    # A more sophisticated approach would use AST to remove the entire unused function/class
                    lines[line_idx] = f"# REMOVED BY CODE_CLEANER (Unused): {lines[line_idx]}"
                    modified = True
                    fixed_count += 1
            
            if modified and auto_fix:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                logger.info(f"Fixed {len(items)} unused code items in {file_path}")
        
        except Exception as e:
            logger.error(f"Error cleaning unused code in {file_path}: {e}")
    
    return fixed_count

def fix_import_issues(import_issues: List[Dict], auto_fix: bool = False) -> int:
    """Fix import issues"""
    if not import_issues:
        return 0
    
    fixed_count = 0
    logger.info(f"{'Auto-fixing' if auto_fix else 'Would fix'} {len(import_issues)} import issues")
    
    # Group by file for efficiency
    file_issues = {}
    for issue in import_issues:
        file_path = issue["file"]
        if file_path not in file_issues:
            file_issues[file_path] = []
        file_issues[file_path].append(issue)
    
    for file_path, issues in file_issues.items():
        # Fix unsorted imports with isort
        if any(issue["type"] == "unsorted_imports" for issue in issues):
            try:
                if auto_fix:
                    subprocess.run(["isort", file_path], check=True)
                    logger.info(f"Sorted imports in {file_path}")
                fixed_count += 1
            except Exception as e:
                logger.error(f"Error sorting imports in {file_path}: {e}")
        
        # Fix unused imports (would need a more sophisticated AST-based approach)
        unused_imports = [i for i in issues if i["type"] == "unused_import"]
        if unused_imports and auto_fix:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Sort by line number in reverse order to avoid index shifts
                unused_imports.sort(key=lambda x: x["line"], reverse=True)
                
                modified = False
                for issue in unused_imports:
                    line_idx = issue["line"] - 1
                    if line_idx < len(lines):
                        # Comment out the unused import
                        lines[line_idx] = f"# REMOVED BY CODE_CLEANER (Unused import): {lines[line_idx]}"
                        modified = True
                        fixed_count += 1
                
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    logger.info(f"Commented out {len(unused_imports)} unused imports in {file_path}")
            
            except Exception as e:
                logger.error(f"Error fixing unused imports in {file_path}: {e}")
    
    return fixed_count

def suggest_fixes_for_circular_imports(circular_imports: List[Dict]) -> List[str]:
    """Suggest fixes for circular imports"""
    if not circular_imports:
        return []
    
    suggestions = []
    logger.info(f"Suggesting fixes for {len(circular_imports)} circular import chains")
    
    for idx, circularity in enumerate(circular_imports):
        modules = circularity["modules"]
        if len(modules) < 2:
            continue
        
        suggestion = f"Circular import #{idx+1}: {' -> '.join(modules)}\n"
        suggestion += "Possible fixes:\n"
        
        # Suggest different import strategies
        suggestion += "1. Move one of the imports inside a function or method\n"
        suggestion += f"   Example: In '{modules[-1]}', move the import of '{modules[0]}' inside a function\n\n"
        
        # Suggest creating an intermediate module
        suggestion += "2. Create an intermediate module that both modules import\n"
        suggestion += f"   Example: Move shared code between '{modules[0]}' and '{modules[-1]}' to a new module\n\n"
        
        # Suggest using dependency injection
        suggestion += "3. Use dependency injection to break the circular dependency\n"
        suggestion += f"   Example: Pass objects of '{modules[0]}' as arguments to functions in '{modules[-1]}'\n"
        
        suggestions.append(suggestion)
    
    return suggestions

def identify_orphaned_files(python_files: List[Path]) -> List[Path]:
    """Identify orphaned files that aren't imported anywhere"""
    logger.info("Identifying orphaned files...")
    
    # First get all module names from imports
    imported_modules = set()
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Find all import statements
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imported_modules.add(name.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported_modules.add(node.module)
        except Exception as e:
            logger.error(f"Error parsing imports in {file_path}: {e}")
    
    # Now check which files aren't imported
    orphaned_files = []
    for file_path in python_files:
        # Convert file path to module name
        rel_path = file_path.relative_to(PROJECT_ROOT)
        module_name = str(rel_path).replace(os.path.sep, '.').replace('.py', '')
        
        # Check if this module is imported anywhere
        if module_name not in imported_modules:
            # Check if it's a main module or test
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip files that have a main block or are tests
            if '__main__' in content or 'test_' in file_path.name:
                continue
                
            orphaned_files.append(file_path)
    
    logger.info(f"Found {len(orphaned_files)} potentially orphaned files")
    return orphaned_files

def clean_orphaned_files(orphaned_files: List[Path], auto_fix: bool = False) -> int:
    """Move orphaned files to an archive directory"""
    if not orphaned_files:
        return 0
    
    archive_dir = PROJECT_ROOT / "archive"
    if not archive_dir.exists() and auto_fix:
        archive_dir.mkdir(exist_ok=True)
    
    moved_count = 0
    logger.info(f"{'Moving' if auto_fix else 'Would move'} {len(orphaned_files)} orphaned files to archive")
    
    for file_path in orphaned_files:
        rel_path = file_path.relative_to(PROJECT_ROOT)
        target_path = archive_dir / rel_path
        
        logger.info(f"{'Moving' if auto_fix else 'Would move'} orphaned file: {rel_path}")
        
        if auto_fix:
            # Create necessary directories
            if not target_path.parent.exists():
                target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            try:
                shutil.move(str(file_path), str(target_path))
                moved_count += 1
                logger.info(f"Moved {rel_path} to archive")
            except Exception as e:
                logger.error(f"Error moving {rel_path}: {e}")
    
    return moved_count

def run_code_quality_check(python_files: List[Path]) -> Dict:
    """Run pylint for code quality checking"""
    logger.info("Running code quality check with pylint...")
    quality_report = {
        "overall_score": 0,
        "issues": []
    }
    
    # Create a temporary file with all Python file paths
    temp_file = PROJECT_ROOT / "temp_files.txt"
    with open(temp_file, 'w') as f:
        for file_path in python_files:
            f.write(f"{file_path}\n")
    
    try:
        # Run pylint on all files
        result = subprocess.run(
            ["pylint", f"--files-from={temp_file}", "--output-format=json"],
            capture_output=True,
            text=True
        )
        
        # Parse pylint output
        if result.stdout:
            try:
                import json
                issues = json.loads(result.stdout)
                
                # Calculate overall score (pylint gives a score out of 10)
                if result.stderr:
                    score_match = re.search(r'Your code has been rated at ([\d\.]+)/10', result.stderr)
                    if score_match:
                        quality_report["overall_score"] = float(score_match.group(1))
                
                quality_report["issues"] = issues
                STATS["quality_issues"] = len(issues)
                logger.info(f"Found {len(issues)} code quality issues, overall score: {quality_report['overall_score']}/10")
            except json.JSONDecodeError:
                logger.error("Failed to parse pylint JSON output")
    except Exception as e:
        logger.error(f"Error running code quality check: {e}")
    finally:
        # Clean up temporary file
        if temp_file.exists():
            temp_file.unlink()
    
    return quality_report

def generate_report(
    python_files: List[Path],
    unused_items: List[Dict],
    circular_imports: List[Dict],
    import_issues: List[Dict],
    duplicate_blocks: List[Dict],
    orphaned_files: List[Path],
    quality_report: Dict
) -> str:
    """Generate a comprehensive report"""
    report = []
    
    report.append("=" * 50)
    report.append("ALGOTRADEPRO5 CODE CLEANER REPORT")
    report.append("=" * 50)
    report.append("")
    
    # Summary
    report.append(f"Files scanned: {len(python_files)}")
    report.append(f"Unused code items: {len(unused_items)}")
    report.append(f"Circular import chains: {len(circular_imports)}")
    report.append(f"Import issues: {len(import_issues)}")
    report.append(f"Duplicate code blocks: {len(duplicate_blocks)}")
    report.append(f"Orphaned files: {len(orphaned_files)}")
    report.append(f"Code quality issues: {len(quality_report.get('issues', []))}")
    report.append(f"Overall code quality score: {quality_report.get('overall_score', 0)}/10")
    report.append("")
    
    # Unused Code
    if unused_items:
        report.append("-" * 50)
        report.append("UNUSED CODE")
        report.append("-" * 50)
        for item in unused_items[:10]:  # Limit to first 10 for brevity
            report.append(f"{item['file']}:{item['line']}: {item['description']} ({item['confidence']}% confidence)")
        if len(unused_items) > 10:
            report.append(f"... and {len(unused_items) - 10} more unused items")
        report.append("")
    
    # Circular Imports
    if circular_imports:
        report.append("-" * 50)
        report.append("CIRCULAR IMPORTS")
        report.append("-" * 50)
        for item in circular_imports:
            report.append(f"Circular chain: {item['description']}")
        report.append("")
        
        # Add suggestions
        suggestions = suggest_fixes_for_circular_imports(circular_imports)
        if suggestions:
            report.append("SUGGESTIONS TO FIX CIRCULAR IMPORTS")
            for suggestion in suggestions:
                report.append(suggestion)
            report.append("")
    
    # Import Issues
    if import_issues:
        report.append("-" * 50)
        report.append("IMPORT ISSUES")
        report.append("-" * 50)
        for item in import_issues[:10]:  # Limit to first 10 for brevity
            if 'line' in item:
                report.append(f"{item['file']}:{item['line']}: {item['description']}")
            else:
                report.append(f"{item['file']}: {item['description']}")
        if len(import_issues) > 10:
            report.append(f"... and {len(import_issues) - 10} more import issues")
        report.append("")
    
    # Duplicate Code
    if duplicate_blocks:
        report.append("-" * 50)
        report.append("DUPLICATE CODE")
        report.append("-" * 50)
        for block in duplicate_blocks[:5]:  # Limit to first 5 for brevity
            report.append(f"Duplicate block ({block['size']} lines) found in:")
            for instance in block['instances']:
                report.append(f"  - {instance['file']}:{instance['start_line']}-{instance['end_line']}")
            report.append("")
        if len(duplicate_blocks) > 5:
            report.append(f"... and {len(duplicate_blocks) - 5} more duplicate blocks")
        report.append("")
    
    # Orphaned Files
    if orphaned_files:
        report.append("-" * 50)
        report.append("ORPHANED FILES")
        report.append("-" * 50)
        for file_path in orphaned_files:
            report.append(f"{file_path}")
        report.append("")
    
    # Code Quality Issues (top 10 most severe)
    if quality_report.get('issues'):
        report.append("-" * 50)
        report.append("CODE QUALITY ISSUES (MOST SEVERE)")
        report.append("-" * 50)
        
        # Sort issues by severity
        sorted_issues = sorted(quality_report['issues'], key=lambda x: x.get('message-id', ''), reverse=True)
        
        for issue in sorted_issues[:10]:
            report.append(f"{issue.get('path', '')}:{issue.get('line', '')}: {issue.get('message', '')} ({issue.get('message-id', '')})")
        
        if len(quality_report['issues']) > 10:
            report.append(f"... and {len(quality_report['issues']) - 10} more quality issues")
        report.append("")
    
    report.append("=" * 50)
    return "\n".join(report)

def save_report(report: str, filename: str = "code_cleaner_report.txt"):
    """Save the report to a file"""
    report_path = PROJECT_ROOT / filename
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    logger.info(f"Report saved to {report_path}")
    return report_path

class CodeChangeHandler(FileSystemEventHandler):
    """Handle file system events for continuous monitoring"""
    def __init__(self, auto_fix=False):
        self.auto_fix = auto_fix
        self.last_scan_time = 0
        self.debounce_seconds = 5  # Minimum time between scans
    
    def on_modified(self, event):
        # Only respond to Python file changes
        if not event.is_directory and event.src_path.endswith('.py'):
            current_time = time.time()
            
            # Debounce to avoid too frequent scans
            if current_time - self.last_scan_time > self.debounce_seconds:
                self.last_scan_time = current_time
                logger.info(f"Change detected in {event.src_path}, running scan...")
                run_full_scan(auto_fix=self.auto_fix)
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.py'):
            current_time = time.time()
            if current_time - self.last_scan_time > self.debounce_seconds:
                self.last_scan_time = current_time
                logger.info(f"New file detected: {event.src_path}, running scan...")
                run_full_scan(auto_fix=self.auto_fix)

def run_full_scan(auto_fix=False):
    """Run a full code base scan"""
    start_time = time.time()
    
    # Reset stats
    for key in STATS:
        STATS[key] = 0
    
    # Get Python files to scan
    python_files = get_python_files()
    STATS["files_scanned"] = len(python_files)
    
    # Run all checks
    unused_items = check_unused_code(python_files)
    circular_imports = detect_circular_imports(python_files)
    import_issues = check_import_issues(python_files)
    duplicate_blocks = find_duplicate_code(python_files)
    orphaned_files = identify_orphaned_files(python_files)
    quality_report = run_code_quality_check(python_files)
    
    # Generate and save report
    report = generate_report(
        python_files,
        unused_items,
        circular_imports,
        import_issues,
        duplicate_blocks,
        orphaned_files,
        quality_report
    )
    report_path = save_report(report)
    
    # Fix issues if requested
    if auto_fix:
        fixes_count = 0
        fixes_count += clean_unused_code(unused_items, auto_fix=True)
        fixes_count += fix_import_issues(import_issues, auto_fix=True)
        fixes_count += clean_orphaned_files(orphaned_files, auto_fix=True)
        
        if fixes_count > 0:
            logger.info(f"Applied {fixes_count} automatic fixes")
    
    elapsed_time = time.time() - start_time
    logger.info(f"Full scan completed in {elapsed_time:.2f} seconds")
    
    # Print summary to console
    print("\n" + "=" * 50)
    print("CODE CLEANER SCAN SUMMARY")
    print("=" * 50)
    print(f"Files scanned: {STATS['files_scanned']}")
    print(f"Unused code items: {STATS['unused_code']}")
    print(f"Circular import chains: {STATS['circular_imports']}")
    print(f"Import issues: {STATS['import_issues']}")
    print(f"Duplicate code blocks: {STATS['duplicate_code']}")
    print(f"Code quality issues: {STATS['quality_issues']}")
    print(f"Report saved to: {report_path}")
    print("=" * 50)
    
    return report_path

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AlgoTradePro5 Code Cleaner")
    parser.add_argument("--clean", action="store_true", help="Auto-fix issues where possible")
    parser.add_argument("--watch", action="store_true", help="Watch for file changes and run continuously")
    parser.add_argument("--report-only", action="store_true", help="Only generate a report, don't fix anything")
    
    args = parser.parse_args()
    
    # Load environment variables
    load_environment_vars()
    
    # Run initial scan
    report_path = run_full_scan(auto_fix=args.clean)
    
    # Watch for changes if requested
    if args.watch:
        logger.info("Starting continuous monitoring of code changes...")
        event_handler = CodeChangeHandler(auto_fix=args.clean)
        observer = Observer()
        observer.schedule(event_handler, str(PROJECT_ROOT), recursive=True)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    main()