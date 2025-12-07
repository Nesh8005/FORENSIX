import os
import mmap
import re

class MemoryAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        # Patterns to hunt in memory
        self.patterns = {
            "FLAG": re.compile(b'(CTF\{.+?\}|flag\{.+?\})', re.IGNORECASE),
            "PASSWORD_TERM": re.compile(b'(password|passwd|pwd)\s*[:=]\s*[^\s]+', re.IGNORECASE),
            "HTTP_AUTH": re.compile(b'Authorization: Basic [a-zA-Z0-9+/=]+'),
            "PRIVATE_KEY": re.compile(b'-----BEGIN PRIVATE KEY-----'),
        }

    def analyze(self):
        if not os.path.exists(self.filepath):
            return []
            
        file_size = os.path.getsize(self.filepath)
        if file_size == 0:
            return []

        try:
            with open(self.filepath, 'rb') as f:
                # Use Memory Mapping for large files
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    self.findings.append(f"Memory Analysis: Scanning {file_size/1024/1024:.1f} MB dump...")
                    
                    for name, pattern in self.patterns.items():
                        for match in pattern.finditer(mm):
                            val = match.group(0)
                            if len(val) < 200: # Sanity filter
                                try:
                                    decoded = val.decode('utf-8', errors='ignore')
                                    # self.findings.append(f"MEM_HIT [{name}]: {decoded}")
                                    # Limit findings to avoid spam
                                    if len([x for x in self.findings if name in x]) < 5: 
                                        self.findings.append(f"🔥 MEMORY ARTIFACT: {decoded}")
                                except: pass
                                
        except Exception as e:
            self.findings.append(f"Memory Scan Error: {str(e)}")

        return self.findings
