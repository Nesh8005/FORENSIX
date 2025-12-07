import os
import hashlib
import re
from datetime import datetime
from .signatures import detect_signature

class FileAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.filesize = 0
        self.filetype = "unknown"
        self.hashes = {}
        self.metadata = {}
        self.strings = []
        self.is_valid = False

    def analyze(self, deep=False):
        """Main analysis pipeline"""
        if not os.path.exists(self.filepath):
            return False
            
        try:
            self.filesize = os.path.getsize(self.filepath)
            
            # 1. Read File Head & Content
            with open(self.filepath, 'rb') as f:
                head = f.read(2048) # Read first 2KB for signature
                f.seek(0)
                content = f.read()  # CAUTION: Reading full file into memory (for demo speed)
                
            # 2. Magic Byte Detection
            self.filetype = detect_signature(head)
            
            # 3. Hash Calculation (Integrity)
            self.hashes['md5'] = hashlib.md5(content).hexdigest()
            self.hashes['sha256'] = hashlib.sha256(content).hexdigest()
            
            # 4. Basic Metadata
            stats = os.stat(self.filepath)
            self.metadata['created'] = datetime.fromtimestamp(stats.st_ctime).isoformat()
            self.metadata['modified'] = datetime.fromtimestamp(stats.st_mtime).isoformat()
            self.metadata['accessed'] = datetime.fromtimestamp(stats.st_atime).isoformat()
            
            # 5. String Extraction (If deep analysis)
            if deep:
                self.strings = self._extract_strings(content)

            self.is_valid = True
            return True

        except Exception as e:
            print(f"Error analyzing file: {e}")
            return False

    def _extract_strings(self, data, min_len=4):
        """Extracts printable strings (ASCII & Unicode)"""
        results = []
        # ASCII characters range (usually 32-126) plus tab (9)
        # We look for sequences of 4 or more
        ascii_pattern = re.compile(b'[ -~]{4,}')
        
        # Simple Unicode/Wide char pattern (basic approach)
        # Matches char + null byte sequences
        unicode_pattern = re.compile(b'(?:[ -~]\x00){4,}')

        for match in ascii_pattern.finditer(data):
            try:
                decoded = match.group().decode('ascii')
                results.append(decoded)
            except:
                pass
                
        for match in unicode_pattern.finditer(data):
            try:
                decoded = match.group().decode('utf-16le') # Common Windows encoding
                results.append(decoded)
            except:
                pass
                
        return results

    def get_report_data(self):
        """Returns structured data for the report"""
        return {
            "filename": self.filename,
            "type": self.filetype,
            "size_bytes": self.filesize,
            "hashes": self.hashes,
            "metadata": self.metadata,
            "strings_count": len(self.strings),
            "strings_sample": self.strings[:10] if self.strings else [] # Preview only
        }
