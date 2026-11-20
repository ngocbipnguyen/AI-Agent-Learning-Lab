import sqlite3
from news_schema import News


from contextlib import contextmanager


@contextmanager
def get_connection():
    connection = sqlite3.connect("news.db")
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def create_table():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT,
                source TEXT
            )
        """)

def count_news():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM news")

        return cursor.fetchone()[0]

def get_all_news():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM news ORDER BY id DESC")

        return cursor.fetchall()




def add_news(title: str, category: str, source: str):
    news = News(
        title=title,
        category=category,
        source=source
    )

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO news (title, category, source)
            VALUES (?, ?, ?)
        """, (news.title, news.category, news.source))


def update_news_source(news_id: int, source: str):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE news
            SET source = ?
            WHERE id = ?
        """, (source, news_id))

        return cursor.rowcount


def delete_news(news_id: int):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM news
            WHERE id = ?
        """, (news_id,))

        return cursor.rowcount


def search_news(keyword: str):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM news
            WHERE title LIKE ?
            ORDER BY id DESC
        """, (f"%{keyword}%",))

        return cursor.fetchall()

def get_news_by_category(category: str):
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM news
            WHERE category = ?
            ORDER BY id DESC
        """, (category,))

        return cursor.fetchall()


def get_news_paginated(page: int = 1, page_size: int = 10):
    if page < 1 or page_size < 1:
        raise ValueError("Page và page_size phải lớn hơn 0")

    offset = (page - 1) * page_size

    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT * FROM news
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """, (page_size, offset))

        return cursor.fetchall()


def create_indexes():
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_news_category
            ON news(category)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_news_title
            ON news(title)
        """)

        print("Tạo Index thành công!")