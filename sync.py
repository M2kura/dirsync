# Please implement a program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of source folder at replica folder.

# Synchronization must be one-way: after the synchronization content of the replica folder should be modified to exactly match content of the source folder.

# Synchronization should be performed periodically, but limited amount of times. Program should stop after the last synchronization.

# File creation/copying/removal operations as well as error messages should be logged to a file and to the console output.

# It is undesirable to use third-party libraries that implement folder synchronization.

# It is allowed (and recommended) to use libraries implementing other well-known algorithms. For example, there is no point in implementing yet another function that calculates MD5 if you need it for the task – it is perfectly acceptable to use a built-in library.

# 1) Expect command line arguments in a fixed aforementioned order.
# 2) Write all code in a single file. This is not a production-level practice, but for the purpose of compliance with environment limitations we ask you to do this. Still, we encourage you to build your solution with good structure: you should use functions and classes as you see fit.
# 3) Use main() function as your entry point. This function will be called from the environment during validation. Command line arguments can be accessed as usual.
# 4) Do not use sys.exit calls.
# 5) Solution must be singlethreaded.
# 6) Solution must not read input. As it was mentioned before the task will undergo automated validation that doesn't interact with the code via input. It will only pass command line arguments.
# 7) Solution must not have any infinite loops.
# 8) Solution must be implemented using only standard Python libraries.
# 9) Solution must gracefully finish its work in any case.

import sys
import os
import time
from datetime import datetime
import shutil

def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    with open("logs.txt", "a") as f:
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
        log("Usage: python sync.py <srcPath> <repPath> <interval> <count> <logPath>")
    else:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
