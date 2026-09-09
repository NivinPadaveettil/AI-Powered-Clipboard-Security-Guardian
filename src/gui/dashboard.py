from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt

from src.database.sqlite_logger import logger


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName("Dashboard")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # =====================================================
        # Title
        # =====================================================

        title = QLabel("Security Dashboard")
        title.setObjectName("Title")

        subtitle = QLabel(
            "AI-powered clipboard security monitoring"
        )
        subtitle.setObjectName("Subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # =====================================================
        # Statistics Cards
        # =====================================================

        grid = QGridLayout()
        grid.setSpacing(15)

        self.total_card = self.create_card(
            "TOTAL DETECTIONS",
            "0",
            "total"
        )

        self.critical_card = self.create_card(
            "CRITICAL",
            "0",
            "critical"
        )

        self.high_card = self.create_card(
            "HIGH RISK",
            "0",
            "high"
        )

        self.safe_card = self.create_card(
            "SAFE",
            "0",
            "safe"
        )

        grid.addWidget(self.total_card, 0, 0)
        grid.addWidget(self.critical_card, 0, 1)
        grid.addWidget(self.high_card, 1, 0)
        grid.addWidget(self.safe_card, 1, 1)

        main_layout.addLayout(grid)

        # =====================================================
        # Clipboard Monitor Status
        # =====================================================

        status_frame = QFrame()
        status_frame.setObjectName("StatusFrame")

        status_layout = QVBoxLayout(status_frame)

        status_title = QLabel("Clipboard Monitor")
        status_title.setObjectName("SectionTitle")

        self.status_label = QLabel(
            "● Monitoring Active"
        )

        self.status_label.setObjectName(
            "ActiveStatus"
        )

        status_layout.addWidget(status_title)
        status_layout.addWidget(self.status_label)

        main_layout.addWidget(status_frame)

        main_layout.addStretch()

        self.setLayout(main_layout)

        # Load database statistics
        self.load_statistics()

    # =========================================================
    # Create Statistics Card
    # =========================================================

    def create_card(self, title, value, card_type):

        frame = QFrame()
        frame.setObjectName("StatCard")

        layout = QVBoxLayout(frame)

        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")

        value_label = QLabel(value)
        value_label.setObjectName("CardValue")

        value_label.setProperty(
            "cardType",
            card_type
        )

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return frame

    # =========================================================
    # Load Statistics From SQLite
    # =========================================================

    def load_statistics(self):

        try:

            total = logger.get_total_count()
            critical = logger.get_critical_count()
            high = logger.get_high_count()
            safe = logger.get_safe_count()

            self.update_statistics(
                total,
                critical,
                high,
                safe
            )

            print(
                f"Dashboard statistics loaded: "
                f"total={total}, "
                f"critical={critical}, "
                f"high={high}, "
                f"safe={safe}"
            )

        except Exception as e:

            print(
                "Dashboard Statistics Error:",
                e
            )

    # =========================================================
    # Update Statistics
    # =========================================================

    def update_statistics(
        self,
        total,
        critical,
        high,
        safe
    ):

        total_label = self.total_card.findChild(
            QLabel,
            "CardValue"
        )

        critical_label = self.critical_card.findChild(
            QLabel,
            "CardValue"
        )

        high_label = self.high_card.findChild(
            QLabel,
            "CardValue"
        )

        safe_label = self.safe_card.findChild(
            QLabel,
            "CardValue"
        )

        if total_label:
            total_label.setText(str(total))

        if critical_label:
            critical_label.setText(str(critical))

        if high_label:
            high_label.setText(str(high))

        if safe_label:
            safe_label.setText(str(safe))

    # =========================================================
    # Refresh Dashboard
    # =========================================================

    def refresh(self):

        self.load_statistics()