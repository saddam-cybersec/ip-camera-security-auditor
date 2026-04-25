import socket, ipaddress, requests, time, subprocess, re, os
from PyQt5.QtCore import QThread, pyqtSignal
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from app.config.settings import *

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class NetworkScanWorker(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    device_found = pyqtSignal(dict)
    finished_scan = pyqtSignal()

    def __init__(self, subnet):
        super().__init__()
        self.subnet = subnet
        self._stop = False

    def stop(self): self._stop = True

    def run(self):
        try:
            net = ipaddress.ip_network(self.subnet, strict=False)
            hosts = list(net.hosts())
            total = len(hosts)
            for i, ip in enumerate(hosts):
                if self._stop: break
                ip_str = str(ip)
                hostname = "N/A"
                try: hostname = socket.gethostbyaddr(ip_str)[0]
                except: pass
                open_p = []
                for p in CAMERA_PORTS:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.2)
                    if s.connect_ex((ip_str, p)) == 0: open_p.append(p)
                    s.close()
                if open_p:
                    self.device_found.emit({"ip": ip_str, "hostname": hostname, "open_ports": open_p, "status": "Discovered"})
                self.progress.emit(int((i + 1) / total * 100))
        except Exception as e: self.log.emit(f"[!] Error: {e}")
        self.finished_scan.emit()

class EnumerationWorker(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    endpoint_found = pyqtSignal(dict)
    device_updated = pyqtSignal(dict)
    finished_enum = pyqtSignal()

    def __init__(self, devices):
        super().__init__()
        self.devices = devices
        self._stop = False

    def stop(self): self._stop = True

    def run(self):
        total = len(self.devices)
        for idx, dev in enumerate(self.devices):
            if self._stop: break
            web_ports = [p for p in dev['open_ports'] if p in [80, 443, 8000, 8080, 81, 8899]]
            for port in web_ports:
                protocol = "https" if port == 443 else "http"
                for path in HTTP_PATHS:
                    try:
                        url = f"{protocol}://{dev['ip']}:{port}{path}"
                        r = requests.get(url, timeout=1.5, verify=False)
                        low_body = r.text.lower()
                        if "hikvision" in low_body or "login.asp" in r.url:
                            dev['vendor'] = "Hikvision"; self.device_updated.emit(dev)
                        elif "dahua" in low_body or "cgi-bin/config" in r.url:
                            dev['vendor'] = "Dahua"; self.device_updated.emit(dev)
                        if r.status_code in [200, 301, 302, 401]:
                            self.endpoint_found.emit({"ip": dev['ip'], "type": "HTTP", "url": url, "code": r.status_code, "auth": r.status_code == 401, "length": len(r.content)})
                    except: pass
            self.progress.emit(int((idx + 1) / total * 100))
        self.finished_enum.emit()

class AuthTestWorker(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    result_ready = pyqtSignal(dict)
    finished_auth = pyqtSignal()

    def __init__(self, devices, wordlist=None, delay=0):
        super().__init__(); self.devices = devices; self.wordlist = wordlist; self.delay = delay; self._stop = False

    def stop(self): self._stop = True

    def _load_creds(self):
        if self.wordlist and os.path.exists(self.wordlist):
            creds = []
            try:
                with open(self.wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if ':' in line: creds.append(line.strip().split(':', 1))
                return creds
            except: pass
        return DEFAULT_CREDENTIALS

    def run(self):
        creds_to_test = self._load_creds()
        total_attempts = len(self.devices) * len(creds_to_test)
        current_attempt = 0
        
        for idx, dev in enumerate(self.devices):
            if self._stop: break
            web_ports = [p for p in dev['open_ports'] if p in [80, 443, 8080, 8000]]
            for port in web_ports:
                url = f"{'https' if port==443 else 'http'}://{dev['ip']}:{port}"
                baseline_len = -1
                try: baseline_len = len(requests.get(url, auth=HTTPBasicAuth("fake_u", "fake_p"), timeout=3, verify=False).content)
                except: pass
                
                for u, p in creds_to_test:
                    if self._stop: break
                    current_attempt += 1
                    self.progress.emit(int((current_attempt / total_attempts) * 100))
                    self.log.emit(f"[*] Testing {u}:{p} on {dev['ip']}...")
                    
                    if self.delay > 0: time.sleep(self.delay)
                    for auth_t in [HTTPDigestAuth, HTTPBasicAuth]:
                        try:
                            r = requests.get(url, auth=auth_t(u, p), timeout=4, verify=False)
                            if r.status_code == 200 and (abs(len(r.content)-baseline_len) > 300 or 'Set-Cookie' in r.headers):
                                if 'type="password"' not in r.text.lower():
                                    self.result_ready.emit({"ip": dev['ip'], "port": port, "username": u, "password": p, "method": auth_t.__name__.replace('HTTP',''), "success": True})
                                    break
                        except: continue
        self.progress.emit(100)
        self.finished_auth.emit()

class StreamValidationWorker(QThread):
    progress = pyqtSignal(int); log = pyqtSignal(str); stream_result = pyqtSignal(dict); finished_streams = pyqtSignal()
    def __init__(self, devices): super().__init__(); self.devices = devices; self._stop = False
    def stop(self): self._stop = True
    def run(self):
        for idx, dev in enumerate(self.devices):
            if self._stop: break
            for p in [p for p in dev['open_ports'] if p in [80, 443, 8000, 8080]]:
                try:
                    url = f"{'https' if p==443 else 'http'}://{dev['ip']}:{p}/snapshot.jpg"
                    r = requests.get(url, timeout=3, verify=False)
                    is_img = "image" in r.headers.get("Content-Type", "").lower()
                    status = "Live" if is_img else "Corrupted/HTML" if r.status_code==200 else "Auth Required" if r.status_code==401 else "None"
                    self.stream_result.emit({"ip": dev['ip'], "type": "HTTP", "url": url, "accessible": r.status_code==200, "screenshot": status})
                except: pass
            self.progress.emit(int((idx+1)/len(self.devices)*100))
        self.finished_streams.emit()