import os
import sys
# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

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
            
            # 1. SMART READ (Prevent Memory Explosion)
            # Read header for detection first
            with open(self.filepath, 'rb') as f:
                head = f.read(2048)
                
            # 2. Magic Byte & Text Detection
            self.filetype = detect_signature(head, self.filepath)
            
            # Decisions based on size
            is_large_file = self.filesize > 100 * 1024 * 1024 # 100MB limit for RAM operations
            content = b""

            # 3. Full Content Analysis (Only for small files)
            if not is_large_file:
                with open(self.filepath, 'rb') as f:
                    content = f.read()
                
                # Integrity & Entropy (Small files only)
                self.hashes['sha256'] = hashlib.sha256(content).hexdigest()
                self.entropy = self._calculate_entropy(content)
                
                # Deep Text Analysis
                if deep or "text" in self.filetype:
                    self.strings = self._extract_strings(content)
                    self._find_interesting_patterns()
            else:
                self.interesting_findings.append(f"INFO: Large file ({self.filesize/1024/1024:.0f}MB). Skipped deep string/entropy scan.")

            # 4. Metadata (Always safe)
            stats = os.stat(self.filepath)
            self.metadata['modified'] = datetime.fromtimestamp(stats.st_mtime).isoformat()
            
            # --- SPECIALIZED ANALYZERS (Safe for Large Files) ---

            # 5. Steganography Check (Images)
            if deep and "image" in self.filetype and not is_large_file:
                try: from forensix.modules.stego import StegoDetector
                except ImportError: from modules.stego import StegoDetector
                
                stego = StegoDetector(self.filepath)
                stego_findings = stego.scan()
                if stego_findings:
                    self.interesting_findings.extend(stego_findings)

            # 6. Network Forensics (PCAP)
            if "pcap" in self.filetype:
                try: from forensix.modules.pcap_analyzer import PcapAnalyzer
                except ImportError: from modules.pcap_analyzer import PcapAnalyzer
                
                pcap_engine = PcapAnalyzer(self.filepath)
                pcap_findings = pcap_engine.analyze()
                if pcap_findings:
                    self.interesting_findings.extend(pcap_findings)

            # 7. Audio Analysis (WAV/MP3)
            if "audio" in self.filetype or self.filepath.endswith(('.wav', '.mp3')):
                try: from forensix.modules.audio import AudioAnalyzer
                except ImportError: from modules.audio import AudioAnalyzer
                
                audio_engine = AudioAnalyzer(self.filepath)
                self.interesting_findings.extend(audio_engine.analyze())

            # 8. Memory Dump Analysis (Designed for huge files via mmap)
            if "memory-dump" in self.filetype or self.filesize > 500 * 1024 * 1024:
                # If it's huge, give memory analyzer a shot even if signature missed
                if self.filesize > 1024*1024:
                     try: from forensix.modules.memory import MemoryAnalyzer
                     except ImportError: from modules.memory import MemoryAnalyzer
                     
                     mem_engine = MemoryAnalyzer(self.filepath)
                     self.interesting_findings.extend(mem_engine.analyze())
                
            # 9. Document Metadata (Office/PDF)
            if self.filepath.endswith(('.docx', '.xlsx', '.pptx', '.pdf')):
                try: from forensix.modules.metadata import MetadataExtractor
                except ImportError: from modules.metadata import MetadataExtractor
                
                meta_engine = MetadataExtractor(self.filepath)
                self.interesting_findings.extend(meta_engine.analyze())

            self.is_valid = True
            return True

        except Exception as e:
            self.interesting_findings.append(f"Analysis Error: {str(e)}")
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
