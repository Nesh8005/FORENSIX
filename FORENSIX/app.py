import sys
import time
import os
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Group

# Import our UI components
from interface.theme import UI
from interface.banner import show_banner

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class ForensixApp:
    def __init__(self):
        self.target = None
        self.modules_loaded = []

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
                progress.update(task1, advance=0.9)
                progress.update(task2, advance=1.2)
                progress.update(task3, advance=0.5)
                time.sleep(0.02)

        UI.print_success("All Modules Loaded Successfully")

    def show_main_menu(self):
        while True:
            clear_screen()
            show_banner()
            
            # Status Board
            target_display = f"[bold green]{self.target}[/bold green]" if self.target else "[bold red]NONE SELECTED[/bold red]"
            
            table = Table(show_header=False, box=None, padding=0)
            table.add_column("Key", style="bold yellow", width=4)
            table.add_column("Action", style="cyan")
            table.add_column("Description", style="dim")

            table.add_row("1", "🎯 SET TARGET", "Select file, disk image, or directory to analyze")
            table.add_row("2", "🚀 QUICK SCAN", "Fast analysis of metadata and surface artifacts")
            table.add_row("3", "🔥 DEEP FORENSICS", "The 'Beast Mode' - Infinite recursion & hidden data")
            table.add_row("4", "🤖 AI FLAG HUNT", "Use Neural Networks to find CTF flags")
            table.add_row("5", "📊 VIEW REPORT", "Open the HTML/PDF report of findings")
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
                self.run_scan(mode="quick")
            elif choice == "3":
                self.run_scan(mode="deep")
            elif choice == "4":
                self.run_ai_hunt()
            elif choice == "5":
                self.view_report()
            elif choice == "0":
                UI.console.print("[bold red]Shutting down...[/bold red]")
                sys.exit(0)

    def set_target(self):
        target = Prompt.ask("\n[bold cyan]Enter path to target file/directory[/bold cyan]")
        if os.path.exists(target):
            self.target = os.path.abspath(target)
            UI.print_success(f"Target set to: {self.target}")
            time.sleep(1)
        else:
            UI.print_error("Path does not exist!")
            time.sleep(1.5)

    def run_scan(self, mode):
        if not self.target:
            UI.print_error("Please set a target first!")
            time.sleep(1.5)
            return

        UI.console.print(f"\n[bold]Starting {mode.upper()} SCAN on {self.target}...[/bold]")
        
        # Simulate scanning visual
        from rich.live import Live
        from rich.table import Table
        
        scan_table = Table(title=f"Live Scan Results - {mode.upper()}")
        scan_table.add_column("File", style="cyan")
        scan_table.add_column("Status", style="green")
        scan_table.add_column("Findings", style="magenta")

        with Live(scan_table, refresh_per_second=4) as live:
            # Fake findings for demo
            time.sleep(0.5)
            scan_table.add_row("image.jpg", "Parsed", "Exif: GPS Found")
            time.sleep(0.5)
            scan_table.add_row("backup.zip", "Extracted", "2 nested files")
            time.sleep(0.5)
            if mode == "deep":
                scan_table.add_row("hidden_conf.txt", "Analyzed", "API Key Found")
                time.sleep(0.5)
                scan_table.add_row("memory.dmp", "Processed", "Password in stack")
                
        UI.print_success("Scan Complete! Report generated.")
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
        UI.console.print("[dim]Loading CNN Stego Classifier...[/dim]")
        time.sleep(1)
        
        UI.print_success("AI Models Active. Hunting for flags...")
        time.sleep(2)
        
        UI.console.print(Panel("[bold red]🚩 FLAG FOUND![/bold red]\n\nValue: [yellow]CTF{ai_found_this_flag}[/yellow]\nConfidence: [green]99.8%[/green]", title="Detection Alert", border_style="red"))
        Prompt.ask("Press Enter to continue")

    def view_report(self):
        UI.print_info("Opening HTML report...")
        time.sleep(1)
        # Here we would open the browser
        UI.print_success("Report opened in default browser.")
        time.sleep(1)

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
