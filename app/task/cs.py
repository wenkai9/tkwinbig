import json
import random
import string
import requests
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
django.setup()

from app.task.models import Task, Tk_invacation, Creators
from app.goods.models import Goods, RaidsysRule
from app.users.models import User


# file_path = 'C://Users//Administrator//Desktop//测试200.xlsx'
# dd = 70
# task_id = "783qw212"  # 783qw213 口红刮毛器     65sd4156  扎带机
# task = Task.objects.get(taskId=task_id)
# print(task.send_quantity)
# task.send_quantity += dd
# task.save()
# print(task.send_quantity)



'''
total_invitations
'''

# token = (
#     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI1ZDVkMGU4MS1lNGE2LTQ3Y2QtYjAyNy03ZWU2ZTE2ZjRmYmMiLCJ1bmlxdWVfbmFtZSI6InNvbmciLCJlbWFpbCI6IjIxODEyNTE4NDNAcXEuY29tIiwiZ2l2ZW5fbmFtZSI6InNvbmciLCJmYW1pbHlfbmFtZSI6IiIsInNvdXJjZSI6ImludGVybmFsIiwiZXh0ZXJuYWxfaWQiOiIiLCJqdGkiOiI1MjQzNTQ4Ni1jZmZhLTRkYmQtYjY1Zi1mZTMxMzE1YTdhYzUiLCJwaG9uZSI6IiIsIm5iZiI6MTcyNDA2MDg2NCwiZXhwIjoxNzI0MDY4MDY0LCJpYXQiOjE3MjQwNjA4NjQsImlzcyI6InF0b3NzIiwiYXVkIjoicXRvc3MifQ.jUwR74vKbC8Ou7rbrZIgwamsFgwsBHwJ1TpCl6NoHcg")
# token = 'Bearer ' + token
# headers = {'Content-Type': 'application/json', 'Authorization': token}

'''
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI1ZDVkMGU4MS1lNGE2LTQ3Y2QtYjAyNy03ZWU2ZTE2ZjRmYmMiLCJ1bmlxdWVfbmFtZSI6InNvbmciLCJlbWFpbCI6IjIxODEyNTE4NDNAcXEuY29tIiwiZ2l2ZW5fbmFtZSI6InNvbmciLCJmYW1pbHlfbmFtZSI6IiIsInNvdXJjZSI6ImludGVybmFsIiwiZXh0ZXJuYWxfaWQiOiIiLCJqdGkiOiI1MjQzNTQ4Ni1jZmZhLTRkYmQtYjY1Zi1mZTMxMzE1YTdhYzUiLCJwaG9uZSI6IiIsIm5iZiI6MTcyNDA2MDg2NCwiZXhwIjoxNzI0MDY4MDY0LCJpYXQiOjE3MjQwNjA4NjQsImlzcyI6InF0b3NzIiwiYXVkIjoicXRvc3MifQ.jUwR74vKbC8Ou7rbrZIgwamsFgwsBHwJ1TpCl6NoHcg'''


# def get_creator_ids(task_id, start_index, batch_size):
#     """ 从数据库中获取创作者 ID 列表 """
#     return list(Creators.objects.filter(taskId=task_id)
#                 .values_list("product", flat=True)
#                 [start_index:start_index + batch_size])
#
#
# def tk_invitation(taskId):
#     try:
#         # 获取任务信息
#         task = Task.objects.get(taskId=taskId)
#         user = User.objects.get(user_id=task.user_id)
#         products = Goods.objects.filter(id=task.product_id).first()
#         product_id = task.product_id
#         product = Goods.objects.get(id=product_id)
#         rule_id = product.raidsysrule_id
#         rule = RaidsysRule.objects.get(id=rule_id)
#         requirement = rule.requirement
#         region = task.region
#         shop_id = task.shop_id
#         if not products:
#             print(f"找不到与 taskId {taskId} 相关的商品信息。")
#             return
#
#         # 设置分页参数
#         start_index = 0
#         batch_size = 50
#         task_count = 0
#
#         while True:
#             # 从数据库中获取创作者ID列表
#             creator_ids = get_creator_ids(taskId, start_index, batch_size)
#             if not creator_ids:
#                 break
#
#             refTaskId = ''.join(random.choices(string.digits, k=9))  # 生成随机的refTaskId
#             n = ''.join(random.choices(string.digits, k=4))
#
#             data = {
#                 "type": 2,
#                 "region": region,
#                 "refTaskId": refTaskId,
#                 "content": {
#                     "shopId": shop_id,
#                     "name": f"YJQ-08-19-{n}",
#                     "products": [
#                         {
#                             "productId": task.product_id,
#                             "commissionRate": float(products.commissionRate)
#                         }
#                     ],
#                     "creatorIds": creator_ids,
#                     "expireDateTime": "2024-08-30",
#                     "sampleRule": {
#                         "hasFreeSample": True,
#                         "sampleQuantity": 10
#                     },
#                     "message": requirement,
#                     "contactInfo": {
#                         "email": user.email,
#                         "phone": user.number,
#                         "country": user.company
#                     }
#                 }
#             }
#
#             print(f"发送数据到 taskId {taskId}: {data}")
#             print(json.dumps(data))
#             url = f'https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation'
#             response = requests.post(url=url, headers=headers, json=data)
#             print(response.status_code)
#             res = response.json()
#             if response.status_code == 200:
#                 Tk_invacation.objects.create(
#                     userId=data.get('userId'),
#                     taskId=res.get('taskId'),
#                     type=res.get('type'),
#                     region=res.get('region'),
#                     refTaskid=data.get('refTaskId'),
#                     status=res.get('status'),
#                     receivestatus=res.get('receivestatus'),
#                     message=res.get('message'),
#                     createAt=res.get('createdAt'),
#                     complateAt=res.get('complatedAt'),
#                 )
#                 task_count += len(creator_ids)
#
#             # 更新起始索引
#             start_index += batch_size
#
#         print(f"邀请流程完成,共发送了{task_count}个邀请。")
#
#     except Task.DoesNotExist:
#         print(f"找不到 taskId {taskId} 对应的任务。")
#     except User.DoesNotExist:
#         print(f"找不到与 taskId {taskId} 相关的用户信息。")
#     except Goods.DoesNotExist:
#         print(f"找不到与 taskId {taskId} 相关的商品信息。")
#     except Exception as e:
#         print(f"发生异常: {str(e)}")
#
#
# # 示例用法
# tk_invitation(taskId)
