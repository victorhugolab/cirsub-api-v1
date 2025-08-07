import os
from datetime import datetime
from pathlib import Path

LOG_DIR = "logs"

def get_log_file_path():
    today = datetime.now().strftime("%d-%m-%Y")
    Path(LOG_DIR).mkdir(exist_ok=True)
    return os.path.join(LOG_DIR, f"{today}.log")

def log_to_file(action: str, message: str, code: str = "-", ip: str = "-"):
    now = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # HH:MM:SS.mmm
    line = f"[{now}] | {action.upper():<5} | {message} | {code} | {ip}\n"
    with open(get_log_file_path(), "a", encoding="utf-8") as log_file:
        log_file.write(line)
