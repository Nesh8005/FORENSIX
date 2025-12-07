import sys
import time
import os
from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.console import Group

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
        """Simulate loading heavy AI modules with a progress bar"""
        from rich.progress import Progress, SpinnerColumn, TextColumn
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task1 = progress.add_task("[cyan]Loading AI Neural Networks...", total=100)
            task2 = progress.add_task("[magenta]Initializing File System Parsers...", total=100)
            task3 = progress.add_task("[green]Calibrating Steganography Detectors...", total=100)

            while not progress.finished:
                progress.update(task1, advance=2.0) # Faster for dev
                progress.update(task2, advance=3.0)
                progress.update(task3, advance=1.5)
                time.sleep(0.01)

        UI.print_success("All Modules Loaded Successfully")

    def show_main_menu(self):
        while True:
            clear_screen()
            show_banner()
            
            # Status Board
            if self.target:
                target_display = f"[bold green]{self.target}[/bold green]"
            else:
                target_display = "[bold red]NONE SELECTED[/bold red]"
            
            table = Table(show_header=False, box=None, padding=0)
            table.add_column("Key", style="bold yellow", width=4)
            table.add_column("Action", style="cyan")
            table.add_column("Description", style="dim")

            table.add_row("1", "🎯 SET TARGET", "Select file, disk image, or directory to analyze")
            table.add_row("2", "🚀 QUICK SCAN", "Fast analysis of metadata and surface artifacts")
            table.add_row("3", "🔥 DEEP FORENSICS", "The 'Beast Mode' - String extraction & deep analysis")
            table.add_row("4", "🤖 AI FLAG HUNT", "Use Neural Networks to find CTF flags")
            table.add_row("5", "📊 VIEW REPORT", "View detailed analysis results")
            table.add_row("0", "❌ EXIT", "Close Forensix Sentinel")
            
            panel = Panel(
                Group(
                    f"Current Target: {target_display}",
                    "",  # Spacer
                    table
                ),
                title="[bold]COMMAND CENTER[/bold]",
                border_style="blue"
            )
            UI.console.print(panel)

            choice = Prompt.ask("Select Action", choices=["1", "2", "3", "4", "5", "0"])

            if choice == "1":
                self.set_target()
            elif choice == "2":
                self.run_scan(deep=False)
            elif choice == "3":
                self.run_scan(deep=True)
            elif choice == "4":
                self.run_ai_hunt()
            elif choice == "5":
                self.view_report()
            elif choice == "0":
                UI.console.print("[bold red]Shutting down...[/bold red]")
                sys.exit(0)

    def set_target(self):
        target = Prompt.ask("\n[bold cyan]Enter path to target file/directory (absolute path)[/bold cyan]")
        
        # Remove quotes if user dragged and dropped
        target = target.strip('"\'')
        
        if os.path.exists(target):
            self.target = os.path.abspath(target)
            UI.print_success(f"Target set to: {self.target}")
            time.sleep(1)
        else:
            UI.print_error("Path does not exist!")
            time.sleep(1.5)

    def run_scan(self, deep=False):
        if not self.target:
            UI.print_error("Please set a target first!")
            time.sleep(1.5)
            return

        mode_name = "DEEP" if deep else "QUICK"
        UI.console.print(f"\n[bold]Starting {mode_name} SCAN on {self.target}...[/bold]")
        
        # Prepare file list
        files_to_scan = []
        if os.path.isfile(self.target):
            files_to_scan = [self.target]
        else:
            for root, dirs, files in os.walk(self.target):
                for file in files:
                    files_to_scan.append(os.path.join(root, file))

        # Setup Live Table
        scan_table = Table(title=f"Live Scan Results - {mode_name}")
        scan_table.add_column("File", style="cyan")
        scan_table.add_column("Type", style="bold magenta")
        scan_table.add_column("Size", style="dim")
        scan_table.add_column("Status", style="green")

        self.analysis_results = [] # Reset results

        with Live(scan_table, refresh_per_second=10) as live:
            count = 0
            for filepath in files_to_scan:
                filename = os.path.basename(filepath)
                
                # Update status
                # (Ideally we'd update a progress bar here too)
                
                # Analyze
                analyzer = FileAnalyzer(filepath)
                success = analyzer.analyze(deep=deep)
                
                if success:
                    report = analyzer.get_report_data()
                    self.analysis_results.append(report)
                    
                    # Add to table (limit visuals to last 10 lines to avoid scroll spam)
                    scan_table.add_row(
                        filename[:20], 
                        report['type'], 
                        f"{report['size_bytes']} B", 
                        "✅ Done"
                    )
                    count += 1
                    time.sleep(0.1) # Artifical delay so user can see it happening

        UI.print_success(f"Scan Complete! Processed {count} files.")
        Prompt.ask("Press Enter to continue")

    def run_ai_hunt(self):
        if not self.target:
            UI.print_error("Please set a target first!")
            time.sleep(1.5)
            return
            
        UI.header("🤖 INITIALIZING AI FLAG HUNTER")
        # Placeholder for AI logic
        UI.console.print("[dim]Loading GPT-2 Detection Model...[/dim]")
        time.sleep(1)
        
        UI.print_success("AI Models Active. Hunting for flags...")
        time.sleep(1)
        
        # Simple string search for flags in previous results
        found_flags = []
        for res in self.analysis_results:
            if 'strings_sample' in res:
                for s in res['strings_sample']:
                    if "CTF" in s or "flag" in s.lower():
                        found_flags.append(f"{res['filename']}: {s}")
        
        if found_flags:
            UI.console.print(Panel(
                "\n".join(found_flags), 
                title="[bold red]🚩 POTENTIAL FLAGS FOUND![/bold red]", 
                border_style="red"
            ))
        else:
             UI.console.print("[yellow]No obvious flags found in scan data. Try Deep Scan first?[/yellow]")

        Prompt.ask("Press Enter to continue")

    def view_report(self):
        if not self.analysis_results:
            UI.print_warning("No scan results yet! Run a scan first.")
            time.sleep(1.5)
            return

        clear_screen()
        UI.header("📊 ANALYSIS REPORT")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Filename", style="cyan")
        table.add_column("Type")
        table.add_column("SHA256 (First 8)", style="dim")
        table.add_column("Strings Found", justify="right")
        
        for res in self.analysis_results:
            sha_short = res['hashes']['sha256'][:8] + "..."
            strings_count = res.get('strings_count', 0)
            table.add_row(
                res['filename'],
                res['type'],
                sha_short,
                str(strings_count)
            )
            
        UI.console.print(table)
        Prompt.ask("\nPress Enter to return to menu")

def main():
    clear_screen()
    show_banner(animate=True)
    time.sleep(0.5)
    
    app = ForensixApp()
    app.load_modules()
    time.sleep(0.5)
    app.show_main_menu()

if __name__ == "__main__":
    main()
