import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def generate_manifest(manifest_file):
    """
    Regenerate the project manifest by walking through the project folder.
    Excludes folders like .git, node_modules, and venv.
    """
    with open(manifest_file, 'w', encoding='utf-8') as mf:
        for root, dirs, files in os.walk("."):
            # Exclude unwanted directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv'}]
            indent = ' ' * (root.count(os.sep))
            mf.write(f"{indent}{os.path.basename(root)}/\n")
            for f in files:
                mf.write(f"{indent}  {f}\n")

class ManifestUpdateHandler(FileSystemEventHandler):
    def __init__(self, manifest_file):
        self.manifest_file = manifest_file

    def on_any_event(self, event):
        print("Change detected; updating manifest...")
        generate_manifest(self.manifest_file)

if __name__ == "__main__":
    manifest_path = "project_manifest.txt"  # This file will be created in C:\AlgoTradPro5
    generate_manifest(manifest_path)  # Initial generation
    event_handler = ManifestUpdateHandler(manifest_path)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()
    print("Watching for file changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
