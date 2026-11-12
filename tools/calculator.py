
def calculator(operation: str, a: float, b: float) -> float:
    """
    Thực hiện phép tính cơ bản.

    Args:
        operation: Phép tính (add, subtract, multiply, divide).
        a: Số thứ nhất.
        b: Số thứ hai.

    Returns:
        Kết quả phép tính.
    """

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            raise ValueError("Không thể chia cho 0.")

        return a / b

    else:
        raise ValueError("Phép tính không hợp lệ.")
