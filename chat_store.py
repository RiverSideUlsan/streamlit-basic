"""로그인 사용자별 채팅 세션과 대화 턴을 SQLite에 저장합니다."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path


DB_PATH = Path(__file__).resolve().with_name("chat_history.db")
MAX_SESSIONS = 10
MAX_TURNS = 100


def _connect(database_path=DB_PATH):
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def _database_connection(database_path):
    connection = _connect(database_path)
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_database(database_path=DB_PATH):
    """기존 messages 테이블은 건드리지 않고 새 저장 구조만 만듭니다."""
    with _database_connection(database_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                persona TEXT NOT NULL DEFAULT 'dawon',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS chat_turns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                user_text TEXT NOT NULL,
                assistant_text TEXT NOT NULL,
                assistant_mood TEXT NOT NULL DEFAULT 'hi',
                file_name TEXT,
                file_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
            );
            """
        )
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(chat_sessions)").fetchall()
        }
        if "persona" not in columns:
            connection.execute(
                "ALTER TABLE chat_sessions "
                "ADD COLUMN persona TEXT NOT NULL DEFAULT 'dawon'"
            )

        turn_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(chat_turns)").fetchall()
        }
        if "assistant_mood" not in turn_columns:
            connection.execute(
                "ALTER TABLE chat_turns "
                "ADD COLUMN assistant_mood TEXT NOT NULL DEFAULT 'hi'"
            )


def create_session(user_id, title="새 채팅", database_path=DB_PATH, persona="dawon"):
    with _database_connection(database_path) as connection:
        cursor = connection.execute(
            "INSERT INTO chat_sessions (user_id, title, persona) VALUES (?, ?, ?)",
            (user_id, title, persona),
        )
        session_id = cursor.lastrowid
        _trim_sessions(connection, user_id)
    return session_id


def _trim_sessions(connection, user_id):
    old_rows = connection.execute(
        """
        SELECT id FROM chat_sessions
        WHERE user_id = ?
        ORDER BY updated_at DESC, id DESC
        LIMIT -1 OFFSET ?
        """,
        (user_id, MAX_SESSIONS),
    ).fetchall()
    for row in old_rows:
        connection.execute("DELETE FROM chat_sessions WHERE id = ?", (row["id"],))


def list_sessions(user_id, database_path=DB_PATH):
    with _database_connection(database_path) as connection:
        return connection.execute(
            """
            SELECT id, title, persona, created_at, updated_at
            FROM chat_sessions
            WHERE user_id = ?
            ORDER BY updated_at DESC, id DESC
            """,
            (user_id,),
        ).fetchall()


def get_session(user_id, session_id, database_path=DB_PATH):
    with _database_connection(database_path) as connection:
        return connection.execute(
            "SELECT id, title, persona FROM chat_sessions WHERE user_id = ? AND id = ?",
            (user_id, session_id),
        ).fetchone()


def list_turns(user_id, session_id, database_path=DB_PATH):
    with _database_connection(database_path) as connection:
        return connection.execute(
            """
            SELECT chat_turns.id, user_text, assistant_text, assistant_mood,
                   file_name, file_content,
                   chat_turns.created_at
            FROM chat_turns
            JOIN chat_sessions ON chat_sessions.id = chat_turns.session_id
            WHERE chat_sessions.user_id = ? AND chat_turns.session_id = ?
            ORDER BY chat_turns.id ASC
            """,
            (user_id, session_id),
        ).fetchall()


def save_turn(user_id, session_id, user_text, assistant_text, file_name=None,
              file_content=None, assistant_mood="agree", database_path=DB_PATH):
    with _database_connection(database_path) as connection:
        session = connection.execute(
            "SELECT id FROM chat_sessions WHERE user_id = ? AND id = ?",
            (user_id, session_id),
        ).fetchone()
        if not session:
            return

        connection.execute(
            """
            INSERT INTO chat_turns (
                session_id, user_text, assistant_text, assistant_mood, file_name, file_content
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                user_text,
                assistant_text,
                assistant_mood,
                file_name,
                file_content,
            ),
        )
        connection.execute(
            """
            UPDATE chat_sessions
            SET title = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (user_text[:30] or "새 채팅", session_id),
        )
        _trim_turns(connection, session_id)


def _trim_turns(connection, session_id):
    old_rows = connection.execute(
        """
        SELECT id FROM chat_turns
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT -1 OFFSET ?
        """,
        (session_id, MAX_TURNS),
    ).fetchall()
    for row in old_rows:
        connection.execute("DELETE FROM chat_turns WHERE id = ?", (row["id"],))
