import sys
import os
import time

# Robust Import Logic (Handles running from root OR inside folder)
try:
    # Try fully qualified package import
    from forensix.interface.theme import UI
    from forensix.interface.banner import show_banner
    from forensix.core.file_analyzer import FileAnalyzer
    from forensix.modules.extractor import ArchiveExtractor, cleanup_extracted
    from forensix.modules.reporting import ReportGenerator
except ImportError:
    # Fallback to local import (if running inside 'forensix' folder)
    # Add current dir to path just in case
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from interface.theme import UI
        from interface.banner import show_banner
        from core.file_analyzer import FileAnalyzer
        from modules.extractor import ArchiveExtractor, cleanup_extracted
        from modules.reporting import ReportGenerator
    except ImportError as e:
        print(f"CRITICAL ERROR: Could not import modules. {e}")
        sys.exit(1)

from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.console import Group
from rich.text import Text

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class ForensixApp:
    def __init__(self):
        self.target = None
        self.analysis_results = [] # Store results here

    def load_modules(self):
        # ... (Same loading animation as before) ...
        pass # Skipping re-implementation for brevity

    def show_main_menu(self):
        # ... (Same menu structure) ...
        while True:
            clear_screen()
            show_banner()
            
            target_display = f"[bold green]{self.target}[/bold green]" if self.target else "[bold red]NONE SELECTED[/bold red]"
            
            table = Table(show_header=False, box=None, padding=0)
            table.add_column("Key", style="bold yellow", width=4)
            table.add_column("Action", style="cyan")
            table.add_column("Description", style="dim")

            table.add_row("1", "🎯 SET TARGET", "Select file, disk image, or directory to analyze")
            table.add_row("2", "🚀 QUICK SCAN", "Fast analysis of metadata and surface artifacts")
            table.add_row("3", "🔥 DEEP FORENSICS", "The 'Beast Mode' - Entropy, Strings, Secrets")
            table.add_row("4", "🤖 AI FLAG HUNT", "Use Neural Networks to find CTF flags")
            table.add_row("5", "📊 VIEW REPORT", "View detailed analysis results")
            table.add_row("0", "❌ EXIT", "Close Forensix Sentinel")
            
            panel = Panel(Group(f"Target: {target_display}", "", table), title="[bold]COMMAND CENTER[/bold]", border_style="blue")
            UI.console.print(panel)

            choice = Prompt.ask("Select Action", choices=["1", "2", "3", "4", "5", "0"])

            if choice == "1": self.set_target()
            elif choice == "2": self.run_scan(deep=False)
            elif choice == "3": self.run_scan(deep=True)
            elif choice == "4": self.run_god_mode() 
            elif choice == "5": self.view_report()
            elif choice == "0": sys.exit(0)

    def run_god_mode(self):
        if not self.target:
            UI.print_error("Set a target first!")
            time.sleep(1)
            return
            
        try:
            from forensix.core.god_mode import GodMode
            gm = GodMode(self.target)
            gm.hunt()
            
            # Save results to main list for reporting
            # This is a bit of a hack to merge UI, but fine for now
            # self.analysis_results.extend(gm.results) 
            
            Prompt.ask("\nPress Enter to return to menu")
        except ImportError:
            # Local fallback
            try:
                from core.god_mode import GodMode
                gm = GodMode(self.target)
                gm.hunt()
                Prompt.ask("\nPress Enter to return to menu")
            except Exception as e:
                UI.print_error(f"God Mode Failed: {e}")

    def set_target(self):
        target = Prompt.ask("\n[bold cyan]Enter path to target file/directory[/bold cyan]").strip('"\'')
        if os.path.exists(target):
            self.target = os.path.abspath(target)
        else:
            UI.print_error("Path does not exist!")
            time.sleep(1)

    def run_scan(self, deep=False):
        if not self.target:
            return

        mode_name = "DEEP FORENSICS" if deep else "SURFACE RECON"
        UI.console.print(f"\n[bold]Starting {mode_name} on {self.target}...[/bold]")
        
        # Prepare file list traversal
        files_to_scan = []
        if os.path.isfile(self.target): 
            files_to_scan = [self.target]
        else:
            for root, dirs, files in os.walk(self.target):
                for file in files: files_to_scan.append(os.path.join(root, file))

        # ⚡ THE ADVANCED DASHBOARD ⚡
        scan_table = Table(title=f"LIVE INTELLIGENCE FEED", border_style="blue")
        scan_table.add_column("File", style="cyan", width=30)
        scan_table.add_column("Type", style="dim", width=15)
        scan_table.add_column("Score / AI", style="magenta", width=20) # Wider for AI Badge
        scan_table.add_column("INTELLIGENCE FINDINGS", style="bold red") # The good stuff

        self.analysis_results = [] 
        
        # Import Extractor (Moved to Global)
        extractor = ArchiveExtractor()

        with Live(scan_table, refresh_per_second=10) as live:
            count = 0
            
            # Use index-based loop because files_to_scan grows dynamically
            i = 0
            while i < len(files_to_scan):
                filepath = files_to_scan[i]
                i += 1
                
                # Check for recursion bomb (limit 1000 files for safety)
                if count > 1000: break

                try:
                    analyzer = FileAnalyzer(filepath)
                    success = analyzer.analyze(deep=deep)
                    
                    if success:
                        report = analyzer.get_report_data()
                        self.analysis_results.append(report)
                        
                        # RECURSIVE EXTRACTION
                        if deep and "archive" in report['type']:
                            new_files = extractor.extract(filepath)
                            if new_files:
                                files_to_scan.extend(new_files)
                                report['findings'].append(f"Extracted {len(new_files)} files")

                        # Determine Status/Color based on findings
                        findings_text = ""
                        if report['findings']:
                            # Highlight findings in RED
                            findings_text = "[bold red]" + ", ".join(report['findings']) + "[/bold red]"
                        elif report['entropy'] > 7.5:
                            findings_text = "[yellow]⚠️  High Entropy (Encrypted?)[/yellow]"
                        elif "text" in report['type'] and report['strings_count'] > 0:
                            findings_text = f"[green]Parsed {report['strings_count']} strings[/green]"
                        else:
                            findings_text = "[dim]Clean[/dim]"

                        # Add row (Manage table size)
                        if scan_table.row_count > 15:
                            # Rich tables don't support removing rows easily, so we just clear/rebuild rarely or let it scroll
                            # For dashboard feel, we focus on *last* entries
                            pass 

                        # AI / NEURAL ANALYSIS
                        try:
                            from forensix.core.neural_engine import NeuralEngine
                            brain = NeuralEngine()
                            ai_result = brain.score_artifact(report['entropy'], report['findings'], report['type'])
                            
                            ai_badge = ""
                            if ai_result['score'] > 80:
                                ai_badge = "[bold red blink]☠️ CRITICAL[/bold red blink]"
                            elif ai_result['score'] > 50:
                                ai_badge = "[bold yellow]⚠️ SUSPICIOUS[/bold yellow]"
                            else:
                                ai_badge = "[green]✓ SAFE[/green]"
                                
                            # Update findings to include AI badge
                            report['findings'].insert(0, f"AI: {ai_result['assessment']} ({ai_result['score']}%)")
                        except ImportError:
                            # Fallback if module issue
                            ai_badge = "[dim]AI OFF[/dim]"

                        # Use AI Badge in table instead of raw entropy sometimes? 
                        # Or just append to findings
                        
                        scan_table.add_row(
                            os.path.basename(filepath)[:28], 
                            report['type'], 
                            f"{report['entropy']} {ai_badge}", 
                            findings_text
                        )
                        count += 1
                except Exception as e:
                    pass

        UI.print_success(f"Analysis Complete. {count} Artifacts Processed.")
        cleanup_extracted() # Clean up temp files
        Prompt.ask("Press Enter to continue")

    def view_report(self):
        if not self.analysis_results:
            UI.print_warning("No scan results yet! Run a scan (Option 2 or 3) first.")
            time.sleep(2)
            return

        clear_screen()
        UI.header("📊 GENERATING REPORT")
        
        import webbrowser
        
        try:
            generator = ReportGenerator()
            report_path = generator.generate(self.analysis_results, str(self.target))
            
            UI.print_success(f"Report Generated: {report_path}")
            UI.print_info("Opening in browser...")
            time.sleep(1)
            
            webbrowser.open('file://' + os.path.abspath(report_path))
            
        except Exception as e:
            UI.print_error(f"Report generation failed: {e}")
        
        Prompt.ask("\nPress Enter to return to menu")
        
    # ... (Other methods) ...

def main():
    clear_screen()
    show_banner(animate=False)
    app = ForensixApp()
    app.show_main_menu()

if __name__ == "__main__":
    main()
