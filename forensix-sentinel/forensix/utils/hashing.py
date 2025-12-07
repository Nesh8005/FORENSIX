import hashlib
import os

BLOCK_SIZE = 65536  # 64KB chunks

def calculate_hashes(file_path):
    """
    Calculate MD5, SHA1, and SHA256 hashes in a single pass.
    Returns a dictionary with the hashes.
    """
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BLOCK_SIZE)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)
                sha256.update(data)
                
        return {
            "md5": md5.hexdigest(),
            "sha1": sha1.hexdigest(),
            "sha256": sha256.hexdigest()
        }
    except PermissionError:
        return {"error": "Permission Denied"}
    except OSError as e:
        return {"error": str(e)}

def calculate_hash(file_path, algorithm='md5'):
    """
    Calculate a single hash for a file.
    """
    try:
        hash_func = getattr(hashlib, algorithm)()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(BLOCK_SIZE), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        return None
