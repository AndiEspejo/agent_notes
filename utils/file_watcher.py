import os
import time
from typing import Callable, Dict, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

class DocumentWatcher(FileSystemEventHandler):
    def __init__(self, watch_dir: str, callback: Callable[[str], None], file_types: List[str] = None):
        self.watch_dir = watch_dir
        self.callback = callback
        self.file_types = file_types or [".pdf", ".docx", ".doc"]
        self.observer = Observer()
        
    def on_created(self, event):
        if not event.is_directory and any(event.src_path.endswith(ext) for ext in self.file_types):
            self.callback(event.src_path)
            
    def start(self):
        self.observer.schedule(self, self.watch_dir, recursive=True)
        self.observer.start()
        
    def stop(self):
        self.observer.stop()
        self.observer.join() 