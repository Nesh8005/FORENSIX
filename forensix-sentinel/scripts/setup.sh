#!/bin/bash

# 🛡️ Forensix Sentinel - Kali Linux Setup Script
# =================================================

set -e

echo -e "\033[1;32m[+] Starting Forensix Sentinel Setup...\033[0m"

# 1. Update System
echo -e "\033[1;34m[*] Updating system repositories...\033[0m"
sudo apt-get update

# 2. Install System Dependencies (Kali specific)
echo -e "\033[1;34m[*] Installing system dependencies...\033[0m"
sudo apt-get install -y \
    python3-venv \
    python3-pip \
    python3-dev \
    libmagic1 \
    libewf-dev \
    libtsk-dev \
    exiftool \
    binwalk \
    foremost \
    volatility3 \
    wireshark-common \
    tshark \
    sleuthkit

# 3. Create Virtual Environment
echo -e "\033[1;34m[*] Creating Python virtual environment...\033[0m"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "    Created 'venv'"
else
    echo "    'venv' already exists"
fi

# 4. Activate and Install Python Deps
echo -e "\033[1;34m[*] Installing Python packages...\033[0m"
source venv/bin/activate
pip install --upgrade pip
pip install -e .

# 5. Download AI Models
echo -e "\033[1;34m[*] Downloading AI models...\033[0m"
python3 -m spacy download en_core_web_sm

echo -e "\033[1;32m[+] Setup Complete! 🐉\033[0m"
echo -e "    Run: source venv/bin/activate"
echo -e "    Run: forensix --help"
