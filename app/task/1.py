import json
import requests
import os
import django
import random
import string
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
django.setup()
from django.forms.models import model_to_dict
from app.task.models import Tk_chat, Task, Creators, Tk_invacation
from app.task.models import Task, Tk_invacation, Creators
from app.goods.models import Goods, RaidsysRule
from app.users.models import User





# token = (
#     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI1ZDVkMGU4MS1lNGE2LTQ3Y2QtYjAyNy03ZWU2ZTE2ZjRmYmMiLCJ1bmlxdWVfbmFtZSI6InNvbmciLCJlbWFpbCI6IjIxODEyNTE4NDNAcXEuY29tIiwiZ2l2ZW5fbmFtZSI6InNvbmciLCJmYW1pbHlfbmFtZSI6IiIsInNvdXJjZSI6ImludGVybmFsIiwiZXh0ZXJuYWxfaWQiOiIiLCJqdGkiOiI1MzlhYTU2ZC04MjUwLTQ3ZTQtYThmMy1hMGY1YjE5MGFlMjUiLCJwaG9uZSI6IiIsIm5iZiI6MTcyMzQzMTc3NSwiZXhwIjoxNzIzNDM4OTc1LCJpYXQiOjE3MjM0MzE3NzUsImlzcyI6ImJvdHNoYXJwIiwiYXVkIjoiYm90c2hhcnAifQ.BEIJ0rh4WU2Jb2JcjmFtWFKKav6M_2HzRBsMNUGsW58")
# token = 'Bearer ' + token
# headers = {'Content-Type': 'application/json', 'Authorization': token}
# taskId = "65sd4156"
#
# task = Creators.objects.filter(taskId=taskId).values_list("product", flat=True)[0:10]
# print(task)
#
# task = Task.objects.get(taskId=taskId)
# user = User.objects.get(user_id=task.user_id)
# products = Goods.objects.filter(id=task.product_id).first()
# product_id = task.product_id
# product = Goods.objects.get(id=product_id)
# rule_id = product.raidsysrule_id
# rule = RaidsysRule.objects.get(id=rule_id)
# requirement = rule.requirement
# print(requirement)


# try:
#     task = Task.objects.get(taskId=taskId)
#     print(task)
#     shop_id = task.shop_id
#     creator_id = Creators.objects.filter(taskId=task).values_list("product", flat=True).first()
#     print(creator_id)
#     refTaskId = ''.join(random.choices(string.digits, k=9))  # 生成随机的refTaskId
#     data = {
#         "type": 1,
#         "region": "US",
#         "refTaskId": refTaskId,
#         "content": {
#             "shopId": shop_id,
#             "UserName": creator_id,
#             "text": "Hi, dear! We have been following your amazing content and believe that your unique style and creativity would be a perfect fit for our brand! We are here to invite you to try and test our yoga ball. If you have any interest, please let us know, so that we can discuss more details. Thank you so much!"
#         }
#     }
#     url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/seller-im"
#     response = requests.post(url=url, headers=headers, json=data)
#     data = response.json()
#     print(data)
# except Exception as e:
#     print(e)

# from bson import ObjectId
#
# # 生成新的 ObjectId
# new_id = ObjectId()
# print(f"New ObjectId: {new_id}")

# params ={
#     "task_id": "783qw213",
#     "shop_id": "youwei",
#     "products": "Lipstick Shaver"
# }
#
# response = requests.post("http://120.27.208.224:8003/retrival", json=params)
# retrieval_result = response.json()
# print(retrieval_result)
# product_list = retrieval_result.get(params["products"], [])
#
# # 将每个产品插入数据库
# for product in product_list:
#     Creators.objects.create(
#         taskId=params["task_id"],
#         tag=params["products"],
#         product=product,
#     )
# import requests
# import pandas as pd
#
# # 请求数据
# params = {
#     "task_id": "783qw21",
#     "shop_id": "youwei",
#     "products": "Lipstick Shaver"
# }
#
# response = requests.post("http://120.27.208.224:8003/retrival", json=params)
# retrieval_result = response.json()
#
# # 获取产品列表
# product_list = retrieval_result.get(params["products"], [])
#
# # 将数据转换为 DataFrame
# df = pd.DataFrame({
#     "taskId": [params["task_id"]] * len(product_list),
#     "tag": [params["products"]] * len(product_list),
#     "product": product_list
# })
#
# # 写入 Excel 文件
# df.to_excel("output.xlsx", index=False, engine='openpyxl')
#
# print("数据已成功写入 output.xlsx 文件")
