import asyncio

news_list = [
    "OpenAI ra mắt mô hình AI mới",
    "Google phát triển công nghệ AI",
    "Microsoft đầu tư vào trung tâm dữ liệu",
    "NVIDIA giới thiệu chip AI mới",
    "Apple phát triển tính năng AI"
]

async def researcher(queue, researcher_id):
    while True:
        news = await queue.get()

        print(f"Researcher {researcher_id}: Đang phân tích {news}")

        await asyncio.sleep(1)

        print(f"Researcher {researcher_id}: Đã phân tích xong {news}")

        queue.task_done()

async def producer(queue):
    for news in news_list:
        print(f"Producer: Đã thu thập {news}")
        await queue.put(news)

        await asyncio.sleep(0.5)


async def main():
    queue = asyncio.Queue()

    # Tạo Producer
    producer_task = asyncio.create_task(producer(queue))

    # Tạo 3 Researchers
    researcher_tasks = [
        asyncio.create_task(researcher(queue, i))
        for i in range(1, 4)
    ]

    # Chờ Producer hoàn thành
    await producer_task

    # Chờ tất cả tin được xử lý
    await queue.join()

    # Hủy 3 Researchers
    for task in researcher_tasks:
        task.cancel()

    # Chờ Researchers kết thúc
    await asyncio.gather(
        *researcher_tasks,
        return_exceptions=True
    )


asyncio.run(main())