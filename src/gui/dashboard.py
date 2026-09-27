from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt, QTimer

from src.database.sqlite_logger import logger
from src.config.settings_manager import settings_manager


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("Dashboard")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("Security Dashboard")
        title.setObjectName("Title")

        subtitle = QLabel("AI-powered clipboard security monitoring and real-time status")
        subtitle.setObjectName("Subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Statistics Cards Grid
        grid = QGridLayout()
        grid.setSpacing(15)

        self.total_card = self.create_card("TOTAL DETECTIONS", "0", "total")
        self.critical_card = self.create_card("CRITICAL", "0", "critical")
        self.high_card = self.create_card("HIGH RISK", "0", "high")
        self.medium_card = self.create_card("MEDIUM RISK", "0", "medium")
        self.safe_card = self.create_card("SAFE", "0", "safe")

        grid.addWidget(self.total_card, 0, 0)
        grid.addWidget(self.critical_card, 0, 1)
        grid.addWidget(self.high_card, 0, 2)
        grid.addWidget(self.medium_card, 1, 0)
        grid.addWidget(self.safe_card, 1, 1)

        main_layout.addLayout(grid)

        # System Status Panel
        status_frame = QFrame()
        status_frame.setObjectName("StatusFrame")
        status_layout = QVBoxLayout(status_frame)

        status_title = QLabel("System Protection Status")
        status_title.setObjectName("SectionTitle")
        status_layout.addWidget(status_title)

        statuses_hbox = QHBoxLayout()

        self.monitor_status_label = QLabel("● Monitoring: Active")
        self.monitor_status_label.setObjectName("ActiveStatus")

        self.autoclear_status_label = QLabel("● Auto-Clear: Enabled")
        self.autoclear_status_label.setObjectName("ActiveStatus")

        self.notify_status_label = QLabel("● Notifications: Enabled")
        self.notify_status_label.setObjectName("ActiveStatus")

        statuses_hbox.addWidget(self.monitor_status_label)
        statuses_hbox.addWidget(self.autoclear_status_label)
        statuses_hbox.addWidget(self.notify_status_label)
        statuses_hbox.addStretch()

        status_layout.addLayout(statuses_hbox)
        main_layout.addWidget(status_frame)

        main_layout.addStretch()
        self.setLayout(main_layout)

        # QTimer for automatic statistics & status refresh
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(5000)  # 5 seconds
        self.refresh_timer.timeout.connect(self.refresh)
        self.refresh_timer.start()

        # Load database statistics & system status
        self.load_statistics()
        self.load_status_indicators()

    def create_card(self, title, value, card_type):
        frame = QFrame()
        frame.setObjectName("StatCard")

        layout = QVBoxLayout(frame)

        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")

        value_label = QLabel(value)
        value_label.setObjectName("CardValue")
        value_label.setProperty("cardType", card_type)

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        frame.value_label = value_label
        return frame

    def load_status_indicators(self):
        try:
            settings = settings_manager.get_all()

            # Monitoring
            if settings.get("monitoring_enabled", True):
                self.monitor_status_label.setText("● Monitoring: ACTIVE")
                self.monitor_status_label.setStyleSheet("color: #0d7a43; font-weight: bold;")
            else:
                self.monitor_status_label.setText("○ Monitoring: PAUSED")
                self.monitor_status_label.setStyleSheet("color: #dc2626; font-weight: bold;")

            # Auto Clear
            if settings.get("auto_clear_enabled", True):
                timeout = settings.get("clear_timeout", 15)
                self.autoclear_status_label.setText(f"● Auto-Clear: ON ({timeout}s)")
                self.autoclear_status_label.setStyleSheet("color: #0d7a43; font-weight: bold;")
            else:
                self.autoclear_status_label.setText("○ Auto-Clear: OFF")
                self.autoclear_status_label.setStyleSheet("color: #64748b; font-weight: bold;")

            # Notifications
            if settings.get("notifications_enabled", True):
                self.notify_status_label.setText("● Notifications: ON")
                self.notify_status_label.setStyleSheet("color: #0d7a43; font-weight: bold;")
            else:
                self.notify_status_label.setText("○ Notifications: OFF")
                self.notify_status_label.setStyleSheet("color: #64748b; font-weight: bold;")

        except Exception as e:
            print("Dashboard Status Indicator Error:", e)

    def load_statistics(self):
        try:
            total = logger.get_total_count()
            critical = logger.get_critical_count()
            high = logger.get_high_count()
            medium = logger.get_medium_count()
            safe = logger.get_safe_count()

            self.update_statistics(total, critical, high, medium, safe)

        except Exception as e:
            print("Dashboard Statistics Error:", e)

    def update_statistics(self, total, critical, high, medium, safe):
        if hasattr(self.total_card, "value_label"):
            self.total_card.value_label.setText(str(total))

        if hasattr(self.critical_card, "value_label"):
            self.critical_card.value_label.setText(str(critical))

        if hasattr(self.high_card, "value_label"):
            self.high_card.value_label.setText(str(high))

        if hasattr(self.medium_card, "value_label"):
            self.medium_card.value_label.setText(str(medium))

        if hasattr(self.safe_card, "value_label"):
            self.safe_card.value_label.setText(str(safe))

    def refresh(self):
        self.load_statistics()
        self.load_status_indicators()