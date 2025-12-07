import os
import zipfile
import re

class MetadataExtractor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        self.meta = {}

    def analyze(self):
        if self._is_office_file():
            self._analyze_office()
        elif self._is_pdf():
            self._analyze_pdf()
        return self.findings

    def _is_office_file(self):
        return self.filepath.lower().endswith(('.docx', '.xlsx', '.pptx', '.odt'))

    def _is_pdf(self):
        return self.filepath.lower().endswith('.pdf')

    def _analyze_office(self):
        try:
            if zipfile.is_zipfile(self.filepath):
                with zipfile.ZipFile(self.filepath, 'r') as zf:
                    # Look for core.xml (standard OOXML metadata)
                    if 'docProps/core.xml' in zf.namelist():
                        data = zf.read('docProps/core.xml').decode('utf-8', errors='ignore')
                        # Regex extract (XML parsing is cleaner but regex works without lxml)
                        creator = re.search(r'<dc:creator>(.*?)</dc:creator>', data)
                        modifier = re.search(r'<cp:lastModifiedBy>(.*?)</cp:lastModifiedBy>', data)
                        
                        if creator: self.findings.append(f"Author: {creator.group(1)}")
                        if modifier: self.findings.append(f"Last Modified By: {modifier.group(1)}")

        except Exception as e:
            pass

    def _analyze_pdf(self):
        # Basic raw PDF analysis without heavy PyPDF2
        try:
            with open(self.filepath, 'rb') as f:
                content = f.read()
                # Search for /Author (text string)
                author = re.search(b'/Author\s*\((.*?)\)', content)
                creator = re.search(b'/Creator\s*\((.*?)\)', content)
                
                if author: 
                    self.findings.append(f"PDF Author: {author.group(1).decode('utf-8', errors='ignore')}")
                if creator: 
                    self.findings.append(f"PDF Creator: {creator.group(1).decode('utf-8', errors='ignore')}")

        except Exception:
            pass
