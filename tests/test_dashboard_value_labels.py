from PyQt6.QtWidgets import QApplication, QLabel

from src.gui.dashboard import Dashboard


def test_dashboard_card_value_labels_have_object_name():
    app = QApplication.instance() or QApplication([])

    dashboard = Dashboard()

    assert dashboard.total_card.findChild(QLabel, "CardValue") is not None
    assert dashboard.critical_card.findChild(QLabel, "CardValue") is not None
    assert dashboard.high_card.findChild(QLabel, "CardValue") is not None
    assert dashboard.safe_card.findChild(QLabel, "CardValue") is not None
