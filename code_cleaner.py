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
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from threading import Lock
import threading
import pickle
import json

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RealTimeOutputHandler(logging.Handler):
    """Custom handler to ensure real-time console output"""
    def emit(self, record):
        try:
            msg = self.format(record)
            print(msg, flush=True)  # Force flush after each message
        except Exception:
            self.handleError(record)

# Configure logging with more detail and verbosity
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for maximum verbosity
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    force=True,
    handlers=[
        logging.FileHandler("code_cleaner.log", mode='w', encoding='utf-8'),  # Overwrite log each run
        RealTimeOutputHandler()  # Custom handler for real-time console output
    ]
)

logger = logging.getLogger("CodeCleaner")
logger.setLevel(logging.DEBUG)

# Add file handler with more detailed format for the log file
file_handler = logging.FileHandler("code_cleaner_detailed.log", mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s'
))
logger.addHandler(file_handler)

# Add thread-safe logging
class ThreadSafeLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.lock = Lock()
        
    def debug(self, msg, *args, **kwargs):
        with self.lock:
            self.logger.debug(msg, *args, **kwargs)
            
    def info(self, msg, *args, **kwargs):
        with self.lock:
            self.logger.info(msg, *args, **kwargs)
            
    def warning(self, msg, *args, **kwargs):
        with self.lock:
            self.logger.warning(msg, *args, **kwargs)
            
    def error(self, msg, *args, **kwargs):
        with self.lock:
            self.logger.error(msg, *args, **kwargs)

# Replace logger with thread-safe version
logger = ThreadSafeLogger("CodeCleaner")

# Thread-safe stats counter
class Stats:
    def __init__(self):
        self._stats = {
            "unused_code": 0,
            "circular_imports": 0,
            "duplicate_code": 0,
            "import_issues": 0,
            "quality_issues": 0,
            "files_scanned": 0
        }
        self._lock = Lock()
    
    def increment(self, key, amount=1):
        with self._lock:
            self._stats[key] += amount
    
    def get(self, key):
        with self._lock:
            return self._stats[key]
    
    def set(self, key, value):
        with self._lock:
            self._stats[key] = value
            
    def get_all(self):
        with self._lock:
            return self._stats.copy()

# Replace global STATS with thread-safe version
STATS = Stats()

# File cache for optimizing imports analysis
class FileCache:
    """Cache for file content hashes to avoid reprocessing unchanged files"""
    def __init__(self, cache_file=None):
        self.cache_file = cache_file or Path(os.path.dirname(os.path.abspath(__file__))) / ".filecache.pkl"
        self.cache = {}
        self.load_cache()
        self.lock = Lock()
        
    def load_cache(self):
        """Load cache from disk"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
        except Exception as e:
            # If loading fails, start with empty cache
            self.cache = {}
    
    def save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
        except Exception as e:
            pass  # Gracefully handle cache save failures
            
    def get_file_hash(self, file_path: Path) -> str:
        """Calculate hash of file contents"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except Exception:
            return ""  # Return empty string for failed hashes
    
    def is_cached(self, file_path: Path, file_hash: str) -> bool:
        """Check if file is in cache with matching hash"""
        with self.lock:
            path_str = str(file_path)
            return path_str in self.cache and self.cache[path_str] == file_hash
    
    def update_cache(self, file_path: Path, file_hash: str):
        """Update cache with new file hash"""
        with self.lock:
            self.cache[str(file_path)] = file_hash
            
    def clear_cache(self):
        """Clear the entire cache"""
        with self.lock:
            self.cache = {}
            if self.cache_file.exists():
                self.cache_file.unlink()

# Initialize file cache
file_cache = FileCache()

def check_file_imports(file_path: Path) -> List[Dict]:
    """Check a single file for import issues"""
    issues = []
    
    try:
        # Call isort in check-only mode
        isort_result = subprocess.run(
            ["isort", "--check-only", "--quiet", str(file_path)],
            capture_output=True,
            text=True
        )
        
        if isort_result.returncode != 0:
            issues.append({
                "file": str(file_path),
                "type": "unsorted_imports",
                "description": "Unsorted imports detected"
            })
        
        # Check for unused imports with pyflakes
        pyflakes_result = subprocess.run(
            ["pyflakes", str(file_path)],
            capture_output=True,
            text=True
        )
        
        if pyflakes_result.stdout:
            for line in pyflakes_result.stdout.splitlines():
                match = re.match(r'(.+):(\d+):(\d+): (.*)', line)
                if match:
                    _, line_num, _, message = match.groups()
                    if "imported but unused" in message:
                        issues.append({
                            "file": str(file_path),
                            "line": int(line_num),
                            "type": "unused_import",
                            "description": message
                        })
        
        # Update cache with current file hash
        file_hash = file_cache.get_file_hash(file_path)
        file_cache.update_cache(file_path, file_hash)
        
    except Exception as e:
        logger.error(f"Error checking imports in {file_path}: {e}")
    
    return issues

def analyze_imports(python_files: List[Path]) -> Tuple[List[Dict], Set[str]]:
    """Analyze imports across all Python files"""
    logger.info("Analyzing imports across all files...")
    import_issues = []
    imported_modules = set()
    
    for file_path in python_files:
        try:
            # Skip checking if file is in cache and unchanged
            file_hash = file_cache.get_file_hash(file_path)
            if file_cache.is_cached(file_path, file_hash):
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            try:
                tree = ast.parse(content)
            except SyntaxError:
                # Skip files with syntax errors
                continue
                
            # Find all imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imported_name = name.name.split('.')[0]  # Get top-level module
                        imported_modules.add(imported_name)
                        
                elif isinstance(node, ast.ImportFrom) and node.module:
                    # For relative imports, we need the full context
                    if node.level > 0:
                        # Relative import, get the current module's context
                        rel_path = file_path.relative_to(PROJECT_ROOT)
                        current_module = str(rel_path).replace(os.path.sep, '.').replace('.py', '')
                        parts = current_module.split('.')
                        # Adjust for the level of relative import
                        if node.level <= len(parts):
                            parent_module = '.'.join(parts[:-node.level])
                            if parent_module:
                                full_module = f"{parent_module}.{node.module}"
                            else:
                                full_module = node.module
                            imported_modules.add(full_module.split('.')[0])
                    else:
                        # Absolute import
                        imported_modules.add(node.module.split('.')[0])
                    
            # Update cache
            file_cache.update_cache(file_path, file_hash)
            
        except Exception as e:
            logger.error(f"Error analyzing imports in {file_path}: {e}")
    
    logger.info(f"Found {len(imported_modules)} unique imported modules")
    return import_issues, imported_modules

# Project configuration
PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = PROJECT_ROOT / ".env"

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

# Original EXCLUDED_DIRS list expanded to match .gitignore patterns
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

def load_environment_vars():
    """Load environment variables from .env file"""
    try:
        if not ENV_FILE.exists():
            logger.debug(".env file not found, skipping environment variable loading")
            return
        
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                try:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"\'')
                except ValueError:
                    logger.warning(f"Skipping invalid environment variable line: {line}")
                    continue
        logger.info("Environment variables loaded successfully")
    except Exception as e:
        logger.error(f"Error loading environment variables: {e}")
        # Continue execution even if env vars fail to load
        return

def validate_python_file(file_path: Path) -> bool:
    """Validate Python file syntax before processing"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            ast.parse(content)
        return True
    except SyntaxError as se:
        logger.error(f"Syntax error in {file_path}: {str(se)}")
        return False
    except UnicodeDecodeError:
        # Try alternate encodings
        for encoding in ['latin1', 'cp1252', 'iso-8859-1']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    ast.parse(content)
                return True
            except (UnicodeDecodeError, SyntaxError):
                continue
        logger.error(f"Failed to decode {file_path} with any supported encoding")
        return False
    except Exception as e:
        logger.error(f"Error validating {file_path}: {str(e)}")
        return False

def parallel_file_validation(files: List[Path], max_workers: int) -> List[Path]:
    """Validate Python files in parallel"""
    valid_files = []
    validation_lock = Lock()
    
    def validate_file(file_path: Path) -> Optional[Path]:
        try:
            if validate_python_file(file_path):
                with validation_lock:
                    valid_files.append(file_path)
                return file_path
        except Exception as e:
            logger.error(f"Error validating {file_path}: {e}")
        return None
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(executor.map(validate_file, files))
    
    return valid_files

def get_python_files(exclude_dirs: List[str] = None, exclude_files: List[str] = None) -> List[Path]:
    """Get all Python files in parallel"""
    if exclude_dirs is None:
        exclude_dirs = EXCLUDED_DIRS
    if exclude_files is None:
        exclude_files = EXCLUDED_FILES
    
    python_files = []
    file_lock = Lock()
    
    logger.info("Starting parallel Python file scan...")
    
    def process_directory(dir_path: Path) -> List[Path]:
        local_files = []
        try:
            for entry in os.scandir(dir_path):
                if entry.is_file() and entry.name.endswith('.py'):
                    file_path = Path(entry.path)
                    # Check exclusions
                    if not any(pattern in str(file_path) for pattern in exclude_files):
                        local_files.append(file_path)
                elif entry.is_dir():
                    # Check if directory should be excluded
                    dir_name = entry.name
                    rel_path = os.path.relpath(entry.path, PROJECT_ROOT)
                    if not any(excluded in rel_path for excluded in exclude_dirs):
                        local_files.extend(process_directory(Path(entry.path)))
        except Exception as e:
            logger.error(f"Error scanning directory {dir_path}: {e}")
        return local_files
    
    # First collect all Python files
    all_files = process_directory(PROJECT_ROOT)
    logger.info(f"Found {len(all_files)} potential Python files")
    
    # Then validate them in parallel
    max_workers = max(2, os.cpu_count() - 1)
    valid_files = parallel_file_validation(all_files, max_workers)
    
    logger.info(f"Validated {len(valid_files)} Python files")
    return valid_files

def process_file_batch(batch: List[Path], min_confidence: int = 60) -> List[Dict]:
    """Process a batch of files in parallel for unused code detection"""
    unused_items = []
    
    for file_path in batch:
        try:
            logger.debug(f"Processing file: {file_path}")
            cmd = [
                "vulture",
                "--min-confidence", str(min_confidence),
                "--sort-by-size",
                "--verbose",
                str(file_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                for line in result.stdout.splitlines():
                    for pattern in [
                        r'(.+):(\d+): (.+) \((\d+)% confidence\)',
                        r'(.+):(\d+): (.+)',
                        r'(.+):(\d+):\d+: (.+) \((\d+)% confidence\)',
                    ]:
                        match = re.match(pattern, line)
                        if match:
                            groups = match.groups()
                            item = {
                                "file": groups[0],
                                "line": int(groups[1]),
                                "description": groups[2],
                                "confidence": int(groups[3]) if len(groups) > 3 else min_confidence
                            }
                            
                            if not any(skip in item["description"].lower() for skip in [
                                "unused import",
                                "__init__",
                                "__str__",
                                "__repr__",
                                "test_",
                                "pytest"
                            ]):
                                unused_items.append(item)
                            break
                            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            
    return unused_items

def get_optimal_thread_count():
    """Get optimal thread count based on CPU cores"""
    cpu_count = os.cpu_count()
    if cpu_count is None:
        return 4  # Conservative fallback
    
    # For your i7-7820X with 8 cores/16 threads, we'll use all threads
    # but leave 1 for the OS
    return max(2, cpu_count - 1)

def get_optimal_batch_size(total_files: int) -> int:
    """Calculate optimal batch size based on file count and CPU cores"""
    cpu_count = os.cpu_count() or 4
    # Aim for each core to process at least 2-3 batches for better load balancing
    target_batch_count = cpu_count * 3
    return max(5, min(50, -(-total_files // target_batch_count)))  # Ceiling division

def check_unused_code(python_files: List[Path], min_confidence: int = 60) -> List[Dict]:
    """Multithreaded unused code detection with optimized parallelization"""
    logger.info("Starting parallel unused code check with Vulture...")
    all_unused_items = []
    processed_files = 0
    total_files = len(python_files)
    
    # Use optimized thread count
    max_workers = get_optimal_thread_count()
    batch_size = get_optimal_batch_size(total_files)
    
    logger.info(f"Using {max_workers} worker threads with batch size of {batch_size}")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_batch = {}
        
        # Submit batches to thread pool
        for i in range(0, total_files, batch_size):
            batch = python_files[i:i+batch_size]
            future = executor.submit(process_file_batch, batch, min_confidence)
            future_to_batch[future] = batch
        
        # Process completed batches with progress tracking
        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                unused_items = future.result()
                all_unused_items.extend(unused_items)
                processed_files += len(batch)
                progress = (processed_files / total_files) * 100
                
                # Log progress every 5%
                if processed_files % max(1, total_files // 20) == 0:
                    logger.info(f"Progress: {progress:.1f}% ({processed_files}/{total_files} files)")
                
                STATS.increment("files_scanned", len(batch))
            except Exception as e:
                logger.error(f"Batch processing failed: {e}")
    
    # Sort results
    all_unused_items.sort(key=lambda x: (-x["confidence"], x["file"]))
    
    STATS.set("unused_code", len(all_unused_items))
    logger.info(f"Completed parallel unused code check. Found {len(all_unused_items)} unused code items")
    
    # Log some examples of found unused code
    if all_unused_items:
        logger.info("Examples of unused code found:")
        for item in all_unused_items[:5]:
            logger.info(f"{item['file']}:{item['line']} - {item['description']} ({item['confidence']}% confidence)")
    
    return all_unused_items

def detect_circular_imports(python_files: List[Path]) -> List[Dict]:
    """Detect circular imports using a custom implementation"""
    logger.info("Checking for circular imports...")
    circular_imports = []
    
    # Process files in smaller batches
    batch_size = 50
    graph = {}
    
    for i in range(0, len(python_files), batch_size):
        batch = python_files[i:i+batch_size]
        logger.debug(f"Processing batch of {len(batch)} files for circular imports...")
        
        for file_path in batch:
            try:
                # Skip files in excluded directories using path parts comparison
                rel_path = file_path.relative_to(PROJECT_ROOT)
                path_parts = rel_path.parts
                
                if any(excluded in path_parts for excluded in EXCLUDED_DIRS):
                    continue

                module_name = str(rel_path).replace('\\', '.').replace('/', '.').replace('.py', '')
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    tree = ast.parse(content)
                except (SyntaxError, UnicodeDecodeError) as e:
                    logger.error(f"Error parsing {file_path}: {str(e)}")
                    continue
                
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
    
    # Find cycles in smaller subgraphs to prevent stack overflow
    def find_cycles_in_subgraph(subgraph):
        cycles = []
        visited = set()
        
        def find_cycle(node: str, path: List[str], visited_in_path: Set[str]):
            if node in visited_in_path:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:])
                return
            
            if node in visited or node not in subgraph:
                return
            
            visited.add(node)
            visited_in_path.add(node)
            path.append(node)
            
            for neighbor in subgraph.get(node, []):
                find_cycle(neighbor, path.copy(), visited_in_path.copy())
        
        for node in subgraph:
            if node not in visited:
                find_cycle(node, [], set())
        
        return cycles
    
    # Split graph into smaller subgraphs and find cycles
    subgraph_size = 50
    nodes = list(graph.keys())
    
    for i in range(0, len(nodes), subgraph_size):
        subgraph_nodes = nodes[i:i+subgraph_size]
        subgraph = {node: graph[node] for node in subgraph_nodes if node in graph}
        
        cycles = find_cycles_in_subgraph(subgraph)
        for cycle in cycles:
            circular_imports.append({
                "modules": cycle,
                "description": " -> ".join(cycle)
            })
    
    STATS.set("circular_imports", len(circular_imports))
    logger.info(f"Found {len(circular_imports)} circular import chains")
    return circular_imports

def check_import_issues(python_files: List[Path]) -> List[Dict]:
    """Check for import issues with improved performance"""
    logger.info("Checking for import issues...")
    
    # Use cached import analysis
    import_issues, _ = analyze_imports(python_files)
    
    # Run isort and pyflakes in parallel for remaining files
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = []
        for file_path in python_files:
            file_hash = file_cache.get_file_hash(file_path)
            
            if file_cache.is_cached(file_path, file_hash):
                continue
                
            futures.append(executor.submit(check_file_imports, file_path))
        
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    import_issues.extend(result)
            except Exception as e:
                logger.error(f"Error checking imports: {e}")
    
    STATS.set("import_issues", len(import_issues))
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
    
    STATS.set("duplicate_code", len(duplicate_blocks))
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
    """Identify truly orphaned files with improved accuracy"""
    logger.info("Identifying orphaned files...")
    
    # First get all module names that are imported anywhere
    _, imported_modules = analyze_imports(python_files)
    
    # Special handling for common module patterns
    def is_special_module(file_path: Path) -> bool:
        """Check if file is a special module that shouldn't be considered orphaned"""
        special_patterns = [
            "__init__.py",
            "conftest.py",
            "test_*.py",
            "*_test.py",
            "setup.py",
            "plugins/*.py",  # Plugin files
            "commands/*.py"  # Command files
        ]
        
        return any(file_path.match(pattern) for pattern in special_patterns)
    
    # Build module map
    module_map = {}
    for file_path in python_files:
        rel_path = file_path.relative_to(PROJECT_ROOT)
        module_name = str(rel_path).replace(os.path.sep, '.').replace('.py', '')
        module_map[module_name] = file_path
        
        # Handle package names
        package_name = module_name.split('.')[0]
        if package_name not in module_map:
            module_map[package_name] = file_path
    
    orphaned_files = []
    for file_path in python_files:
        if is_special_module(file_path):
            continue
            
        rel_path = file_path.relative_to(PROJECT_ROOT)
        module_name = str(rel_path).replace(os.path.sep, '.').replace('.py', '')
        
        # Check if module or any of its parent packages are imported
        is_imported = False
        parts = module_name.split('.')
        for i in range(len(parts)):
            check_name = '.'.join(parts[:i+1])
            if check_name in imported_modules:
                is_imported = True
                break
        
        if not is_imported:
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
                STATS.set("quality_issues", len(issues))
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
    """Run a full code base scan with optimized parallel processing"""
    start_time = time.time()
    max_workers = get_optimal_thread_count()
    logger.info(f"Starting parallel scan with {max_workers} workers...")
    
    try:
        # Reset stats
        for key in STATS._stats:
            STATS.set(key, 0)
        
        # Get Python files
        python_files = get_python_files()
        if not python_files:
            logger.warning("No Python files found to scan")
            return None
            
        total_files = len(python_files)
        STATS.set("files_scanned", total_files)
        logger.info(f"Found {total_files} Python files to scan")
        
        # Create thread pool for parallel tasks with dynamic task allocation
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all analysis tasks
            futures = {
                "unused": executor.submit(check_unused_code, python_files),
                "circular": executor.submit(detect_circular_imports, python_files),
                "imports": executor.submit(check_import_issues, python_files),
                "duplicate": executor.submit(find_duplicate_code, python_files),
                "orphaned": executor.submit(identify_orphaned_files, python_files),
                "quality": executor.submit(run_code_quality_check, python_files)
            }
            
            # Process results as they complete with timeout
            results = {}
            timeout_per_task = 300  # 5 minutes per task
            
            for name, future in futures.items():
                try:
                    results[name] = future.result(timeout=timeout_per_task)
                    logger.info(f"Completed {name} analysis")
                except concurrent.futures.TimeoutError:
                    logger.error(f"{name} analysis timed out after {timeout_per_task} seconds")
                    results[name] = []
                except Exception as e:
                    logger.error(f"Error in {name} analysis: {e}")
                    results[name] = []
        
        # Generate and save report
        report = generate_report(
            python_files,
            results.get("unused", []),
            results.get("circular", []),
            results.get("imports", []),
            results.get("duplicate", []),
            results.get("orphaned", []),
            results.get("quality", {})
        )
        report_path = save_report(report)
        
        # Fix issues if requested
        if auto_fix:
            with ThreadPoolExecutor(max_workers=max(2, max_workers // 2)) as fix_executor:
                fix_futures = [
                    fix_executor.submit(clean_unused_code, results.get("unused", []), True),
                    fix_executor.submit(fix_import_issues, results.get("imports", []), True),
                    fix_executor.submit(clean_orphaned_files, results.get("orphaned", []), True)
                ]
                
                fixes_count = sum(f.result(timeout=300) for f in as_completed(fix_futures))
                if fixes_count > 0:
                    logger.info(f"Applied {fixes_count} automatic fixes")
        
        elapsed_time = time.time() - start_time
        logger.info(f"Full parallel scan completed in {elapsed_time:.2f} seconds")
        
        # Print summary
        stats = STATS.get_all()
        summary = f"""
{'='*50}
CODE CLEANER SCAN SUMMARY
{'='*50}
Files scanned: {stats['files_scanned']}
Unused code items: {stats['unused_code']}
Circular import chains: {stats['circular_imports']}
Import issues: {stats['import_issues']}
Duplicate code blocks: {stats['duplicate_code']}
Code quality issues: {stats['quality_issues']}
Report saved to: {report_path}
Scan duration: {elapsed_time:.2f} seconds
{'='*50}
"""
        print(summary)
        logger.info(summary)
        
        return report_path
        
    except KeyboardInterrupt:
        logger.info("Scan interrupted by user")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during parallel scan: {e}")
        return None

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
    # Force stdout to be unbuffered
    sys.stdout.reconfigure(line_buffering=True)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nCode cleaner interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)