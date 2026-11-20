from database import get_connection

with get_connection() as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM news")

    news_list = cursor.fetchall()

    for news in news_list:
        print(dict(news))

# Kiểm tra kết nối đã đóng
print("\nKết nối đã đóng:", connection is not None)

try:
    connection.execute("SELECT 1")
except Exception as e:
    print("Không thể sử dụng kết nối:", e)