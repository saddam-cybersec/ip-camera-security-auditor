# IP Camera Security Auditor ⬡

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

## 🛠️ Installation & Setup

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
<summary><b>2. Linux Setup (Kali/Ubuntu/Debian)</b></summary>
1. Install system dependencies:
sudo apt update
sudo apt install python3-pip python3-pyqt5 ffmpeg -y
1. Install Python requirements:
pip3 install -r requirements.txt
1. Run the application:
python3 main.py

Looking at your screenshots, the reason it looks "massive" and cluttered is that the Markdown syntax for the Linux, Termux, and Workflow sections got merged into a single paragraph. GitHub needs extra empty lines to separate sections correctly.
Here is a cleaned-up, highly organized version of the README.md. I have used collapsible sections (dropdowns) for the installation steps. This makes the page look very short and professional, but all the information is still there if someone clicks on it.
Copy and Paste this into your README.md:
code
Markdown

# IP Camera Security Auditor ⬡

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

## 🛠️ Installation & Setup

<details>
<summary><b>1. Windows Setup (Click to expand)</b></summary>

1. Install [Python 3.10+](https://www.python.org/downloads/).
2. Open PowerShell in the project folder:

```powershell
pip install -r requirements.txt
python main.py
</details>
<details>
<summary><b>2. Linux Setup (Kali/Ubuntu/Debian)</b></summary>
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
</details>
<details>
<summary><b>3. Termux Setup (Android)</b></summary>
Note: Requires an X11 environment or VNC for GUI display.
1. Setup X11 Repo and Python:
```

pkg install x11-repo
pkg install python python-pip qt5-base-desktop-minimal-common

1. Install requirements and run:
pip install -r requirements.txt
python main.py
</details>
📖 Audit Workflow
The tool enforces a sequential security methodology:
Scan Network: Discover live assets on the subnet.
Enumerate Services: Identify vendor signatures and active endpoints.
Audit Settings: Load custom passwords.txt and set delays.
Test Authentication: Perform the strict credential audit.
Validate Streams: Confirm unauthorized access to video feeds.
Export: Generate a professional PDF or CSV report.
📂 Project Structure
ip-cam-auditor/
├── main.py              # Application Entry Point
├── app/
│   ├── config/          # Port definitions and credentials
│   ├── core/            # Worker logic (Scan, Auth, Enum)
│   ├── ui/              # GUI Layouts and Styles
│   └── utils/           # Helper functions and PDF engines
├── requirements.txt     # Python Dependencies
└── LICENSE              # MIT License
📄 License
Distributed under the MIT License. See LICENSE for more information.
