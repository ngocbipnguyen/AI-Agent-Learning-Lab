from crewai import Agent
from crewai import Agent, Task, Crew, Process

from dotenv import load_dotenv

load_dotenv(override=True)
researcher = Agent(
    role="Technology Researcher",
    goal="Tìm kiếm và thu thập thông tin công nghệ chính xác.",
    backstory="Bạn là một chuyên gia nghiên cứu công nghệ, có khả năng phân tích và tổng hợp thông tin.",
    llm="openai/gpt-4o-mini"
)

print(researcher.role)

research_task = Task(
    description="Nghiên cứu 3 xu hướng AI nổi bật trong năm 2026.",
    expected_output="Báo cáo gồm 3 xu hướng AI, mô tả ngắn gọn từng xu hướng.",
    agent=researcher
)

print(research_task.description)

research_crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

print("Crew đã được khởi tạo thành công!")

result = research_crew.kickoff()

print("\n=== KẾT QUẢ NGHIÊN CỨU ===")
print(result)