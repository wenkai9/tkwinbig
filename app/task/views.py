from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Task
from ..goods.models import Goods
from ..shops.models import Shop
from ..users.models import User
from ..areas.models import Area
from datetime import datetime
import json


@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['name', 'productId', 'shopId', 'userId', 'p_name', 'c_name', 'r_name']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"code": 400, "errmsg": f"缺少字段： {field}"}, status=400)
            task = Task.objects.create(
                name=data.get('name'),
                product_id=data.get('productId'),
                user_id=data.get('userId'),
                shop_id=data.get('shopId'),
                region=f"{data['p_name']}-{data['c_name']}-{data['r_name']}",
                status='1',
                match_quantity=data.get('match_quantity'),
                willing_quantity=data.get('willing_quantity'),
                send_quantity=data.get('send_quantity'),
                createAt=datetime.now()
            )

            task_data = {
                'taskId': task.taskId,
                "name": task.name,
                "productId": task.product_id,
                "userId": task.user_id,
                "shopId": task.shop_id,
                "status": task.status,
                "region": task.region,  # 返回包含省市区名称的 region 字段
                "match_quantity": task.match_quantity,
                "willing_quantity": task.willing_quantity,
                "send_quantity": task.send_quantity,
                "createAt": task.createAt.strftime("%Y-%m-%d %H:%M:%S")
            }
            return JsonResponse({"code": 200, "msg": "任务创建成功", "data": task_data}, status=200)
        except KeyError as e:
            return JsonResponse({"code": 400, "errmsg": f"缺少字段： {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"code": 400, "errmsg": str(e)}, status=404)


@csrf_exempt
def start_task(request, taskId):
    if request.method == 'POST':
        try:
            task = Task.objects.get(taskId=taskId)
            if task.status in ['2', '3']:
                return JsonResponse({'code': 200, 'msg': '该任务已启动'}, status=200)
            else:
                task.status = '2'
                task.save()
                return JsonResponse({'code': 200, 'msg': '任务已成功启动'}, status=200)
        except Task.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '未找到任务'}, status=400)
    else:
        return JsonResponse({'code': 400, 'errmsg': '请求方法不支持'}, status=400)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def list_tasks(request, page=None):
    if request.method == 'GET':
        all_tasks = Task.objects.all().order_by('taskId')
        total_tasks = all_tasks.count()
        # 从请求中获取 size 参数，如果未提供，默认为 10
        size = int(request.GET.get('size', 10))
        paginator = Paginator(all_tasks, size)
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)
        serialized_tasks = []
        for task in tasks:
            serialized_task = {
                'taskId': task.taskId,
                'name': task.name,
                'product_title': Goods.objects.get(id=task.product_id).title,
                'status': {"1": "未启动", "2": "正在进行", "3": "已完成"}[task.status],
                'send_quantity': task.send_quantity,
                'willing_quantity': task.willing_quantity,
                'match_quantity': task.match_quantity,
                'createAt': task.createAt.strftime('%Y-%m-%d %H:%M:%S'),
                # 包含用户信息
                'user': {
                    'id': task.user.user_id,
                    'username': task.user.username,
                    'email': task.user.email,
                    'number': task.user.number,
                    'company': task.user.company
                }
            }
            serialized_tasks.append(serialized_task)
        return JsonResponse(
            {"code": 200, "tasks": serialized_tasks, "page": tasks.number, "total_tasks": total_tasks})
    else:
        return JsonResponse({'code': 400, 'errmsg': '请求方法不支持'}, status=400)


@csrf_exempt
def get_tasks_sum(request):
    if request.method == 'GET':
        send_quantity_sum = Task.objects.aggregate(Sum('send_quantity'))['send_quantity__sum'] or 0
        willing_quantity_sum = Task.objects.aggregate(Sum('willing_quantity'))['willing_quantity__sum'] or 0
        match_quantity_sum = Task.objects.aggregate(Sum('match_quantity'))['match_quantity__sum'] or 0
        response_data = {
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
            return JsonResponse({'code': 400, 'errmsg': '未找到任务'}, status=400)
    else:
        return JsonResponse({'code': 400, 'errmsg': '请求方法不支持'}, status=400)
