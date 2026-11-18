import logging
import logging.handlers
logger = logging.getLogger("TechnologyAgent")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
            logging.handlers.RotatingFileHandler(
            "agent.log",
            maxBytes=1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger.info("Agent bắt đầu nghiên cứu tin tức")
logger.warning("Không tìm thấy đủ 5 tin tức")
logger.error("Không thể kết nối API")