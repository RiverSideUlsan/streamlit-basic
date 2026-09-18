import sqlite3
import tempfile
import unittest
from pathlib import Path

from chat_app.auth_store import authenticate_user, create_user, init_user_database


class AuthStoreTest(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "auth.db"
        init_user_database(self.database_path)

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_creates_and_authenticates_a_user(self):
        self.assertTrue(create_user("learner", "safe-password", self.database_path))
        self.assertTrue(authenticate_user("learner", "safe-password", self.database_path))
        self.assertFalse(authenticate_user("learner", "wrong-password", self.database_path))

    def test_does_not_store_the_plaintext_password(self):
        create_user("learner", "safe-password", self.database_path)

        connection = sqlite3.connect(self.database_path)
        try:
            stored_hash = connection.execute(
                "SELECT password_hash FROM users WHERE username = ?",
                ("learner",),
            ).fetchone()[0]
        finally:
            connection.close()

        self.assertNotEqual(stored_hash, "safe-password")

    def test_rejects_duplicate_or_short_credentials(self):
        self.assertFalse(create_user("learner", "short", self.database_path))
        self.assertTrue(create_user("learner", "safe-password", self.database_path))
        self.assertFalse(create_user("learner", "another-password", self.database_path))
