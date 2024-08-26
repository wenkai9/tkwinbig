import os
import pandas as pd
import random
import requests
import string
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
django.setup()

from app.task.models import Task, Tk_invacation
from app.goods.models import Goods
from app.users.models import User

file_path = 'C://Users//Administrator//Desktop//测试邀约数据.xlsx'
taskId = "836599560"


def read_excel_handle(file_path, start_index, batch_size=70):
    try:
        df = pd.read_excel(file_path)
        handle_list = df['handle'].tolist()
        end_index = min(start_index + batch_size, len(handle_list))
        return handle_list[start_index:end_index], end_index >= len(handle_list)
    except Exception as e:
        print(f"读取Excel文件出错: {str(e)}")
        return [], True


def tk_invitation(taskId):
    try:
        task = Task.objects.get(taskId=taskId)  # 获取任务信息
        user = User.objects.get(user_id=task.user_id)  # 获取用户信息
        products = Goods.objects.filter(id=task.product_id).first()  # 获取商品信息
        region = task.region  # 任务的区域信息
        shop_id = task.shop_id  # 任务的商店ID
        start_index = 0  # 批处理的起始索引
        batch_size = 70  # 每次处理的批次大小

        while True:
            creator_ids, end_of_data = read_excel_handle(file_path, start_index, batch_size)
            start_index += batch_size

            if not creator_ids:
                break

            refTaskId = ''.join(random.choices(string.digits, k=9))  # 生成随机的refTaskId

            data = {
                "type": 2,  # 邀请类型
                "region": region,  # 区域信息
                "refTaskId": refTaskId,  # 随机生成的任务ID
                "content": {
                    "shopId": shop_id,  # 商店ID
                    "name": "GTJ-06-18",  # 活动名称
                    "products": [
                        {
                            "productId": task.product_id,  # 商品ID
                            "commissionRate": products.commissionRate  # 佣金比例
                        }
                    ],
                    "creatorIds": creator_ids,  # 待邀请的创作者ID列表
                    "expireDateTime": "2024-06-30",  # 过期时间
                    "sampleRule": {
                        "hasFreeSample": True,  # 是否有免费样品
                        "sampleQuantity": 10  # 样品数量
                    },
                    "message": "Hi, dear! We have been following your amazing content and believe that your unique style and creativity would be a perfect fit for our brand! We are here to invite you to try and test our Lipstick Shaver. If you have any interest, please let us know, so that we can discuss more details. Thank you so much!",
                    # 邀请消息
                    "contactInfo": {
                        "email": user.email,  # 用户邮箱
                        "phone": user.number,  # 用户电话
                        "country": user.company  # 用户公司信息
                    }
                }
            }

            print(f"发送数据到 taskId {taskId}: {data}")

            url = f'https://qtoss-connect-dev.azurewebsites.net/qtoss-connect/tiktok/creator-invitation'
            token = 'Bearer ' + user.token
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            tt = requests.post(url=url, headers=headers, json=data)
            res = tt.json()
            if tt.status_code == 200:
                Tk_invacation.objects.create(
                    userId=data.get('userId'),
                    taskId=res.get('taskId'),
                    type=res.get('type'),
                    region=res.get('region'),
                    refTaskid=data.get('refTaskId'),
                    status=res.get('status'),
                    message=res.get('message'),
                    createAt=res.get('createdAt'),
                    complateAt=res.get('complatedAt'),
                )
            print(res)

        print("邀请流程完成。")

    except Task.DoesNotExist:
        print(f"找不到 taskId {taskId} 对应的任务。")
    except User.DoesNotExist:
        print(f"找不到与 taskId {taskId} 相关的用户信息。")
    except Goods.DoesNotExist:
        print(f"找不到与 taskId {taskId} 相关的商品信息。")
    except Exception as e:
        print(f"发生异常: {str(e)}")


# 示例用法
tk_invitation(taskId)

"""
循环
    首先遍历出来excel文件下handle列的数据，每次取70个
    把这些数据插入到creatorIds字段中
    然后循环调用接口，发送邀请
    接口返回成功后，插入到数据库中
    已经邀约过的达人不能重复使用
直到循环完excel里的数据
            token = (
                'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI2MTNjOGMyMS0wZTJhLTRmNWUtOTA0YS0zMjE2MTJhOWI3NGYiLCJ1bm'
                'lxdWVfbmFtZSI6ImhjaGVuIiwiZW1haWwiOiJoYWlwaW5nMDA4QGdtYWlsLmNvbSIsImdpdmVuX25hbWUiOiJIYWlwaW5nIiwiZmFtaWx5X'
                '25hbWUiOiJDaGVuIiwic291cmNlIjoiaW50ZXJuYWwiLCJleHRlcm5hbF9pZCI6IiIsImp0aSI6Ijg4MDFlZWI2LTJkOWItNDAwOS04OGYzL'
                'Tk0NGM4MTFlNjViZiIsIm5iZiI6MTcxNjgxMDQ5NCwiZXhwIjoxNzE2ODE3Njk0LCJpYXQiOjE3MTY4MTA0OTQsImlzcyI6ImJvdHNoYXJwIi'
                'wiYXVkIjoiYm90c2hhcnAifQ.Sd4PbyeQCZw3zMh64S9hfItY2SVSzJjoIzR7iureAm8')
            token = 'Bearer ' + token
"""
