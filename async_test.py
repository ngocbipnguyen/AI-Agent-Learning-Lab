# # import asyncio
# # import httpx

# # import asyncio
# # import httpx
# # import time
# # async def fetch_data(client, post_id):
# #     response = await client.get(
# #         f"https://jsonplaceholder.typicode.com/posts/{post_id}"
# #     )

# #     response.raise_for_status()
# #     return response.json()

# # async def main():
# #     start = time.perf_counter()
# #     async with httpx.AsyncClient() as client:
# #         results = await asyncio.gather(
# #             fetch_data(client, 1),
# #             fetch_data(client, 2),
# #             fetch_data(client, 3)
# #         )

# #         print(f"Tổng số bài viết: {len(results)}")

# #     end = time.perf_counter()
# #     print(f"\nThời gian thực thi: {end - start:.2f} giây")

# # asyncio.run(main())


# # import asyncio

# # semaphore = asyncio.Semaphore(5)

# # async def task(name):
# #     async with semaphore:
# #         print(f"Bắt đầu {name}")

# #         await asyncio.sleep(2)

# #         print(f"Hoàn thành {name}")

# # async def main():
# #     await asyncio.gather(
# #         *(task(f"Task {i}") for i in range(1, 11))
# #     )

# # asyncio.run(main())



# # import asyncio
# # import httpx

# # semaphore = asyncio.Semaphore(3)

# # async def fetch_data(client, post_id):
# #     async with semaphore:
# #         print(f"Bắt đầu request {post_id}")

# #         response = await client.get(
# #             f"https://jsonplaceholder.typicode.com/posts/{post_id}"
# #         )
# #         response.raise_for_status()

# #         data = response.json()

# #         print(f"Hoàn thành request {post_id}")
# #         return data

# # async def main():
# #     async with httpx.AsyncClient() as client:
# #         results = await asyncio.gather(
# #             *(fetch_data(client, i) for i in range(1, 11))
# #         )

# #     print(f"\nTổng số kết quả: {len(results)}")

# # asyncio.run(main())


# # import asyncio
# # import httpx
# # import time

# # # semaphore = asyncio.Semaphore(3)

# # async def fetch_data(client, post_id):
# #     # async with semaphore:
# #     #     response = await client.get(
# #     #         f"https://jsonplaceholder.typicode.com/posts/{post_id}"
# #     #     )
# #     #     response.raise_for_status()
# #     #     return response.json()
# #     async def fetch_data(client, post_id):
# #         response = await client.get(
# #             f"https://jsonplaceholder.typicode.com/posts/{post_id}"
# #         )
# #         response.raise_for_status()
# #         return response.json()

# # async def main():
# #     start = time.perf_counter()

# #     async with httpx.AsyncClient() as client:
# #         results = await asyncio.gather(
# #             *(fetch_data(client, i) for i in range(1, 11))
# #         )

# #     elapsed = time.perf_counter() - start

# #     print(f"Tổng số kết quả: {len(results)}")
# #     print(f"Thời gian thực thi: {elapsed:.2f} giây")

# # asyncio.run(main())


# # import asyncio

# # async def long_task():
# #     try:
# #         print("Task bắt đầu")

# #         await asyncio.sleep(10)

# #         print("Task hoàn thành")

# #     except asyncio.CancelledError:
# #         print("Task đã bị hủy")
# #         raise

# # async def main():
# #     task = asyncio.create_task(long_task())

# #     await asyncio.sleep(2)

# #     task.cancel()

# #     try:
# #         await task
# #     except asyncio.CancelledError:
# #         print("Main: Đã xử lý việc hủy Task")
# #     print("Task done:", task.done())
# #     print("Task cancelled:", task.cancelled())

# #     if not task.cancelled():
# #         print("Task result:", task.result())
# #     else:
# #         print("Không thể lấy kết quả vì Task đã bị hủy")



# # asyncio.run(main())


# import asyncio

# async def worker(name, duration):
#     try:
#         print(f"{name}: Bắt đầu")

#         await asyncio.sleep(duration)

#         print(f"{name}: Hoàn thành")
#         return f"{name}: Kết quả thành công"

#     except asyncio.CancelledError:
#         print(f"{name}: Đã bị hủy")
#         raise

# async def main():
#     task1 = asyncio.create_task(worker("Task 1", 3))
#     task2 = asyncio.create_task(worker("Task 2", 5))
#     task3 = asyncio.create_task(worker("Task 3", 7))

#     await asyncio.sleep(2)

#     print("\nĐang hủy Task 2...")
#     task2.cancel()

#     results = await asyncio.gather(
#         task1, task2, task3,
#         return_exceptions=True
#     )

#     print("\n=== KẾT QUẢ ===")

#     for i, result in enumerate(results, start=1):
#         if isinstance(result, BaseException):
#             print(f"Task {i}: {type(result).__name__}")
#         else:
#             print(f"Task {i}: {result}")

#     print("\n=== TRẠNG THÁI TASK ===")
#     print("Task 1 done:", task1.done())
#     print("Task 2 done:", task2.done())
#     print("Task 3 done:", task3.done())

#     print("Task 1 cancelled:", task1.cancelled())
#     print("Task 2 cancelled:", task2.cancelled())
#     print("Task 3 cancelled:", task3.cancelled())

# asyncio.run(main())



import asyncio

async def worker(name, duration):
    print(f"{name}: Bắt đầu")

    await asyncio.sleep(duration)

    if name == "Task 2":
        raise ValueError("Task 2 gặp lỗi")
    print(f"{name}: Hoàn thành")
    return f"{name}: Kết quả thành công"

async def main():
    tasks = [
        asyncio.create_task(worker("Task 1", 2)),
        asyncio.create_task(worker("Task 2", 4)),
        asyncio.create_task(worker("Task 3", 6))
    ]

    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_EXCEPTION
    )

    print("\n=== KẾT QUẢ ===")
    print("Số Task hoàn thành:", len(done))
    print("Số Task đang chờ:", len(pending))

    for task in done:
        try:
            print(task.result())
        except Exception as e:
            print(f"Task gặp lỗi: {e}")
    if pending:
        print("\nĐang chờ các Task còn lại...")

        results = await asyncio.gather(
            *pending,
            return_exceptions=True
        )

        for result in results:
            if isinstance(result, Exception):
                print("Task gặp lỗi:", result)
            else:
                print("Kết quả:", result)

asyncio.run(main())


