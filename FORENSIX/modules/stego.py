import os
import struct

class StegoDetector:
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
    
    def scan(self):
        """Scans for common steganography techniques"""
        if not os.path.exists(self.filepath):
            return []
            
        with open(self.filepath, 'rb') as f:
            data = f.read()

        # 1. Trailing Data Check (Overlay Steganography)
        # Did someone append a zip to a jpg?
        self._check_trailing_data(data)
        
        # 2. Keyphrase Search (Simple tool signatures)
        self._check_tool_signatures(data)

        return self.findings

    def _check_trailing_data(self, data):
        """Detects data appended after the end of file marker"""
        # JPEG End of Image (EOI)
        if data.startswith(b'\xFF\xD8'): 
            eoi = data.rfind(b'\xFF\xD9')
            if eoi != -1 and eoi < len(data) - 2:
                # Calculate size of trailing data
                extra_bytes = len(data) - (eoi + 2)
                if extra_bytes > 100: # Ignore tiny noise
                    self.findings.append(f"Suspicious: {extra_bytes} bytes found after JPEG EOF (Hidden Archive?)")
        
        # PNG End (IEND chunk)
        elif data.startswith(b'\x89PNG'):
            iend = data.rfind(b'IEND')
            if iend != -1:
                # IEND chunk includes 4 byte CRC after "IEND"
                # so actual end is iend + 4 + 4 = iend + 8
                eof = iend + 8
                if eof < len(data):
                    extra_bytes = len(data) - eof
                    if extra_bytes > 50:
                        self.findings.append(f"Suspicious: {extra_bytes} bytes found after PNG EOF")

    def _check_tool_signatures(self, data):
        """Detects signatures of common CTF stego tools"""
        tools = {
            b'steghide': "Steghide detected",
            b'outguess': "Outguess detected",
            b'F5': "F5 Steganography detected",
            b'openstego': "OpenStego detected"
        }
        for sig, name in tools.items():
            if sig in data:
                self.findings.append(f"Tool Signature: {name}")

