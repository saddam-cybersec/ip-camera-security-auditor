# IP Camera Security Auditor ⬡

![Field](https://img.shields.io/badge/Field-CyberSecurity-red)
![Certification](https://img.shields.io/badge/Auditor-CEH_Certified-blue)
![Language](https://img.shields.io/badge/Language-Python_3.10+-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

A professional, GUI-based security orchestration tool designed for auditing IP cameras within authorized lab environments. This tool automates the process of network discovery, service enumeration, credential auditing (with rate limiting), and high-level PDF reporting.

## 👤 Developed By

**SADDAM HUSSAIN**  
_Certified Ethical Hacker (CEH) | CyberSecurity Professional_

- **LinkedIn:** [saddam-cybersec](https://www.linkedin.com/in/saddam-cybersec/)
- **GitHub:** [saddam-cybersec](https://github.com/saddam-cybersec)
- **Email (Official):** mail.cybersec92@gmail.com
- **Email (General):** f.saddam319@gmail.com

---

## ⚖️ Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING ONLY.**  
Use of this tool against targets without prior written consent is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this software. All testing should be performed within a controlled, authorized environment.

---

## 🚀 Key Features

- **Network Discovery:** Multi-threaded TCP scanning to identify active camera hardware and open ports.
- **Advanced Enumeration:** Signature-based vendor detection (Hikvision, Dahua, Axis, etc.) and service identification (Web, RTSP, ONVIF).
- **Credential Auditing:** Support for custom `user:pass` wordlists with configurable rate limiting to bypass IP lockouts.
- **Strict Verification:** Uses "Baseline Comparison" logic to eliminate "False Positive" successful logins.
- **Professional Reporting:** Generates corporate-grade PDF Audit Reports including Executive Summaries and highlighted risks.
- **Context-Aware UI:** Built-in Cyberpunk dark theme with right-click support to copy data directly from results.

---

## 🛠️ Installation & Setup

### 1. Windows

1. Install [Python 3.10 or higher](https://www.python.org/downloads/).
2. Open PowerShell in the project folder:
   ```powershell
   pip install -r requirements.txt
   python main.py
   ```
3. Linux (Kali / Ubuntu / Debian)
   Install system dependencies:
   code
   Bash
   sudo apt update
   sudo apt install python3-pip python3-pyqt5 ffmpeg -y
   Install Python requirements:
   code
   Bash
   pip3 install -r requirements.txt
   Run the application:
   code
   Bash
   python3 main.py
4. Termux (Android)
   Note: This tool requires a Graphical User Interface (GUI). You must use an X11 environment or VNC.
   Setup X11 Repo and Python:
   code
   Bash
   pkg install x11-repo
   pkg install python python-pip qt5-base-desktop-minimal-common
   Install requirements:
   code
   Bash
   pip install -r requirements.txt
   Ensure your display is active (via VNC/Termux-X11), then run:
   code
   Bash
   python main.py
   📖 Audit Workflow
   To maintain professional methodology, the tool enforces a sequential workflow:
   Scan Network: Discover live assets on the subnet.
   Enumerate Services: Identify vendor signatures and active endpoints.
   Audit Settings: (Optional) Configure custom wordlists and delays in the Settings tab.
   Test Authentication: Perform the credential audit.
   Validate Streams: Check for unauthorized access to video feeds.
   Export Results: Generate a professional PDF or CSV report for the client.
   📂 Project Structure
   code
   Text
   ip-cam-auditor/
   ├── main.py # Application Entry Point
   ├── app/
   │ ├── config/ # Port definitions and default credentials
   │ ├── core/ # Back-end Worker logic (Scan, Auth, Enum)
   │ ├── ui/ # GUI Layouts and Cyberpunk Styling
   │ └── utils/ # Helper functions and PDF engines
   ├── requirements.txt # Python Dependencies
   ├── .gitignore # Security rule to prevent data leaks
   └── README.md # Documentation
   📄 License
   Distributed under the MIT License. See LICENSE for more information.
