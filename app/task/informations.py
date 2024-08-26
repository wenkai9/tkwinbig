# import json
# import os
# import requests
# import schedule
# import time
# import django
# import random
# import string
#
# # 设置Django环境
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
# django.setup()
#
# from app.task.models import Tkuser_im, Tk_chat, Tk_information, Task
# # from app.task.views import tkuser_im
# # processed_task_ids = set()  # 存储已处理过的任务ID
# completed_task_ids = set()  # 存储已完成的任务ID（状态为5）
#
#
# def status():
#     try:
#         # 从数据库获取所有状态不是5的任务ID
#         task_ids = Tkuser_im.objects.exclude(status=8).values_list('taskId', flat=True)
#         return task_ids
#     except Exception as e:
#         print(f"获取状态不是5的任务ID时出错: {str(e)}")
#         return []
#
#
# def job():
#     global completed_task_ids
#
#     try:
#         # 获取数据库中状态不是8的任务ID列表
#         task_ids = status()
#
#         # 处理状态不是8的任务ID
#         for task_id in task_ids:
#             if task_id in completed_task_ids:
#                 continue  # 如果任务ID已经处理过，则跳过
#             print(f"处理任务 ID {task_id}...")
#             request_api(task_id)
#
#             # 检查任务是否已经完成（状态为8并且收信状态为8）
#             task = Tkuser_im.objects.get(taskId=task_id)
#             if task.status == 8 and task.receivestatus == 8 and task_id not in completed_task_ids:
#                 print(f"任务 ID {task_id} 已完成。正在获取对话记录...")
#                 retrieve_dialog(task_id)
#                 completed_task_ids.add(task_id)
#
#     except Exception as e:
#         print(f"执行任务时出错: {str(e)}")
#
#
# def request_api(task_id):
#     try:
#         # 发送请求获取任务数据
#         url = f'http://127.0.0.1:8833/get_tk_im/{task_id}'
#         response = requests.get(url)
#         data = response.json()
#         print(f"收到任务 ID {task_id} 的数据: {data}")
#
#     except Exception as e:
#         print(f"获取任务 ID {task_id} 数据时出错: {str(e)}")
#         time.sleep(5)  # 出错时延迟5秒再重试
#
#
# def retrieve_dialog(task_id):
#     try:
#         # 发送请求获取对话记录数据
#         dialog_url = f'http://127.0.0.1:8833/tk_im_dialog/{task_id}'
#         dialog_response = requests.get(dialog_url)
#         dialog_data = dialog_response.json()
#         last_dialog = dialog_data['data'][-1]
#         print(f"任务 ID {task_id} 的最后一条对话记录: {last_dialog}")
#         username = Tk_information.objects.get(taskId=task_id).userName
#         process_taskid(username)
#         completed_task_ids.add(task_id)
#     except Exception as e:
#         print(f"获取任务 ID {task_id} 对话记录时出错: {str(e)}")
#         time.sleep(5)  # 出错时延迟5秒再重试
#
#
# def process_taskid(username, taskId):
#     try:
#         # 处理任务ID
#         taskId = tkuser_im(taskId=taskId)
#         tasks = Tk_chat.objects.filter(userName=username).last()
#         content = Tk_information.objects.filter(userName=username).last()
#         content = content.content
#         # content = content.last()
#         print(content)
#         data = {
#             # "task_id": ''.join(random.choices(string.digits, k=9)),
#             "task_id": tasks.taskId,
#             "creator": tasks.userName,
#             "content": content,
#             "shop_id": "Vexloria",
#             "brand": "Vexloria",
#             "product_info": "Vexloria",
#             "product_link": "https://shop.tiktok.com",
#             "reward": "-20% Sales Commission",
#             "requirement": "-A 30 - 60 seconds video showing our product",
#             "limits": "200 dollars"
#         }
#         print(data)
#         url = 'http://120.27.208.224:8002/chat'
#         headers = {'Content-Type': 'application/json'}
#         response = requests.post(url, headers=headers, json=data)  # 调用chat接口
#         res = response.json()
#         Tk_chat.objects.create(
#             taskId=data['task_id'],
#             userName=data['creator'],
#             content=res,
#             isAgree_invitation=res[1],
#             sendTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         )
#         print(res)
#         num = 0
#         if res[1] and res[1] == "True":
#             num += 1
#         task = Task.objects.get(taskId=taskId)
#         task.match_quantity = num
#         task.save()
#     except Exception as e:
#         print(f"处理任务时出错: {str(e)}")
#
#
# # 每10秒执行一次任务
# schedule.every(10).seconds.do(job)
#
# # 主循环，保持程序运行
# while True:
#     schedule.run_pending()
#     time.sleep(1)