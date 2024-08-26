import json
import os
import pandas as pd
import random
import requests
import string
from decimal import Decimal
from django.conf import settings
from app.task.models import Task, Tk_invacation
from app.goods.models import Goods
from app.users.models import User


def read_excel_handle(file_path, start_index, batch_size=70):
    try:
        df = pd.read_excel(file_path)
        handle_list = df['handle'].tolist()
        end_index = min(start_index + batch_size, len(handle_list))
        return handle_list[start_index:end_index], end_index >= len(handle_list)
    except Exception as e:
        print(f"读取Excel文件出错: {str(e)}")
        return [], True


def tk_invitation(task_id):
    try:
        task = Task.objects.get(taskId=task_id)
        user = User.objects.get(user_id=task.user_id)
        products = Goods.objects.filter(id=task.product_id).first()
        region = task.region
        shop_id = task.shop_id
        start_index = 0
        batch_size = 70
        file_path = os.path.join(settings.BASE_DIR, 'C://Users//Administrator//Desktop//测试邀约数据.xlsx')

        while True:
            creator_ids, end_of_data = read_excel_handle(file_path, start_index, batch_size)
            start_index += batch_size

            if not creator_ids:
                break

            refTaskId = ''.join(random.choices(string.digits, k=9))

            data = {
                "type": 2,
                "region": region,
                "refTaskId": refTaskId,
                "content": {
                    "shopId": shop_id,
                    "name": "GTJ-06-24",
                    "products": [
                        {
                            "productId": task.product_id,
                            "commissionRate": float(products.commissionRate)
                        }
                    ],
                    "creatorIds": creator_ids,
                    "expireDateTime": "2024-7-15",
                    "sampleRule": {
                        "hasFreeSample": True,
                        "sampleQuantity": 0
                    },
                    "message": "Hi, dear! We have been following your amazing content and believe that your unique style and creativity would be a perfect fit for our brand! We are here to invite you to try and test our head shavers for bald men and women. If you have any interest, please let us know, so that we can discuss more details. Thank you so much!",
                    "contactInfo": {
                        "email": user.email,
                        "phone": user.number,
                        "country": user.company
                    }
                }
            }
            print(f"发送数据到 taskId {task_id}: {data}")
            data = json.dumps(data)
            print(data)
            url = 'https://qtoss-connect-dev.azurewebsites.net/qtoss-connect/tiktok/creator-invitation'
            token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI2MTNjOGMyMS0wZTJhLTRmNWUtOTA0YS0zMjE2MTJh'
                     'OWI3NGYiLCJ1bmlxdWVfbmFtZSI6ImhjaGVuIiwiZW1haWwiOiJoYWlwaW5nMDA4QGdtYWlsLmNvbSIsImdpdmVuX25hb'
                     'WUiOiJIYWlwaW5nIiwiZmFtaWx5X25hbWUiOiJDaGVuIiwic291cmNlIjoiaW50ZXJuYWwiLCJleHRlcm5hbF9pZCI6Ii'
                     'IsImp0aSI6Ijg4MDFlZWI2LTJkOWItNDAwOS04OGYzLTk0NGM4MTFlNjViZiIsIm5iZiI6MTcxNjgxMDQ5NCwiZXhwIjox'
                     'NzE2ODE3Njk0LCJpYXQiOjE3MTY4MTA0OTQsImlzcyI6ImJvdHNoYXJwIiwiYXVkIjoiYm90c2hhcnAifQ.Sd4PbyeQCZw3'
                     'zMh64S9hfItY2SVSzJjoIzR7iureAm8')
            token = 'Bearer ' + token
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            tt = requests.post(url=url, headers=headers, json=data)
            print(tt.status_code)
            print(tt)
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
        print(f"找不到 taskId {task_id} 对应的任务。")
    except User.DoesNotExist:
        print(f"找不到与 taskId {task_id} 相关的用户信息。")
    except Goods.DoesNotExist:
        print(f"找不到与 taskId {task_id} 相关的商品信息。")
    except Exception as e:
        print(f"发生异常: {str(e)}")
