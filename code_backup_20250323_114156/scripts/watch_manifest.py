import os
import time
from functools import wraps
from threading import Lock, Timer

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


# REMOVED_UNUSED_CODE: def debounce(wait):
# REMOVED_UNUSED_CODE:     """Decorator to debounce function calls"""
# REMOVED_UNUSED_CODE:     def decorator(fn):
# REMOVED_UNUSED_CODE:         lock = Lock()
# REMOVED_UNUSED_CODE:         timer = None
# REMOVED_UNUSED_CODE:         
# REMOVED_UNUSED_CODE:         @wraps(fn)
# REMOVED_UNUSED_CODE:         def debounced(*args, **kwargs):
# REMOVED_UNUSED_CODE:             nonlocal timer
# REMOVED_UNUSED_CODE:             
# REMOVED_UNUSED_CODE:             with lock:
# REMOVED_UNUSED_CODE:                 if timer is not None:
# REMOVED_UNUSED_CODE:                     timer.cancel()
# REMOVED_UNUSED_CODE:                 timer = Timer(wait, lambda: fn(*args, **kwargs))
# REMOVED_UNUSED_CODE:                 timer.start()
# REMOVED_UNUSED_CODE:                 
# REMOVED_UNUSED_CODE:         return debounced
# REMOVED_UNUSED_CODE:     return decorator

# Directories and files to exclude from manifest
EXCLUDED_DIRS = {
    '.git',
    '.venv',
    '.pytest_cache',
    '.mypy_cache',
    '.ruff_cache',
    '__pycache__',
    'node_modules',
    'venv',
    'build',
    'dist',
    'site-packages',
    '.vscode',
    'logs',  # Exclude runtime logs
    'dependencies',  # External dependencies directory
    'models',  # Large model files
    'data',  # Data files and databases
}

EXCLUDED_FILES = {
    '.pyc',
    '.pyo',
    '.pyd',
    '.so',
    '.dll',
    '.dylib',
    '.log',
    '.sqlite',
    '.sqlite-shm',
    '.sqlite-wal',
    '.pkl',
    '.pt',
    '.bin',
    '.model',
    '.safetensors',
}

def should_include(path, name):
    """Determine if a file or directory should be included in the manifest"""
    # Check if it's in excluded directories
    if name in EXCLUDED_DIRS:
        return False
        
    # Check file extensions
    if any(name.endswith(ext) for ext in EXCLUDED_FILES):
        return False
        
    # Skip hidden files and directories
    if name.startswith('.'):
        return False
        
    return True

def generate_manifest(manifest_file):
    """
    Regenerate the project manifest by walking through the project folder.
    Excludes non-core files and directories.
    """
    with open(manifest_file, 'w', encoding='utf-8') as mf:
        for root, dirs, files in os.walk("."):
            # Filter directories in-place
            dirs[:] = [d for d in dirs if should_include(os.path.join(root, d), d)]
            
            # Filter files
            files = [f for f in files if should_include(os.path.join(root, f), f)]
            
            if files or dirs:  # Only write dirs that contain included files
                indent = ' ' * (root.count(os.sep))
                mf.write(f"{indent}{os.path.basename(root)}/\n")
                for f in sorted(files):  # Sort files for consistency
                    mf.write(f"{indent}  {f}\n")

class ManifestUpdateHandler(FileSystemEventHandler):
    def __init__(self, manifest_file):
        self.manifest_file = manifest_file
        super().__init__()
    
# REMOVED_UNUSED_CODE:     @debounce(wait=1.0)
# REMOVED_UNUSED_CODE:     def update_manifest(self):
# REMOVED_UNUSED_CODE:         print("Change detected; updating manifest...")
# REMOVED_UNUSED_CODE:         generate_manifest(self.manifest_file)
# REMOVED_UNUSED_CODE:         print("Manifest updated. Watching for changes...")

# REMOVED_UNUSED_CODE:     def on_any_event(self, event):
# REMOVED_UNUSED_CODE:         # Skip if the path contains any excluded directory
# REMOVED_UNUSED_CODE:         if any(excl in event.src_path for excl in EXCLUDED_DIRS):
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE:             
# REMOVED_UNUSED_CODE:         # Skip if the file has an excluded extension
# REMOVED_UNUSED_CODE:         if any(event.src_path.endswith(ext) for ext in EXCLUDED_FILES):
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE:             
# REMOVED_UNUSED_CODE:         # Skip the manifest file itself
# REMOVED_UNUSED_CODE:         if event.src_path.endswith(self.manifest_file):
# REMOVED_UNUSED_CODE:             return
# REMOVED_UNUSED_CODE:             
# REMOVED_UNUSED_CODE:         self.update_manifest()

if __name__ == "__main__":
    manifest_path = "project_manifest.txt"
    generate_manifest(manifest_path)
    print(f"Initial manifest generated at {manifest_path}")
    
    event_handler = ManifestUpdateHandler(manifest_path)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()
    print("Watching for file changes. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file watcher...")
        observer.stop()
    observer.join()
    print("File watcher stopped.")
