import os
import zipfile
import tarfile
import shutil
from datetime import datetime

class ArchiveExtractor:
    def __init__(self, output_base="_extracted"):
        self.output_base = output_base
        if not os.path.exists(output_base):
            os.makedirs(output_base)

    def extract(self, filepath):
        """Extracts supported archives to a temp folder"""
        if not zipfile.is_zipfile(filepath) and not tarfile.is_tarfile(filepath):
            return []

        timestamp = datetime.now().strftime("%H%M%S")
        filename = os.path.basename(filepath)
        extract_dir = os.path.join(self.output_base, f"{filename}_{timestamp}")
        
        extracted_files = []

        try:
            if zipfile.is_zipfile(filepath):
                with zipfile.ZipFile(filepath, 'r') as zf:
                    zf.extractall(extract_dir)
                    # Walk the extracted files
                    for root, dirs, files in os.walk(extract_dir):
                        for file in files:
                            extracted_files.append(os.path.join(root, file))
                            
            elif tarfile.is_tarfile(filepath):
                with tarfile.open(filepath, 'r:*') as tf:
                    tf.extractall(extract_dir)
                    for root, dirs, files in os.walk(extract_dir):
                        for file in files:
                            extracted_files.append(os.path.join(root, file))

        except Exception as e:
            # print(f"Extraction failed: {e}")
            pass

        return extracted_files

def cleanup_extracted():
    if os.path.exists("_extracted"):
        shutil.rmtree("_extracted", ignore_errors=True)
