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
     S  E  N  T  I  N  E  L    v 4 . 0    G O D   M O D E
"""

def show_banner(animate=False):
    """Displays the epic banner"""
    if animate:
        # Simple loading animation effect
        for _ in range(5):
            colors = ["red", "magenta", "cyan", "blue", "green"]
            color = random.choice(colors)
            styled_art = Text(ASCII_ART, style=f"bold {color}")
            panel = Panel(
                Align.center(styled_art),
                border_style=f"bold {color}",
                subtitle="[dim]CONNECTING TO NEURAL CLOUD...[/dim]"
            )
            UI.console.clear()
            UI.console.print(panel)
            time.sleep(0.15)

    # Final Static Display
    styled_art = Text(ASCII_ART, style="bold red") # RED FOR GOD MODE
    
    panel = Panel(
        Align.center(styled_art),
        border_style="bold red",
        padding=(1, 2),
        title="[bold yellow]★ APEX PREDATOR ACTIVATED ★[/bold yellow]",
        subtitle="[bold white on red] AI-CORE ONLINE • AUTONOMOUS HUNTING • GOD MODE ENABLED [/bold white on red]"
    )
    UI.console.print(panel)
    UI.console.print(Align.center("[bold dim]The Eye That Sees All[/bold dim]"))
    UI.console.print()
