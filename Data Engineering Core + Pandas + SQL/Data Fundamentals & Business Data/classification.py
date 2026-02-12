import os
import shutil

FILES = "incoming_data"
PROCESSED_FILES = "processed_data"

STRUCTURED_EXT = [".csv", ".xlsx"]
SEMI_STRUCTURED_EXT = [".json", ".xml"]
UNSTRUCTURED_EXT = [".txt", ".log", ".jpg", ".png"]


def extension(filename):
    ext = os.path.splitext(filename)[1].lower()

    if ext in STRUCTURED_EXT:
        return "structured"
    elif ext in SEMI_STRUCTURED_EXT:
        return "semi_structured"
    else:
        return "unstructured"


def classification():
    for file_name in os.listdir(FILES):
        file_path = os.path.join(FILES, file_name)

        if os.path.isfile(file_path):
            category = extension(file_name)

            destination = os.path.join(PROCESSED_FILES, category)
            os.makedirs(destination, exist_ok=True)

            shutil.move(file_path, destination)
            print(f"{file_name} → {category}")


if __name__ == "__main__":
    classification()
