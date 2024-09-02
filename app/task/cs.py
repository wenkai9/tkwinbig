import json
import random
import string
import requests
import os
import django
# from django.utils.dateparse import parse_datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
django.setup()
import base64
from app.task.models import Task, Tk_invacation, Creators, Rpa_key,Tk_Invitation
from app.goods.models import Goods, RaidsysRule
from app.users.models import User
from utils.get_token import get_token

# access_token = get_token('song', '306012')
# taskId = "783qw212"
# tasks = Tk_invacation.objects.filter(delivery_id=taskId).values_list("taskId", flat=True)
# print("任务ID列表:", tasks)

# def get_rpa_creator(taskId):
#     try:
#         try:
#             invitation = Tk_Invitation.objects.get(id=taskId)
#         except Tk_Invitation.DoesNotExist:
#             return "未找到该任务"
#
#         # access_token = get_token('song', '306012')
#         access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI1ZDVkMGU4MS1lNGE2LTQ3Y2QtYjAyNy03ZWU2ZTE2ZjRmYmMiLCJ1bmlxdWVfbmFtZSI6InNvbmciLCJlbWFpbCI6IjIxODEyNTE4NDNAcXEuY29tIiwiZ2l2ZW5fbmFtZSI6InNvbmciLCJmYW1pbHlfbmFtZSI6IiIsInNvdXJjZSI6ImludGVybmFsIiwiZXh0ZXJuYWxfaWQiOiIiLCJqdGkiOiJhNTQyYWIxZS1iZWRkLTQ3YjktODQzMi1kNzQxYmRlMmE2NTYiLCJwaG9uZSI6IiIsIm5iZiI6MTcyNTAwODk3NSwiZXhwIjoxNzI1MDE2MTc1LCJpYXQiOjE3MjUwMDg5NzUsImlzcyI6InF0b3NzIiwiYXVkIjoicXRvc3MifQ.DO0pfJCj81jgU8eGoKnXCPRPwZGUGY6uZ1QDFXDgsg8"
#         token = 'Bearer ' + access_token
#         headers = {'Content-Type': 'application/json', 'Authorization': token}
#
#         # 请求 URL
#         url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation/{taskId}/detail"
#
#         try:
#             response = requests.get(url=url, headers=headers)
#             response.raise_for_status()
#             data = response.json()
#             creators = data.get('creator_id_list', [])
#             creators_data = [
#                 {
#                     "creator_id": creator['base_info']['creator_id'],
#                     "nick_name": creator['base_info']['nick_name'],
#                     "user_name": creator['base_info']['user_name'],
#                     "selection_region": creator['base_info']['selection_region'],
#                     "product_add_cnt": creator['product_add_cnt'],
#                     "content_posted_cnt": creator['content_posted_cnt']
#                 }
#                 for creator in creators
#             ]
#
#             # 打印 JSON 数据用于调试
#             print("响应数据:", json.dumps(creators_data))
#
#             return json.dumps(creators_data)
#
#         except requests.exceptions.RequestException as e:
#             print(f"请求失败: {e}")
#             return None
#     except Exception as e:
#         print(f"发生了意外错误: {e}")
#         return None
#
#
# taskId = "66bb565c505b91c8db51905a"
# print(get_rpa_creator(taskId))

# 逐个请求任务数据并更新数据库
# def update_task(taskId):
#     results = []  # 用于存储所有成功更新后的记录
#
#     try:
#         # 获取所有相关的 taskId
#         tasks = Tk_invacation.objects.filter(delivery_id=taskId).values_list("taskId", flat=True)
#         print("任务ID列表:", tasks)
#
#         for taskid in tasks:
#             access_token = get_token('song', '306012')
#             # access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI1ZDVkMGU4MS1lNGE2LTQ3Y2QtYjAyNy03ZWU2ZTE2ZjRmYmMiLCJ1bmlxdWVfbmFtZSI6InNvbmciLCJlbWFpbCI6IjIxODEyNTE4NDNAcXEuY29tIiwiZ2l2ZW5fbmFtZSI6InNvbmciLCJmYW1pbHlfbmFtZSI6IiIsInNvdXJjZSI6ImludGVybmFsIiwiZXh0ZXJuYWxfaWQiOiIiLCJqdGkiOiJhMTlmNDY4Ni01NjcwLTRhYjQtOTMzMC03N2MzOWUxNzAyOTIiLCJwaG9uZSI6IiIsIm5iZiI6MTcyNTAxMjcxNSwiZXhwIjoxNzI1MDE5OTE1LCJpYXQiOjE3MjUwMTI3MTUsImlzcyI6InF0b3NzIiwiYXVkIjoicXRvc3MifQ.fDiDjn3hstAH7b6LqmHU-A62kSibJxNLL8c-8XZYPuI"
#             token = 'Bearer ' + access_token
#             headers = {'Content-Type': 'application/json', 'Authorization': token}
#             url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation/{taskid}"
#
#             try:
#                 response = requests.get(url=url, headers=headers)
#                 response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
#
#                 data = response.json()
#
#                 # 更新记录
#                 updated_count = Tk_invacation.objects.filter(
#                     taskId=taskid
#                 ).update(
#                     userId=data.get('userId'),
#                     taskId=data.get('taskId'),
#                     delivery_id=taskId,
#                     type=data.get('type'),
#                     region=data.get('region'),
#                     refTaskid=data.get('refTaskId'),
#                     status=data.get('status'),
#                     receivestatus=data.get('receivestatus'),
#                     message=data.get('message'),
#                     createAt=data.get('createdAt'),  # 处理时间字段
#                     complateAt=data.get('complatedAt'),  # 处理时间字段
#                 )
#
#                 if updated_count > 0:
#                     updated_record = Tk_invacation.objects.get(taskId=taskid)
#                     results.append({
#                         "taskId": updated_record.taskId,
#                         "userId": updated_record.userId,
#                         "type": updated_record.type,
#                         "region": updated_record.region,
#                         "refTaskid": updated_record.refTaskid,
#                         "status": updated_record.status,
#                         "receivestatus": updated_record.receivestatus,
#                         "message": updated_record.message,
#                         "createAt": updated_record.createAt,
#                         "complateAt": updated_record.complateAt,
#                     })
#
#             except requests.exceptions.RequestException as e:
#                 print(f"请求失败: taskId={taskid}, 错误信息: {e}")
#             except Exception as e:
#                 print(f"更新失败: taskId={taskid}, 错误信息: {e}")
#
#     except Exception as e:
#         print(f"获取任务ID失败: {e}")
#
#     print(results)
#
#
# taskId = ("783qw212")
# update_task(taskId)

# user_id =20
#
# username = Rpa_key.objects.get(user_id=user_id).username
# password = Rpa_key.objects.get(user_id=user_id).password
#
# access_token = get_token(username, password)
# print(access_token)



def get_token(username, password):
    try:
        your_string = f"{username}:{password}"
        b = base64.b64encode(your_string.encode('utf-8'))
        url = "https://qtoss-connect.azurewebsites.net/token"
        base64_str = b.decode('utf-8')
        authorization = 'Basic ' + base64_str
        print("authorization", authorization)
        response = requests.post(url=url, headers={'Content-Type': 'application/json',
                                                   'Authorization': authorization})
        data = response.json()
        access_token = data['access_token']
        if response.status_code == 200:
            # print(access_token)
            return access_token
        else:
            return None
    except Exception as e:
        print(e)
        return None

username = "song"
password = "306012"
print(get_token(username, password))


# token = (
#     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI1ZDVkMGU4MS1lNGE2LTQ3Y2QtYjAyNy03ZWU2ZTE2ZjRmYmMiLCJ1bmlxdWVfbmFtZSI6InNvbmciLCJlbWFpbCI6IjIxODEyNTE4NDNAcXEuY29tIiwiZ2l2ZW5fbmFtZSI6InNvbmciLCJmYW1pbHlfbmFtZSI6IiIsInNvdXJjZSI6ImludGVybmFsIiwiZXh0ZXJuYWxfaWQiOiIiLCJqdGkiOiI1MjQzNTQ4Ni1jZmZhLTRkYmQtYjY1Zi1mZTMxMzE1YTdhYzUiLCJwaG9uZSI6IiIsIm5iZiI6MTcyNDA2MDg2NCwiZXhwIjoxNzI0MDY4MDY0LCJpYXQiOjE3MjQwNjA4NjQsImlzcyI6InF0b3NzIiwiYXVkIjoicXRvc3MifQ.jUwR74vKbC8Ou7rbrZIgwamsFgwsBHwJ1TpCl6NoHcg")
# token = 'Bearer ' + token
# headers = {'Content-Type': 'application/json', 'Authorization': token}

'''
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI1ZDVkMGU4MS1lNGE2LTQ3Y2QtYjAyNy03ZWU2ZTE2ZjRmYmMiLCJ1bmlxdWVfbmFtZSI6InNvbmciLCJlbWFpbCI6IjIxODEyNTE4NDNAcXEuY29tIiwiZ2l2ZW5fbmFtZSI6InNvbmciLCJmYW1pbHlfbmFtZSI6IiIsInNvdXJjZSI6ImludGVybmFsIiwiZXh0ZXJuYWxfaWQiOiIiLCJqdGkiOiI1MjQzNTQ4Ni1jZmZhLTRkYmQtYjY1Zi1mZTMxMzE1YTdhYzUiLCJwaG9uZSI6IiIsIm5iZiI6MTcyNDA2MDg2NCwiZXhwIjoxNzI0MDY4MDY0LCJpYXQiOjE3MjQwNjA4NjQsImlzcyI6InF0b3NzIiwiYXVkIjoicXRvc3MifQ.jUwR74vKbC8Ou7rbrZIgwamsFgwsBHwJ1TpCl6NoHcg
'''


