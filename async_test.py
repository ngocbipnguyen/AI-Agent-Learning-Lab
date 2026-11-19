# # # # import asyncio
# # # # import httpx

# # # # import asyncio
# # # # import httpx
# # # # import time
# # # # async def fetch_data(client, post_id):
# # # #     response = await client.get(
# # # #         f"https://jsonplaceholder.typicode.com/posts/{post_id}"
# # # #     )

# # # #     response.raise_for_status()
# # # #     return response.json()

# # # # async def main():
# # # #     start = time.perf_counter()
# # # #     async with httpx.AsyncClient() as client:
# # # #         results = await asyncio.gather(
# # # #             fetch_data(client, 1),
# # # #             fetch_data(client, 2),
# # # #             fetch_data(client, 3)
# # # #         )

# # # #         print(f"Tổng số bài viết: {len(results)}")

# # # #     end = time.perf_counter()
# # # #     print(f"\nThời gian thực thi: {end - start:.2f} giây")

# # # # asyncio.run(main())


# # # # import asyncio

# # # # semaphore = asyncio.Semaphore(5)

# # # # async def task(name):
# # # #     async with semaphore:
# # # #         print(f"Bắt đầu {name}")

# # # #         await asyncio.sleep(2)

# # # #         print(f"Hoàn thành {name}")

# # # # async def main():
# # # #     await asyncio.gather(
# # # #         *(task(f"Task {i}") for i in range(1, 11))
# # # #     )

# # # # asyncio.run(main())



# # # # import asyncio
# # # # import httpx

# # # # semaphore = asyncio.Semaphore(3)

# # # # async def fetch_data(client, post_id):
# # # #     async with semaphore:
# # # #         print(f"Bắt đầu request {post_id}")

# # # #         response = await client.get(
# # # #             f"https://jsonplaceholder.typicode.com/posts/{post_id}"
# # # #         )
# # # #         response.raise_for_status()

# # # #         data = response.json()

# # # #         print(f"Hoàn thành request {post_id}")
# # # #         return data

# # # # async def main():
# # # #     async with httpx.AsyncClient() as client:
# # # #         results = await asyncio.gather(
# # # #             *(fetch_data(client, i) for i in range(1, 11))
# # # #         )

# # # #     print(f"\nTổng số kết quả: {len(results)}")

# # # # asyncio.run(main())


# # # # import asyncio
# # # # import httpx
# # # # import time

# # # # # semaphore = asyncio.Semaphore(3)

# # # # async def fetch_data(client, post_id):
# # # #     # async with semaphore:
# # # #     #     response = await client.get(
# # # #     #         f"https://jsonplaceholder.typicode.com/posts/{post_id}"
# # # #     #     )
# # # #     #     response.raise_for_status()
# # # #     #     return response.json()
# # # #     async def fetch_data(client, post_id):
# # # #         response = await client.get(
# # # #             f"https://jsonplaceholder.typicode.com/posts/{post_id}"
# # # #         )
# # # #         response.raise_for_status()
# # # #         return response.json()

# # # # async def main():
# # # #     start = time.perf_counter()

# # # #     async with httpx.AsyncClient() as client:
# # # #         results = await asyncio.gather(
# # # #             *(fetch_data(client, i) for i in range(1, 11))
# # # #         )

# # # #     elapsed = time.perf_counter() - start

# # # #     print(f"Tổng số kết quả: {len(results)}")
# # # #     print(f"Thời gian thực thi: {elapsed:.2f} giây")

# # # # asyncio.run(main())


# # # # import asyncio

# # # # async def long_task():
# # # #     try:
# # # #         print("Task bắt đầu")

# # # #         await asyncio.sleep(10)

# # # #         print("Task hoàn thành")

# # # #     except asyncio.CancelledError:
# # # #         print("Task đã bị hủy")
# # # #         raise

# # # # async def main():
# # # #     task = asyncio.create_task(long_task())

# # # #     await asyncio.sleep(2)

# # # #     task.cancel()

# # # #     try:
# # # #         await task
# # # #     except asyncio.CancelledError:
# # # #         print("Main: Đã xử lý việc hủy Task")
# # # #     print("Task done:", task.done())
# # # #     print("Task cancelled:", task.cancelled())

# # # #     if not task.cancelled():
# # # #         print("Task result:", task.result())
# # # #     else:
# # # #         print("Không thể lấy kết quả vì Task đã bị hủy")



# # # # asyncio.run(main())


# # # import asyncio

# # # async def worker(name, duration):
# # #     try:
# # #         print(f"{name}: Bắt đầu")

# # #         await asyncio.sleep(duration)

# # #         print(f"{name}: Hoàn thành")
# # #         return f"{name}: Kết quả thành công"

# # #     except asyncio.CancelledError:
# # #         print(f"{name}: Đã bị hủy")
# # #         raise

# # # async def main():
# # #     task1 = asyncio.create_task(worker("Task 1", 3))
# # #     task2 = asyncio.create_task(worker("Task 2", 5))
# # #     task3 = asyncio.create_task(worker("Task 3", 7))

# # #     await asyncio.sleep(2)

# # #     print("\nĐang hủy Task 2...")
# # #     task2.cancel()

# # #     results = await asyncio.gather(
# # #         task1, task2, task3,
# # #         return_exceptions=True
# # #     )

# # #     print("\n=== KẾT QUẢ ===")

# # #     for i, result in enumerate(results, start=1):
# # #         if isinstance(result, BaseException):
# # #             print(f"Task {i}: {type(result).__name__}")
# # #         else:
# # #             print(f"Task {i}: {result}")

# # #     print("\n=== TRẠNG THÁI TASK ===")
# # #     print("Task 1 done:", task1.done())
# # #     print("Task 2 done:", task2.done())
# # #     print("Task 3 done:", task3.done())

# # #     print("Task 1 cancelled:", task1.cancelled())
# # #     print("Task 2 cancelled:", task2.cancelled())
# # #     print("Task 3 cancelled:", task3.cancelled())

# # # asyncio.run(main())



# # # import asyncio

# # # async def worker(name, duration):
# # #     print(f"{name}: Bắt đầu")

# # #     await asyncio.sleep(duration)

# # #     if name == "Task 2":
# # #         raise ValueError("Task 2 gặp lỗi")
# # #     print(f"{name}: Hoàn thành")
# # #     return f"{name}: Kết quả thành công"

# # # async def main():
# # #     tasks = [
# # #         asyncio.create_task(worker("Task 1", 2)),
# # #         asyncio.create_task(worker("Task 2", 4)),
# # #         asyncio.create_task(worker("Task 3", 6))
# # #     ]

# # #     done, pending = await asyncio.wait(
# # #         tasks,
# # #         return_when=asyncio.FIRST_EXCEPTION
# # #     )

# # #     print("\n=== KẾT QUẢ ===")
# # #     print("Số Task hoàn thành:", len(done))
# # #     print("Số Task đang chờ:", len(pending))

# # #     for task in done:
# # #         try:
# # #             print(task.result())
# # #         except Exception as e:
# # #             print(f"Task gặp lỗi: {e}")
# # #     if pending:
# # #         print("\nĐang chờ các Task còn lại...")

# # #         results = await asyncio.gather(
# # #             *pending,
# # #             return_exceptions=True
# # #         )

# # #         for result in results:
# # #             if isinstance(result, Exception):
# # #                 print("Task gặp lỗi:", result)
# # #             else:
# # #                 print("Kết quả:", result)

# # # asyncio.run(main())


# # # import asyncio

# # # async def main():
# # #     queue = asyncio.Queue()

# # #     await queue.put("Tin tức AI")
# # #     await queue.put("Tin tức Python")
# # #     await queue.put("Tin tức Robot")

# # #     print("Số phần tử trong Queue:", queue.qsize())

# # #     while not queue.empty():
# # #         item = await queue.get()
# # #         print("Đã lấy:", item)

# # #     print("Queue còn:", queue.qsize())

# # # asyncio.run(main())


# # # import asyncio

# # # async def producer(queue):
# # #     for i in range(1, 6):
# # #         news = f"Tin tức công nghệ {i}"

# # #         await queue.put(news)
# # #         print(f"Producer thêm: {news}")
# # #         print(f"Queue hiện có: {queue.qsize()} phần tử")

# # #         await asyncio.sleep(1)

# # # async def consumer(queue):
# # #     while True:
# # #         news = await queue.get()

# # #         print(f"Consumer xử lý: {news}")

# # #         await asyncio.sleep(2)

# # #         queue.task_done()

# # # async def main():
# # #     queue = asyncio.Queue(maxsize=2)

# # #     producer_task = asyncio.create_task(producer(queue))
# # #     consumer_task = asyncio.create_task(consumer(queue))

# # #     await producer_task
# # #     await queue.join()

# # #     consumer_task.cancel()

# # #     try:
# # #         await consumer_task
# # #     except asyncio.CancelledError:
# # #         print("Consumer đã dừng")

# # # asyncio.run(main())



# # # import asyncio

# # # async def producer(queue):
# # #     for i in range(1, 11):
# # #         news = f"Tin tức công nghệ {i}"

# # #         await queue.put(news)
# # #         print(f"Producer thêm: {news}")

# # #         await asyncio.sleep(0.5)

# # # async def consumer(queue, name):
# # #     while True:
# # #         news = await queue.get()

# # #         try:
# # #             print(f"{name} đang xử lý: {news}")

# # #             await asyncio.sleep(2)

# # #             print(f"{name} hoàn thành: {news}")

# # #         finally:
# # #             queue.task_done()

# # # async def main():
# # #     queue = asyncio.Queue(maxsize=3)

# # #     producer_task = asyncio.create_task(producer(queue))

# # #     consumers = [
# # #         asyncio.create_task(consumer(queue, f"Consumer {i}"))
# # #         for i in range(1, 4)
# # #     ]

# # #     await producer_task
# # #     await queue.join()

# # #     for task in consumers:
# # #         task.cancel()

# # #     await asyncio.gather(*consumers, return_exceptions=True)

# # #     print("\nTất cả tin tức đã được xử lý!")

# # # asyncio.run(main())


# # # import asyncio

# # # async def producer(news_queue):
# # #     for i in range(1, 6):
# # #         news = f"Tin tức công nghệ {i}"

# # #         await news_queue.put(news)
# # #         print(f"Producer: Đã thu thập {news}")

# # #         await asyncio.sleep(0.5)

# # #     for _ in range(2):
# # #         await news_queue.put(None)


# # # async def researcher(news_queue, result_queue, researcher_id):
# # #     while True:
# # #         news = await news_queue.get()

# # #         try:
# # #             if news is None:
# # #                 break

# # #             print(f"Researcher {researcher_id}: Đang phân tích {news}")

# # #             await asyncio.sleep(1)

# # #             result = f"{news} - Đã phân tích"

# # #             await result_queue.put(result)

# # #         finally:
# # #             news_queue.task_done()


# # # async def writer(result_queue):
# # #     while True:
# # #         result = await result_queue.get()

# # #         try:
# # #             if result is None:
# # #                 break

# # #             print(f"Writer: Đang viết {result}")

# # #             await asyncio.sleep(0.5)

# # #         finally:
# # #             result_queue.task_done()


# # # async def main():
# # #     news_queue = asyncio.Queue(maxsize=3)
# # #     result_queue = asyncio.Queue(maxsize=3)

# # #     producer_task = asyncio.create_task(
# # #         producer(news_queue)
# # #     )

# # #     researcher_tasks = [
# # #         asyncio.create_task(
# # #             researcher(news_queue, result_queue, researcher_id)
# # #         )
# # #         for researcher_id in range(1, 3)
# # #     ]

# # #     writer_task = asyncio.create_task(
# # #         writer(result_queue)
# # #     )

# # #     await producer_task
# # #     await news_queue.join()
# # #     await asyncio.gather(*researcher_tasks)

# # #     await result_queue.put(None)

# # #     await result_queue.join()
# # #     await writer_task

# # #     print("\nPipeline hoàn thành!")


# # # asyncio.run(main())

# # # import asyncio


# # # async def worker(name, delay):
# # #     print(f"{name}: Bắt đầu")
# # #     if name == "Task 2":
# # #         raise ValueError("Task 2 gặp lỗi!")
# # #     if name == "Task 3":
# # #         raise TypeError("Task 3 gặp lỗi!")
# # #     await asyncio.sleep(delay)

# # #     print(f"{name}: Hoàn thành")


# # # async def main():
# # #     try:
# # #         async with asyncio.TaskGroup() as tg:
# # #             tg.create_task(worker("Task 1", 2))
# # #             tg.create_task(worker("Task 2", 1))
# # #             tg.create_task(worker("Task 3", 3))

# # #     except* ValueError as e:
# # #         print(f"\nĐã xử lý lỗi ValueError: {e.exceptions}")

# # #     except* TypeError as e:
# # #         print(f"\nĐã xử lý lỗi TypeError: {e.exceptions}")

# # #     print("\nChương trình tiếp tục!")


# # # asyncio.run(main())


# # # import asyncio


# # # async def worker(name, delay):
# # #     print(f"{name}: Bắt đầu")

# # #     await asyncio.sleep(delay)

# # #     if name == "Task 2":
# # #         raise ValueError("Task 2 gặp lỗi!")

# # #     print(f"{name}: Hoàn thành")

# # #     return f"Kết quả {name}"


# # # async def main():
# # #     try:
# # #         results = await asyncio.gather(
# # #             worker("Task 1", 2),
# # #             worker("Task 2", 1),
# # #             worker("Task 3", 3),
# # #             return_exceptions=True
# # #         )

# # #         for result in results:
# # #             if isinstance(result, Exception):
# # #                 print(f"Task gặp lỗi: {result}")
# # #             else:
# # #                 print(f"Task thành công: {result}")

# # #         print(results)

# # #     except ValueError as e:
# # #         print(f"\nĐã bắt lỗi: {e}")

# # #     await asyncio.sleep(3)

# # #     print("\nChương trình kết thúc!")


# # # asyncio.run(main())


# # # import asyncio


# # # async def worker(name, delay):
# # #     print(f"{name}: Bắt đầu")

# # #     await asyncio.sleep(delay)

# # #     print(f"{name}: Hoàn thành")

# # #     return f"Kết quả {name}"


# # # async def main():
# # #     async with asyncio.TaskGroup() as tg:
# # #         task1 = tg.create_task(worker("Task 1", 2))
# # #         task2 = tg.create_task(worker("Task 2", 1))
# # #         task3 = tg.create_task(worker("Task 3", 3))

# # #     print("\n=== KẾT QUẢ ===")

# # #     print(task1.result())
# # #     print(task2.result())
# # #     print(task3.result())


# # # asyncio.run(main())

# # import asyncio
# # from unittest import result
# # import random

# # async def fetch_data(attempt):
# #     print("Đang gọi API...")

# #     if attempt < 7:
# #         raise ConnectionError("Không thể kết nối API!")

# #     return "Dữ liệu công nghệ đã được tải!"


# # async def main():
# #     for attempt in range(1, 7):
# #         try:
# #             result = await fetch_data(attempt)
# #             print(result)
# #             print("Lấy dữ liệu thành công!")
# #             break

# #         except ConnectionError as e:
# #             print(f"Lần thử {attempt} thất bại: {e}")

# #             if attempt == 6:
# #                 print("Đã hết số lần thử!")
# #             else:
# #                 delay = random.uniform(
# #                     0,
# #                     min(2 ** (attempt - 1), 5)
# #                 )

# #                 print(f"Chờ {delay} giây trước khi thử lại...")

# #                 await asyncio.sleep(delay)


# # asyncio.run(main())


# import asyncio
# import random


# class AuthenticationError(Exception):
#     pass


# async def fetch_data(error_type):
#     print("Đang gọi API...")

#     if error_type == "connection":
#         if not hasattr(fetch_data, "attempts"):
#             fetch_data.attempts = 0

#         fetch_data.attempts += 1

#         if fetch_data.attempts < 3:
#             raise ConnectionError("Lỗi kết nối API!")

#     if error_type == "authentication":
#         raise AuthenticationError("API Key không hợp lệ!")

#     return "Lấy dữ liệu thành công!"


# async def main():
#     for attempt in range(1, 4):
#         try:
#             result = await fetch_data("connection")
#             print(result)
#             break

#         except ConnectionError as e:
#             print(f"Lỗi có thể Retry: {e}")

#             if attempt == 3:
#                 print("Đã hết số lần thử!")
#             else:
#                 delay = random.uniform(
#                     0,
#                     min(2 ** (attempt - 1), 5)
#                 )

#                 print(f"Chờ {delay:.2f} giây trước khi thử lại...")
#                 await asyncio.sleep(delay)

#         except AuthenticationError as e:
#             print(f"Lỗi không thể Retry: {e}")
#             break


# asyncio.run(main())

import asyncio

async def fetch_data():
    print("Đang gọi API...")
    await asyncio.sleep(5)
    return "Lấy dữ liệu thành công!"

async def main():
    for attempt in range(1, 4):
        try:
            result = await asyncio.wait_for(
                fetch_data(),
                timeout=2
            )
            print(result)
            break

        except asyncio.TimeoutError:
            print(f"Lần thử {attempt}: API timeout!")

            if attempt < 3:
                delay = 2 ** (attempt - 1)
                print(f"Chờ {delay} giây trước khi thử lại...")
                await asyncio.sleep(delay)

    else:
        print("Đã hết số lần thử!")

asyncio.run(main())