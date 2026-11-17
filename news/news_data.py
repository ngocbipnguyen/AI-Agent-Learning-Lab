import pandas as pd


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