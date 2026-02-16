import time
from threading import Thread

def process_file(file):
    with open(file, "r") as f:
        content = f.read()
        lines = content.splitlines()
        words = content.split()

    print(f"{file} → Lines: {len(lines)}, Words: {len(words)}")

def threaded_processing(files):
    threads = []
    start = time.perf_counter()

    for file in files:
        t = Thread(target=process_file, args=(file,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end = time.perf_counter()
    print(f"\nMultithreaded execution time: {end - start:.4f} seconds")

def main():
    files = ["Multi File Processor/file1.txt", 
             "Multi File Processor/file2.txt", 
             "Multi File Processor/file3.txt"]

    print("\nMultithreaded Processing ")
    threaded_processing(files)

if __name__ == "__main__":
    main()
