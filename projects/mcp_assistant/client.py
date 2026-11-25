
import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import logging
from logging.handlers import RotatingFileHandler


# Load environment variables
ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env", override=True)

# Logging configuration
LOG_DIR = ROOT_DIR / "projects" / "mcp_assistant" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "agent.log"

logger = logging.getLogger("mcp_assistant")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# Write logs to file, rotate when file reaches 1 MB
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=1_000_000,
    backupCount=5,
    encoding="utf-8",
)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Display logs in terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


# Initialize OpenAI
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
MAX_ITERATIONS = 5


# MCP Server paths
NEWS_SERVER_PATH = (
    ROOT_DIR / "projects" / "mcp_assistant"
    / "server" / "news_server.py"
)

# NEWS_SERVER_PATH = (
#     ROOT_DIR / "projects" / "mcp_assistant"
#     / "server" / "news_server_missing.py"
# )

UTILITY_SERVER_PATH = (
    ROOT_DIR / "projects" / "mcp_assistant"
    / "server" / "utility_server.py"
)


async def main():

    # Configure News Server
    news_params = StdioServerParameters(
        command=sys.executable,
        args=[str(NEWS_SERVER_PATH)],
        env=None,
    )

    # Configure Utility Server
    utility_params = StdioServerParameters(
        command=sys.executable,
        args=[str(UTILITY_SERVER_PATH)],
        env=None,
    )

    # Connect to both MCP Servers
    async with stdio_client(news_params) as (news_read, news_write):

        async with stdio_client(utility_params) as (
            utility_read, utility_write
        ):

            async with ClientSession(
                news_read, news_write
            ) as news_session:

                async with ClientSession(
                    utility_read, utility_write
                ) as utility_session:

                    # Initialize both sessions
                    try:
                        await news_session.initialize()
                        logger.info("News MCP Server initialized")

                        await utility_session.initialize()
                        logger.info("Utility MCP Server initialized")

                    except Exception:
                        logger.exception("Failed to initialize MCP Servers")
                        print("\nKhông thể kết nối đến MCP Server. Vui lòng kiểm tra Server.")
                        return

                    print("News MCP Server connected!")
                    print("Utility MCP Server connected!")
                    logger.info("News MCP Server connected")
                    logger.info("Utility MCP Server connected")

                    # Collect tools from both servers
                    news_tools = await news_session.list_tools()
                    utility_tools = await utility_session.list_tools()

                    # Map tool names to their sessions
                    tool_sessions = {}

                    openai_tools = []

                    for tool in news_tools.tools:

                        tool_sessions[tool.name] = news_session

                        openai_tools.append({
                            "type": "function",
                            "function": {
                                "name": tool.name,
                                "description": tool.description or "",
                                "parameters": tool.inputSchema,
                            },
                        })

                    for tool in utility_tools.tools:

                        if tool.name in tool_sessions:
                            raise ValueError(
                                f"Duplicate Tool name: {tool.name}"
                            )

                        tool_sessions[tool.name] = utility_session

                        openai_tools.append({
                            "type": "function",
                            "function": {
                                "name": tool.name,
                                "description": tool.description or "",
                                "parameters": tool.inputSchema,
                            },
                        })

                    print("\n=== AVAILABLE MCP TOOLS ===")

                    for tool in openai_tools:
                        function = tool["function"]
                        print(
                            f"- {function['name']}: "
                            f"{function['description']}"
                        )

                    # User input
                    user_message = input(
                        "\nBạn muốn thực hiện công việc gì? "
                    )

                    messages = [
                        {
                            "role": "system",
                            "content": (
                                "Bạn là trợ lý AI có khả năng nghiên cứu "
                                "tin tức và thực hiện tính toán. "
                                "Sử dụng các Tools phù hợp với yêu cầu. "
                                "Không tự bịa thông tin."
                            ),
                        },
                        {
                            "role": "user",
                            "content": user_message,
                        },
                    ]

                    # Agent Loop
                    for iteration in range(MAX_ITERATIONS):

                        print(
                            f"\n[Agent Loop] "
                            f"Lượt {iteration + 1}/{MAX_ITERATIONS}"
                        )

                        logger.info(
                            "Agent loop iteration: %s",
                            iteration + 1
                        )

                        
                        try:
                            response = openai_client.chat.completions.create(
                                model=MODEL_NAME,
                                messages=messages,
                                tools=openai_tools,
                                tool_choice="auto",
                            )

                        except Exception:
                            logger.exception("OpenAI API request failed")
                            print("\nĐã xảy ra lỗi khi gọi OpenAI API.")
                            break


                        assistant_message = response.choices[0].message

                        # Finish when no more Tool calls are needed
                        if not assistant_message.tool_calls:

                            print("\n=== AI ASSISTANT ===")
                            print(assistant_message.content or "")
                            logger.info("Agent completed successfully")
                            break

                        messages.append(
                            assistant_message.model_dump(
                                exclude_none=True
                            )
                        )

                        # Execute Tool calls
                        for tool_call in assistant_message.tool_calls:

                            tool_name = tool_call.function.name

                            arguments = json.loads(
                                tool_call.function.arguments
                            )

                            print(f"\nLLM yêu cầu gọi Tool: {tool_name}")
                            print(f"Arguments: {arguments}")

                            logger.info(
                                "Tool requested: %s | Arguments: %s",
                                tool_name,
                                arguments
                            )

                            # Find the correct MCP Client
                            session = tool_sessions.get(tool_name)

                            if session is None:
                                result_text = (
                                    f"Tool không tồn tại: {tool_name}"
                                )

                            else:
                                try:
                                    tool_result = await session.call_tool(
                                        tool_name,
                                        arguments=arguments,
                                    )

                                except Exception:
                                    logger.exception(
                                        "MCP Tool execution failed: %s",
                                        tool_name
                                    )

                                    result_text = (
                                        f"Tool {tool_name} gặp lỗi khi thực thi. "
                                        "Vui lòng thử lại hoặc sử dụng Tool khác."
                                    )

                                else:
                                    result_text = "\n".join(
                                        content.text
                                        for content in tool_result.content
                                        if hasattr(content, "text")
                                    )

                                    if tool_result.isError:
                                        logger.error("Tool returned an error: %s", tool_name)
                                        result_text = f"Tool execution error: {result_text}"
                                    else:
                                        logger.info("Tool executed successfully: %s", tool_name)

                                result_text = "\n".join(
                                    content.text
                                    for content in tool_result.content
                                    if hasattr(content, "text")
                                )

                                if tool_result.isError:
                                    result_text = (
                                        f"Tool execution error: "
                                        f"{result_text}"
                                    )
                                    logger.error(
                                        "Tool execution failed: %s",
                                        tool_name
                                    )
                                else:
                                    logger.info(
                                        "Tool executed successfully: %s",
                                        tool_name
                                    )

                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": result_text,
                            })

                    else:
                        print(
                            "\nAgent đã đạt giới hạn "
                            f"{MAX_ITERATIONS} lượt gọi LLM."
                        )


if __name__ == "__main__":
    asyncio.run(main())
