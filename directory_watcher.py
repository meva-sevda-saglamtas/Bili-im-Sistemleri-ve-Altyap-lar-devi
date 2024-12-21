import sys
import time
import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, directory_to_watch="/home/kali/bsm/test", log_file="/home/kali/bsm/logs/changes.json"):
        self.directory_to_watch = directory_to_watch
        self.log_file = log_file
        self.observer = Observer()
        
        # Log dizininin varlığını kontrol et
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        event_handler = Handler(self.log_file)
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        
        print(f"İzleniyor: {self.directory_to_watch}")
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("\nİzleme durduruldu")
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file
        
    def on_any_event(self, event):
        if event.is_directory:
            return
        
        print(f"Olay algılandı: {event.event_type} - {event.src_path}")

        log_entry = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            with open(self.log_file, 'a') as log_file:
                json.dump(log_entry, log_file, ensure_ascii=False)
                log_file.write('\n')
        except Exception as e:
            print(f"Log yazma hatası: {e}")

if __name__ == '__main__':
    w = Watcher()
    w.run()
