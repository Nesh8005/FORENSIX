import os
import hashlib
import re
import math
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
        self.entropy = 0
        self.interesting_findings = []
        self.is_valid = False

    def analyze(self, deep=False):
        """Main analysis pipeline"""
        if not os.path.exists(self.filepath):
            return False
            
        try:
            self.filesize = os.path.getsize(self.filepath)
            
            # 1. Read File Content
            # For massive files, we would chunk this. For now, read all (up to 100MB limitation implied)
            if self.filesize > 100 * 1024 * 1024: # Skip > 100MB for demo
                return False

            with open(self.filepath, 'rb') as f:
                content = f.read() 
                
            # 2. Magic Byte & Text Detection
            self.filetype = detect_signature(content[:2048])
            
            # 3. Hash Calculation (Integrity)
            self.hashes['sha256'] = hashlib.sha256(content).hexdigest()
            
            # 4. Entropy Calculation
            self.entropy = self._calculate_entropy(content)
            
            # 5. Metadata
            stats = os.stat(self.filepath)
            self.metadata['modified'] = datetime.fromtimestamp(stats.st_mtime).isoformat()
            
            # 6. Deep Analysis (Strings & Patterns)
            if deep or "text" in self.filetype: # Always scan text files for secrets
                self.strings = self._extract_strings(content)
                self._find_interesting_patterns()

            # 7. Steganography Check (Images)
            if deep and "image" in self.filetype:
                from forensix.modules.stego import StegoDetector
                stego = StegoDetector(self.filepath)
                stego_findings = stego.scan()
                if stego_findings:
                    self.interesting_findings.extend(stego_findings)

            self.is_valid = True
            return True

        except Exception as e:
            # print(f"Error analyzing file: {e}") # Silent fail for UI cleanliness
            return False

    def _calculate_entropy(self, data):
        """Calculates Shannon entropy."""
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(x))/len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def _extract_strings(self, data, min_len=4):
        """Extracts printable strings (ASCII & Unicode)"""
        results = []
        # ASCII characters range (usually 32-126) plus tab (9)
        ascii_pattern = re.compile(b'[ -~]{4,}')
        unicode_pattern = re.compile(b'(?:[ -~]\x00){4,}')

        # Limit total strings to avoid memory explosion on large binaries
        limit = 5000 
        
        for match in ascii_pattern.finditer(data):
            if len(results) >= limit: break
            try:
                results.append(match.group().decode('ascii'))
            except: pass
                
        for match in unicode_pattern.finditer(data):
            if len(results) >= limit: break
            try:
                results.append(match.group().decode('utf-16le'))
            except: pass
                
        return results

    def _find_interesting_patterns(self):
        """Scans extracted strings for secrets/flags"""
        patterns = {
            "FLAG": re.compile(r'(CTF\{.+?\}|flag\{.+?\})', re.IGNORECASE),
            "API_KEY": re.compile(r'(api_key|apikey|secret|token)[\"\']?\s*[:=]\s*[\"\']?([a-zA-Z0-9_\-]{20,})', re.IGNORECASE),
            "URL": re.compile(r'(https?|ftp)://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:/[^\s<>"]*)?', re.IGNORECASE),
            "EMAIL": re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', re.IGNORECASE),
            "IP": re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
        }
        
        for s in self.strings:
            for name, pattern in patterns.items():
                match = pattern.search(s)
                if match:
                    # Capture the full match or specific group
                    val = match.group(0)
                    if len(val) < 200: # Sanity check length
                        self.interesting_findings.append(f"{name}: {val}")

    def get_report_data(self):
        """Returns structured data for the report"""
        return {
            "filename": self.filename,
            "type": self.filetype,
            "size_bytes": self.filesize,
            "entropy": round(self.entropy, 2),
            "hashes": self.hashes,
            "metadata": self.metadata,
            "findings": self.interesting_findings[:5], # Top 5 findings
            "strings_count": len(self.strings)
        }
