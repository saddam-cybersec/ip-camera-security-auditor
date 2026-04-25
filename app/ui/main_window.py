import os, datetime, json, csv
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

from app.ui.styles import *
from app.core.workers import NetworkScanWorker, EnumerationWorker, AuthTestWorker, StreamValidationWorker

class IPCamAuditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.devices = []; self.auth_results = []; self.stream_results = []; self.current_worker = None
        self.active_phase = "IDLE"
        
        self.setWindowTitle("IP Camera Security Auditor | Saddam Hussain (CEH)")
        self.resize(1350, 900); self.setStyleSheet(MAIN_STYLE); self._build_ui()

    def _build_ui(self):
        central = QWidget(); self.setCentralWidget(central); root = QVBoxLayout(central)
        root.setContentsMargins(15, 15, 15, 15); root.setSpacing(10)

        header = QHBoxLayout(); title = QLabel("⬡ IP CAM AUDITOR"); title.setObjectName("title_label"); header.addWidget(title); header.addStretch()
        warn = QLabel("⚠  FOR AUTHORIZED LAB TESTING ONLY  —  No Unauthorized Access."); warn.setObjectName("warning_label"); header.addWidget(warn); header.addStretch()
        self.export_btn = QPushButton("⬇ Export Results"); self.export_btn.clicked.connect(self._export_results); header.addWidget(self.export_btn)
        root.addLayout(header)

        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget(); left_widget.setFixedWidth(300); left_lay = QVBoxLayout(left_widget)
        left_lay.setContentsMargins(0, 0, 5, 0); left_lay.setSpacing(10)
        
        scan_box = QGroupBox("Network Discovery"); sb_lay = QVBoxLayout(scan_box)
        self.subnet_input = QLineEdit("192.168.0.0/24"); sb_lay.addWidget(QLabel("Target Subnet:")); sb_lay.addWidget(self.subnet_input)
        self.nmap_cb = QCheckBox("Use nmap"); sb_lay.addWidget(self.nmap_cb)
        self.scan_btn = QPushButton("▶  Scan Network"); self.scan_btn.clicked.connect(self._start_scan); self.scan_bar = QProgressBar()
        sb_lay.addWidget(self.scan_btn); sb_lay.addWidget(self.scan_bar); left_lay.addWidget(scan_box)

        self.enum_btn, self.enum_bar = self._add_phase_widget(left_lay, "▶  Enumerate Services", ACCENT_GREEN, "#0d3d1e")
        self.auth_btn, self.auth_bar = self._add_phase_widget(left_lay, "▶  Test Authentication", ACCENT_YELLOW, "#3d2b00")
        self.stream_btn, self.stream_bar = self._add_phase_widget(left_lay, "▶  Validate Streams", ACCENT_PURPLE, "#280d3d")
        
        self.enum_btn.clicked.connect(self._start_enumeration); self.auth_btn.clicked.connect(self._start_auth_test); self.stream_btn.clicked.connect(self._start_stream_validation)
        
        self.stop_btn = QPushButton("⏹  Stop Process"); self.stop_btn.setEnabled(False); self.stop_btn.setStyleSheet(f"color: {ACCENT_RED}; border-color: {ACCENT_RED}; background: #3d0d0d;")
        self.stop_btn.clicked.connect(self._stop_worker); left_lay.addWidget(self.stop_btn)

        left_lay.addStretch(); author_frame = QFrame(); author_frame.setStyleSheet(f"border-top: 1px solid {DARK_BORDER};"); auth_lay = QVBoxLayout(author_frame)
        name_lbl = QLabel("SADDAM HUSSAIN"); name_lbl.setObjectName("author_name"); bio_lbl = QLabel("CEH | CyberSecurity Professional"); bio_lbl.setObjectName("author_bio")
        auth_lay.addWidget(name_lbl); auth_lay.addWidget(bio_lbl); left_lay.addWidget(author_frame); splitter.addWidget(left_widget)

        self.tabs = QTabWidget()
        self.device_table = self._create_table(["IP", "Hostname", "Open Ports", "Vendor", "Model", "Status"]); self.tabs.addTab(self.device_table, "Devices")
        self.endpoint_table = self._create_table(["IP", "Type", "URL", "Code", "Auth"]); self.tabs.addTab(self.endpoint_table, "Endpoints")
        self.auth_table = self._create_table(["IP", "Port", "User", "Pass", "Method", "Result"]); self.tabs.addTab(self.auth_table, "Auth Results")
        self.stream_table = self._create_table(["IP", "Type", "URL", "Accessible", "Screenshot"]); self.tabs.addTab(self.stream_table, "Streams")
        self.tabs.addTab(self._build_settings_tab(), "Audit Settings")
        self.tabs.addTab(self._build_about_tab(), "About / Credits")
        splitter.addWidget(self.tabs); splitter.setSizes([300, 1000]); root.addWidget(splitter, 1)

        log_box = QGroupBox("Console Log"); log_lay = QVBoxLayout(log_box); self.log_console = QTextEdit(); self.log_console.setReadOnly(True); self.log_console.setFixedHeight(140); log_lay.addWidget(self.log_console); root.addWidget(log_box)

    def _create_table(self, headers):
        t = QTableWidget(0, len(headers)); t.setHorizontalHeaderLabels(headers); t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        t.setEditTriggers(QAbstractItemView.NoEditTriggers); t.setSelectionBehavior(QAbstractItemView.SelectRows); t.setSelectionMode(QAbstractItemView.ExtendedSelection)
        t.setContextMenuPolicy(Qt.CustomContextMenu); t.customContextMenuRequested.connect(lambda pos: self._show_context_menu(pos, t))
        t.setAlternatingRowColors(True); return t

    def _show_context_menu(self, pos, table):
        menu = QMenu(); copy_cell = menu.addAction("📋 Copy Selected Cell"); copy_row = menu.addAction("📑 Copy Full Row")
        action = menu.exec_(table.viewport().mapToGlobal(pos))
        if action == copy_cell:
            item = table.itemAt(pos) # Gets the exact cell clicked
            if item: QApplication.clipboard().setText(item.text())
        elif action == copy_row:
            row = table.rowAt(pos.y())
            if row != -1:
                row_data = [table.item(row, col).text() for col in range(table.columnCount()) if table.item(row, col)]
                QApplication.clipboard().setText(" | ".join(row_data))

    def _build_settings_tab(self):
        widget = QWidget(); lay = QVBoxLayout(widget)
        
        # Dictionary Section
        dict_box = QGroupBox("Dictionary & Brute-Force Strategy"); dl = QVBoxLayout(dict_box)
        self.wordlist_path = QLineEdit(); self.wordlist_path.setPlaceholderText("Leaving blank uses default credentials...")
        pick_btn = QPushButton("📁 Load Wordlist (.txt)"); pick_btn.clicked.connect(self._pick_wordlist)
        self.delay_input = QSpinBox(); self.delay_input.setRange(0, 30); self.delay_input.setSuffix("s delay")
        dl.addWidget(QLabel("Wordlist Path:")); dl.addWidget(self.wordlist_path); dl.addWidget(pick_btn); dl.addWidget(QLabel("Rate Limit:")); dl.addWidget(self.delay_input)
        lay.addWidget(dict_box)

        # Auditor Information Section (FOR PDF ONLY)
        audit_box = QGroupBox("Auditor Information (For PDF Report Only)"); al = QVBoxLayout(audit_box)
        self.pdf_name = QLineEdit("SADDAM HUSSAIN"); self.pdf_title = QLineEdit("CEH | CyberSecurity Professional"); self.pdf_org = QLineEdit("Independent Audit")
        al.addWidget(QLabel("Lead Auditor Name:")); al.addWidget(self.pdf_name)
        al.addWidget(QLabel("Professional Title:")); al.addWidget(self.pdf_title)
        al.addWidget(QLabel("Organization/Company:")); al.addWidget(self.pdf_org)
        lay.addWidget(audit_box); lay.addStretch(); return widget

    def _build_about_tab(self):
        widget = QWidget(); lay = QVBoxLayout(widget); view = QTextBrowser(); view.setReadOnly(True); view.setOpenExternalLinks(True)
        view.setHtml(f"<h2>SADDAM HUSSAIN</h2><p><b>CEH | CyberSecurity Professional</b></p><hr><p>LinkedIn: <a href='https://www.linkedin.com/in/saddam-cybersec/'>saddam-cybersec</a></p><p>GitHub: <a href='https://github.com/saddam-cybersec'>saddam-cybersec</a></p>"); lay.addWidget(view); return widget

    def _add_phase_widget(self, layout, label, color, bg):
        box = QGroupBox(); lay = QVBoxLayout(box); btn = QPushButton(label); btn.setStyleSheet(f"color: {color}; border-color: {color}; background: {bg};")
        btn.setEnabled(False); bar = QProgressBar(); bar.setValue(0); lay.addWidget(btn); lay.addWidget(bar); layout.addWidget(box); return btn, bar

    def _log(self, msg): self.log_console.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}"); self.log_console.moveCursor(QTextCursor.End)

    def _run_worker(self, worker):
        if self.current_worker and self.current_worker.isRunning(): return
        self.current_worker = worker; self.current_worker.start(); self.stop_btn.setEnabled(True); self.scan_btn.setEnabled(False)

    def _stop_worker(self):
        if self.current_worker and self.current_worker.isRunning(): self.current_worker.stop(); self._log("[!] Stopping active process...")
        self.stop_btn.setEnabled(False)

    def _on_finished(self):
        self._log(f"[*] {self.active_phase} Phase Completed."); self.stop_btn.setEnabled(False); self.scan_btn.setEnabled(True)
        if self.active_phase == "SCAN" and self.devices: self.enum_btn.setEnabled(True)
        elif self.active_phase == "ENUMERATION": self.auth_btn.setEnabled(True); self.tabs.setCurrentIndex(4); QMessageBox.information(self, "Sequence", "Enumeration Done. Now configure your Audit Settings.")
        elif self.active_phase == "AUTHENTICATION": self.stream_btn.setEnabled(True)
        self.active_phase = "IDLE"

    def _start_scan(self):
        self.active_phase = "SCAN"; self.device_table.setRowCount(0); self.devices = []; self.enum_btn.setEnabled(False); self.auth_btn.setEnabled(False); self.stream_btn.setEnabled(False)
        worker = NetworkScanWorker(self.subnet_input.text())
        worker.progress.connect(self.scan_bar.setValue); worker.device_found.connect(self._on_device_found); worker.finished_scan.connect(self._on_finished); self._run_worker(worker)

    def _on_device_found(self, dev):
        self.devices.append(dev); row = self.device_table.rowCount(); self.device_table.insertRow(row)
        self.device_table.setItem(row, 0, QTableWidgetItem(dev['ip'])); self.device_table.setItem(row, 1, QTableWidgetItem(dev.get('hostname', 'N/A')))
        self.device_table.setItem(row, 2, QTableWidgetItem(str(dev['open_ports']))); self.device_table.setItem(row, 5, QTableWidgetItem(dev['status']))

    def _start_enumeration(self):
        self.active_phase = "ENUMERATION"; self.endpoint_table.setRowCount(0); self.tabs.setCurrentIndex(1)
        worker = EnumerationWorker(self.devices); worker.progress.connect(self.enum_bar.setValue); worker.log.connect(self._log); worker.endpoint_found.connect(self._on_endpoint_found); worker.device_updated.connect(self._on_device_updated); worker.finished_enum.connect(self._on_finished); self._run_worker(worker)

    def _on_device_updated(self, dev):
        for row in range(self.device_table.rowCount()):
            if self.device_table.item(row, 0).text() == dev['ip']:
                self.device_table.setItem(row, 3, QTableWidgetItem(dev.get('vendor', 'Unknown'))); self.device_table.setItem(row, 4, QTableWidgetItem(dev.get('model', 'IP Camera'))); break

    def _on_endpoint_found(self, ep):
        row = self.endpoint_table.rowCount(); self.endpoint_table.insertRow(row); self.endpoint_table.setItem(row, 0, QTableWidgetItem(ep['ip']))
        self.endpoint_table.setItem(row, 1, QTableWidgetItem(ep['type'])); self.endpoint_table.setItem(row, 2, QTableWidgetItem(ep['url']))
        self.endpoint_table.setItem(row, 3, QTableWidgetItem(str(ep['code']))); self.endpoint_table.setItem(row, 4, QTableWidgetItem("YES" if ep['auth'] else "no"))

    def _start_auth_test(self):
        self.active_phase = "AUTHENTICATION"; self.auth_table.setRowCount(0); self.auth_results = []; self.tabs.setCurrentIndex(2); self.auth_bar.setValue(0)
        worker = AuthTestWorker(self.devices, self.wordlist_path.text(), self.delay_input.value())
        worker.progress.connect(self.auth_bar.setValue); worker.result_ready.connect(self._on_auth_result); worker.finished_auth.connect(self._on_finished); self._run_worker(worker)

    def _on_auth_result(self, res):
        self.auth_results.append(res); row = self.auth_table.rowCount(); self.auth_table.insertRow(row)
        self.auth_table.setItem(row, 0, QTableWidgetItem(res['ip'])); self.auth_table.setItem(row, 1, QTableWidgetItem(str(res['port'])))
        self.auth_table.setItem(row, 2, QTableWidgetItem(res['username'])); self.auth_table.setItem(row, 3, QTableWidgetItem(res['password']))
        self.auth_table.setItem(row, 4, QTableWidgetItem(res.get('method', 'Basic')))
        status = QTableWidgetItem("✓ VULNERABLE" if res['success'] else "✗ Failed")
        if res['success']: status.setForeground(QColor(ACCENT_RED))
        self.auth_table.setItem(row, 5, status)

    def _start_stream_validation(self):
        self.active_phase = "VALIDATION"; self.stream_table.setRowCount(0); self.stream_results = []; self.tabs.setCurrentIndex(3)
        worker = StreamValidationWorker(self.devices); worker.progress.connect(self.stream_bar.setValue); worker.log.connect(self._log); worker.stream_result.connect(self._on_stream_result); worker.finished_streams.connect(self._on_finished); self._run_worker(worker)

    def _on_stream_result(self, res):
        self.stream_results.append(res); row = self.stream_table.rowCount(); self.stream_table.insertRow(row)
        self.stream_table.setItem(row, 0, QTableWidgetItem(res['ip'])); self.stream_table.setItem(row, 1, QTableWidgetItem(res['type'])); self.stream_table.setItem(row, 2, QTableWidgetItem(res['url']))
        acc_item = QTableWidgetItem("YES" if res['accessible'] else "no")
        if res['accessible']: acc_item.setForeground(QColor(ACCENT_RED))
        self.stream_table.setItem(row, 3, acc_item); self.stream_table.setItem(row, 4, QTableWidgetItem(res['screenshot']))

    def _pick_wordlist(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Dictionary", "", "Text Files (*.txt)"); 
        if path: self.wordlist_path.setText(path)

    def _export_results(self):
        if not self.devices: QMessageBox.warning(self, "Export", "No data to export."); return
        path, _ = QFileDialog.getSaveFileName(self, "Export", f"Audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}", "PDF (*.pdf);;JSON (*.json);;CSV (*.csv)")
        if not path: return
        try:
            if path.endswith(".pdf"): self._export_pdf(path)
            elif path.endswith(".csv"): self._export_csv(path)
            else:
                with open(path, "w") as f: json.dump({"ts": str(datetime.datetime.now()), "subnet": self.subnet_input.text(), "devices": self.devices, "auth": self.auth_results, "streams": self.stream_results}, f, indent=4)
            QMessageBox.information(self, "Export", f"Saved: {path}")
        except Exception as e: QMessageBox.critical(self, "Export Error", f"Failed: {str(e)}")

    def _export_pdf(self, path):
        doc = SimpleDocTemplate(path, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
        styles = getSampleStyleSheet(); elements = []
        title_s = ParagraphStyle('T', fontSize=22, textColor=colors.HexColor("#388bfd"), alignment=1, spaceAfter=20)
        head_s = ParagraphStyle('H', fontSize=14, textColor=colors.HexColor("#0d1117"), spaceBefore=15, spaceAfter=10)
        body_s = styles['Normal']

        elements.append(Paragraph("IP CAMERA SECURITY AUDIT REPORT", title_s))
        elements.append(Paragraph(f"<b>Lead Auditor:</b> {self.pdf_name.text()}", body_s))
        elements.append(Paragraph(f"<b>Professional Title:</b> {self.pdf_title.text()}", body_s))
        elements.append(Paragraph(f"<b>Organization:</b> {self.pdf_org.text()}", body_s))
        elements.append(Paragraph(f"<b>Date:</b> {datetime.datetime.now().strftime('%B %d, %Y')}", body_s))
        elements.append(Paragraph(f"<b>Target Scope:</b> {self.subnet_input.text()}", body_s))
        elements.append(Spacer(1, 0.3*inch)); elements.append(Paragraph("<hr/>", body_s))

        elements.append(Paragraph("EXECUTIVE SUMMARY", head_s))
        vulns = sum(1 for r in self.auth_results if r['success'])
        elements.append(Paragraph(f"Audit of network <b>{self.subnet_input.text()}</b> revealed <b>{len(self.devices)}</b> active camera systems. Identified <b>{vulns}</b> vulnerable systems.", body_s))

        elements.append(Paragraph("1. ASSET INVENTORY", head_s))
        d_data = [["IP Address", "Hostname", "Vendor", "Ports"]]
        for d in self.devices: d_data.append([d['ip'], d.get('hostname','N/A'), d.get('vendor','Unknown'), str(d['open_ports']).strip('[]')])
        t1 = Table(d_data, colWidths=[1.2*inch, 1.8*inch, 1.5*inch, 1.5*inch])
        t1.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor("#388bfd")),('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),('GRID',(0,0),(-1,-1),0.5,colors.grey)]))
        elements.append(t1)

        elements.append(Paragraph("2. AUTHENTICATION AUDIT", head_s))
        a_data = [["Target IP", "Port", "User", "Pass", "Status"]]
        for r in self.auth_results: a_data.append([r['ip'], str(r['port']), r['username'], r['password'], "VULNERABLE" if r['success'] else "Secure"])
        t2 = Table(a_data, colWidths=[1.2*inch, 0.8*inch, 1.5*inch, 1.5*inch, 1*inch])
        t2_s = [('BACKGROUND',(0,0),(-1,0),colors.HexColor("#24292e")),('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),('GRID',(0,0),(-1,-1),0.5,colors.grey)]
        for i, r in enumerate(self.auth_results):
            if r['success']: t2_s.append(('TEXTCOLOR', (-1, i+1), (-1, i+1), colors.red))
        t2.setStyle(TableStyle(t2_s)); elements.append(t2)

        def footer(canvas, doc):
            canvas.saveState(); canvas.setFont('Helvetica', 8); canvas.drawString(0.5*inch, 0.5*inch, f"IP Camera Audit | Lead Auditor: {self.pdf_name.text()} | Page {doc.page}"); canvas.drawRightString(8*inch, 0.5*inch, "CONFIDENTIAL"); canvas.restoreState()
        doc.build(elements, onFirstPage=footer, onLaterPages=footer)

    def _export_csv(self, path):
        with open(path, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["IP", "Hostname", "Ports", "Vendor"])
            for d in self.devices: w.writerow([d['ip'], d.get('hostname',''), str(d['open_ports']), d.get('vendor','')])