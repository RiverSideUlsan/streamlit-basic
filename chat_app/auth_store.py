"""SQLite에 로그인 계정과 비밀번호 해시를 저장합니다."""

import hashlib
import hmac
import secrets
import sqlite3

from chat_app.chat_store import DB_PATH


PASSWORD_ITERATIONS = 210_000


def init_user_database(database_path=DB_PATH):
    connection = sqlite3.connect(database_path)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def _make_password_hash(password):
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS,
    )
    return "$".join([str(PASSWORD_ITERATIONS), salt.hex(), password_hash.hex()])


def _verify_password(password, stored_password_hash):
    iterations, salt_hex, password_hash_hex = stored_password_hash.split("$")
    calculated_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        int(iterations),
    )
    return hmac.compare_digest(calculated_hash.hex(), password_hash_hex)


def create_user(username, password, database_path=DB_PATH):
    username = username.strip()
    if not username or len(password) < 8:
        return False

    try:
        connection = sqlite3.connect(database_path)
        try:
            connection.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, _make_password_hash(password)),
            )
            connection.commit()
        finally:
            connection.close()
    except sqlite3.IntegrityError:
        return False

    return True


def authenticate_user(username, password, database_path=DB_PATH):
    username = username.strip()
    connection = sqlite3.connect(database_path)
    try:
        row = connection.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    finally:
        connection.close()

    return bool(row and _verify_password(password, row[0]))
