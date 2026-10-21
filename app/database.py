
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "campuslens.db"


def get_connection():
    """Create a connection to the CampusLens AI database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the documents table if it does not exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


if __name__ == "__main__":
    initialize_database()
    print("CampusLens AI database initialized successfully!")
