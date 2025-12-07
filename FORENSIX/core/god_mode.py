import os
import re
import time
from rich.console import Console
from forensix.core.file_analyzer import FileAnalyzer
from forensix.modules.extractor import ArchiveExtractor
from forensix.core.tools import Tools

console = Console()

class GodMode:
    def __init__(self, root_target):
        self.root_target = root_target
        self.queue = []
        self.processed = set()
        self.loot = []
        self.artifacts_dir = f"artifacts_{int(time.time())}"
        
        # Initialize
        if os.path.isfile(root_target):
            self.queue.append(root_target)
        elif os.path.isdir(root_target):
            for root, _, files in os.walk(root_target):
                for f in files:
                    self.queue.append(os.path.join(root, f))
                    
        if not os.path.exists(self.artifacts_dir):
            os.makedirs(self.artifacts_dir)

    def hunt(self):
        """The Main Autonomous Loop"""
        console.print(f"[bold red]🔥 GOD MODE ACTIVATED on {self.root_target}[/bold red]")
        
        while self.queue:
            current_file = self.queue.pop(0)
            if current_file in self.processed:
                continue
            
            self.processed.add(current_file)
            console.print(f"[yellow]Analyzing:[/yellow] {os.path.basename(current_file)}")
            
            # 1. Analyze
            analyzer = FileAnalyzer(current_file)
            analyzer.analyze(deep=True)
            report = analyzer.get_report_data()
            
            # 2. Check for Flags instantly
            self._scan_for_flags(analyzer.strings, current_file)
            
            # 3. Auto-Extraction Logic
            new_files = []
            
            # A. Archives
            if "archive" in report['type'] or report['type'] == "zip":
                extractor = ArchiveExtractor(self.artifacts_dir)
                extracted = extractor.extract(current_file)
                if not extracted:
                    # Try password cracking?
                    pwd = extractor.try_crack(current_file)
                    if pwd:
                        console.print(f"[green]🔓 CRACKED PASSWORD:[/green] {pwd}")
                        self.loot.append(f"Password for {os.path.basename(current_file)}: {pwd}")
                        extracted = extractor.extract(current_file, password=pwd)
                
                if extracted:
                    console.print(f"[bold cyan]=> Extracted {len(extracted)} files[/bold cyan]")
                    new_files.extend(extracted)

            # B. Steganography (Steghide)
            # If Steghide detected, try to extract with empty pass
            for finding in report['findings']:
                if "Steghide" in finding and Tools.has_tool('steghide'):
                    out_file = os.path.join(self.artifacts_dir, f"stego_{os.path.basename(current_file)}.txt")
                    success, _, _ = Tools.run_command('steghide', ['extract', '-sf', current_file, '-p', '', '-xf', out_file])
                    if success and os.path.exists(out_file):
                        console.print(f"[bold cyan]=> Steghide Extracted payload![/bold cyan]")
                        new_files.append(out_file)

            # C. Binwalk (dd/firmware)
            if Tools.has_tool('binwalk'):
                # We blindly try binwalk extraction on everything 'suspicious' or large blobs
                # But to save time, only if 'findings' suggested it or high entropy
                if report['entropy'] > 7 or "Binwalk" in str(report['findings']):
                    success, _, _ = Tools.run_command('binwalk', ['-e', current_file, '-C', self.artifacts_dir, '--run-as=root']) 
                    # Note: --run-as=root might be needed if in docker, but usually -e is safe. 
                    # Checking if binwalk created a directory
                    # This is tricky as binwalk names folders dynamically. 
                    # We simple walk the artifacts dir again to find new stuff.
                    pass

            # Add new files to queue
            for nf in new_files:
                if nf not in self.processed:
                    self.queue.append(nf)
        
        # Final Report
        self._print_loom()

    def _scan_for_flags(self, strings, filename):
        flag_patterns = [
            r'flag\{[^}]+\}',
            r'CTF\{[^}]+\}',
            r'hkcert\{[^}]+\}' 
        ]
        
        for s in strings:
            for pat in flag_patterns:
                if re.search(pat, s, re.IGNORECASE):
                    console.print(f"[bold red]🚩 FLAG FOUND in {os.path.basename(filename)}: {s}[/bold red]")
                    self.loot.append(f"FLAG: {s} ({filename})")

    def _print_loom(self):
        console.print("\n[bold green]=== MISSION COMPLETE ===[/bold green]")
        if self.loot:
            console.print("[bold]🏆 LOOT SECURED:[/bold]")
            for item in self.loot:
                console.print(f" - {item}")
        else:
            console.print("[dim]No definitive flags found.[/dim]")
