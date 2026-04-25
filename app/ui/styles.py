# --- COLORS ---
DARK_BG        = "#0d1117"
DARK_SURFACE   = "#161b22"
DARK_BORDER    = "#30363d"
DARK_TEXT      = "#e6edf3"
DARK_MUTED     = "#8b949e"
ACCENT_BLUE    = "#388bfd"
ACCENT_GREEN   = "#3fb950"
ACCENT_YELLOW  = "#d29922"
ACCENT_RED     = "#f85149"
ACCENT_PURPLE  = "#bc8cff"
ACCENT_CYAN    = "#39d0d0"

MAIN_STYLE = f"""
* {{
    font-family: 'Consolas', 'Courier New', monospace;
}}
QMainWindow, QWidget {{
    background-color: {DARK_BG};
    color: {DARK_TEXT};
}}
QGroupBox {{
    border: 1px solid {DARK_BORDER};
    border-radius: 6px;
    margin-top: 15px;
    padding-top: 10px;
    font-size: 11px;
    color: {DARK_MUTED};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: {ACCENT_CYAN};
    font-weight: bold;
}}
QPushButton {{
    background-color: {DARK_SURFACE};
    color: {DARK_TEXT};
    border: 1px solid {DARK_BORDER};
    border-radius: 4px;
    padding: 6px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: {ACCENT_BLUE};
    color: #ffffff;
}}
QLineEdit, QSpinBox {{
    background-color: #010409;
    color: {DARK_TEXT};
    border: 1px solid {DARK_BORDER};
    padding: 5px;
}}
QTableWidget {{
    background-color: {DARK_SURFACE};
    gridline-color: {DARK_BORDER};
    border: 1px solid {DARK_BORDER};
}}
QHeaderView::section {{
    background-color: {DARK_BG};
    color: {ACCENT_CYAN};
    padding: 4px;
    border: none;
    border-bottom: 1px solid {DARK_BORDER};
}}
QProgressBar {{
    background-color: {DARK_SURFACE};
    border: 1px solid {DARK_BORDER};
    height: 12px;
    text-align: center;
    font-size: 9px;
}}
QProgressBar::chunk {{ background-color: {ACCENT_BLUE}; }}
QLabel#author_name {{ color: {ACCENT_CYAN}; font-weight: bold; font-size: 13px; }}
QLabel#author_bio {{ color: {DARK_MUTED}; font-size: 10px; }}
"""