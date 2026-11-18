
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TechnologyAgent")


class InvalidNewsError(Exception):
    pass


def validate_news(news):
    if not news:
        raise InvalidNewsError("Không tìm thấy tin tức")

    return True


try:
    validate_news(["OpenAI ra mắt mô hình AI mới"])
except InvalidNewsError:
    logger.exception("Lỗi dữ liệu tin tức")
