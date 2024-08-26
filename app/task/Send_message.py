"""
循环
       循环首先从测试200.xlsx中获取到所有handle下的信息，遍历handle_list
       data中有type、region、refTaskId、userName、text
       然后content中的userName为handle下的信息，text为固定信息content
       refTaskId为随机生成的9位数字
       type为4，region为US
       }
       路由是127.0.0.1:8833/tk_im/，参数为data
       打印出来结果，保存到数据库 信息里有status状态
        去数据库查找到所有status不为5的taskId
        然后拿这些taskId去http://127.0.0.1:8833/get_tk_im/{taskId}接口请求
        更新数据库status状态
        然后再去数据库查询这个任务的status状态
        如果status是5, 则去http://127.0.0.1:8833/tk_im_dialog/{taskId}接口请求对话记录
        存下对方回话的信息到数据库(taskId,username,content,time)
        然后再拿这个信息去调用http://127.0.0.1:8833/chat/{taskId}接口生成要回复的信息(username,content)
        拿着生成的回复信息去调用http://127.0.0.1:8833/send_tk_im/接口发送回复信息
"""

# import os
# import pandas as pd
# import random
# import requests
# import time
# import string
# import django
#
# # 设置 Django 环境
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
# django.setup()
#
# # 导入 Django 模型
# from app.task.models import Tk_chat
#
# # Excel 文件路径
# file_path = 'C://Users//Administrator//Desktop//测试200.xlsx'
# df = pd.read_excel(file_path)
# handle_list = df['handle'].tolist()
# handle_list = handle_list[0:1]
# print(handle_list)
#
# task_id = ''.join(random.choices(string.digits, k=9))  # 生成随机的refTaskId
# # 循环任务
# try:
#     for handle in handle_list:
#         chat_url = 'http://120.27.208.224:8002/chat'
#         chat_data = {
#             "task_id": task_id,
#             "creator": handle,
#             "content": "",
#             "shop_id": "Vexloria",
#             "brand": "Vexloria",
#             "product_info": "Vexloria",
#             "product_link": "https://shop.tiktok.com",
#             "reward": "-20% Sales Commission",
#             "requirement": "-A 30 - 60 seconds video showing our product",
#             "limits": "200 dollars"
#         }
#         chat_res = requests.post(chat_url, json=chat_data)
#         chat_message = chat_res.json()
#         print(chat_message)
#         Tk_chat.objects.create(
#             taskId=task_id,
#             userName=handle,
#             content=chat_message,
#             sendTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#             )
#         im_url = 'http://127.0.0.1:8833/tk_im/'
#         im_data = {
#             "type": 4,
#             "region": "US",
#             "refTaskId": ''.join(random.choices(string.digits, k=9)),
#             "content": {
#                 "userName": handle,
#                 "text": chat_message
#             }
#         }
#         print(f"准备发送给 {handle} 的信息: {im_data}")
#         im_res = requests.post(im_url, json=im_data)
#         print(f"返回结果: {im_res.json()}")
#
#     print("所有信息发送完成。")
#
# except KeyboardInterrupt:
#     print("用户终止了程序。")
# except Exception as e:
#     print(f"发生异常: {str(e)}")



"""
循环
  首先从测试200.xlsx中获取到所有handle下的信息，遍历handle_list
  然后那这个遍历的达人去调用chat接口，生成信息message，遍历这些内容，调用http://127.0.0.1:8833/tk_im/接口发送信息
循环结束
"""