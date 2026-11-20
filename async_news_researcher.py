import asyncio

news_list = [
    "OpenAI ra mắt mô hình AI mới",
    "Google phát triển công nghệ AI",
    "Microsoft đầu tư vào trung tâm dữ liệu",
    "NVIDIA giới thiệu chip AI mới",
    "Apple phát triển tính năng AI"
]

async def researcher(news_queue, result_queue, researcher_id):
    while True:
        news = await news_queue.get()

        try:
            print(f"Researcher {researcher_id}: Đang phân tích {news}")

            await asyncio.sleep(1)

            result = f"{news} - Đã phân tích"

            print(f"Researcher {researcher_id}: Đã phân tích xong {news}")

            await result_queue.put(result)

        finally:
            news_queue.task_done()

async def writer(result_queue):
    report = []
    while True:
        result = await result_queue.get()

        if result is None:
            result_queue.task_done()
            break
        try:
            print(f"Writer: Đang viết {result}")

            await asyncio.sleep(0.5)
            report.append(result)

            print(f"Writer: Hoàn thành {result}")

        finally:
            result_queue.task_done()
    return report

async def producer(news_queue):
    for news in news_list:
        print(f"Producer: Đã thu thập {news}")
        print(f"Producer: Chuẩn bị đưa tin vào Queue")

        await news_queue.put(news)

        print(f"Producer: Đã đưa tin vào Queue")

        await asyncio.sleep(0.1)


async def main():
    news_queue = asyncio.Queue(maxsize=2)
    result_queue = asyncio.Queue(maxsize=2)

    # Khởi chạy Producer
    producer_task = asyncio.create_task(
        producer(news_queue)
    )

    # Khởi chạy 3 Researchers
    researcher_tasks = [
        asyncio.create_task(
            researcher(news_queue, result_queue, i)
        )
        for i in range(1, 2)
    ]

    # Khởi chạy Writer
    writer_task = asyncio.create_task(
        writer(result_queue)
    )

    # Chờ Producer hoàn thành
    await producer_task

    # Chờ tất cả tin được Researchers phân tích
    await news_queue.join()

    # Dừng Researchers
    for task in researcher_tasks:
        task.cancel()

    await asyncio.gather(
        *researcher_tasks,
        return_exceptions=True
    )

    # Gửi tín hiệu kết thúc cho Writer
    await result_queue.put(None)

    # Chờ Writer xử lý hết kết quả và kết thúc
    await result_queue.join()
    await writer_task

    # Lấy báo cáo
    report = writer_task.result()

    print("\n===== BÁO CÁO CUỐI CÙNG =====")

    for item in report:
        print(item)


asyncio.run(main())