import unittest
from unittest.mock import MagicMock, patch
import json
import tempfile
from pathlib import Path

from src.config.settings_manager import SettingsManager, DEFAULT_SETTINGS
from src.services.notification_service import NotificationService
from src.core.risk_scoring import RiskResult


class TestSettingsManager(unittest.TestCase):

    def test_default_settings_keys(self):
        self.assertIn("monitoring_enabled", DEFAULT_SETTINGS)
        self.assertIn("auto_clear_enabled", DEFAULT_SETTINGS)
        self.assertIn("clear_timeout", DEFAULT_SETTINGS)
        self.assertIn("notifications_enabled", DEFAULT_SETTINGS)
        self.assertIn("start_monitoring_automatically", DEFAULT_SETTINGS)

    def test_save_and_load_settings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_file = Path(tmpdir) / "settings.json"

            with patch("src.config.settings_manager.CONFIG_DIR", Path(tmpdir)), \
                 patch("src.config.settings_manager.SETTINGS_FILE", settings_file):

                sm = SettingsManager()
                self.assertTrue(sm.get("notifications_enabled"))

                new_settings = {
                    "monitoring_enabled": False,
                    "auto_clear_enabled": True,
                    "clear_timeout": 45,
                    "notifications_enabled": False,
                    "start_monitoring_automatically": False,
                }
                sm.save(new_settings)

                # Re-load
                sm2 = SettingsManager()
                self.assertFalse(sm2.get("monitoring_enabled"))
                self.assertEqual(sm2.get("clear_timeout"), 45)
                self.assertFalse(sm2.get("notifications_enabled"))
                self.assertFalse(sm2.get("start_monitoring_automatically"))


class TestNotificationService(unittest.TestCase):

    @patch("plyer.notification.notify")
    def test_show_notification(self, mock_notify):
        dummy_risk = RiskResult(
            category="password",
            confidence=0.98,
            risk_score=100,
            risk_level="Critical",
            explanation="Password detected in clipboard.",
            action="Clear clipboard immediately.",
            timeout=15,
        )

        NotificationService.show_notification(dummy_risk)

        mock_notify.assert_called_once()
        kwargs = mock_notify.call_args.kwargs
        self.assertIn("Critical Risk", kwargs["title"])
        self.assertIn("Category: password", kwargs["message"])
        self.assertIn("100/100", kwargs["message"])

    @patch("plyer.notification.notify", side_effect=Exception("Plyer error"))
    def test_notification_error_handled(self, mock_notify):
        dummy_risk = RiskResult(
            category="api_key",
            confidence=0.95,
            risk_score=95,
            risk_level="Critical",
            explanation="API key detected.",
            action="Clipboard will be cleared.",
            timeout=15,
        )

        # Should not raise exception
        NotificationService.show_notification(dummy_risk)


class TestClipboardMonitorIntegration(unittest.TestCase):

    @patch("src.core.clipboard_monitor.NotificationService.show_notification")
    @patch("src.core.clipboard_monitor.predict", return_value=("password", 0.99))
    @patch("src.core.clipboard_monitor.logger.log_detection")
    def test_process_clipboard_triggers_notification_when_enabled(
        self, mock_log, mock_predict, mock_notify
    ):
        from src.core.clipboard_monitor import ClipboardMonitor
        monitor = ClipboardMonitor()
        monitor.settings.set("notifications_enabled", True)

        monitor.process_clipboard("MySecretPass123!")

        mock_notify.assert_called_once()
        self.assertEqual(mock_notify.call_args[0][0].category, "password")

    @patch("src.core.clipboard_monitor.NotificationService.show_notification")
    @patch("src.core.clipboard_monitor.predict", return_value=("password", 0.99))
    @patch("src.core.clipboard_monitor.logger.log_detection")
    def test_process_clipboard_suppresses_notification_when_disabled(
        self, mock_log, mock_predict, mock_notify
    ):
        from src.core.clipboard_monitor import ClipboardMonitor
        monitor = ClipboardMonitor()
        monitor.settings.set("notifications_enabled", False)

        monitor.process_clipboard("MySecretPass123!")

        mock_notify.assert_not_called()


if __name__ == "__main__":
    unittest.main()

