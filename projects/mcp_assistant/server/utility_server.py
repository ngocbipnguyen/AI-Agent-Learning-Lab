from mcp.server.fastmcp import FastMCP
from pydantic import Field
from typing import Literal
from mcp.server.fastmcp.exceptions import ToolError
mcp = FastMCP("Utility Server")


@mcp.tool()
def calculator(
    operation: Literal["add", "subtract", "multiply", "divide"],
    a: float,
    b: float
) -> str:
    """
    Thực hiện phép tính cộng, trừ, nhân, chia.
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise ToolError("Không thể chia cho 0.")
        result = a / b
    else:
        return "Lỗi: Phép tính không hợp lệ."

    return str(result)


if __name__ == "__main__":
    mcp.run(transport="stdio")