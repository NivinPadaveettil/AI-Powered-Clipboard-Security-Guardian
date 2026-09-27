import unittest
import json
from src.web.web_app import app


class TestFlaskWebInterface(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI Security Clipboard Guardian", response.data)

    def test_api_stats_route(self):
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("total", data)
        self.assertIn("critical", data)
        self.assertIn("high", data)

    def test_api_history_route(self):
        response = self.client.get("/api/history")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("history", data)

    def test_api_settings_get_and_post(self):
        get_res = self.client.get("/api/settings")
        self.assertEqual(get_res.status_code, 200)

        post_res = self.client.post("/api/settings", json={
            "monitoring_enabled": True,
            "auto_clear_enabled": True,
            "clear_timeout": 20,
            "notifications_enabled": True,
            "start_monitoring_automatically": True,
        })
        self.assertEqual(post_res.status_code, 200)
        data = json.loads(post_res.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["settings"]["clear_timeout"], 20)

    def test_api_predict_route(self):
        post_res = self.client.post("/api/predict", json={
            "text": "my_secret_db_password_123!"
        })
        self.assertEqual(post_res.status_code, 200)
        data = json.loads(post_res.data)
        self.assertTrue(data["success"])
        self.assertIn("category", data)
        self.assertIn("risk_level", data)


if __name__ == "__main__":
    unittest.main()
