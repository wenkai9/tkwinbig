import json
import random
import string
import requests
import os
import django
from django.http import JsonResponse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
django.setup()

from app.task.models import Task, Tk_invacation, Creators, Tk_seller_im
from app.goods.models import Goods, RaidsysRule
from app.users.models import User

taskId = "65sd4156"  # 固定的 taskId


def send_seller_messages(taskId):
    usernames = ["ash_bash28",
                 "kenjahb",
                 "placenta_6",
                 "dre_da_dancer",
                 "thecraftygrrl",
                 "realnikocado",
                 "christianmamamary",
                 "twtttl",
                 "coolwhitaker",
                 "mialorenclark",
                 "woodsie.tv",
                 "sharkbait_kitty",
                 "gagedancin",
                 "tow_ninja68",
                 "deathenjoyer420",
                 "mikey_rothgeb",
                 "powerthighcarol",
                 "just_marina6"]

    try:
        # 获取任务信息
        task = Task.objects.get(taskId=taskId)
        shop_id = task.shop_id
        product_id = task.product_id
        product = Goods.objects.get(id=product_id)
        rule_id = product.raidsysrule_id
        rule = RaidsysRule.objects.get(id=rule_id)
        requirement = rule.requirement

        url = "https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/seller-im"
        token = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI1ZDVkMGU4MS1lNGE2LTQ3Y2QtYjAyNy03ZWU2ZTE2ZjRmYmMiLCJ1bmlxdWVfbmFtZSI6InNvbmciLCJlbWFpbCI6IjIxODEyNTE4NDNAcXEuY29tIiwiZ2l2ZW5fbmFtZSI6InNvbmciLCJmYW1pbHlfbmFtZSI6IiIsInNvdXJjZSI6ImludGVybmFsIiwiZXh0ZXJuYWxfaWQiOiIiLCJqdGkiOiI1MjQzNTQ4Ni1jZmZhLTRkYmQtYjY1Zi1mZTMxMzE1YTdhYzUiLCJwaG9uZSI6IiIsIm5iZiI6MTcyNDA2MDg2NCwiZXhwIjoxNzI0MDY4MDY0LCJpYXQiOjE3MjQwNjA4NjQsImlzcyI6InF0b3NzIiwiYXVkIjoicXRvc3MifQ.jUwR74vKbC8Ou7rbrZIgwamsFgwsBHwJ1TpCl6NoHcg")
        token = 'Bearer ' + token
        headers = {'Content-Type': 'application/json', 'Authorization': token}

        for username in usernames:
            refTaskId = ''.join(random.choices(string.digits, k=9))  # 生成随机的 refTaskId
            data = {
                "type": 3,
                "region": "US",
                "refTaskId": refTaskId,
                "content": {
                    "shopId": shop_id,
                    "UserName": username,
                    "text": requirement
                }
            }
            print(json.dumps(data))  # 打印调试信息

            try:
                response = requests.post(url=url, headers=headers, json=data)
                response.raise_for_status()  # 检查请求是否成功

                if response.status_code == 200:
                    response_data = response.json()
                    print(response_data)  # 打印响应数据
                    invitation_instance = Tk_seller_im(
                        _id=response_data.get('_id'),
                        userId=response_data.get('userId'),
                        taskId=response_data.get('taskId'),
                        type=response_data.get('type'),
                        region=response_data.get('region'),
                        status=response_data.get('status'),
                        refTaskId=response_data.get('refTaskId'),
                        receiveStatus=response_data.get('receiveStatus'),
                        sendRetryCount=response_data.get('sendRetryCount'),
                        sendFailureCode=response_data.get('sendFailureCode'),
                        message=response_data.get('message'),
                        createdAt=response_data.get('createdAt'),
                        completedAt=response_data.get('completedAt'),
                        checkedAt=response_data.get('checkedAt'),
                        sentAt=response_data.get('sentAt')
                    )
                    # 保存数据到 MongoDB
                    invitation_instance.save()
                    print(f"保存成功任务{response_data.get('_id')}")
            except requests.RequestException as e:
                print(f"请求失败: {e}")

        return JsonResponse({"message": "Messages sent successfully"}, status=200)

    except Task.DoesNotExist:
        return JsonResponse({"code": 400, "errmsg": "未找到任务"}, status=400)
    except Goods.DoesNotExist:
        return JsonResponse({"code": 400, "errmsg": "未找到商品"}, status=400)
    except RaidsysRule.DoesNotExist:
        return JsonResponse({"code": 400, "errmsg": "未找到规则"}, status=400)
    except Exception as e:
        return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)


send_seller_messages(taskId)
