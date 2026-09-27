import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import sys

from src.utils.app_logger import AppLogger
from src.services.startup_service import StartupService
from src.core.risk_scoring import calculate_risk, RISK_TABLE


class TestAppLogger(unittest.TestCase):

    def test_log_file_creation(self):
        log_path = AppLogger.get_log_file_path()
        self.assertTrue(log_path.endswith("app.log"))

    def test_log_event(self):
        AppLogger.log_event("TEST_EVENT", "Testing logger execution")


class TestRiskEngineCategories(unittest.TestCase):

    def test_all_8_categories_present(self):
        expected_categories = {
            "safe", "password", "api_key", "jwt",
            "ssh_key", "db_credentials", "payment", "otp"
        }
        self.assertEqual(set(RISK_TABLE.keys()), expected_categories)

    def test_risk_score_calculation(self):
        password_risk = calculate_risk("password", 0.95)
        self.assertEqual(password_risk.risk_level, "Critical")
        self.assertEqual(password_risk.risk_score, 100)

        safe_risk = calculate_risk("safe", 0.99)
        self.assertEqual(safe_risk.risk_level, "Low")
        self.assertEqual(safe_risk.risk_score, 0)


class TestStartupService(unittest.TestCase):

    def test_executable_path(self):
        path = StartupService.get_executable_path()
        self.assertIn("python", path.lower())


if __name__ == "__main__":
    unittest.main()
