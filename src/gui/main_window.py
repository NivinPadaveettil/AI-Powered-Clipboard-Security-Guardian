from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QLabel,
)
from PyQt6.QtCore import Qt

from src.gui.dashboard import Dashboard
from src.gui.history import History
from src.gui.settings import Settings


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "AI Security Clipboard Guardian"
        )

        self.resize(1100, 700)

        # =====================================================
        # Central Widget
        # =====================================================

        central = QWidget()

        main_layout = QHBoxLayout(
            central
        )

        # =====================================================
        # Sidebar
        # =====================================================

        sidebar = QWidget()

        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(
            sidebar
        )

        logo = QLabel(
            "Clipboard\nGuardian"
        )

        logo.setObjectName("Logo")

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        sidebar_layout.addWidget(logo)

        # -----------------------------------------------------
        # Navigation Buttons
        # -----------------------------------------------------

        self.dashboard_button = QPushButton(
            "Dashboard"
        )

        self.history_button = QPushButton(
            "Detection History"
        )

        self.settings_button = QPushButton(
            "Settings"
        )

        sidebar_layout.addWidget(
            self.dashboard_button
        )

        sidebar_layout.addWidget(
            self.history_button
        )

        sidebar_layout.addWidget(
            self.settings_button
        )

        sidebar_layout.addStretch()

        version = QLabel(
            "AI Security Clipboard Guardian\nv1.0"
        )

        version.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        sidebar_layout.addWidget(version)

        # =====================================================
        # Content
        # =====================================================

        self.stack = QStackedWidget()

        self.dashboard = Dashboard()
        self.history = History()
        self.settings = Settings()

        self.stack.addWidget(
            self.dashboard
        )

        self.stack.addWidget(
            self.history
        )

        self.stack.addWidget(
            self.settings
        )

        # =====================================================
        # Navigation
        # =====================================================

        self.dashboard_button.clicked.connect(
            lambda: self.show_page(0)
        )

        self.history_button.clicked.connect(
            lambda: self.show_page(1)
        )

        self.settings_button.clicked.connect(
            lambda: self.show_page(2)
        )

        # =====================================================
        # Layout
        # =====================================================

        main_layout.addWidget(
            sidebar
        )

        main_layout.addWidget(
            self.stack
        )

        self.setCentralWidget(
            central
        )

        # =====================================================
        # Styles
        # =====================================================

        self.apply_styles()

        # Load dashboard statistics
        self.dashboard.refresh()

    # =========================================================
    # Page Navigation
    # =========================================================

    def show_page(self, index):

        self.stack.setCurrentIndex(index)

        # -----------------------------------------------------
        # Dashboard
        # -----------------------------------------------------

        if index == 0:

            self.dashboard.refresh()

        # -----------------------------------------------------
        # Detection History
        # -----------------------------------------------------

        elif index == 1:

            self.history.load_history()

    # =========================================================
    # Styles
    # =========================================================

    def apply_styles(self):

        self.setStyleSheet("""

            QMainWindow {
                background: #f5f7fb;
            }

            QWidget {
                font-family: Arial;
                font-size: 14px;
            }

            #Logo {
                font-size: 22px;
                font-weight: bold;
                padding: 20px;
            }

            QPushButton {
                background: transparent;
                border: none;
                padding: 12px;
                text-align: left;
                border-radius: 6px;
            }

            QPushButton:hover {
                background: #e8edf7;
            }

            #Title {
                font-size: 28px;
                font-weight: bold;
            }

            #Subtitle {
                color: #777;
                font-size: 14px;
            }

            #StatCard {
                background: white;
                border-radius: 10px;
                padding: 10px;
                min-height: 100px;
            }

            #CardTitle {
                color: #777;
                font-size: 12px;
                font-weight: bold;
            }

            #CardValue {
                font-size: 30px;
                font-weight: bold;
            }

            #StatusFrame {
                background: white;
                border-radius: 10px;
                padding: 15px;
            }

            #SectionTitle {
                font-size: 18px;
                font-weight: bold;
            }

            #ActiveStatus {
                color: #1a9c55;
                font-weight: bold;
            }

            QTableWidget {
                background: white;
                border: none;
                gridline-color: #eeeeee;
            }

            QHeaderView::section {
                background: #eef1f6;
                padding: 8px;
                font-weight: bold;
                border: none;
            }

        """)