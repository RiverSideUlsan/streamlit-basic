import sqlite3
import tempfile
import unittest
from pathlib import Path

from app2.chat_store import (
    create_session,
    get_session,
    get_user_model,
    get_user_persona,
    init_database,
    list_sessions,
    list_turns,
    save_turn,
    save_user_model,
    save_user_persona,
)


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

    def test_saves_the_assistant_mood_for_chat_avatars(self):
        session_id = create_session("user-a", database_path=self.database_path)
        save_turn(
            "user-a",
            session_id,
            "질문",
            "답변",
            assistant_mood="agree",
            database_path=self.database_path,
        )

        turn = list_turns("user-a", session_id, self.database_path)[0]

        self.assertEqual(turn["assistant_mood"], "agree")

    def test_adds_assistant_mood_to_an_existing_database(self):
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("DROP TABLE chat_turns")
            connection.execute(
                """
                CREATE TABLE chat_turns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    user_text TEXT NOT NULL,
                    assistant_text TEXT NOT NULL,
                    file_name TEXT,
                    file_content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.commit()
        finally:
            connection.close()

        init_database(self.database_path)

        connection = sqlite3.connect(self.database_path)
        try:
            columns = {
                row[1] for row in connection.execute("PRAGMA table_info(chat_turns)")
            }
        finally:
            connection.close()

        self.assertIn("assistant_mood", columns)

    def test_saves_the_selected_persona_with_a_session(self):
        session_id = create_session(
            "user-a",
            database_path=self.database_path,
            persona="junho",
        )

        session = list_sessions("user-a", self.database_path)[0]

        self.assertEqual(session["id"], session_id)
        self.assertEqual(session["persona"], "junho")

    def test_saves_a_character_opening_message_with_a_session(self):
        opening_message = "반가워요. 오늘은 어떤 이야기를 나눌까요?"
        session_id = create_session(
            "user-a",
            database_path=self.database_path,
            persona="junho",
            opening_message=opening_message,
        )

        session = get_session("user-a", session_id, self.database_path)

        self.assertEqual(session["opening_message"], opening_message)

    def test_saves_a_user_persona_by_user(self):
        save_user_persona("user-a", "프로그래밍 초보자", self.database_path)
        save_user_persona("user-b", "창업 준비자", self.database_path)

        self.assertEqual(get_user_persona("user-a", self.database_path), "프로그래밍 초보자")
        self.assertEqual(get_user_persona("user-b", self.database_path), "창업 준비자")

    def test_saves_a_chat_model_by_user(self):
        save_user_model("user-a", "gpt-5.5", self.database_path)

        self.assertEqual(get_user_model("user-a", self.database_path), "gpt-5.5")
