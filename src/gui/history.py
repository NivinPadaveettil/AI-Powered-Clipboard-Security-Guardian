from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QHeaderView,
    QDialog,
    QFormLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from src.database.sqlite_logger import logger
from src.core.risk_scoring import RISK_TABLE


class DetectionDetailsDialog(QDialog):

    def __init__(self, record, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Detection Details")
        self.resize(450, 320)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel(f"Detection #{record[0]}")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e293b;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        # Record fields: id, timestamp, category, confidence, risk_score, risk_level, action
        rec_id, timestamp, category, confidence, risk_score, risk_level, action = record

        try:
            conf_str = f"{float(confidence) * 100:.2f}%"
        except (ValueError, TypeError):
            conf_str = str(confidence)

        explanation = RISK_TABLE.get(category, None)
        exp_text = explanation.explanation if explanation else "Sensitivity analysis record."

        form.addRow("Timestamp:", QLabel(str(timestamp)))
        form.addRow("Category:", QLabel(str(category).upper()))
        form.addRow("Confidence Score:", QLabel(conf_str))
        form.addRow("Risk Score:", QLabel(f"{risk_score} / 100"))
        form.addRow("Risk Level:", QLabel(str(risk_level)))
        form.addRow("Recommended Action:", QLabel(str(action)))
        form.addRow("Explanation:", QLabel(exp_text))

        layout.addLayout(form)
        layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)



class History(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        # ============================================================
        # TITLE
        # ============================================================

        title = QLabel("Detection History")
        title.setObjectName("Title")

        subtitle = QLabel(
            "Previously detected clipboard content"
        )
        subtitle.setObjectName("Subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ============================================================
        # FILTER / SEARCH BAR
        # ============================================================

        filter_layout = QHBoxLayout()

        # Search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search category, risk level, action..."
        )
        self.search_box.textChanged.connect(self.apply_filters)

        filter_layout.addWidget(self.search_box, 2)

        # Category filter
        self.category_filter = QComboBox()
        self.category_filter.addItems([
            "All Categories",
            "api_key",
            "db_credentials",
            "jwt",
            "otp",
            "password",
            "payment",
            "safe",
            "ssh_key",
        ])
        self.category_filter.currentTextChanged.connect(
            self.apply_filters
        )

        filter_layout.addWidget(self.category_filter)

        # Risk filter
        self.risk_filter = QComboBox()
        self.risk_filter.addItems([
            "All Risk Levels",
            "Critical",
            "High",
            "Medium",
            "Low",
        ])
        self.risk_filter.currentTextChanged.connect(
            self.apply_filters
        )

        filter_layout.addWidget(self.risk_filter)

        layout.addLayout(filter_layout)

        # ============================================================
        # BUTTONS
        # ============================================================

        button_layout = QHBoxLayout()

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_history)

        clear_button = QPushButton("Clear History")
        clear_button.clicked.connect(self.clear_history)

        button_layout.addWidget(refresh_button)
        button_layout.addWidget(clear_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # ============================================================
        # TABLE
        # ============================================================

        self.table = QTableWidget()

        self.table.setColumnCount(7)
        self.table.setMinimumHeight(420)
        self.table.setMaximumHeight(500)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(True)
        self.table.setShowGrid(True)
        self.table.setAlternatingRowColors(True)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Time",
            "Category",
            "Confidence",
            "Risk Score",
            "Risk Level",
            "Action",
        ])

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        # Column sizing
        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            5,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            6,
            QHeaderView.ResizeMode.Stretch
        )

        # Make the history table visibly stable inside the
        # page stack and prevent the extra row-header column
        # from visually collapsing the content region.
        self.table.setSizeAdjustPolicy(
            QTableWidget.SizeAdjustPolicy.AdjustToContents
        )

        self.table.cellDoubleClicked.connect(self.show_record_details)

        layout.addWidget(self.table)
        self.setLayout(layout)

        # Store records for filtering
        self.records = []

        # Initial load
        self.load_history()

    # ================================================================
    # SHOW RECORD DETAILS
    # ================================================================

    def show_record_details(self, row, column):
        item = self.table.item(row, 0)
        if item:
            record_data = item.data(Qt.ItemDataRole.UserRole)
            if record_data:
                dialog = DetectionDetailsDialog(record_data, self)
                dialog.exec()

    # ================================================================
    # LOAD HISTORY
    # ================================================================

    def load_history(self):

        try:

            self.records = logger.fetch_all()

            self.apply_filters()

            print(
                f"History loaded: {len(self.records)} records"
            )

        except Exception as e:

            print("History Error:", e)

    # ================================================================
    # APPLY FILTERS
    # ================================================================

    def apply_filters(self):

        try:

            search_text = (
                self.search_box.text()
                .strip()
                .lower()
            )

            selected_category = (
                self.category_filter.currentText()
            )

            selected_risk = (
                self.risk_filter.currentText()
            )

            self.table.setRowCount(0)

            for row_data in self.records:

                # ----------------------------------------------------
                # Category filter
                # ----------------------------------------------------

                category = str(row_data[2])

                if (
                    selected_category != "All Categories"
                    and category != selected_category
                ):
                    continue

                # ----------------------------------------------------
                # Risk filter
                # ----------------------------------------------------

                risk_level = str(row_data[5])

                if (
                    selected_risk != "All Risk Levels"
                    and risk_level != selected_risk
                ):
                    continue

                # ----------------------------------------------------
                # Search
                # ----------------------------------------------------

                searchable_text = " ".join(
                    str(value)
                    for value in row_data
                ).lower()

                if (
                    search_text
                    and search_text not in searchable_text
                ):
                    continue

                # ----------------------------------------------------
                # Add row
                # ----------------------------------------------------

                row = self.table.rowCount()

                self.table.insertRow(row)

                for column, value in enumerate(row_data):

                    # Confidence formatting
                    if column == 3:

                        try:
                            display_value = (
                                f"{float(value) * 100:.2f}%"
                            )

                        except (ValueError, TypeError):

                            display_value = str(value)

                    else:

                        display_value = str(value)

                    item = QTableWidgetItem(
                        display_value
                    )

                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                    # Risk Level color formatting (Column 5)
                    if column == 5:
                        rl = str(value).lower()
                        if "critical" in rl:
                            item.setForeground(QColor("#dc2626"))  # Red
                        elif "high" in rl:
                            item.setForeground(QColor("#ea580c"))  # Orange
                        elif "medium" in rl:
                            item.setForeground(QColor("#d97706"))  # Amber/Yellow
                        else:
                            item.setForeground(QColor("#16a34a"))  # Green

                    # Store full row data in item payload for details dialog
                    item.setData(Qt.ItemDataRole.UserRole, row_data)

                    self.table.setItem(
                        row,
                        column,
                        item
                    )

            print(
                f"History filtered: "
                f"{self.table.rowCount()} records"
            )

        except Exception as e:

            print("History Filter Error:", e)

    # ================================================================
    # CLEAR HISTORY
    # ================================================================

    def clear_history(self):

        reply = QMessageBox.question(
            self,
            "Clear Detection History",
            "Are you sure you want to delete all detection history?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:

            logger.clear_history()

            self.records = []

            self.table.setRowCount(0)

            print("Detection history cleared.")

        except Exception as e:

            print("Clear History Error:", e)

            QMessageBox.critical(
                self,
                "Error",
                f"Failed to clear history:\n{e}"
            )