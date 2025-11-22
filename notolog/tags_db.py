import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "database.sqlite3"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Chunks table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            start_idx INTEGER NOT NULL,
            end_idx INTEGER NOT NULL
        );
        """
    )

    # Tags table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        """
    )

    # Link table for many-to-many
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chunk_tags (
            chunk_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (chunk_id, tag_id),
            FOREIGN KEY(chunk_id) REFERENCES chunks(id) ON DELETE CASCADE,
            FOREIGN KEY(tag_id) REFERENCES tags(id) ON DELETE CASCADE
        );
        """
    )

    conn.commit()
    conn.close()


def add_chunk(file_path: str, start_idx: int, end_idx: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chunks (file_path, start_idx, end_idx) VALUES (?, ?, ?)",
        (file_path, start_idx, end_idx),
    )
    conn.commit()
    chunk_id = cur.lastrowid
    conn.close()
    return chunk_id


def add_tag(name: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO tags (name) VALUES (?)", (name,))
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        cur.execute("SELECT id FROM tags WHERE name = ?", (name,))
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def attach_tag_to_chunk(chunk_id: int, tag_id: int):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT OR IGNORE INTO chunk_tags (chunk_id, tag_id) VALUES (?, ?)",
            (chunk_id, tag_id),
        )
        conn.commit()
    finally:
        conn.close()


def get_tags_for_chunk(chunk_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT tags.id, tags.name
        FROM tags
        JOIN chunk_tags ON tags.id = chunk_tags.tag_id
        WHERE chunk_tags.chunk_id = ?
        ORDER BY tags.name ASC
        """,
        (chunk_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
