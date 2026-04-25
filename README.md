# ⬡ IP Camera Security Auditor ⬡

![Field](https://img.shields.io/badge/Field-CyberSecurity-red)
![Certification](https://img.shields.io/badge/Auditor-CEH_Certified-blue)
![Language](https://img.shields.io/badge/Language-Python_3.10+-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

A professional, GUI-based security orchestration tool designed for auditing IP cameras within authorized lab environments.

## 👤 Developed By

**SADDAM HUSSAIN**  
_Certified Ethical Hacker (CEH) | CyberSecurity Professional_

- **LinkedIn:** [saddam-cybersec](https://www.linkedin.com/in/saddam-cybersec/)
- **GitHub:** [saddam-cybersec](https://github.com/saddam-cybersec)
- **Email:** mail.cybersec92@gmail.com | f.saddam319@gmail.com

---

## ⚖️ Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING ONLY.**  
Use of this tool against targets without prior written consent is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this software.

---

## 🚀 Key Features

- **Network Discovery:** Multi-threaded TCP scanning to identify active IoT assets.
- **Advanced Enumeration:** Signature-based vendor detection (Hikvision, Dahua, etc.).
- **Smart Auth Auditing:** Baseline comparison logic to eliminate false-positives.
- **Professional PDF Reporting:** Generates high-level reports with risk highlights.
- **Context-Aware UI:** Right-click support to copy cell/row data for documentation.

---

<details>
<summary><b>1. Windows Setup (Click to expand)</b></summary>

1. Install [Python 3.10+](https://www.python.org/downloads/).
2. Open PowerShell in the project folder:

```powershell
pip install -r requirements.txt
python main.py
```

</details>
<details>
<summary><b>2. Linux Setup (Kali/Ubuntu/Debian) (Click to expand)</b></summary>
1. Install system dependencies:
```Bash
sudo apt update
sudo apt install python3-pip python3-pyqt5 ffmpeg -y
```
2. Install Python requirements:
```Bash
pip3 install -r requirements.txt
```
3. Run the application:
```Bash
python3 main.py
```
</details>
<details>
<summary><b>3. Termux Setup (Android) (Click to expand)</b></summary>
Note: Requires an X11 environment or VNC for GUI display.
1. Setup X11 Repo and Python:
```Bash
pkg install x11-repo
pkg install python python-pip qt5-base-desktop-minimal-common
```
2. Install requirements and run:
```Bash
pip install -r requirements.txt
python main.py
```
</details>

---

## 📖 Audit Workflow

The tool enforces a sequential security methodology:
Scan Network: Discover live assets on the subnet.
Enumerate Services: Identify vendor signatures and active endpoints.
Audit Settings: Load custom passwords.txt and set delays.
Test Authentication: Perform the strict credential audit.
Validate Streams: Confirm unauthorized access to video feeds.
Export: Generate a professional PDF or CSV report.

---

## 📄 License

Distributed under the[MIT](https://github.com/saddam-cybersec/ip-camera-security-auditor?tab=MIT-1-ov-file)
License
See LICENSE for more information.

---
