from django.db.models import Sum
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.task.models import (Task, Tk_im, Creators, Tkuser_im, Tk_invacation, Tk_im, Tk_chat, Tk_information,
                             Tk_seller_im, Content, Tk_Invitation, Creator, BaseInfo, Product, Image, Rpa_key)
import base64
from django.db import transaction
from bson import ObjectId
from mongoengine import DoesNotExist
import json
from datetime import datetime
import random
import string
from ..goods.models import Goods, RaidsysRule
from ..users.models import User
import requests
# import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from utils.get_token import get_token
from utils.updata_task import update_task
from utils.get_rpa_creator import get_rpa_creator
import jwt
from django.conf import settings

'''
D://PyCharmProject//tkwinbig//djangoProject1//settings.py
'''


@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['name', 'productId', 'shopId', 'userId', 'p_name', 'c_name', 'r_name']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"code": 400, "errmsg": f"缺少字段： {field}"}, status=400)
            taskid = ''.join(random.choices(string.digits, k=9))
            task = Task.objects.create(
                taskId=taskid,
                name=data.get('name'),
                product_id=data.get('productId'),
                user_id=data.get('userId'),
                shop_id=data.get('shopId'),
                region=f"{data['p_name']}{data['c_name']}{data['r_name']}",
                status='1',
                match_quantity=0,
                willing_quantity=0,
                send_quantity=0,
                total_invitations=0,
                createAt=datetime.now()
            )

            # 调用retrieval接口
            retrieval_url = "http://120.27.208.224:8003/retrival"
            params = {
                "task_id": task.taskId,
                "shop_id": data.get('shopId'),
                "products": Goods.objects.get(product_id=data.get('productId')).match_tag
            }
            response = requests.post(retrieval_url, json=params)

            if response.status_code == 200:
                retrieval_result = response.json()

                # 将返回的数据存入数据库
                for tag, products in retrieval_result.items():
                    for product in products:
                        Creators.objects.create(
                            taskId=task,
                            tag=tag,  # 换成产品名称
                            product=product
                        )

                return JsonResponse({"code": 200, "msg": "任务创建成功"}, status=200)
            else:
                return JsonResponse({"code": response.status_code, "errmsg": "检索接口请求失败"},
                                    status=response.status_code)
        except KeyError as e:
            return JsonResponse({"code": 400, "errmsg": f"缺少字段： {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"code": 404, "errmsg": str(e)}, status=404)


@csrf_exempt
def start_task(request, taskId):
    if request.method == 'POST':

        try:
            task = Task.objects.get(taskId=taskId)
            print(task.status)
            if task.status in ['2', '3']:
                return JsonResponse({'code': 200, 'msg': '该任务已启动'}, status=200)
            else:
                task.status = '2'
                task.save()
                return JsonResponse({'code': 200, 'msg': '任务已成功启动'}, status=200)
        except Task.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '未找到任务'}, status=400)
    else:
        return JsonResponse({'code': 405, 'errmsg': '请求方法不支持'}, status=400)


@csrf_exempt
def list_tasks(request, task_id=None):
    if request.method == 'GET':
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
        try:
            if task_id:
                try:
                    task = Task.objects.get(taskId=task_id)
                    serialized_task = {
                        'taskId': task.taskId,
                        'name': task.name,
                        'product_title': Goods.objects.get(product_id=task.product_id).title,
                        'status': {"1": "未启动", "2": "正在进行", "3": "已完成"}[task.status],
                        'shop_id': task.shop_id,
                        'shop_name': task.shop.shop_name,
                        'send_quantity': task.send_quantity,
                        'willing_quantity': task.willing_quantity,
                        'match_quantity': task.match_quantity,
                        'total_invitations': task.total_invitations,
                        'createAt': task.createAt.strftime('%Y-%m-%d %H:%M:%S'),
                        'user': {
                            'id': task.user.user_id,
                            'username': task.user.username,
                            'email': task.user.email,
                            'number': task.user.number,
                            'company': task.user.company
                        }
                    }
                    return JsonResponse({"code": 200, "task": serialized_task})
                except Task.DoesNotExist:
                    return JsonResponse({"code": 404, "errmsg": "任务不存在"})
            else:
                all_tasks = Task.objects.all().order_by('taskId')
                total_tasks = all_tasks.count()
                size = int(request.GET.get('size', 10))  # 默认大小为 10，如果未提供
                paginator = Paginator(all_tasks, size)
                page_number = request.GET.get('page', 1)  # 默认第一页，如果未提供
                try:
                    tasks = paginator.page(page_number)
                except PageNotAnInteger:
                    tasks = paginator.page(1)
                except EmptyPage:
                    tasks = paginator.page(paginator.num_pages)

                serialized_tasks = []
                for task in tasks:
                    serialized_task = {
                        'taskId': task.taskId,
                        'name': task.name,
                        'product_title': Goods.objects.get(product_id=task.product_id).title,
                        'status': {"1": "未启动", "2": "正在进行", "3": "已完成"}[task.status],
                        'shop_id': task.shop_id,
                        'shop_name': task.shop.shop_name,
                        'send_quantity': task.send_quantity,
                        'willing_quantity': task.willing_quantity,
                        'match_quantity': task.match_quantity,
                        'total_invitations': task.total_invitations,
                        'createAt': task.createAt.strftime('%Y-%m-%d %H:%M:%S'),
                        'user': {
                            'id': task.user.user_id,
                            'username': task.user.username,
                            'email': task.user.email,
                            'number': task.user.number,
                            'company': task.user.company
                        }
                    }
                    serialized_tasks.append(serialized_task)

                return JsonResponse({
                    "code": 200,
                    "tasks": serialized_tasks,
                    "page": tasks.number,
                    "total_pages": paginator.num_pages,
                    "total_tasks": total_tasks
                })
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({'code': 405, 'errmsg': '仅支持 GET 请求'}, status=405)


@csrf_exempt
def get_shop(request, taskId):
    if request.method == 'GET':
        try:
            task = Task.objects.get(taskId=taskId)
            serialized_task = {
                'user_id': task.user_id,
                'shop_id': task.shop_id,
                'shop_name': task.shop.shop_name,
            }
            return JsonResponse({"code": 200, "data": serialized_task}, status=200)
        except Task.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '未找到任务'})
    else:
        return JsonResponse({'code': 405, 'errmsg': '请求方法不支持'}, status=400)


@csrf_exempt
def get_tasks_sum(request):
    if request.method == 'GET':
        send_quantity_sum = Task.objects.aggregate(Sum('send_quantity'))['send_quantity__sum'] or 0
        willing_quantity_sum = Task.objects.aggregate(Sum('willing_quantity'))['willing_quantity__sum'] or 0
        match_quantity_sum = Task.objects.aggregate(Sum('match_quantity'))['match_quantity__sum'] or 0
        total_invitations_sum = Task.objects.aggregate(Sum('total_invitations'))['total_invitations__sum'] or 0
        response_data = {
            "total_invitations_sum": total_invitations_sum,
            "send_quantity_sum": send_quantity_sum,
            "willing_quantity_sum": willing_quantity_sum,
            "match_quantity_sum": match_quantity_sum
        }
        return JsonResponse({"code": 200, "data": response_data}, status=200)


@csrf_exempt
def delete_task(request, taskId):
    if request.method == 'DELETE':
        try:
            task = Task.objects.get(taskId=taskId)
            task.delete()
            return JsonResponse({"code": 200, "msg": "任务删除成功"}, status=200)
        except Task.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '未找到任务'})
    else:
        return JsonResponse({'code': 400, 'errmsg': '请求方法不支持'}, status=400)


'''
查找所有投放任务下发送邀约任务发送成功的达人数量
'''


@csrf_exempt
def get_creator_count(request):
    if request.method == 'POST':
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证，请重新登录'}, status=401)

        # 解码 JWT 令牌以获取用户信息
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'errmsg': '身份认证过期，请重新登录'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'code': 401, 'errmsg': '无效的身份认证，请重新登录'}, status=401)

        user_id = payload.get('user_id')
        if not user_id:
            return JsonResponse({'code': 401, 'errmsg': '无效的用户信息，请重新登录'}, status=401)

        # 获取 RPA 认证信息
        try:
            rpa_key = Rpa_key.objects.get(user_id=user_id)
            username = rpa_key.username
            password = rpa_key.password
        except Rpa_key.DoesNotExist:
            return JsonResponse({'code': 404, 'errmsg': '未找到用户的 RPA 信息'}, status=404)

        # 获取 API 访问令牌
        token = get_token(username, password)
        Authorization = f"Bearer {token}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        # 遍历所有投放计划
        tasks = Task.objects.all()
        update_data = []

        for task in tasks:
            task_id = task.taskId

            # 获取状态为8的成功邀约任务
            successful_invocations = Tk_invacation.objects.filter(delivery_id=task_id, status=8)
            total_creator_cnt = 0

            # 遍历每个邀约任务的 taskId
            for inv_task in successful_invocations:
                inv_task_id = inv_task.taskId

                response = requests.get(
                    f'https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation/{inv_task_id}/detail',
                    headers=headers
                )

                if response.status_code == 200:
                    data = response.json()
                    creator_cnt = data.get('creator_cnt', 0)
                    total_creator_cnt += creator_cnt
                else:
                    # 如果获取达人数量失败，继续下一个任务
                    print(f"获取任务 ID 为 {inv_task_id} 的数据失败。状态码: {response.status_code}")
                    continue

            # 将计算出的达人数量更新到投放计划的 match_quantity 字段
            update_data.append({'taskId': task_id, 'match_quantity': total_creator_cnt})

        # 批量更新 Task 表的 match_quantity 字段
        for update in update_data:
            Task.objects.filter(taskId=update['taskId']).update(match_quantity=update['match_quantity'])

        return JsonResponse({'status': 'success', 'updated_tasks': update_data})

    return JsonResponse({'error': '请求方法无效'}, status=405)


'''
检索接口，http://120.27.208.224:8003/retrival，参数{"task_id": "1234abcd", "shop_id": "qwer222",  "products": "Resistance Bands,Balding Clippers"}
'''


@csrf_exempt
def retrieval(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['task_id', 'shop_id', 'products']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"code": 400, "errmsg": f"缺少字段： {field}"}, status=400)

            params = {
                "task_id": data.get('task_id'),
                "shop_id": data.get('shop_id'),
                "products": data.get('products')
            }
            print(params)
            response = requests.post("http://120.27.208.224:8003/retrival", json=params)
            if response.status_code == 200:
                retrieval_result = response.json()
                product_list = retrieval_result.get(params["products"], [])
                for product in product_list:
                    Creators.objects.create(
                        taskId=params["task_id"],
                        tag=params["products"],
                        product=product,
                    )

                return JsonResponse({"code": 200, "data": retrieval_result}, status=200)
            else:
                return JsonResponse({"code": response.status_code, "errmsg": "检索接口请求失败"},
                                    status=response.status_code)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "请求方法不支持"}, status=405)


'''
对话接口
http://120.27.208.224:8002/chat，参数{"task_id": "2024zxcv","creator": "Maxim","content": "", "shop_id" : "Vexloria", 
"brand":  "Vexloria", "product_info": "Vexloria", "product_link" : "https://shop.tiktok.com", "reward" : "-20% Sales Commission",
 "requirement": "-A 30 - 60 seconds video showing our product", "limits" : "200 dollars"}
'''


@csrf_exempt
def chat(request, taskId):
    if request.method == 'POST':
        try:
            tk_infos = list(Tk_information.objects.filter(taskId=taskId))
            tk_info = tk_infos[-1]
            print(tk_info)
            data = {
                "task_id": tk_info.taskId,
                "creator": tk_info.userName,
                "content": tk_info.content,
                "shop_id": "Vexloria",
                "brand": "Vexloria",
                "product_info": "Vexloria",
                "product_link": "https://shop.tiktok.com/view/product/1729495557098410763?region=US&locale=en",
                "reward": "-15% Sales Commission",
                "requirement": "-A 30 - 60 seconds video showing our product",
                "limits": "0 dollars"
            }
            print(data)
            response = requests.post("http://120.27.208.224:8002/chat", json=data)
            if response.status_code == 200:
                chat_result = response.json()
                print(chat_result)
                tk_chat_obj = Tk_chat.objects.create(
                    taskId=taskId,
                    userName=data["creator"],
                    content=chat_result,
                    sendTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                return JsonResponse({"code": 200, "creator": data["creator"], "creator_content": data["content"],
                                     'sendtime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                     "data": tk_chat_obj.content},
                                    status=200)
            else:
                return JsonResponse({"code": response.status_code, "errmsg": "对话接口请求失败"},
                                    status=response.status_code)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "请求方法不支持"}, status=405)


'''
http://120.27.208.224:8002/chat2
返回信息格式：第一个是生成的回复内容 第二个值是达人是否接受邀约的判断标识(True或False)
根据第二个值你可以判断rpa任务状态，即邀约目的是否达到，为True时需要更新rpa任务的状态
'''


@csrf_exempt
def chat2(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = requests.post("http://120.27.208.224:8002/chat2", json=data)
            if response.status_code == 200:
                return JsonResponse(
                    {"code": 200, "data": data, 'sendtime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                    status=200)
            else:
                return JsonResponse({"code": response.status_code, "errmsg": "对话接口请求失败"},
                                    status=response.status_code)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "请求方法不支持"}, status=405)


'''
获取RPA客户端的密钥
'''


@csrf_exempt
def get_rpa_key(request):
    if request.method == 'POST':
        try:

            with transaction.atomic():
                token = request.COOKIES.get('Authorization')
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']

                # 查询用户信息
                user = User.objects.get(user_id=user_id)
                request_data = json.loads(request.body)
                username = request_data.get('username')
                password = request_data.get('password')

                if not username or not password:
                    return JsonResponse({"code": 400, "errmsg": "缺少用户名或密码"}, status=400)

                # 检查给定的用户名和密码是否已有 RPA 密钥
                rpa_key_obj, created = Rpa_key.objects.get_or_create(
                    username=username,
                    password=password,
                    user_id=user_id,
                    defaults={'key': '', 'has_requested': False}
                )

                if not created and rpa_key_obj.has_requested:
                    # 如果 has_requested 为 True，返回现有的密钥
                    return JsonResponse({
                        "code": 200,
                        "msg": f"{rpa_key_obj.key}",
                        "has_requested": rpa_key_obj.has_requested
                    }, status=200)
                else:
                    # 生成新的 RPA 密钥
                    key = f"{username}:{password}"
                    rpa_key = (base64.b64encode(key.encode('utf-8'))).decode('utf-8')

                    # 更新密钥并将 has_requested 设置为 True
                    rpa_key_obj.username = username
                    rpa_key_obj.password = password
                    rpa_key_obj.key = rpa_key
                    rpa_key_obj.user_id = user_id
                    rpa_key_obj.has_requested = True
                    rpa_key_obj.save()

                    return JsonResponse({
                        "code": 200,
                        "msg": f"RPA密钥为: {rpa_key}",
                        "has_requested": rpa_key_obj.has_requested
                    }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"code": 400, "errmsg": "请求数据格式错误"}, status=400)

        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": f"服务器内部错误: {str(e)}"}, status=500)

    else:
        return JsonResponse({"code": 405, "errmsg": "方法不允许"}, status=405)


@csrf_exempt
def get_db_key(request):
    if request.method == 'POST':
        try:
            token = request.COOKIES.get('Authorization')
            if not token:
                return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'}, status=401)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return JsonResponse({'code': 401, 'errmsg': 'token已过期'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'code': 401, 'errmsg': '无效的token'}, status=401)

            user_id = payload['user_id']

            try:
                rpa_key = Rpa_key.objects.get(user_id=user_id)
            except Rpa_key.DoesNotExist:
                return JsonResponse({"code": 404, "errmsg": "未找到用户的数据库密钥,请先获取RPA客户端秘钥"}, status=404)

            data = {
                "key": rpa_key.key,
                "has_requested": rpa_key.has_requested
            }

            if rpa_key.key:
                return JsonResponse({"code": 200, "data": data}, status=200)
            else:
                return JsonResponse({"code": 404, "errmsg": "未找到用户的数据库密钥"}, status=404)

        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": f"服务器内部错误: {str(e)}"}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "方法不允许"}, status=405)


'''
登录tiktok店铺
'''


@csrf_exempt
def login_shop(request, taskId):
    if request.method == 'POST':
        try:
            token = request.COOKIES.get('Authorization')
            if not token:
                return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'}, status=401)
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            username = Rpa_key.objects.get(user_id=user_id).username
            password = Rpa_key.objects.get(user_id=user_id).password
            access_token = get_token(username, password)
            data = json.loads(request.body)
            task_id = data.get('taskId')
            email = data.get('email')
            password = data.get('password')
            task = Task.objects.get(taskId=task_id)
            shop_id = task.shop_id
            refTaskId = ''.join(random.choices(string.digits, k=9))
            data = {
                "type": 1,
                "region": "US",
                "shopId": shop_id,
                "refTaskId": refTaskId,
                "content": {
                    "method": "email",
                    "email": email,
                    "password": password
                }
            }
            token = 'Bearer ' + access_token
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = 'https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/seller-login'
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                res = response.json()
                return JsonResponse({"code": 200, "data": res}, status=200)
            else:
                return JsonResponse({"code": response.status_code, "errmsg": "登录失败"}, status=response.status_code)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": f"服务器内部错误: {str(e)}"}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "方法不允许"}, status=405)


'''
达人邀约
'''


def get_creator_ids(task_id, start_index, batch_size):
    """ 从数据库中获取创作者 ID 列表 """
    return list(Creators.objects.filter(taskId=task_id)
                .values_list("product", flat=True)
                [start_index:start_index + batch_size])


@csrf_exempt
def tk_invitation(request):
    if request.method == 'POST':
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            username = Rpa_key.objects.get(user_id=user_id).username
            password = Rpa_key.objects.get(user_id=user_id).password
            data = json.loads(request.body)
            task_id = data.get('taskId')

            if not task_id:
                return JsonResponse({"code": 400, "errmsg": "缺少字段： taskId"}, status=400)

            task = Task.objects.get(taskId=task_id)
            user = User.objects.get(user_id=task.user_id)
            products = Goods.objects.filter(product_id=task.product_id).first()
            product_id = task.product_id
            product = Goods.objects.get(product_id=product_id)
            rule_id = product.raidsysrule_id
            rule = RaidsysRule.objects.get(id=rule_id)
            requirement = rule.requirement
            shop_id = task.shop_id

            if not products:
                return JsonResponse({"code": 404, "errmsg": f"找不到与 taskId {task_id} 相关的商品信息。"})

            start_index = 0
            batch_size = 50
            total_tasks_sent = 0
            total_creator_count = 0
            task_details = []

            while True:
                creator_ids = get_creator_ids(task_id, start_index, batch_size)
                if not creator_ids:
                    break

                refTaskId = ''.join(random.choices(string.digits, k=9))  # 生成随机的refTaskId
                n = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))  # 生成字母加数字的组合
                # now = datetime.datetime.now()  # 获取当前时间
                # date_string = now.strftime('%Y%m%d')  # 转换当前时间到"20240905"的格式

                data_to_send = {
                    "type": 2,
                    "region": "US",
                    "refTaskId": refTaskId,
                    "shopId": shop_id,
                    "content": {
                        "name": f"{product.title}-20240906-{n}",
                        "products": [
                            {
                                "productId": task.product_id,
                                "commissionRate": float(products.commissionRate)
                            }
                        ],
                        "creatorIds": creator_ids,
                        "expireDateTime": "2024-09-20",
                        "sampleRule": {
                            "hasFreeSample": True,
                            "sampleQuantity": 10
                        },
                        "message": requirement,
                        "contactInfo": {
                            "email": user.email,
                            "phone": user.number,
                            "country": user.company
                        }
                    }
                }

                url = 'https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation'
                access_token = get_token(username, password)
                token = 'Bearer ' + access_token
                headers = {'Content-Type': 'application/json', 'Authorization': token}
                response = requests.post(url=url, headers=headers, json=data_to_send)

                if response.status_code == 200:
                    res = response.json()
                    Tk_invacation.objects.create(
                        userId=user.user_id,
                        taskId=res.get('taskId'),
                        delivery_id=task_id,
                        type=res.get('type'),
                        region=res.get('region'),
                        refTaskid=res.get('refTaskId'),
                        status=res.get('status'),
                        receivestatus=res.get('receivestatus'),
                        message=res.get('message'),
                        createAt=res.get('createdAt'),
                        complateAt=res.get('complatedAt'),
                    )
                    total_tasks_sent += 1
                    total_creator_count += len(creator_ids)  # 累加总创作者数量
                    task.total_invitations = total_creator_count
                    task.save()
                    print(task.total_invitations)

                    task_details.append({
                        "任务名称": f"YJQ-08-19-{n}",
                        "任务邀约数": len(creator_ids)
                    })  # 记录每个任务的名称和创作者数量
                else:
                    return JsonResponse({"code": response.status_code, "errmsg": "外部接口请求失败"},
                                        status=response.status_code)

                # 更新起始索引
                start_index += batch_size

            return JsonResponse({
                "code": 200,
                "msg": "邀请流程完成",
                "发送的任务总数": total_tasks_sent,
                "总邀约达人数": total_creator_count,  # 返回总创作者数
                "任务详情": task_details  # 返回每个任务的详情
            }, status=200)

        except Task.DoesNotExist:
            return JsonResponse({"code": 404, "errmsg": f"找不到 taskId {task_id} 对应的任务."})
        except User.DoesNotExist:
            return JsonResponse({"code": 404, "errmsg": f"找不到与 taskId {task_id} 相关的用户信息."})
        except Goods.DoesNotExist:
            return JsonResponse({"code": 404, "errmsg": f"找不到与 taskId {task_id} 相关的商品信息."})
        except Exception as e:
            print(e)
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)


@csrf_exempt
def get_invitation(request, taskId):
    if request.method == 'GET':
        try:
            token = request.COOKIES.get('Authorization')
            if not token:
                return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            username = Rpa_key.objects.get(user_id=user_id).username
            password = Rpa_key.objects.get(user_id=user_id).password
            access_token = get_token(username, password)
            token = 'Bearer ' + access_token
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation/{taskId}"
            response = requests.get(url=url, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                data = response.json()
                invitation_msg = Tk_invacation.objects.update(
                    userId=user_id,
                    taskId=data.get('taskId'),
                    delivery_id=taskId,
                    type=data.get('type'),
                    region=data.get('region'),
                    refTaskid=data.get('refTaskId'),
                    status=data.get('status'),
                    receivestatus=data.get('receivestatus'),
                    message=data.get('message'),
                    createAt=data.get('createdAt'),
                    complateAt=data.get('complatedAt'),
                )
                invitation_msg.save()
                return JsonResponse(data, status=200)
            else:
                return JsonResponse({"code": response.status_code, "errmsg": "获取邀请信息失败"},
                                    status=response.status_code)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "请求方法不支持"}, status=405)


'''
达人邀约接收邀约信息
'''


@csrf_exempt
def get_invitation_detail(request, taskId):
    if request.method == 'GET':
        try:
            token = request.COOKIES.get('Authorization')
            if not token:
                return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            username = Rpa_key.objects.get(user_id=user_id).username
            password = Rpa_key.objects.get(user_id=user_id).password
            access_token = get_token(username, password)
            token = 'Bearer ' + access_token
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation/{taskId}/detail"
            response = requests.get(url=url, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                data = response.json()
                creators = [
                    Creator(
                        product_add_cnt=item['product_add_cnt'],
                        content_posted_cnt=item['content_posted_cnt'],
                        base_info=BaseInfo(
                            creator_id=item['base_info']['creator_id'],
                            nick_name=item['base_info']['nick_name'],
                            user_name=item['base_info']['user_name'],
                            # agreement=item['base_info']['agreement'],
                            selection_region=item['base_info']['selection_region']
                        )
                    ) for item in data.get('creator_id_list', [])
                ]

                # 处理 product_list
                products = [
                    Product(
                        product_id=item['product_id'],
                        product_status=item['product_status'],
                        group_product_status=item['group_product_status'],
                        title=item['title'],
                        image=Image(
                            thumb_url_list=item['image']['thumb_url_list']
                        ),
                        item_sold=item['item_sold'],
                        target_commission=item['target_commission'],
                        commission_effective_time=item['commission_effective_time'],
                        open_commission=item['open_commission'],
                        effective_status=item['effective_status']
                    ) for item in data.get('product_list', [])
                ]

                # 创建并保存 MainData 文档
                invitation = Tk_Invitation(
                    id=taskId,
                    name=data['name'],
                    creator_cnt=data['creator_cnt'],
                    creator_added_cnt=data['creator_added_cnt'],
                    creator_posted_cnt=data['creator_posted_cnt'],
                    product_cnt=data['product_cnt'],
                    group_type=data['group_type'],
                    start_time=data['start_time'],
                    end_time=data['end_time'],
                    update_time=data['update_time'],
                    creator_id_list=creators,
                    product_list=products
                )
                invitation.save()
                return JsonResponse(data, status=200)
            else:
                return JsonResponse({"code": response.status_code, "errmsg": "获取邀请信息失败"},
                                    status=response.status_code)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "请求方法不支持"}, status=405)


'''
展示邀约任务的达人
'''
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@csrf_exempt
def get_task_creator(request, taskId):
    if request.method == 'GET':
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})

        # 解析 JWT token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'errmsg': 'Token 已过期'})
        except jwt.DecodeError:
            return JsonResponse({'code': 401, 'errmsg': '无效的 Token'})

        # 获取用户认证信息
        user_id = payload['user_id']
        try:
            user = Rpa_key.objects.get(user_id=user_id)
            username = user.username
            password = user.password
            print(username, password)
        except Rpa_key.DoesNotExist:
            return JsonResponse({'code': 404, 'errmsg': '用户认证信息未找到'})

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
        data = get_rpa_creator(taskId, username, password, page, size)
        return JsonResponse(data, safe=False, status=200)
    else:
        return JsonResponse({"code": 405, "errmsg": "请求方法不支持"}, status=405)


'''
修改RPA任务邀约状态
'''


@csrf_exempt
def modify_rpa_state(request, taskId):
    if request.method == 'PUT':
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            username = Rpa_key.objects.get(user_id=user_id).username
            password = Rpa_key.objects.get(user_id=user_id).password
            data = {
                "status": 1
            }
            access_token = get_token(username, password)
            token = 'Bearer ' + access_token
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = f"https://qtoss-connect.azurewebsites.net/qtoss-rpa/task/{taskId}"
            response = requests.put(url=url, headers=headers, json=data)
            print(response.status_code)
            if response.status_code == 200:
                return JsonResponse({"code": response.status_code, "msg": "修改任务状态成功"}, status=200)
            else:
                return JsonResponse({"code": response.status_code, "errmsg": "修改任务状态失败"},
                                    status=response.status_code)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "请求方法不支持"}, status=405)


'''
达人私信
'''


@csrf_exempt
def seller_im(request, taskId):
    if request.method == 'POST':
        try:
            token = request.COOKIES.get('Authorization')
            if not token:
                return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            username = Rpa_key.objects.get(user_id=user_id).username
            password = Rpa_key.objects.get(user_id=user_id).password
            task = Task.objects.get(taskId=taskId)
            shop_id = task.shop_id
            creator_username = Creators.objects.filter(taskId=task).values_list("product", flat=True).first()
            refTaskId = ''.join(random.choices(string.digits, k=9))  # 生成随机的refTaskId
            data = {
                "type": 3,
                "region": "US",
                "refTaskId": refTaskId,
                "content": {
                    "shopId": shop_id,
                    "UserName": creator_username,
                    "text": "Hi, dear! We have been following your amazing content and believe that your unique style and creativity would be a perfect fit for our brand! We are here to invite you to try and test our yoga ball. If you have any interest, please let us know, so that we can discuss more details. Thank you so much!"
                }
            }
            print(json.dumps(data))
            access_token = get_token(username, password)
            token = 'Bearer ' + access_token
            headers = {'Content-Type': 'application/json', 'Authorization': token}
            url = "https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/seller-im"
            response = requests.post(url=url, headers=headers, json=data)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                _id = ObjectId()
                invitation_instance = Tk_seller_im(
                    _id=_id,
                    userId=data.get('userId'),
                    taskId=data.get('taskId'),
                    type=data.get('type'),
                    region=data.get('region'),
                    status=data.get('status'),
                    refTaskId=data.get('refTaskId'),
                    receiveStatus=data.get('receiveStatus'),
                    sendRetryCount=data.get('sendRetryCount'),
                    sendFailureCode=data.get('sendFailureCode'),
                    message=data.get('message'),
                    createdAt=data.get('createdAt'),
                    completedAt=data.get('completedAt'),
                    checkedAt=data.get('checkedAt'),
                    sentAt=data.get('sentAt')
                )

                # 保存数据到MongoDB
                invitation_instance.save()
                return JsonResponse(data, status=200)
        except Task.DoesNotExist:
            return JsonResponse({"code": 200, "errmsg": "未找到任务"})
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)


'''
达人私信获取私信状态
'''


@csrf_exempt
def get_im(request, taskId):
    try:
        # 获取 token
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})

        # 解析 JWT token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'errmsg': 'Token 已过期'})
        except jwt.DecodeError:
            return JsonResponse({'code': 401, 'errmsg': '无效的 Token'})

        # 获取用户认证信息
        user_id = payload['user_id']
        try:
            user = Rpa_key.objects.get(user_id=user_id)
            username = user.username
            password = user.password
        except Rpa_key.DoesNotExist:
            return JsonResponse({'code': 404, 'errmsg': '用户认证信息未找到'})
        access_token = get_token(username, password)
        token = 'Bearer ' + access_token
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/seller-im/{taskId}"
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            unique_id = str(ObjectId())
            content_data = data.get('content', {})
            content_instance = Content(
                shopId=content_data.get('shopId'),
                creatorId=content_data.get('creatorId'),
                text=content_data.get('text')
            )

            try:
                invitation_instance = Tk_seller_im.objects.get(taskId=data.get('taskId'))

                # 更新字段
                invitation_instance._id = unique_id
                invitation_instance.userId = data.get('userId')
                invitation_instance.type = data.get('type')
                invitation_instance.region = data.get('region')
                invitation_instance.status = data.get('status')
                invitation_instance.refTaskId = data.get('refTaskId')
                invitation_instance.dialogId = data.get('dialogId')
                invitation_instance.receiveStatus = data.get('receiveStatus')
                invitation_instance.sendRetryCount = data.get('sendRetryCount')
                invitation_instance.sendFailureCode = data.get('sendFailureCode')
                invitation_instance.message = data.get('message')
                invitation_instance.content = content_instance
                invitation_instance.createdAt = datetime.fromisoformat(data.get('createdAt').replace('Z', '+00:00'))
                invitation_instance.completedAt = datetime.fromisoformat(
                    data.get('completedAt').replace('Z', '+00:00')) if data.get('completedAt') else None
                invitation_instance.checkedAt = datetime.fromisoformat(
                    data.get('checkedAt').replace('Z', '+00:00')) if data.get('checkedAt') else None
                invitation_instance.sentAt = datetime.fromisoformat(
                    data.get('sentAt').replace('Z', '+00:00')) if data.get('sentAt') else None

                # 保存更新
                invitation_instance.save()
            except DoesNotExist:
                # 如果文档不存在，则创建一个新文档
                invitation_instance = Tk_seller_im(
                    _id=unique_id,
                    userId=data.get('userId'),
                    taskId=data.get('taskId'),
                    type=data.get('type'),
                    region=data.get('region'),
                    status=data.get('status'),
                    refTaskId=data.get('refTaskId'),
                    dialogId=data.get('dialogId'),
                    receiveStatus=data.get('receiveStatus'),
                    sendRetryCount=data.get('sendRetryCount'),
                    sendFailureCode=data.get('sendFailureCode'),
                    message=data.get('message'),
                    content=content_instance,
                    createdAt=datetime.fromisoformat(data.get('createdAt').replace('Z', '+00:00')),
                    completedAt=datetime.fromisoformat(data.get('completedAt').replace('Z', '+00:00')) if data.get(
                        'completedAt') else None,
                    checkedAt=datetime.fromisoformat(data.get('checkedAt').replace('Z', '+00:00')) if data.get(
                        'checkedAt') else None,
                    sentAt=datetime.fromisoformat(data.get('sentAt').replace('Z', '+00:00')) if data.get(
                        'sentAt') else None
                )
                invitation_instance.save()
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({"code": response.status_code, "errmsg": "获取私信信息失败"},
                                status=response.status_code)
    except Exception as e:
        return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)


'''
获取达人私信信息
'''


@csrf_exempt
def get_im_info(request, taskId):
    try:
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        username = Rpa_key.objects.get(user_id=user_id).username
        password = Rpa_key.objects.get(user_id=user_id).password
        access_token = get_token(username, password)
        token = 'Bearer ' + access_token
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/seller-im/{taskId}/detail"
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({"code": response.status_code, "errmsg": "获取达人私信信息失败"},
                                status=response.status_code)
    except Exception as e:
        return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)


'''
获取达人私信聊天记录
'''


@csrf_exempt
def seller_im_msg(request, taskId):
    try:
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        username = Rpa_key.objects.get(user_id=user_id).username
        password = Rpa_key.objects.get(user_id=user_id).password
        access_token = get_token(username, password)
        token = 'Bearer ' + access_token
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/seller-im/{taskId}/receive"
        response = requests.put(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({"code": response.status_code, "errmsg": "获取私信聊天记录失败"},
                                status=response.status_code)
    except Exception as e:
        return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)


'''
获取投放任务下的rpa任务
'''


@csrf_exempt
def get_rpa_tasks(request, taskId):
    try:
        # 获取 token
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})

        # 解析 JWT token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'errmsg': 'Token 已过期'})
        except jwt.DecodeError:
            return JsonResponse({'code': 401, 'errmsg': '无效的 Token'})

        # 获取用户认证信息
        user_id = payload['user_id']
        try:
            user = Rpa_key.objects.get(user_id=user_id)
            username = user.username
            password = user.password
        except Rpa_key.DoesNotExist:
            return JsonResponse({'code': 404, 'errmsg': '用户认证信息未找到'})

        # 获取分页参数
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))

        # 查询任务
        tasks = Tk_invacation.objects.filter(delivery_id=taskId)
        if not tasks.exists():
            return JsonResponse({"code": 204, "errmsg": "未找到任务"})

        data = update_task(taskId, username, password, page, size)
        return JsonResponse(data, safe=False, status=200)

    except Exception as e:
        import traceback
        print("Exception:", str(e))
        print("Traceback:", traceback.format_exc())
        return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)


# @csrf_exempt
# def get_rpa_tasks(request, taskId):
#     try:
#         token = request.COOKIES.get('Authorization')
#         tasks = Tk_invacation.objects.filter(delivery_id=taskId)
#         if not token:
#             return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
#         if not tasks:
#             return JsonResponse({"code": 204, "errmsg": "未找到任务"})
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#         user_id = payload['user_id']
#         username = Rpa_key.objects.get(user_id=user_id).username
#         password = Rpa_key.objects.get(user_id=user_id).password
#         # username = "song"
#         # password = "306012"
#         print(taskId, username, password)
#         data = update_task(taskId, username, password)
#         return data
#
#     except Exception as e:
#         return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)


'''
获取投放任务下的rpa任务
'''
# from django.forms.models import model_to_dict
#
#
# @csrf_exempt
# def get_rpa_tasks(request, taskId):
#     try:
#         tasks = Tk_invacation.objects.filter(delivery_id=taskId)
#         if not tasks:
#             return JsonResponse({"code": 204, "errmsg": "未找到任务"})
#         tasks_data = [model_to_dict(task) for task in tasks]
#
#         return JsonResponse({"code": 200, "data": tasks_data}, status=200)
#
#     except Exception as e:
#         return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)


'''
在邀约前先过滤下达人是否存在
'''


@csrf_exempt
def filter_creator(request, taskId):
    if request.method == 'GET':
        try:
            token = request.COOKIES.get('Authorization')
            if not token:
                return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            username = Rpa_key.objects.get(user_id=user_id).username
            password = Rpa_key.objects.get(user_id=user_id).password
            tasks = Creators.objects.filter(taskId=taskId).values_list("product", flat=True)[0:10]
            for task in tasks:
                params = {
                    "keywords": task
                }
                access_token = get_token(username, password)
                authorization = 'Bearer ' + access_token
                headers = {'Content-Type': 'application/json', 'Authorization': authorization}
                url = f"https://qtoss-crawling-proxy.azurewebsites.net/qtoss-crawling-proxy/tiktok/affiliate-center/creator/search/suggestion"
                response = requests.get(url=url, headers=headers, params=params)
                response.raise_for_status()
                if response.status_code == 200:
                    data = response.json()
                    return JsonResponse(data, status=200)
                else:
                    return JsonResponse({"code": response.status_code, "errmsg": "获取任务失败"},
                                        status=response.status_code)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)
