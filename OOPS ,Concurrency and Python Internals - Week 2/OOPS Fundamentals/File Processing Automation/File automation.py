import os
import shutil
import csv
import json
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s"
)

File_Directory = "files"

FOLDERS = {
    ".csv": "processed_data/sales",
    ".json": "processed_data/logs",
    ".txt": "processed_data/errors"
}

def process_file(filename):
    try:
        file_path = os.path.join(File_Directory, filename)

        if not os.path.isfile(file_path):
            return

        ext = os.path.splitext(filename)[1].lower()

        if ext == ".csv":
            total = 0
            with open(file_path, newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total += float(row.get("Amount", 0))
            logging.info(f"CSV processed: {filename} | Total Sales: {total}")

        elif ext == ".json":
            with open(file_path, "r") as f:
                data = json.load(f)
            count = len(data) if isinstance(data, list) else 1
            logging.info(f"JSON processed: {filename} | Records: {count}")

        elif ext == ".txt":
            with open(file_path, "r", errors="ignore") as f:
                lines = sum(1 for _ in f)
            logging.info(f"TXT processed: {filename} | Error lines: {lines}")

        else:
            return

        os.makedirs(FOLDERS[ext], exist_ok=True)
        shutil.move(file_path, os.path.join(FOLDERS[ext], filename))
        logging.info(f"Moved {filename} to {FOLDERS[ext]}")

    except Exception as e:
        logging.error(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    files = os.listdir(File_Directory)

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_file, files)
