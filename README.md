# GhillieLens 🪖 🌿

<p align="center">
  <img src="https://i.imgur.com/KcT83iu.png" alt="GhillieLens Banner" width="600"/>
</p>

> **GhillieLens** — Stealth Boot-Time Webcam Capture Tool
>
> 🪖 Inspired by sniper ghillie suits, this tool blends into your system, capturing a photo from your webcam at every boot — before login, with zero UI or alerts. For sysadmins, hackers, and those who value stealth and control.

---

## ⚔️ Features

- 📸 **Stealth photo capture** at every system boot (before login)
- 🔒 **Photos saved securely** (chmod 600) in a hidden directory
- 🪖 **No UI, no notifications** — pure stealth
- ⚙️ **Easy CLI management**: enable, disable, status, log
- 🌱 **Military/sniper color palette** for all outputs
- 📁 **Self-contained** — no dependencies beyond Python, OpenCV, and colorama

---

## 📦 Installation

```bash
sudo python3 ghillielens.py --enable
```

- The script copies itself to `/usr/local/bin/ghillielens.py` and creates a systemd service.
- At every boot, systemd runs the script in stealth mode.

<p align="center">
  <img src="https://i.imgur.com/DrUxAww.png" alt="Enable Service" width="600"/>
</p>

---

## 🚩 Uninstall

```bash
sudo python3 ghillielens.py --disable
```

- Removes the systemd service and the script from `/usr/local/bin/`.

<p align="center">
  <img src="https://i.imgur.com/Oo11ZkD.png" alt="Disable Service" width="600"/>
</p>

---

## 🧭 Usage

| Command                                 | Description                                  |
|-----------------------------------------|----------------------------------------------|
| `sudo python3 ghillielens.py --enable`  | 🪖 Enable boot-time capture                  |
| `sudo python3 ghillielens.py --disable` | 🌳 Disable & remove service                  |
| `python3 ghillielens.py --status`       | 🔍 Show service status & last logs           |
| `python3 ghillielens.py --log`          | 📜 Show the photo capture log                |
| `python3 ghillielens.py --boot`         | 📸 (Internal) Stealth capture (systemd)      |

---

## 🌲 How it works

- On install, the script is copied and a systemd service is created.
- At every boot (before user login), systemd runs: `/usr/local/bin/ghillielens.py --boot`
- The script captures a single photo from `/dev/video0` (if available) and saves it to:
  - `~/.ghillielens/photos/boot/YYYY-MM-DD_HH-MM-SS.jpg`
- Photos are saved with permission 600 (owner read/write only).
- All events are logged to: `~/.ghillielens/ghillielens.log`

---

## 🔒 Security

- 🔑 Photos are only accessible by the user (chmod 600)
- 🚫 No UI or notification is shown at boot
- 🛡️ The service runs as root to ensure access before login

---

## 🌱 Example Log & Photo Location

- Photos: `~/.ghillielens/photos/boot/`
- Log:    `~/.ghillielens/ghillielens.log`

---

## 🔭 Tips for Hackers & Sysadmins

- Test the capture manually: `python3 ghillielens.py --boot`
- All actions print colorized, clear feedback
- Designed for minimal footprint and maximum stealth

---

## 👤 Credits

- **Coded By [Br3noAraujo](https://github.com/Br3noAraujo)**
- Inspired by the spirit of the lone sysadmin and the unseen sniper

---

<p align="center">
  <b>github.com/Br3noAraujo</b> | <i>Stay hidden. Stay sharp.</i>
</p> 