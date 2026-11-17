import streamlit as st

st.title("My First Streamlit App")
st.header("Thông tin người dùng")
st.subheader("Nhập thông tin cá nhân")
st.write("Xin chào! Đây là ứng dụng Web đầu tiên của tôi.")

name = st.text_input("Tên của bạn là gì?")

if st.button("Gửi"):
    if name:
        st.success(f"Xin chào {name}!")
    else:
        st.warning("Bạn chưa nhập tên!")

topic = st.selectbox(
    "Bạn quan tâm đến lĩnh vực nào?",
    ["AI", "Cybersecurity", "Cloud Computing", "Robotics"]
)

st.write(f"Lĩnh vực bạn chọn: {topic}")


topics = st.multiselect(
    "Bạn quan tâm đến những lĩnh vực nào?",
    ["AI", "Cybersecurity", "Cloud Computing", "Robotics"]
)

st.write("Các lĩnh vực bạn đã chọn:", topics)

number = st.slider(
    "Bạn muốn tìm kiếm bao nhiêu tin tức?",
    min_value=1,
    max_value=20,
    value=5
)

st.write(f"Số tin tức bạn chọn: {number}")

analysis = st.checkbox("Tôi muốn xem thêm phần phân tích")

if analysis:
    st.write("Bạn đã chọn xem phần phân tích!")
else:
    st.write("Bạn chỉ muốn xem tin tức.")

col1, col2 = st.columns(2)

with col1:
    st.header("Tin tức")
    st.write("Tổng hợp tin tức công nghệ.")

with col2:
    st.header("Phân tích")
    st.write("Phân tích các xu hướng công nghệ.")

col1, col2 = st.columns(2)

with col1:
    st.metric("Tổng số tin tức", 25)

with col2:
    st.metric("Tin tức về AI", 12)


st.info("Hệ thống đang thu thập tin tức.")

st.success("Thu thập tin tức thành công!")

st.error("Không thể kết nối đến nguồn tin tức.")


import pandas as pd

data = {
    "Tiêu đề": [
        "OpenAI ra mắt mô hình AI mới",
        "Google phát triển công nghệ AI",
        "NVIDIA giới thiệu chip mới"
    ],
    "Lĩnh vực": [
        "AI",
        "AI",
        "Hardware"
    ],
    "Nguồn": [
        "OpenAI",
        "Google",
        "NVIDIA"
    ]
}

df = pd.DataFrame(data)

st.subheader("Danh sách tin tức")
st.dataframe(df)

chart_data = {
    "Lĩnh vực": ["AI", "Cybersecurity", "Cloud", "Hardware"],
    "Số lượng tin tức": [12, 8, 5, 10]
}

chart_df = pd.DataFrame(chart_data)

st.subheader("Thống kê tin tức theo lĩnh vực")

st.bar_chart(
    chart_df,
    x="Lĩnh vực",
    y="Số lượng tin tức"
)

line_data = {
    "Ngày": ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6"],
    "Số tin tức": [5, 8, 6, 12, 15]
}

line_df = pd.DataFrame(line_data)

st.subheader("Số lượng tin tức theo ngày")

st.line_chart(
    line_df,
    x="Ngày",
    y="Số tin tức"
)

st.sidebar.title("Bộ lọc tin tức")

selected_topic = st.sidebar.selectbox(
    "Chọn lĩnh vực",
    ["Tất cả", "AI", "Cybersecurity", "Cloud", "Hardware"]
)

st.sidebar.write(f"Lĩnh vực đang chọn: {selected_topic}")

import pandas as pd

csv = df.to_csv(index=False).encode("utf-8-sig")

st.subheader("Tải dữ liệu tin tức")

st.download_button(
    label="Tải danh sách tin tức",
    data=csv,
    file_name="technology_news.csv",
    mime="text/csv"
)

report = """
BÁO CÁO TIN TỨC CÔNG NGHỆ

1. OpenAI ra mắt mô hình AI mới
   Lĩnh vực: AI
   Nguồn: OpenAI

2. Google phát triển công nghệ AI
   Lĩnh vực: AI
   Nguồn: Google

3. NVIDIA giới thiệu chip mới
   Lĩnh vực: Hardware
   Nguồn: NVIDIA
"""

st.download_button(
    label="Tải báo cáo TXT",
    data=report,
    file_name="technology_news_report.txt",
    mime="text/plain"
)

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Tăng bộ đếm"):
    st.session_state.count += 1

st.write(f"Bạn đã nhấn nút {st.session_state.count} lần.")

if st.button("Reset"):
    st.session_state.count = 0