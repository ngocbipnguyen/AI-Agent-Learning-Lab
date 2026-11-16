from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from tools.crewai_search_tool import technology_news_search
load_dotenv(override=True)

# Agent 1: Researcher
researcher = Agent(
    role="Technology News Researcher",
    goal="Thu thập những tin tức công nghệ mới nhất và có giá trị.",
    backstory="Bạn là chuyên gia nghiên cứu tin tức công nghệ, có khả năng tìm kiếm và chọn lọc thông tin đáng tin cậy.",
    llm="openai/gpt-4o-mini",
    tools=[technology_news_search],
    allow_delegation=True,
    verbose=True
)

print("Researcher Tools:", researcher.tools)
# Agent 2: Analyst
analyst = Agent(
    role="Technology News Analyst",
    goal="Phân tích xu hướng, tác động và ý nghĩa của các tin tức công nghệ.",
    backstory="Bạn là chuyên gia phân tích công nghệ, có khả năng đánh giá xu hướng thị trường, nhận diện cơ hội và rủi ro.",
    llm="openai/gpt-4o-mini",
    allow_delegation=True,
    verbose=True
)

# Agent 3: Writer
writer = Agent(
    role="Technology Report Writer",
    goal="Viết báo cáo công nghệ rõ ràng, logic và chuyên nghiệp.",
    backstory="Bạn là chuyên gia viết báo cáo công nghệ, có khả năng chuyển hóa thông tin nghiên cứu và phân tích thành nội dung dễ hiểu.",
    llm="openai/gpt-4o-mini",
    allow_delegation=True,
    verbose=True
)

# Manager Agent
manager = Agent(
    role="Technology Project Manager",
    goal="Điều phối các Agent để hoàn thành báo cáo công nghệ chính xác và chuyên nghiệp.",
    backstory="Bạn là người quản lý một nhóm chuyên gia công nghệ, có khả năng phân công và giám sát công việc.",
    llm="openai/gpt-4o-mini",
    allow_delegation=True,
    verbose=True
)

# Task 1: Research Task
research_task = Task(
    description="""
    Thu thập 5 tin tức công nghệ nổi bật trong tuần gần nhất
    bằng công cụ Technology News Search.

    Ưu tiên các chủ đề:
    - Trí tuệ nhân tạo (AI).
    - Các mô hình và sản phẩm công nghệ mới.
    - Doanh nghiệp công nghệ.
    - An ninh mạng và bảo mật.
    - Thị trường và xu hướng công nghệ.

    Với mỗi tin tức, hãy cung cấp:

    1. Tiêu đề bài viết.
    2. Tên nguồn tin.
    3. Ngày xuất bản.
    4. URL bài viết gốc.
    5. Tóm tắt nội dung chính.
    6. Những dữ kiện hoặc số liệu đáng chú ý.

    Yêu cầu bắt buộc:
    - Chỉ chọn bài viết thực sự liên quan đến công nghệ.
    - Ưu tiên bài báo có ngày xuất bản rõ ràng trong tuần gần nhất.
    - Không chọn hồ sơ công ty hoặc trang giới thiệu sản phẩm
      thay cho một bài báo.
    - Không tự tạo tiêu đề, ngày tháng hoặc số liệu.
    - Không suy diễn nội dung vượt quá thông tin nguồn cung cấp.
    - Nếu không tìm đủ 5 tin đáng tin cậy, hãy báo số lượng
      thực tế thay vì tự tạo thêm tin.
    - Với mỗi số liệu, phải ghi rõ nguồn cung cấp số liệu.
    - Không được tự suy đoán hoặc tạo ra số liệu.
    - Nếu không tìm thấy bằng chứng, ghi rõ: "Chưa xác minh được".
    - Phân biệt rõ thông tin trong bài báo và nhận định của tác giả.
    """,
    expected_output="""
    Danh sách tối đa 5 tin tức công nghệ.
    Mỗi tin gồm tiêu đề, nguồn, ngày xuất bản, URL,
    nội dung tóm tắt và dữ kiện đáng chú ý.
    """,
    agent=researcher
)


# Task 2: Analysis Task

# Task 2: Analysis Task
analysis_task = Task(
    description="""
    Phân tích 5 tin tức công nghệ do Researcher thu thập.

    Với mỗi tin tức, hãy thực hiện:

    1. Xác định xu hướng công nghệ được phản ánh.
    2. Phân tích tác động đối với doanh nghiệp, người dùng
       và thị trường công nghệ.
    3. Chỉ ra cơ hội phát triển.
    4. Chỉ ra rủi ro và thách thức.
    5. Đưa ra dẫn chứng cụ thể từ nội dung tin tức.

    Yêu cầu:
    - Chỉ sử dụng thông tin có trong kết quả nghiên cứu.
    - Không tự tạo số liệu hoặc sự kiện.
    - Nếu thiếu dữ liệu, hãy ghi rõ chưa đủ thông tin.
    - Phân biệt rõ dữ kiện và nhận định phân tích.
    - Với mỗi số liệu quan trọng, phải kiểm tra xem Researcher có cung cấp nguồn bằng chứng hay không.
    - Nếu không có bằng chứng, ghi rõ "Chưa xác minh được".
    - Không biến nhận định của tác giả thành dữ kiện đã được chứng minh.
    - Liên kết từng nhận định phân tích với tin tức và nguồn tương ứng.
    """,
    expected_output="""
    Báo cáo phân tích 5 tin tức công nghệ.

    Mỗi tin phải có:
    - Xu hướng công nghệ.
    - Tác động đối với doanh nghiệp, người dùng và thị trường.
    - Cơ hội phát triển.
    - Rủi ro và thách thức.
    - Dẫn chứng từ nội dung tin tức.
    - Nguồn tin và URL tương ứng với từng dẫn chứng.
    - Phân biệt rõ dữ kiện đã được nguồn cung cấp và nhận định phân tích.
    - Trạng thái xác minh đối với các số liệu quan trọng.
    - Ghi rõ "Chưa xác minh được" nếu không có bằng chứng.
    """,
    agent=analyst,
    context=[research_task]
)

# Task 3: Writing Task

# Task 3: Writing Task
writing_task = Task(
    description="""
    Dựa trên kết quả nghiên cứu của Researcher và phân tích
    của Analyst, hãy viết báo cáo tổng hợp về 5 tin tức
    công nghệ nổi bật.

    Cấu trúc báo cáo:

    1. Tiêu đề báo cáo.
    2. Tổng quan 5 tin tức.
    3. Phân tích các xu hướng công nghệ nổi bật.
    4. Tác động đối với doanh nghiệp và người dùng.
    5. Cơ hội và rủi ro.
    6. Kết luận và nhận định tổng thể.
    7. Danh sách nguồn tham khảo kèm URL.

    Yêu cầu:
    - Nội dung rõ ràng, logic và chuyên nghiệp.
    - Sử dụng dẫn chứng từ kết quả nghiên cứu.
    - Không tự tạo số liệu hoặc thông tin.
    - Không đưa ra kết luận vượt quá bằng chứng.
    - Nếu thông tin chưa được xác minh, phải ghi rõ "Chưa xác minh được".
    - Giữ nguyên trạng thái xác minh của các dữ kiện từ Researcher và Analyst.
    - Mỗi số liệu quan trọng phải đi kèm nguồn bằng chứng tương ứng.
    - Không sử dụng nhận định phân tích như một dữ kiện đã được chứng minh.
    - Không tự tạo hoặc thay đổi URL nguồn tham khảo.
    - Nếu Researcher hoặc Analyst không cung cấp đủ bằng chứng,
      phải nêu rõ giới hạn thông tin trong báo cáo.
    """,
    expected_output="""
    Một báo cáo công nghệ chuyên nghiệp bằng tiếng Việt,
    có đầy đủ 7 phần theo cấu trúc yêu cầu.

    Báo cáo phải đảm bảo:
    - Mỗi tin tức có nguồn tham khảo và URL tương ứng.
    - Các số liệu quan trọng có dẫn chứng từ nguồn.
    - Phân biệt rõ dữ kiện và nhận định phân tích.
    - Ghi rõ "Chưa xác minh được" đối với thông tin thiếu bằng chứng.
    - Giữ nguyên trạng thái xác minh của thông tin từ Researcher và Analyst.
    - Nêu rõ giới hạn thông tin khi chưa đủ bằng chứng.
    - Không tự tạo dữ kiện, số liệu hoặc URL.
    """,
    agent=writer,
    context=[research_task, analysis_task]
)


# Crew: Điều phối 3 Agent
technology_crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.hierarchical,
    manager_agent=manager,
    verbose=True
)

# Chạy Crew
if __name__ == "__main__":
    result = technology_crew.kickoff()

    print("\n=== BÁO CÁO CÔNG NGHỆ ===")
    print(result)