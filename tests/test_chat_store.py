import tempfile
import unittest
from pathlib import Path

from chat_store import create_session, init_database, list_sessions, list_turns, save_turn


class ChatStoreTest(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "chat.db"
        init_database(self.database_path)

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_keeps_only_ten_sessions_per_user(self):
        for number in range(11):
            create_session("user-a", f"채팅 {number}", self.database_path)

        sessions = list_sessions("user-a", self.database_path)
        self.assertEqual(len(sessions), 10)
        self.assertNotIn("채팅 0", [row["title"] for row in sessions])

    def test_keeps_only_one_hundred_turns_per_session(self):
        session_id = create_session("user-a", database_path=self.database_path)
        for number in range(101):
            save_turn("user-a", session_id, f"질문 {number}", f"답변 {number}",
                      database_path=self.database_path)

        turns = list_turns("user-a", session_id, self.database_path)
        self.assertEqual(len(turns), 100)
        self.assertEqual(turns[0]["user_text"], "질문 1")

    def test_separates_users(self):
        first_session = create_session("user-a", database_path=self.database_path)
        second_session = create_session("user-b", database_path=self.database_path)
        save_turn("user-a", first_session, "A 질문", "A 답변", database_path=self.database_path)
        save_turn("user-b", second_session, "B 질문", "B 답변", database_path=self.database_path)

        self.assertEqual(len(list_turns("user-a", first_session, self.database_path)), 1)
        self.assertEqual(len(list_turns("user-a", second_session, self.database_path)), 0)
