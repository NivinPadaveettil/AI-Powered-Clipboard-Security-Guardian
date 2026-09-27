import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QStyle
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QAction

from src.gui.main_window import MainWindow
from src.core.clipboard_monitor import ClipboardMonitor
from src.config.settings_manager import settings_manager
from src.services.notification_service import NotificationService
from src.utils.app_logger import app_logger


class ClipboardMonitorWorker(QThread):

    detection = pyqtSignal()
    notification_requested = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.monitor = ClipboardMonitor(on_notification=self.notification_requested.emit)

    def run(self):
        try:
            self.monitor.monitor()
        except Exception as e:
            app_logger.error(f"Monitor Worker Error: {e}")

    def stop(self):
        self.monitor.stop()


def main():

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    app_logger.log_event("APP_STARTUP", "AI Security Clipboard Guardian starting...")

    # Main Window
    window = MainWindow()
    window.show()

    # Clipboard Monitor
    monitor_worker = ClipboardMonitorWorker()
    monitor_worker.notification_requested.connect(NotificationService.show_notification)
    monitor_worker.start()

    # System Tray Icon & Context Menu
    tray_icon = QSystemTrayIcon(app)
    style = app.style()
    tray_icon.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning))

    tray_menu = QMenu()

    show_action = QAction("Show / Hide Window", window)
    show_action.triggered.connect(
        lambda: window.hide() if window.isVisible() else window.show()
    )

    monitor_action = QAction("Enable Monitoring", window)
    monitor_action.setCheckable(True)
    is_mon_enabled = settings_manager.get("monitoring_enabled")
    monitor_action.setChecked(is_mon_enabled)

    def toggle_monitoring(checked):
        settings_manager.set("monitoring_enabled", checked)
        app_logger.log_event("TRAY_TOGGLE_MONITOR", f"monitoring_enabled={checked}")
        window.dashboard.refresh()

    monitor_action.triggered.connect(toggle_monitoring)

    exit_action = QAction("Exit Application", window)
    exit_action.triggered.connect(app.quit)

    tray_menu.addAction(show_action)
    tray_menu.addAction(monitor_action)
    tray_menu.addSeparator()
    tray_menu.addAction(exit_action)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.setToolTip("AI Security Clipboard Guardian")
    tray_icon.show()

    def on_tray_activated(reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger or reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if window.isVisible():
                window.hide()
            else:
                window.show()
                window.raise_()
                window.activateWindow()

    tray_icon.activated.connect(on_tray_activated)

    # Clean Shutdown
    def shutdown():
        app_logger.log_event("APP_SHUTDOWN", "Stopping clipboard monitor...")
        monitor_worker.stop()
        if monitor_worker.isRunning():
            monitor_worker.wait(3000)
        app_logger.log_event("APP_SHUTDOWN_COMPLETE", "Clipboard monitor stopped successfully.")

    app.aboutToQuit.connect(shutdown)

    # Keep references alive
    window.monitor_worker = monitor_worker
    window.tray_icon = tray_icon

    sys.exit(app.exec())


if __name__ == "__main__":
    main()