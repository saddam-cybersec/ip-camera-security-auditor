import sys
from PyQt5.QtWidgets import QApplication
from app.ui.main_window import IPCamAuditor

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = IPCamAuditor()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()