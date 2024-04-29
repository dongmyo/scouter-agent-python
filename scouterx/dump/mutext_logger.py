import threading
from datetime import datetime


class MutexLogger:
    def __init__(self, file_name):
        self.fileName = file_name
        self.lock = threading.Lock()
        self.log_entries = []

    def acquire(self):
        entry = f"Lock acquired by {threading.current_thread().name} at {datetime.now()}\n"
        self.log_entries.append(entry)
        self.lock.acquire()

    def release(self):
        entry = f"Lock released by {threading.current_thread().name} at {datetime.now()}\n"
        self.log_entries.append(entry)
        self.lock.release()

    def save_log(self):
        with open(self.fileName, 'a') as file:
            file.writelines(self.log_entries)
        self.log_entries = []  # Clear after saving
