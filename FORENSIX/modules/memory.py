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

        # 2. Volatility Integration
        self._run_volatility()

        return self.findings

    def _run_volatility(self):
        try:
            from forensix.core.tools import Tools
            
            # Check for volatility 3 or 2
            vol_cmd = None
            if Tools.has_tool('vol'): vol_cmd = 'vol'
            elif Tools.has_tool('volatility'): vol_cmd = 'volatility'
            
            if vol_cmd:
                self.findings.append("Volatility: Found! Running image info / checks...")
                # We can't automate everything in volatility as it takes forever.
                # But we can try to identify profile or run 'windows.info'
                
                # Simple check: windows.info (Vol3) or imageinfo (Vol2)
                # This is highly dependent on version, so we try basic enumeration
                cmd = [vol_cmd, '-f', self.filepath, 'windows.info']
                success, out, _ = Tools.run_command(vol_cmd, ['-f', self.filepath, 'windows.info'], timeout=120)
                
                if success and "Windows" in out:
                    self.findings.append("Volatility: Windows Image Detected.")
                    # If windows, try to list processes
                    success_ps, out_ps, _ = Tools.run_command(vol_cmd, ['-f', self.filepath, 'windows.pslist'], timeout=120)
                    if success_ps:
                        count = len(out_ps.splitlines()) - 2
                        self.findings.append(f"Volatility: {count} Processes Found (Saved to Report)")
                else:
                    self.findings.append("Volatility: Could not determine profile automatically (Try manually).")

        except Exception as e:
            self.findings.append(f"Volatility Error: {e}")
