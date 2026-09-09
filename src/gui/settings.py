from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QSpinBox,
    QGroupBox,
    QPushButton,
)


class Settings(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Settings")
        title.setObjectName("Title")

        subtitle = QLabel(
            "Configure clipboard security behaviour"
        )
        subtitle.setObjectName("Subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Clipboard monitoring
        monitor_group = QGroupBox(
            "Clipboard Monitoring"
        )

        monitor_layout = QVBoxLayout()

        self.monitor_checkbox = QCheckBox(
            "Enable clipboard monitoring"
        )

        self.monitor_checkbox.setChecked(True)

        monitor_layout.addWidget(
            self.monitor_checkbox
        )

        monitor_group.setLayout(
            monitor_layout
        )

        layout.addWidget(monitor_group)

        # Auto clear
        clear_group = QGroupBox(
            "Automatic Clipboard Clearing"
        )

        clear_layout = QVBoxLayout()

        self.clear_checkbox = QCheckBox(
            "Automatically clear sensitive clipboard data"
        )

        self.clear_checkbox.setChecked(True)

        clear_layout.addWidget(
            self.clear_checkbox
        )

        clear_group.setLayout(
            clear_layout
        )

        layout.addWidget(clear_group)

        # Default timeout
        timeout_group = QGroupBox(
            "Default Clear Timeout"
        )

        timeout_layout = QVBoxLayout()

        self.timeout_spin = QSpinBox()

        self.timeout_spin.setMinimum(1)
        self.timeout_spin.setMaximum(300)
        self.timeout_spin.setValue(15)

        timeout_layout.addWidget(
            QLabel("Seconds:")
        )

        timeout_layout.addWidget(
            self.timeout_spin
        )

        timeout_group.setLayout(
            timeout_layout
        )

        layout.addWidget(timeout_group)

        save_button = QPushButton(
            "Save Settings"
        )

        save_button.clicked.connect(
            self.save_settings
        )

        layout.addWidget(save_button)

        layout.addStretch()

        self.setLayout(layout)

    def save_settings(self):

        print("Settings saved")

        print(
            "Monitoring:",
            self.monitor_checkbox.isChecked()
        )

        print(
            "Auto Clear:",
            self.clear_checkbox.isChecked()
        )

        print(
            "Timeout:",
            self.timeout_spin.value()
        )