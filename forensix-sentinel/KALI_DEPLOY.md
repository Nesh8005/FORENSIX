# 🐉 Deploying Forensix Sentinel to Kali Linux

This project is optimized for **Kali Linux**. Follow these steps to deploy it to your Kali machine.

## 1. Transfer Files

Copy the entire `forensix-sentinel` folder to your Kali machine.
You can use a USB drive, `scp`, or git.

## 2. Run the Setup Script

Open a terminal in the `forensix-sentinel` directory on your Kali machine.

```bash
# Make the script executable
chmod +x scripts/setup.sh

# Run the setup (installs system tools + python env)
./scripts/setup.sh
```

## 3. Activate & Run

```bash
source venv/bin/activate
forensix --help
```

## ⚠️ Kali-Specific Notes

- **Root Permissions**: You might need `sudo` for `volatility` or network capture features later.
- **System Packages**: The `setup.sh` installs: `libmagic1`, `libewf`, `libtsk`, `exiftool`, `volatility3`, `sleuthkit`.
- **Paths**: The tool adheres to standard Linux paths.
