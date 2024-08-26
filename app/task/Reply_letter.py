import os
import django
import time
import random
import string
import requests

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
django.setup()
from app.task.models import Tkuser_im, Tk_chat, Tk_information


processed_task_ids = set()  # 初始化一个空集合来存储已处理的任务ID


def send_message_to_user():
    try:
        # 查询所有状态为5的任务的taskId
        tasks = Tkuser_im.objects.filter(status=8, receivestatus=8).values_list('taskId', flat=True)
        print(tasks)
        for taskId in tasks:
            if taskId in processed_task_ids:
                print(f"任务 taskId {taskId} 已处理过，跳过...")
                continue  # 如果任务已处理过，则跳过处理

            try:
                # 查询 Tk_information 表中 taskId 对应的 userName

                tk_info = Tk_information.objects.filter(taskId=taskId).last()
                username = tk_info.userName
                # 查询 Tk_chat 表中 taskId 对应的 userName 和 content
                chat_data = Tk_chat.objects.filter(userName=username).last()
                print(chat_data)
                time.sleep(10)
                if chat_data:
                    userName = chat_data.userName
                    content = chat_data.content
                    # 随机生成一个新的 refTaskId
                    refTaskId = ''.join(random.choices(string.digits, k=9))
                    data = {
                        "type": 4,
                        "region": "US",
                        "refTaskId": refTaskId,
                        "content": {
                            "userName": userName,
                            "text": content
                        }
                    }
                    print(data)
                    # 构建请求的URL，并发送 POST 请求
                    url = f'http://127.0.0.1:8833/tk_im_reply/{taskId}'
                    response = requests.post(url, json=data)
                    if response.status_code == 200:
                        print(f"已向 taskId {taskId} 的用户 {userName} 发送消息: {content}")
                        processed_task_ids.add(taskId)  # 将已处理过的任务ID添加到集合中
                    else:
                        print(f"向 taskId {taskId} 的用户 {userName} 发送消息失败: {response.text}")
                else:
                    print(f"未找到 taskId {taskId} 对应的聊天记录")
            except Exception as e:
                print(f"处理 taskId {taskId} 出错: {str(e)}")
    except Exception as e:
        print(f"查询 taskId 出错: {str(e)}")


def job():
    try:
        while True:
            print("开始新的循环...")
            send_message_to_user()  # 执行任务处理
            time.sleep(30)  # 每隔30秒执行一次

    except Exception as e:
        print(f"处理任务出错: {str(e)}")


# 启动定时任务
job()


"""
循环
   首先查出来tkuser_im表中status为5的taskId
   然后遍历这些taskId，查询Tk_information的信息
   然后遍历Tk_information的信息，获取taskId、userName和content
   然后调用chat接口(http://120.27.208.224:8002/chat)，发送消息给用户
   chat接口请求参数：data={
                    "task_id": 为tk_information表中的taskId
                    "creator": 为tk_information表中的userName,
                    "content": 为tk_information表中的content,
                    "shop_id": "Vexloria",
                    "brand": "Vexloria",
                    "product_info": "Vexloria",
                    "product_link": "https://shop.tiktok.com",
                    "reward": "-20% Sales Commission",
                    "requirement": "-A 30 - 60 seconds video showing our product",
                    "limits": "200 dollars"
   }
   header: {'Content-Type': 'application/json'}
   请求完之后把taskId、creator和content以及时间存入tk_chat表中以及把taskId、userName和content传给send_message_to_user函数
   已经执过的任务taskId之后不在执行，taskId不重复使用

"""

