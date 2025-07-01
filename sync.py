import sys
import os
import time
from datetime import datetime
import shutil

LOG_PATH = None

def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    if LOG_PATH:
        with open(LOG_PATH, "a") as f:
            f.write(full_message + "\n")
    print(full_message)

def validate(src: str, rep: str, interval: int, count: int):
    if not os.path.exists(src):
        log(f"Source path {src} does not exist")
        return False
    if not os.path.exists(rep):
        try:
            os.makedirs(rep)
            log(f"Replica path {rep} did not exist and was created.")
        except Exception as e:
            log(f"Failed to create replica path {rep}: {e}")
            return False
    if interval <= 0:
        log(f"Interval must be greater than 0")
        return False
    if count <= 0:
        log(f"Count must be greater than 0")
        return False
    return True

def deleteAll(dir: str):
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.remove(file_path)
                log(f"Deleted file: {file_path}")
            except Exception as e:
                log(f"Failed to delete file {file_path}: {e}")
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                os.rmdir(dir_path)
                log(f"Deleted directory: {dir_path}")
            except Exception as e:
                log(f"Failed to delete directory {dir_path}: {e}")

def copyAll(src: str, rep: str):
    for root, _, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        rep_root = os.path.join(rep, rel_path) if rel_path != '.' else rep
        if not os.path.exists(rep_root):
            try:
                os.makedirs(rep_root)
                log(f"Created directory: {rep_root}")
            except Exception as e:
                log(f"Failed to create directory {rep_root}: {e}")
        for file in files:
            src_file = os.path.join(root, file)
            rep_file = os.path.join(rep_root, file)
            try:
                shutil.copy2(src_file, rep_file)
                log(f"Copied file: {src_file} -> {rep_file}")
            except Exception as e:
                log(f"Failed to copy file {src_file} to {rep_file}: {e}")

def main(src: str, rep: str, interval: int, count: int, logs: str):
    global LOG_PATH
    LOG_PATH = logs
    if not validate(src, rep, interval, count):
        return
    log(f"Starting synchronization. Source: {src}, Replica: {rep}, Interval: {interval} seconds, Count: {count}")
    for i in range(count):
        log(f"Synchronization iteration {i+1} of {count}")
        deleteAll(rep)
        copyAll(src, rep)
        if i < count - 1:
            time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python sync.py <srcPath> <repPath> <interval> <count> <logPath>")
    else:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
