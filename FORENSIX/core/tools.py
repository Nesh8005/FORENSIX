import os
import shutil
import subprocess

# Default paths on Kali Linux
WORDLIST_PATH = "/usr/share/wordlists/rockyou.txt"
if not os.path.exists(WORDLIST_PATH):
    # Fallback or empty if not found
    WORDLIST_PATH = None

# Known tool names to check for
REQUIRED_TOOLS = [
    "binwalk", "foremost", "steghide", "zsteg", "strings", 
    "exiftool", "7z", "unzip", "bulk_extractor", "volatility"
]

class ToolManager:
    def __init__(self):
        self.available_tools = {}
        self._check_tools()

    def _check_tools(self):
        """Checks which tools are installed and available in PATH"""
        for tool in REQUIRED_TOOLS:
            path = shutil.which(tool)
            self.available_tools[tool] = path  # Path or None
            
    def has_tool(self, tool_name):
        return self.available_tools.get(tool_name) is not None

    def run_command(self, tool, args, cwd=None, timeout=60):
        """Runs a command and returns distinct stdout/stderr"""
        if not self.has_tool(tool):
            return False, "Tool not found", ""

        cmd = [self.available_tools[tool]] + args
        try:
            # Run with limits
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=cwd, 
                timeout=timeout
            )
            return True, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "Timeout", ""
        except Exception as e:
            return False, str(e), ""

# Global instance
Tools = ToolManager()
