
from mcp.server.fastmcp import FastMCP


# Initialize Utility MCP Server
mcp = FastMCP("Utility Server")


@mcp.tool()
def calculator(operation: str, a: float, b: float) -> str:
    """
    Thực hiện phép tính cộng, trừ, nhân, chia.

    operation chỉ nhận:
    - add
    - subtract
    - multiply
    - divide
    """

    if operation == "add":
        result = a + b

    elif operation == "subtract":
        result = a - b

    elif operation == "multiply":
        result = a * b

    elif operation == "divide":

        if b == 0:
            return "Lỗi: Không thể chia cho 0."

        result = a / b

    else:
        return "Lỗi: Phép tính không hợp lệ."

    return str(result)


if __name__ == "__main__":
    mcp.run(transport="stdio")
