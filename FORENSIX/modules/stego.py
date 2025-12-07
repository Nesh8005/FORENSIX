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

        return self.findings

    def run_deep_scan(self):
        """Runs heavy tools: Binwalk, Steghide, Zsteg"""
        from forensix.core.tools import Tools
        
        # 1. Binwalk (Overlay/Embedded Files)
        if Tools.has_tool('binwalk'):
            # Run binwalk to find signatures
            success, out, _ = Tools.run_command('binwalk', [self.filepath])
            if success and len(out.splitlines()) > 3: # Header + results
                self.findings.append("Binwalk: Hidden data/embedded signatures found.")
                
        # 2. Exiftool (Metadata)
        if Tools.has_tool('exiftool'):
            success, out, _ = Tools.run_command('exiftool', [self.filepath])
            if success:
                # Naive check for comments/warnings
                if "Comment" in out or "Warning" in out:
                     self.findings.append("Exiftool: Interesting metadata found (Check report).")

        # 3. Steghide (Needs Passphrase usually, but we check info)
        if Tools.has_tool('steghide'):
            success, out, err = Tools.run_command('steghide', ['info', self.filepath, '-p', ''])
            if success and "embedded" in out:
                self.findings.append("Steghide: Found embedded data (No password required!)")
            elif "passphrase" in err:
                self.findings.append("Steghide: Compatible file, password likely required.")

        # 4. Zsteg (Ruby tool for PNG/BMP LSB)
        if Tools.has_tool('zsteg') and self.filepath.endswith('.png'):
            success, out, _ = Tools.run_command('zsteg', ['-a', self.filepath])
            if success and "text" in out:
                # Filter noise
                lines = [l for l in out.splitlines() if "text" in l]
                if lines:
                    self.findings.append(f"Zsteg: Potential hidden text in LSB channels.")

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

