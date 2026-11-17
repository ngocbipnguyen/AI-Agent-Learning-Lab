
import streamlit as st
import pandas as pd
from news import load_news_data, filter_news, show_metrics, show_chart, download_news
def load_news_data():
    data = {
        "Tiêu đề": [
            "OpenAI ra mắt mô hình AI mới",
            "Google phát triển công nghệ AI",
            "NVIDIA giới thiệu chip mới",
            "Microsoft tăng cường bảo mật",
            "AWS mở rộng dịch vụ Cloud",
            "OpenAI cải tiến AI Agent"
        ],
        "Lĩnh vực": [
            "AI",
            "AI",
            "Hardware",
            "Cybersecurity",
            "Cloud",
            "AI"
        ],
        "Nguồn": [
            "OpenAI",
            "Google",
            "NVIDIA",
            "Microsoft",
            "AWS",
            "OpenAI"
        ]
    }

    return pd.DataFrame(data)






def main():
    st.title("Technology News Dashboard")

    st.sidebar.title("Bộ lọc tin tức")

    topic = st.sidebar.selectbox(
        "Chọn lĩnh vực công nghệ",
        ["Tất cả", "AI", "Cybersecurity", "Cloud", "Hardware"]
    )

    number_of_news = st.sidebar.slider(
        "Số lượng tin tức",
        min_value=1,
        max_value=20,
        value=5
    )

    st.write(f"Lĩnh vực đang chọn: {topic}")
    st.write(f"Số lượng tin tức: {number_of_news}")

    df = load_news_data()

    filtered_df = filter_news(df, topic, number_of_news)

    st.subheader("Danh sách tin tức")
    st.dataframe(filtered_df, use_container_width=True)

    show_metrics(filtered_df)

    show_chart(filtered_df)

    download_news(filtered_df)


if __name__ == "__main__":
    main()
