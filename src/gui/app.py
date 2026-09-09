import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal

from src.gui.main_window import MainWindow
from src.core.clipboard_monitor import ClipboardMonitor


class ClipboardMonitorWorker(QThread):

    detection = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.monitor = ClipboardMonitor()

    def run(self):
        try:
            self.monitor.monitor()
        except Exception as e:
            print("Monitor Error:", e)

    def stop(self):
        self.monitor.stop()


def main():

    app = QApplication(sys.argv)

    # =====================================================
    # Main Window
    # =====================================================

    window = MainWindow()
    window.show()

    # =====================================================
    # Clipboard Monitor
    # =====================================================

    monitor_worker = ClipboardMonitorWorker()

    monitor_worker.start()

    # =====================================================
    # Clean Shutdown
    # =====================================================

    def shutdown():

        print("Stopping clipboard monitor...")

        monitor_worker.stop()

        if monitor_worker.isRunning():
            monitor_worker.wait(3000)

        print("Clipboard monitor stopped.")

    app.aboutToQuit.connect(shutdown)

    # Keep references alive
    window.monitor_worker = monitor_worker

    sys.exit(app.exec())


if __name__ == "__main__":
    main()