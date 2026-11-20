# import sqlite3

# connection = sqlite3.connect("news.db")

# cursor = connection.cursor()

# # Tạo bảng news
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS news (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         title TEXT NOT NULL,
#         category TEXT,
#         source TEXT
#     )
# """)

# connection.commit()

# print("Tạo bảng news thành công!")
# # cursor.execute("""
# #     INSERT INTO news (title, category, source)
# #     VALUES (?, ?, ?)
# # """, (
# #     "OpenAI ra mắt mô hình AI mới",
# #     "AI",
# #     "OpenAI"
# # ))

# connection.commit()

# # print("Thêm tin tức thành công!")
# # cursor.execute(
# #     "SELECT * FROM news WHERE category = ?",
# #     ("AI",)
# # )

# # news_list = cursor.fetchall()

# # for news in news_list:
# #     print(news)

# # cursor.execute("""
# #     UPDATE news
# #     SET source = ?
# #     WHERE id = ?
# # """, ("The Verge", 1))

# # connection.commit()

# # print("Cập nhật dữ liệu thành công!")

# # cursor.execute("""
# #     DELETE FROM news
# #     WHERE id = ?
# # """, (2,))

# # connection.commit()

# # print("Xóa dữ liệu thành công!")

# # cursor.execute("SELECT COUNT(*) FROM news")

# # total_news = cursor.fetchone()[0]

# # print(f"Tổng số tin tức: {total_news}")

# # news_list = cursor.fetchall()

# # for news in news_list:
# #     print(news)

# cursor.execute("SELECT * FROM news ORDER BY id")

# # Lấy một bản ghi
# first_news = cursor.fetchone()
# print("Tin đầu tiên:", first_news)

# # Lấy tối đa 1 bản ghi tiếp theo
# next_news = cursor.fetchmany(1)
# print("Tin tiếp theo:", next_news)

# connection.close()


# from database import add_news, get_all_news

# add_news(
#     "Google ra mắt công nghệ AI mới",
#     "AI",
#     "Google"
# )

# news_list = get_all_news()

# for news in news_list:
#     print(news)

# from database import add_news, get_all_news
# from pydantic import ValidationError

# try:
#     add_news(
#         "AI",
#         "A",
#         "G"
#     )
# except ValidationError as e:
#     print("Dữ liệu không hợp lệ!")
#     print(e)

# news_list = get_all_news()

# for news in news_list:
#     print(news)


# from database import (
#     update_news_source,
#     delete_news,
#     get_all_news
# )

# # Cập nhật nguồn tin có ID = 4
# updated = update_news_source(4, "Google News")
# print(f"Số bản ghi được cập nhật: {updated}")

# # Xóa tin có ID = 3
# deleted = delete_news(3)
# print(f"Số bản ghi được xóa: {deleted}")

# # Hiển thị dữ liệu sau khi thay đổi
# print("\n=== DATABASE ===")

# for news in get_all_news():
#     print(news)

# from database import search_news

# results = search_news("OpenAI")

# if results:
#     for news in results:
#         print(news)
# else:
#     print("Không tìm thấy tin tức!")

# from database import get_news_by_category

# news_list = get_news_by_category("AI")

# if news_list:
#     for news in news_list:
#         print(news)
# else:
#     print("Không tìm thấy tin tức thuộc lĩnh vực này!")


# from database import get_news_paginated

# # Lấy trang 1, mỗi trang 1 tin
# news_list = get_news_paginated(page=1, page_size=1)

# print("=== TRANG 1 ===")

# for news in news_list:
#     print(news)

# # Lấy trang 2
# news_list = get_news_paginated(page=2, page_size=1)

# print("\n=== TRANG 2 ===")

# for news in news_list:
#     print(news)


# from database import create_indexes

# create_indexes()

# import sqlite3

# connection = sqlite3.connect("news.db")
# cursor = connection.cursor()

# cursor.execute("""
#     EXPLAIN QUERY PLAN
#     SELECT * FROM news
#     WHERE category = 'AI'
# """)

# for row in cursor.fetchall():
#     print(row)

# connection.close()

# import sqlite3

# connection = sqlite3.connect("news.db")
# cursor = connection.cursor()

# try:
#     cursor.execute("""
#         INSERT INTO news (title, category, source)
#         VALUES (?, ?, ?)
#     """, ("Tin tức thử nghiệm", "AI", "Test"))

#     # Mô phỏng lỗi
#     raise ValueError("Có lỗi xảy ra!")

#     connection.commit()

# except ValueError as e:
#     connection.rollback()
#     print(f"Đã rollback: {e}")

# finally:
#     connection.close()

# import sqlite3

# connection = sqlite3.connect("news.db")
# cursor = connection.cursor()

# cursor.execute("""
#     SELECT * FROM news
#     WHERE title = ?
# """, ("Tin tức thử nghiệm",))

# result = cursor.fetchall()

# if result:
#     print("Bản ghi vẫn tồn tại:", result)
# else:
#     print("Rollback thành công! Không tìm thấy bản ghi.")

# connection.close()

import sqlite3
import json
connection = sqlite3.connect("news.db")

# Cho phép truy cập dữ liệu bằng tên cột
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("SELECT * FROM news")

news_list = cursor.fetchall()

news_data = [dict(news) for news in news_list]

json_data = json.dumps(
    news_data,
    ensure_ascii=False,
    indent=4
)

with open("news.json", "w", encoding="utf-8") as file:
    file.write(json_data)

print("Đã lưu dữ liệu vào news.json!")

connection.close()