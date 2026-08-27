# android_adbkit/core/archive_extract.py
import zipfile





def extract_zip(zip_path, destination_dir):
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(destination_dir)