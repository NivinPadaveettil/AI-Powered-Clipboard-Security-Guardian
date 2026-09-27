from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QFormLayout,
    QScrollArea,
)
from PyQt6.QtCore import Qt

from src.database.sqlite_logger import logger


class SecurityPrivacy(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # Title
        title = QLabel("Security & Privacy Guarantees")
        title.setObjectName("Title")

        subtitle = QLabel(
            "Transparency regarding data processing, local AI inference, and zero-retention architecture"
        )
        subtitle.setObjectName("Subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        # Card 1: Local AI Inference
        group1 = QGroupBox("🔒 Local AI Model Execution")
        g1_layout = QVBoxLayout(group1)
        lbl1 = QLabel(
            "All text classification is performed locally on your machine using an embedded DistilBERT "
            "Transformer model. Your clipboard contents are **NEVER** sent to external servers, cloud APIs, "
            "or third-party analytics services."
        )
        lbl1.setWordWrap(True)
        g1_layout.addWidget(lbl1)
        scroll_layout.addWidget(group1)

        # Card 2: Zero Raw Content Retention
        group2 = QGroupBox("🛡️ Zero Sensitive Content Retention")
        g2_layout = QVBoxLayout(group2)
        lbl2 = QLabel(
            "The SQLite database stores ONLY anonymized detection metadata (category, confidence %, "
            "risk score, risk level, action, and timestamp). The actual copied sensitive text is "
            "**NEVER saved to disk** or stored in database tables."
        )
        lbl2.setWordWrap(True)
        g2_layout.addWidget(lbl2)
        scroll_layout.addWidget(group2)

        # Card 3: Automatic Clearing Mechanics
        group3 = QGroupBox("⏱️ Automatic Clearing Protection")
        g3_layout = QVBoxLayout(group3)
        lbl3 = QLabel(
            "When sensitive data (such as passwords, API keys, or private SSH keys) is copied, "
            "the Guardian schedules a background countdown to automatically overwrite the OS clipboard. "
            "If you copy new text before the timer expires, clearing of the new text is automatically skipped."
        )
        lbl3.setWordWrap(True)
        g3_layout.addWidget(lbl3)
        scroll_layout.addWidget(group3)

        # Card 4: Local Storage Information
        group4 = QGroupBox("📁 Local Storage Metadata")
        g4_layout = QFormLayout(group4)
        db_path = logger.get_database_path()
        g4_layout.addRow("Database File Path:", QLabel(db_path))
        g4_layout.addRow("Encryption & Scope:", QLabel("Local User Application Data"))
        scroll_layout.addWidget(group4)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
