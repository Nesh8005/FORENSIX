#!/bin/bash

# COLORS
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}[+] Setting up FORENSIX SENTINEL Environment...${NC}"

# 1. System Packages (APT)
echo -e "${GREEN}[+] Installing System Tools via APT...${NC}"
sudo apt update
# Core tools
sudo apt install -y python3-pip python3-venv binwalk steghide foremost libimage-exiftool-perl 7zip
# Optional: bruteforce-luks if available, else skip
sudo apt install -y bruteforce-luks || echo -e "${RED}[!] bruteforce-luks not found, skipping.${NC}"

# 2. Ruby Tools (Zsteg)
echo -e "${GREEN}[+] Installing Zsteg (Ruby)...${NC}"
# Check if gem exists
if command -v gem &> /dev/null; then
    sudo gem install zsteg
else
    echo -e "${RED}[!] Ruby/Gem not found. Installing ruby-full...${NC}"
    sudo apt install -y ruby-full
    sudo gem install zsteg
fi

# 3. Volatility 3 (Manual Install)
# Volatility 3 is often not in apt. Best to use pip or git.
echo -e "${GREEN}[+] Installing Volatility 3...${NC}"
if ! command -v vol &> /dev/null && ! command -v volatility3 &> /dev/null; then
    # Install via pip/git best practice usually, but let's try pipx or pip
    python3 -m pip install volatility3
    
    # If that fails to put 'vol' in path, we might need symbol lookup tables later, but this is a start.
    echo -e "${GREEN}[+] Volatility3 installed via pip.${NC}"
else
    echo -e "${GREEN}[+] Volatility detected.${NC}"
fi

# 4. Python Dependencies
echo -e "${GREEN}[+] Installing Python Requirements...${NC}"
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

echo -e "${GREEN}[+] SETUP COMPLETE! Run 'python3 app.py' to start.${NC}"
