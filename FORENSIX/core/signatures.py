import os
# 🕵️‍♂️ FORENSIX SENTINEL - FILE SIGNATURE DATABASE
# The "Truth" about file types.

SIGNATURES = {
    # IMAGES
    b'\xFF\xD8\xFF': "image/jpeg",
    b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': "image/png",
    b'\x47\x49\x46\x38': "image/gif",
    b'\x42\x4D': "image/bmp",
    b'\x49\x49\x2A\x00': "image/tiff", # Little endian
    b'\x4D\x4D\x00\x2A': "image/tiff", # Big endian
    b'\x52\x49\x46\x46': "image/webp", # Partial (RIFF)
    
    # DOCUMENTS
    b'\x25\x50\x44\x46': "application/pdf",
    b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1': "application/msword", # OLE CF (Old Office)
    b'\x50\x4B\x03\x04': "application/zip", # ZIP/Office Open XML (docx, xlsx)
    
    # EXECUTABLES
    b'\x4D\x5A': "application/x-dosexec", # PE (Windows EXE/DLL)
    b'\x7F\x45\x4C\x46': "application/x-executable", # ELF (Linux)
    b'\xCA\xFE\xBA\xBE': "application/java-archive", # Java Class/Mach-O
    
    # ARCHIVES
    b'\x52\x61\x72\x21\x1A\x07': "application/x-rar-compressed",
    b'\x37\x7A\xBC\xAF\x27\x1C': "application/x-7z-compressed",
    b'\x1F\x8B': "application/gzip",
    b'\x42\x5A\x68': "application/x-bzip2",
    
    # AUDIO/VIDEO
    b'\x49\x44\x33': "audio/mpeg", # MP3 ID3 tag
    b'\x00\x00\x00\x18\x66\x74\x79\x70': "video/mp4", # MP4
    b'\x00\x00\x00\x20\x66\x74\x79\x70': "video/mp4",
    b'\x1A\x45\xDF\xA3': "video/webm", # Matroska/WebM
    # NETWORK CAPTURES
    b'\xD4\xC3\xB2\xA1': "application/vnd.tcpdump.pcap",
    b'\xA1\xB2\xC3\xD4': "application/vnd.tcpdump.pcap",
    b'\x0A\x0D\x0D\x0A': "application/vnd.tcpdump.pcap", # PCAPNG
}

def detect_signature(head_bytes, filepath=""):
    """Detects file type from the first 32 bytes"""
    for sig, mime in SIGNATURES.items():
        if head_bytes.startswith(sig):
            # Special handling for ZIP vs Docx/Jar
            if mime == "application/zip":
                return "archive/zip-container" 
            return mime
            
    # Fallback: Is it text?
    try:
        # Check if the first chunk is valid UTF-8 text
        head_bytes.decode('utf-8')
        # Check for shebang
        if head_bytes.startswith(b'#!'):
            return "text/script"
        # Check for common source code keywords
        text_preview = head_bytes.decode('utf-8', errors='ignore').lower()
        if any(x in text_preview for x in ['import ', 'def ', 'class ', 'function ', '<?php', 'html']):
            return "text/source-code"
            
        return "text/plain"
    except UnicodeDecodeError:
        pass

    # FALLBACK BY EXTENSION (For things with no magic bytes like raw memory)
    ext = os.path.splitext(filepath)[1].lower()
    if ext in ['.dmp', '.raw', '.vmem', '.mem']:
        return "application/x-memory-dump"

    return "application/octet-stream" # Truly unknown binary
