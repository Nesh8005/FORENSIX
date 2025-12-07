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

    def extract(self, filepath, password=None):
        """
        Extracts supported archives to a temp folder.
        Supports: zip, tar, 7z, rar (via 7z)
        """
        timestamp = datetime.now().strftime("%H%M%S")
        filename = os.path.basename(filepath)
        extract_dir = os.path.join(self.output_base, f"{filename}_{timestamp}")
        
        extracted_files = []
        is_extracted = False

        try:
            from forensix.core.tools import Tools
            
            # 1. Try 7z (The Universal Unpacker)
            # 7z covers zip, rar, tar, gzip, bzip2, etc.
            if Tools.has_tool('7z'):
                cmd = ['x', filepath, f'-o{extract_dir}', '-y']
                if password:
                    cmd.append(f'-p{password}')
                else:
                    cmd.append('-p') # Attempt empty password
                
                success, out, err = Tools.run_command('7z', cmd)
                if success and "Everything is Ok" in out:
                    is_extracted = True
            
            # 2. Python Fallback (Standard Zip/Tar)
            if not is_extracted:
                if zipfile.is_zipfile(filepath):
                    if not os.path.exists(extract_dir): os.makedirs(extract_dir)
                    with zipfile.ZipFile(filepath, 'r') as zf:
                        try:
                            zf.extractall(extract_dir, pwd=password.encode() if password else None)
                            is_extracted = True
                        except RuntimeError: 
                            pass # Password required or wrong password
                            
                elif tarfile.is_tarfile(filepath):
                    if not os.path.exists(extract_dir): os.makedirs(extract_dir)
                    with tarfile.open(filepath, 'r:*') as tf:
                        tf.extractall(extract_dir)
                        is_extracted = True

            # 3. Collect Results
            if is_extracted:
                for root, dirs, files in os.walk(extract_dir):
                    for file in files:
                        extracted_files.append(os.path.join(root, file))

        except Exception as e:
            # Fail silently to keep flow moving
            pass

        return extracted_files

    def try_crack(self, filepath):
        """Attempts to crack archive password using rockyou.txt"""
        from forensix.core.tools import WORDLIST_PATH, Tools
        if not WORDLIST_PATH or not os.path.exists(WORDLIST_PATH):
            return None

        # Simple dictionary attack for ZIPs
        if zipfile.is_zipfile(filepath):
            try:
                with zipfile.ZipFile(filepath) as zf:
                    with open(WORDLIST_PATH, 'rb') as wl:
                        for line in wl:
                            pwd = line.strip()
                            try:
                                zf.extractall(pwd=pwd, path=os.path.join(self.output_base, "cracked"))
                                return pwd.decode()
                            except: continue
            except: pass
            
        return None

def cleanup_extracted():
    if os.path.exists("_extracted"):
        shutil.rmtree("_extracted", ignore_errors=True)
