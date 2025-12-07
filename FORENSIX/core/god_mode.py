import os
import re
import time
from forensix.interface.theme import UI
from forensix.core.file_analyzer import FileAnalyzer
from forensix.modules.extractor import ArchiveExtractor
from forensix.core.tools import Tools

# Remove local console instantiation
# console = Console() 

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
        UI.console.print(f"[bold red]🔥 GOD MODE ACTIVATED on {self.root_target}[/bold red]")
        
        while self.queue:
            current_file = self.queue.pop(0)
            if current_file in self.processed:
                continue
            
            self.processed.add(current_file)
            UI.console.print(f"[yellow]Analyzing:[/yellow] {os.path.basename(current_file)}")
            
            # 1. Analyze
            analyzer = FileAnalyzer(current_file)
            analyzer.analyze(deep=True)
            report = analyzer.get_report_data()
            
            # 2. AI Threat Assessment
            try:
                from forensix.core.neural_engine import NeuralEngine
                brain = NeuralEngine()
                ai_result = brain.score_artifact(report['entropy'], report['findings'], report['type'])
                
                if ai_result['score'] > 80:
                    UI.console.print(f"[bold red blink]☠️  AI DETECTED CRITICAL THREAT: {ai_result['assessment']}[/bold red blink]")
                    # For critical threats, force aggressive extraction
                    report['findings'].append("Mandatory Extraction")
                elif ai_result['score'] > 50:
                    UI.console.print(f"[yellow]⚠️  AI Warning: {ai_result['assessment']}[/yellow]")
            except ImportError: pass

            # 3. Check for Flags instantly
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
                        UI.console.print(f"[green]🔓 CRACKED PASSWORD:[/green] {pwd}")
                        self.loot.append(f"Password for {os.path.basename(current_file)}: {pwd}")
                        extracted = extractor.extract(current_file, password=pwd)
                
                if extracted:
                    UI.console.print(f"[bold cyan]=> Extracted {len(extracted)} files[/bold cyan]")
                    new_files.extend(extracted)

            # B. Steganography (Steghide)
            # If Steghide detected, try to extract with empty pass
            for finding in report['findings']:
                if "Steghide" in finding and Tools.has_tool('steghide'):
                    out_file = os.path.join(self.artifacts_dir, f"stego_{os.path.basename(current_file)}.txt")
                    success, _, _ = Tools.run_command('steghide', ['extract', '-sf', current_file, '-p', '', '-xf', out_file])
                    if success and os.path.exists(out_file):
                        UI.console.print(f"[bold cyan]=> Steghide Extracted payload![/bold cyan]")
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
            r'hkcert\{[^}]+\}',
            r'picoCTF\{[^}]+\}',
            r'HTB\{[^}]+\}',
            r'THM\{[^}]+\}',
            r'flag\s*[:=]\s*[a-zA-Z0-9_]{10,}',
            r'[a-f0-9]{32}', # naked MD5 hash (sometimes a flag)
            r'[a-zA-Z0-9+/]{40,}={0,2}' # Base64 chunks (suspicious)
        ]
        
        for s in strings:
            for pat in flag_patterns:
                if re.search(pat, s, re.IGNORECASE):
                    UI.console.print(f"[bold red]🚩 FLAG FOUND in {os.path.basename(filename)}: {s}[/bold red]")
                    self.loot.append(f"FLAG: {s} ({filename})")

    def _print_loom(self):
        UI.console.print("\n[bold green]=== MISSION COMPLETE ===[/bold green]")
        if self.loot:
            UI.console.print("[bold]🏆 LOOT SECURED:[/bold]")
            for item in self.loot:
                UI.console.print(f" - {item}")
        else:
            UI.console.print("[dim]No definitive flags found.[/dim]")
