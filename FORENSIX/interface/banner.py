from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.layout import Layout
from .theme import UI
import time
import random

ASCII_ART = """
███████╗ ██████╗ ██████╗ ███████╗███╗   ██╗███████╗██╗██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██║╚██╗██╔╝
█████╗  ██║   ██║██████╔╝█████╗  ██╔██╗ ██║███████╗██║ ╚███╔╝ 
██╔══╝  ██║   ██║██╔══██╗██╔══╝  ██║╚██╗██║╚════██║██║ ██╔██╗ 
██║     ╚██████╔╝██║  ██║███████╗██║ ╚████║███████║██║██╔╝ ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═╝
     S  E  N  T  I  N  E  L    v 2 . 0    B E A S T
"""

def show_banner(animate=False):
    """Displays the epic banner"""
    if animate:
        # Simple loading animation effect
        for _ in range(3):
            colors = ["magenta", "cyan", "blue", "green"]
            color = random.choice(colors)
            styled_art = Text(ASCII_ART, style=f"bold {color}")
            panel = Panel(
                Align.center(styled_art),
                border_style=f"bold {color}",
                subtitle="[dim]INITIALIZING NEURAL NETWORKS...[/dim]"
            )
            UI.console.clear()
            UI.console.print(panel)
            time.sleep(0.1)

    # Final Static Display
    styled_art = Text(ASCII_ART, style="bold color(201)") # Hot pink/Magenta
    
    panel = Panel(
        Align.center(styled_art),
        border_style="bold blue",
        padding=(1, 2),
        title="[bold yellow]★ ULTIMATE FORENSICS TOOLKIT ★[/bold yellow]",
        subtitle="[bold cyan]AI-POWERED • INFINITE DEPTH • UNDETECTABLE[/bold cyan]"
    )
    UI.console.print(panel)
    UI.console.print(Align.center("[dim]System Ready... Waiting for Input[/dim]"))
    UI.console.print()
