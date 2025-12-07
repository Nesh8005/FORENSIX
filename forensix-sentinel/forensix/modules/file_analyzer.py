import os
import magic
from rich.console import Console
from forensix.utils.hashing import calculate_hashes

class FileAnalyzer:
    def __init__(self):
        self.console = Console()

    def analyze(self, file_path):
        """
        Analyze a single file.
        """
        # Handle simple file case
        try:
            if not os.path.exists(file_path):
                 return {"error": "File does not exist"}

            # Basic stats
            stat_info = os.stat(file_path)
            
            # Type Detection
            mime_type = self.detect_type(file_path)
            
            # Hashing
            hashes = calculate_hashes(file_path)
            
            file_info = {
                "filename": os.path.basename(file_path),
                "path": os.path.abspath(file_path),
                "size_bytes": stat_info.st_size,
                "mime_type": mime_type,
                "hashes": hashes,
                "accessed": stat_info.st_atime,
                "modified": stat_info.st_mtime,
                "created": stat_info.st_ctime
            }
            
            return file_info
            
        except Exception as e:
            return {"error": str(e), "path": file_path}

    def detect_type(self, file_path):
        """
        Detect file type using magic bytes.
        """
        try:
            return magic.from_file(file_path, mime=True)
        except Exception as e:
            # Fallback for empty files or permission errors
            return "application/octet-stream"
