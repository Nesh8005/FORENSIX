from rich.theme import Theme
from rich.console import Console
from rich.style import Style

# 🎨 THE FORENSIX NEON THEME
# High contrast, cyberpunk functionality
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "yellow",
    "error": "bold red",
    "danger": "bold red reverse blink",
    "success": "bold green",
    "title": "bold magenta",
    "subtitle": "bold blue",
    "highlight": "bold cyan",
    "panel.border": "blue",
    "table.header": "bold magenta",
    "key": "bold yellow",
    "value": "cyan",
    "banner": "bold color(201)", # Hot pink
    "progress.bar": "color(39)", # Deep turquoise
    "progress.percentage": "bold color(39)",
})

class UI:
    """Central UI Manager for a consistent look and feel"""
    console = Console(theme=custom_theme)

    @staticmethod
    def print_error(msg):
        UI.console.print(f"[error]❌ {msg}[/error]")

    @staticmethod
    def print_success(msg):
        UI.console.print(f"[success]✅ {msg}[/success]")

    @staticmethod
    def print_info(msg):
        UI.console.print(f"[info]ℹ️  {msg}[/info]")
    
    @staticmethod
    def print_warning(msg):
        UI.console.print(f"[warning]⚠️  {msg}[/warning]")

    @staticmethod
    def header(text):
        UI.console.print(f"\n[title]═ {text} ═[/title]")
