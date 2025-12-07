import sys
import time
import os
from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.console import Group
from rich.text import Text

# Import our UI components
from interface.theme import UI
from interface.banner import show_banner

# Import Core Engine
from core.file_analyzer import FileAnalyzer

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
            elif choice == "4": self.run_scan(deep=True) # AI Hunt is now integrated into Deep Scan
            elif choice == "5": self.view_report()
            elif choice == "0": sys.exit(0)

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
        scan_table.add_column("Entropy", style="magenta", width=8) # New!
        scan_table.add_column("INTELLIGENCE FINDINGS", style="bold red") # The good stuff

        self.analysis_results = [] 

        with Live(scan_table, refresh_per_second=10) as live:
            count = 0
            for filepath in files_to_scan:
                analyzer = FileAnalyzer(filepath)
                success = analyzer.analyze(deep=deep)
                
                if success:
                    report = analyzer.get_report_data()
                    self.analysis_results.append(report)
                    
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

                    # Add row
                    scan_table.add_row(
                        os.path.basename(filepath)[:28], 
                        report['type'], 
                        str(report['entropy']), 
                        findings_text
                    )
                    count += 1
                    # Keep table short
                    if count > 10: 
                        # In a real app we'd manage a sliding window, here we just keep adding
                        pass

        UI.print_success(f"Analysis Complete. {count} Artifacts Processed.")
        Prompt.ask("Press Enter to continue")

    def view_report(self):
        # Implementation for viewing detailed results...
        pass
        
    # ... (Other methods) ...

def main():
    clear_screen()
    show_banner(animate=False)
    app = ForensixApp()
    app.show_main_menu()

if __name__ == "__main__":
    main()
