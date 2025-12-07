import os
import click
from rich.console import Console
from rich.table import Table
from rich.progress import track
from forensix.modules.file_analyzer import FileAnalyzer

console = Console()

@click.group()
@click.version_option()
def cli():
    """Forensix Sentinel - Advanced Digital Forensics Tool (Kali Optimized)"""
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--recursive', '-r', is_flag=True, help='Recursively scan directories')
def scan(path, recursive):
    """Scan a file or directory for analysis"""
    console.rule("[bold green]Forensix Sentinel - Scan")
    
    analyzer = FileAnalyzer()
    
    # 1. Collect files
    files_to_scan = []
    if os.path.isfile(path):
        files_to_scan.append(path)
    elif os.path.isdir(path):
        if recursive:
            console.print(f"[yellow]Recursively scanning: {path}[/yellow]")
            for root, _, files in os.walk(path):
                for file in files:
                    files_to_scan.append(os.path.join(root, file))
        else:
            # Non-recursive: just files in top dir
            console.print(f"[yellow]Scanning directory (depth=1): {path}[/yellow]")
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isfile(full_path):
                    files_to_scan.append(full_path)
    
    console.print(f"[bold]Found {len(files_to_scan)} files to analyze.[/bold]")
    
    # 2. Setup Table
    table = Table(title="Analysis Results")
    table.add_column("Filename", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Size", justify="right")
    table.add_column("MD5 Hash", style="green")
    
    # 3. Process
    results = []
    for file_path in track(files_to_scan, description="Analyzing..."):
        result = analyzer.analyze(file_path)
        if "error" in result:
             console.print(f"[red]Error analyzing {file_path}: {result['error']}[/red]")
             continue
             
        results.append(result)
        
        # Add to table
        fname = result["filename"]
        ftype = result["mime_type"]
        fsize = f"{result['size_bytes']:,} B"
        fhash = result["hashes"].get("md5", "N/A")
        
        table.add_row(fname, ftype, fsize, fhash)
        
    # 4. Show Output
    console.print(table)
