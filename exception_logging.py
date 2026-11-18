
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("agent.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("TechnologyAgent")




def divide(a, b):
    try:
        if b == 0:
            raise ValueError("Mẫu số không được bằng 0")

        return a / b

    except (ValueError, TypeError):
        logger.exception("Phép tính không hợp lệ")
        return None

    finally:
        logger.info("Hoàn thành phép tính")


result = divide(10, 0)
print(result)


