from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QSpinBox,
    QGroupBox,
    QPushButton,
    QFormLayout,
)

from PyQt6.QtCore import pyqtSignal

from src.config.settings_manager import settings_manager
from src.database.sqlite_logger import logger
from src.services.startup_service import StartupService
from src.utils.app_logger import app_logger


class Settings(QWidget):

    settings_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------

        title = QLabel("Settings")
        title.setObjectName("Title")

        subtitle = QLabel(
            "Configure clipboard security behaviour and application preferences"
        )
        subtitle.setObjectName("Subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # --------------------------------------------------
        # MONITORING & STARTUP
        # --------------------------------------------------

        monitor_group = QGroupBox("Clipboard Monitoring & Startup")
        monitor_layout = QVBoxLayout()

        self.monitor_checkbox = QCheckBox("Enable clipboard monitoring")
        self.auto_start_checkbox = QCheckBox("Start monitoring automatically on application startup")

        monitor_layout.addWidget(self.monitor_checkbox)
        monitor_layout.addWidget(self.auto_start_checkbox)
        monitor_group.setLayout(monitor_layout)
        layout.addWidget(monitor_group)

        # --------------------------------------------------
        # DESKTOP NOTIFICATIONS
        # --------------------------------------------------

        notify_group = QGroupBox("Desktop Notifications")
        notify_layout = QVBoxLayout()

        self.notify_checkbox = QCheckBox("Show desktop notification when sensitive data is detected")
        notify_layout.addWidget(self.notify_checkbox)
        notify_group.setLayout(notify_layout)
        layout.addWidget(notify_group)

        # --------------------------------------------------
        # AUTO CLEAR
        # --------------------------------------------------

        clear_group = QGroupBox("Automatic Clipboard Clearing")
        clear_layout = QVBoxLayout()

        self.clear_checkbox = QCheckBox("Automatically clear sensitive clipboard data")
        clear_layout.addWidget(self.clear_checkbox)
        clear_group.setLayout(clear_layout)
        layout.addWidget(clear_group)

        # --------------------------------------------------
        # TIMEOUT
        # --------------------------------------------------

        timeout_group = QGroupBox("Default Clear Timeout")
        timeout_layout = QHBoxLayout()

        timeout_label = QLabel("Clear delay (seconds):")
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setMinimum(1)
        self.timeout_spin.setMaximum(300)

        timeout_layout.addWidget(timeout_label)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        timeout_group.setLayout(timeout_layout)
        layout.addWidget(timeout_group)

        # --------------------------------------------------
        # DATABASE INFORMATION
        # --------------------------------------------------

        db_group = QGroupBox("Database Information")
        db_layout = QFormLayout()

        self.db_path_label = QLabel()
        self.db_records_label = QLabel()
        self.db_size_label = QLabel()

        db_layout.addRow("Location:", self.db_path_label)
        db_layout.addRow("Total Detections:", self.db_records_label)
        db_layout.addRow("Database Size:", self.db_size_label)

        self.db_refresh_btn = QPushButton("Refresh Database Info")
        self.db_refresh_btn.clicked.connect(self.update_db_info)

        db_layout.addRow("", self.db_refresh_btn)
        db_group.setLayout(db_layout)
        layout.addWidget(db_group)

        # --------------------------------------------------
        # SAVE BUTTON
        # --------------------------------------------------

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        layout.addStretch()
        self.setLayout(layout)

        # Enable/disable timeout control based on auto_clear checkbox
        self.clear_checkbox.stateChanged.connect(self.update_timeout_state)

        # Load saved settings & db info
        self.load_settings()
        self.update_db_info()

    # ------------------------------------------------------
    # LOAD SETTINGS
    # ------------------------------------------------------

    def load_settings(self):
        settings = settings_manager.get_all()

        self.monitor_checkbox.setChecked(settings.get("monitoring_enabled", True))
        self.auto_start_checkbox.setChecked(settings.get("start_monitoring_automatically", True))
        self.notify_checkbox.setChecked(settings.get("notifications_enabled", True))
        self.clear_checkbox.setChecked(settings.get("auto_clear_enabled", True))
        self.timeout_spin.setValue(settings.get("clear_timeout", 15))

        self.update_timeout_state()

    # ------------------------------------------------------
    # TIMEOUT CONTROL
    # ------------------------------------------------------

    def update_timeout_state(self):
        self.timeout_spin.setEnabled(self.clear_checkbox.isChecked())

    # ------------------------------------------------------
    # UPDATE DATABASE INFORMATION
    # ------------------------------------------------------

    def update_db_info(self):
        try:
            path = logger.get_database_path()
            total_count = logger.get_total_count()
            size_bytes = logger.get_database_size()

            if size_bytes >= 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
            else:
                size_str = f"{size_bytes / 1024:.2f} KB"

            self.db_path_label.setText(path)
            self.db_records_label.setText(str(total_count))
            self.db_size_label.setText(size_str)
        except Exception as e:
            self.db_path_label.setText("Error loading DB info")
            self.db_records_label.setText("N/A")
            self.db_size_label.setText(str(e))

    # ------------------------------------------------------
    # SAVE SETTINGS
    # ------------------------------------------------------

    def save_settings(self):
        settings = {
            "monitoring_enabled": self.monitor_checkbox.isChecked(),
            "start_monitoring_automatically": self.auto_start_checkbox.isChecked(),
            "notifications_enabled": self.notify_checkbox.isChecked(),
            "auto_clear_enabled": self.clear_checkbox.isChecked(),
            "clear_timeout": self.timeout_spin.value(),
        }

        settings_manager.save(settings)

        # Update Windows autostart registry
        StartupService.set_autostart(settings["start_monitoring_automatically"])

        # Log event
        app_logger.log_event("SETTINGS_SAVED", str(settings))

        # Notify MainWindow / other components
        self.settings_changed.emit(settings)
        self.update_db_info()

        self.save_button.setText("Settings Saved ✓")

        print()
        print("=" * 60)
        print("SETTINGS SAVED")
        print("=" * 60)
        for k, v in settings.items():
            print(f"{k:<32}: {v}")
        print("=" * 60)