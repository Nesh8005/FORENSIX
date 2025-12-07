import os
import wave
import struct

class AudioAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []

    def analyze(self):
        if not os.path.exists(self.filepath):
            return []

        try:
            # Check file extension/header
            if self.filepath.lower().endswith('.wav'):
                self._analyze_wav()
            elif self.filepath.lower().endswith('.mp3'):
                self._analyze_mp3()
        except Exception as e:
            self.findings.append(f"Audio Analysis Error: {str(e)}")

        return self.findings

    def _analyze_wav(self):
        try:
            with wave.open(self.filepath, 'r') as wav:
                frames = wav.getnframes()
                rate = wav.getframerate()
                duration = frames / float(rate)
                channels = wav.getnchannels()
                
                self.findings.append(f"Audio: WAV, {duration:.2f}s, {rate}Hz, {channels}ch")
                
                # Check for "Deep Sound" or "SilentEye" signatures in header usually
                # But simple check: Extra data at end?
                file_size = os.path.getsize(self.filepath)
                expected_size = 44 + (frames * channels * wav.getsampwidth())
                
                if file_size > expected_size + 1024:
                    diff = file_size - expected_size
                    self.findings.append(f"⚠️ Suspicious: {diff} bytes of extra data detected (Hidden File?)")

        except wave.Error:
            pass

    def _analyze_mp3(self):
        # Native MP3 parsing is hard without libs, but we can look for ID3 tags
        with open(self.filepath, 'rb') as f:
            header = f.read(10)
            if header.startswith(b'ID3'):
                major_version = header[3]
                self.findings.append(f"Audio: MP3 with ID3v2.{major_version} tags")
            
            # Scan for common text hiding in frames? 
            # (Handled by general string extractor in FileAnalyzer)
