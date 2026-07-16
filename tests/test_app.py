import os
import unittest
from unittest.mock import patch

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.client = app.test_client()

    def test_home_and_health(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_empty_message_is_rejected(self):
        response = self.client.post("/api/chat", json={"message": "  "})
        self.assertEqual(response.status_code, 400)

    def test_missing_api_key_is_safe(self):
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post("/api/chat", json={"message": "Hello"})
        self.assertEqual(response.status_code, 503)
        self.assertNotIn("GROQ_API_KEY", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
