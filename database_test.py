from database import (
    create_table,
    add_news,
    get_all_news,
    search_news,
    update_news_source,
    delete_news,
    count_news
)

# create_table()

# # 1. Thêm tin tức
# add_news(
#     "NVIDIA ra mắt chip AI mới",
#     "AI",
#     "NVIDIA"
# )

# # 2. Lấy toàn bộ tin tức
# print("\n=== TẤT CẢ TIN TỨC ===")
# for news in get_all_news():
#     print(dict(news))

# # 3. Tìm kiếm
# print("\n=== TÌM KIẾM ===")
# for news in search_news("NVIDIA"):
#     print(dict(news))

# # 4. Đếm số tin
# print("\nTổng số tin:", count_news())

# 5. Cập nhật nguồn tin
updated = update_news_source(5, "TechCrunch")
print("\nSố bản ghi được cập nhật:", updated)

# 6. Xóa tin tức
deleted = delete_news(5)
print("Số bản ghi được xóa:", deleted)

# 7. Kiểm tra lại
print("Tổng số tin sau khi xóa:", count_news())