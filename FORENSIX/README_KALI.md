# 🐉 Forensix Sentinel: Kali Linux Setup Guide

You have upgraded Forensix Sentinel to **v4.0 (The Apex Predator)**.
To unlock the full potential of "God Mode", you need to ensure your Kali Linux environment has the necessary tools installed.

## 1. Install System Dependencies

Run this command in your Kali terminal to install the heavy-lifting tools:

## 1. Automated Setup (Recommended)

We have included a script to handle the complex dependencies (`zsteg`, `volatility3`, `7zip`).

Run this in your terminal:

```bash
chmod +x setup_kali.sh
./setup_kali.sh
```

## 2. Manual Installation (If script fails)

If you prefer to install manually:

```bash
# 1. System Tools
sudo apt update
sudo apt install -y python3-pip binwalk steghide foremost libimage-exiftool-perl 7zip ruby-full

# 2. Zsteg (Ruby Gem)
sudo gem install zsteg

# 3. Volatility 3 (Python)
python3 -m pip install volatility3
```

## 2. Install Python Requirements

Navigate to the `FORENSIX` folder and install the python libraries:

```bash
pip3 install -r requirements.txt
```

## 3. How to Run God Mode

1. Start the tool: `python3 app.py`
2. Select **Target** (File or Directory).
3. Choose **Option 4 (God Mode)**.
4. Watch it hunt.

### What God Mode Does

* **Recursion**: If it extracts a zip, it analyzes the files *inside* the zip automatically.
* **Stego**: It automatically tries to extract data from images using `steghide` (with empty password).
* **Cracking**: It attempts to crack zip passwords using `/usr/share/wordlists/rockyou.txt` (if present).
* **Memory**: If a memory dump is found, it runs basic Volatility checks.
* **Flags**: It greps for `CTF{...}`, `flag{...}`, etc. in EVERY file it finds.

## 4. Troubleshooting

* **"Tool not found"**: Ensure the tool is in your system `$PATH` (e.g., try running `binwalk --version`).
* **Permission Denied**: Some operations (like mounting) might require `sudo`, but Forensix tries to run as user.
