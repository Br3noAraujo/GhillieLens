#!/usr/bin/python3
#! coding: utf-8
"""Coded By Br3noAraujo"""

import sys
import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from subprocess import run, PIPE
import platform

try:
    import cv2
except ImportError:
    print("[!] OpenCV (cv2) is required. Install with: python3 -m pip install opencv-python")
    sys.exit(1)

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:
    print("[!] colorama is required. Install with: python3 -m pip install colorama")
    sys.exit(1)

colorama_init(autoreset=True)
# Military/Sniper color palette
OLIVE = Fore.YELLOW  # Used as olive/khaki
SNIPER_GREEN = Fore.GREEN
CAMO_GREEN = Fore.LIGHTGREEN_EX
BROWN = Fore.LIGHTYELLOW_EX
DANGER = Fore.LIGHTRED_EX
RESET = Style.RESET_ALL

TOOLNAME = "ghillielens"
IS_LINUX = platform.system().lower().startswith("linux")

BASE_DIR = Path.home() / '.ghillielens'
PHOTO_DIR = BASE_DIR / 'photos' / 'boot'
LOG_FILE = BASE_DIR / 'ghillielens.log'
SERVICE_PATH = Path('/etc/systemd/system/ghillielens.service')
SCRIPT_DST = Path('/usr/local/bin/ghillielens.py')

BANNER = f"""
{OLIVE}
                ╔═════════════════════════════════════════════╗
                ║                {SNIPER_GREEN}GhillieLens{OLIVE}                  ║
                ║    {Style.DIM}Mystic boot-time watcher of the unseen{Style.NORMAL}{OLIVE}   ║
                ╚═════════════════════════════════════════════╝{RESET}
"""

SERVICE_CONTENT = f"""[Unit]
Description=GhillieLens - Boot-Time Webcam Capture
After=multi-user.target
Wants=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/ghillielens.py --boot
User=root
Group=root
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""

def check_root():
    if os.geteuid() != 0:
        print(f"{DANGER}❌ You must run as root!{RESET}")
        sys.exit(1)

def check_camera():
    if not Path('/dev/video0').exists():
        print(f"{BROWN}⚠️  Warning: No webcam detected at /dev/video0!{RESET}")
        return False
    return True

def copy_script():
    src = Path(__file__).absolute()
    if SCRIPT_DST.exists() and src != SCRIPT_DST:
        resp = input(f"{BROWN}⚠️  {SCRIPT_DST} already exists. Overwrite? [y/N]: {RESET}").strip().lower()
        if resp != 'y':
            print(f"{DANGER}❌ Installation aborted by user.{RESET}")
            sys.exit(1)
    if src != SCRIPT_DST:
        shutil.copy2(src, SCRIPT_DST)
        SCRIPT_DST.chmod(0o755)
        print(f"{SNIPER_GREEN}✅ Script copied to {SCRIPT_DST}{RESET}")
    else:
        print(f"{SNIPER_GREEN}✅ Script is already at {SCRIPT_DST}{RESET}")

def create_service():
    if SERVICE_PATH.exists():
        resp = input(f"{BROWN}⚠️  {SERVICE_PATH} already exists. Overwrite? [y/N]: {RESET}").strip().lower()
        if resp != 'y':
            print(f"{DANGER}❌ Installation aborted by user.{RESET}")
            sys.exit(1)
    with open(SERVICE_PATH, 'w') as f:
        f.write(SERVICE_CONTENT)
    print(f"{SNIPER_GREEN}✅ systemd service created at {SERVICE_PATH}{RESET}")

def reload_systemd():
    print(f"{OLIVE}⚙️  Reloading systemd...{RESET}")
    run(['systemctl', 'daemon-reexec'])

def enable_service():
    print(f"{OLIVE}⚙️  Enabling ghillielens service...{RESET}")
    run(['systemctl', 'enable', 'ghillielens.service'])
    print(f"{SNIPER_GREEN}✅ Service enabled for boot!{RESET}")

def remove_all():
    if SCRIPT_DST.exists():
        SCRIPT_DST.unlink()
        print(f"{SNIPER_GREEN}✅ Script removed from {SCRIPT_DST}{RESET}")
    else:
        print(f"{BROWN}⚠️  Script not found at {SCRIPT_DST}{RESET}")
    if SERVICE_PATH.exists():
        run(['systemctl', 'disable', 'ghillielens.service'])
        SERVICE_PATH.unlink()
        print(f"{SNIPER_GREEN}✅ Service removed from {SERVICE_PATH}{RESET}")
    else:
        print(f"{BROWN}⚠️  Service not found at {SERVICE_PATH}{RESET}")
    reload_systemd()
    print(f"{SNIPER_GREEN}✅ Removal complete!{RESET}")

def boot_capture():
    """Capture a photo from the primary webcam and save it with restricted permissions."""
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = PHOTO_DIR / f"{ts}.jpg"
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] Webcam not accessible.\n")
        return
    ret, frame = cap.read()
    cap.release()
    if ret:
        cv2.imwrite(str(filename), frame)
        os.chmod(filename, 0o600)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] Photo captured: {filename}\n")
    else:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] Failed to capture photo.\n")

def show_status():
    """Show the status of the ghillielens systemd service."""
    result = run(['systemctl', 'is-enabled', 'ghillielens.service'], stdout=PIPE, stderr=PIPE, text=True)
    status = result.stdout.strip() or result.stderr.strip()
    print(f"{OLIVE}Service status:{RESET} {BROWN}{status}{RESET}")
    result2 = run(['systemctl', 'status', 'ghillielens.service'], stdout=PIPE, stderr=PIPE, text=True)
    print(result2.stdout)

def show_log():
    """Display the contents of the ghillielens log file."""
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print(f"{DANGER}No log file found.{RESET}")

def print_detailed_help():
    # Do not print BANNER here; main() already prints it
    print(f"""
{SNIPER_GREEN}GhillieLens — Stealth Boot-Time Webcam Capture Tool{RESET}

{CAMO_GREEN}Purpose:{RESET}
  Capture a photo from the primary webcam at every system boot (before login) and save it securely.
  Designed for stealth, automation, and hacker/sysadmin practicality.

{OLIVE}Usage:{RESET}
  sudo python3 ghillielens.py --enable      {BROWN}# Install and enable boot-time capture service{RESET}
  sudo python3 ghillielens.py --disable     {BROWN}# Remove/uninstall the service and script{RESET}
  python3 ghillielens.py --status           {BROWN}# Show systemd service status and last boot logs{RESET}
  python3 ghillielens.py --log              {BROWN}# Show the photo capture log file{RESET}
  python3 ghillielens.py --boot             {BROWN}# (Internal) Run a stealth capture (used by systemd){RESET}

{OLIVE}How it works:{RESET}
  - On install, the script copies itself to /usr/local/bin/ghillielens.py and creates a systemd service.
  - At every boot (before user login), systemd runs: /usr/local/bin/ghillielens.py --boot
  - The script captures a single photo from /dev/video0 (if available) and saves it to:
      {CAMO_GREEN}~/.ghillielens/photos/boot/YYYY-MM-DD_HH-MM-SS.jpg{RESET}
  - Photos are saved with permission 600 (owner read/write only).
  - All events are logged to: {CAMO_GREEN}~/.ghillielens/ghillielens.log{RESET}

{OLIVE}Commands:{RESET}
  {CAMO_GREEN}-e, --enable{RESET}    Install and enable the boot-time capture service (requires root)
  {CAMO_GREEN}-d, --disable{RESET}   Remove/uninstall the service and script (requires root)
  {CAMO_GREEN}-s, --status{RESET}    Show the systemd service status and last boot logs
  {CAMO_GREEN}-l, --log{RESET}       Show the ghillielens log file
  {CAMO_GREEN}--boot{RESET}          (Internal) Run a stealth capture (used by systemd)

{OLIVE}Security:{RESET}
  - Photos are only accessible by the user (chmod 600).
  - The service runs as root to ensure access before login.
  - No UI or notification is shown at boot.

{OLIVE}Examples:{RESET}
  {BROWN}# Install and activate:{RESET}
    sudo python3 ghillielens.py --enable
  {BROWN}# Remove/uninstall:{RESET}
    sudo python3 ghillielens.py --disable
  {BROWN}# Check status:{RESET}
    python3 ghillielens.py --status
  {BROWN}# View log:{RESET}
    python3 ghillielens.py --log

{OLIVE}Log/Photo location:{RESET}
  {CAMO_GREEN}~/.ghillielens/photos/boot/{RESET}   (photos)
  {CAMO_GREEN}~/.ghillielens/ghillielens.log{RESET} (log)

{OLIVE}Hacker/Unix tips:{RESET}
  - You can test the capture manually: python3 ghillielens.py --boot
  - All actions print colorized, clear feedback.
  - Designed for minimal footprint and maximum stealth.

{CAMO_GREEN}github.com/Br3noAraujo | Coded By Br3noAraujo{RESET}
""")

def print_minimal_help():
    print(BANNER)
    print(f"""
{SNIPER_GREEN}GhillieLens — Stealth Boot-Time Webcam Capture Tool{RESET}

{CAMO_GREEN}Usage:{RESET}
  sudo python3 ghillielens.py --enable      {BROWN}# Install and enable boot-time capture service{RESET}
  sudo python3 ghillielens.py --disable     {BROWN}# Remove/uninstall the service and script{RESET}
  python3 ghillielens.py --status           {BROWN}# Show systemd service status{RESET}
  python3 ghillielens.py --log              {BROWN}# Show the photo capture log file{RESET}

{CAMO_GREEN}For detailed help, use:{RESET}  python3 ghillielens.py -h
""")

def main():
    if len(sys.argv) == 1:
        print_minimal_help()
        return
    print(BANNER)
    parser = argparse.ArgumentParser(
        description=f"{TOOLNAME} — Stealth webcam photo capture at boot and installer.",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False)
    parser.add_argument('-h', '--help', action='store_true', help='Show detailed help and exit')
    parser.add_argument('-e', '--enable', action='store_true', help='Enable systemd boot service (install)')
    parser.add_argument('-d', '--disable', action='store_true', help='Disable systemd boot service (uninstall)')
    parser.add_argument('-s', '--status', action='store_true', help='Show systemd service status')
    parser.add_argument('-l', '--log', action='store_true', help='Show log file')
    parser.add_argument('--boot', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.help:
        print_detailed_help()
        return
    if args.boot:
        boot_capture()
        return
    if args.enable:
        check_root()
        check_camera()
        copy_script()
        create_service()
        reload_systemd()
        enable_service()
        print(f"{SNIPER_GREEN}🌌 Installation complete! GhillieLens will capture a photo on next boot.{RESET}")
    elif args.disable:
        check_root()
        remove_all()
    elif args.status:
        show_status()
    elif args.log:
        show_log()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
