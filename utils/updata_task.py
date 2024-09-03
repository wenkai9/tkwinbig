from concurrent.futures import ThreadPoolExecutor, as_completed
from math import ceil

from app.task.models import Tk_invacation
from utils.get_token import get_token
from django.core.cache import cache
import requests
import datetime


def update_task(taskId, username, password, page=1, size=10):
    try:
        # 检查并获取缓存中的访问令牌
        cache_key = f'access_token_{username}'
        cached_data = cache.get(cache_key)
        if cached_data and cached_data['expiry'] > datetime.datetime.now():
            access_token = cached_data['token']
        else:
            access_token = get_token(username, password)
            if not access_token:
                return {'code': 401, 'errmsg': '获取访问令牌失败'}
            # 缓存访问令牌和过期时间
            cache.set(cache_key, {
                'token': access_token,
                'expiry': datetime.datetime.now() + datetime.timedelta(minutes=30)
            })

        token = 'Bearer ' + access_token
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        task_ids = Tk_invacation.objects.filter(delivery_id=taskId).values_list("taskId", flat=True)
        print("任务ID列表:", task_ids)

        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_taskid = {executor.submit(fetch_task_data, taskid, headers): taskid for taskid in task_ids}
            for future in as_completed(future_to_taskid):
                taskid = future_to_taskid[future]
                try:
                    data = future.result()
                    if data:
                        updated_count = Tk_invacation.objects.filter(taskId=taskid).update(
                            userId=data.get('userId'),
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
                        print("保存成功")

                        if updated_count > 0:
                            updated_record = Tk_invacation.objects.get(taskId=taskid)
                            results.append({
                                "taskId": updated_record.taskId,
                                "userId": updated_record.userId,
                                "type": updated_record.type,
                                "region": updated_record.region,
                                "refTaskid": updated_record.refTaskid,
                                "status": updated_record.status,
                                "receivestatus": updated_record.receivestatus,
                                "message": updated_record.message,
                            })
                            print(f"任务{taskid}更新成功")
                        else:
                            print(f"更新失败: taskId {taskid}")
                except Exception as e:
                    print(f"获取或更新任务{taskid}时出错: {e}")

        # 分页逻辑
        total_tasks = len(results)
        total_pages = ceil(total_tasks / size)
        page = max(1, min(page, total_pages))  # 确保当前页在有效范围内
        start = (page - 1) * size
        end = start + size
        paginated_results = results[start:end]

        return {
            "code": 200,
            "data": paginated_results,
            "page": page,
            "total_pages": total_pages,
            "total_tasks": total_tasks
        }

    except Exception as e:
        import traceback
        print("上传任务中出现错误:", str(e))
        print("Traceback:", traceback.format_exc())
        return {'code': 500, 'errmsg': str(e)}


def fetch_task_data(taskid, headers):
    try:
        url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation/{taskid}"
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"获取{taskid}任务时出错 : {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"请求任务{taskid}数据时出错: {e}")
        return None

# 第二版获取投放任务下的所有任务
# def update_task(taskId, username, password):
#     try:
#         # 检查并获取缓存中的访问令牌
#         cache_key = f'access_token_{username}'
#         cached_data = cache.get(cache_key)
#         if cached_data and cached_data['expiry'] > datetime.datetime.now():
#             access_token = cached_data['token']
#         else:
#             access_token = get_token(username, password)
#             if not access_token:
#                 return {'code': 401, 'errmsg': '获取访问令牌失败'}
#             # 缓存访问令牌和过期时间
#             cache.set(cache_key, {
#                 'token': access_token,
#                 'expiry': datetime.datetime.now() + datetime.timedelta(minutes=30)
#             })
#
#         token = 'Bearer ' + access_token
#         headers = {'Content-Type': 'application/json', 'Authorization': token}
#         tasks = Tk_invacation.objects.filter(delivery_id=taskId).values_list("taskId", flat=True)
#         print("任务ID列表:", tasks)
#
#         results = []
#         for taskid in tasks:
#             url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation/{taskid}"
#             print(url)
#             response = requests.get(url=url, headers=headers)
#
#             if response.status_code != 200:
#                 print(f"获取{taskid}任务时出错 : {response.status_code} - {response.text}")
#                 continue
#
#             data = response.json()
#
#             # 更新记录
#             updated_count = Tk_invacation.objects.filter(taskId=taskid).update(
#                 userId=data.get('userId'),
#                 taskId=data.get('taskId'),
#                 delivery_id=taskId,
#                 type=data.get('type'),
#                 region=data.get('region'),
#                 refTaskid=data.get('refTaskId'),
#                 status=data.get('status'),
#                 receivestatus=data.get('receivestatus'),
#                 message=data.get('message'),
#                 createAt=data.get('createdAt'),  # 处理时间字段
#                 complateAt=data.get('complatedAt'),  # 处理时间字段
#             )
#             print("保存成功")
#
#             if updated_count > 0:
#                 try:
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
#                     })
#                     print(f"任务{taskid}更新成功")
#                 except Tk_invacation.DoesNotExist:
#                     print(f"更新后找不到taskId为{taskId}的记录")
#             else:
#                 print(f"更新失败: taskId {taskid}")
#
#         return {"code": 200, "data": results}
#
#     except Exception as e:
#         import traceback
#         print("上传任务中出现错误:", str(e))
#         print("Traceback:", traceback.format_exc())
#         return {'code': 500, 'errmsg': str(e)}


# 第一版获取投放任务下的所有任务
# def update_task(taskId, username, password):
#     try:
#         access_token = get_token(username, password)
#         if not access_token:
#             return {'code': 401, 'errmsg': '获取访问令牌失败'}
#
#         token = 'Bearer ' + access_token
#         headers = {'Content-Type': 'application/json', 'Authorization': token}
#         tasks = Tk_invacation.objects.filter(delivery_id=taskId).values_list("taskId", flat=True)
#         print("任务ID列表:", tasks)
#
#         results = []
#         for taskid in tasks:
#             url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation/{taskid}"
#             print(url)
#             response = requests.get(url=url, headers=headers)
#
#             if response.status_code != 200:
#                 print(f"获取{taskid}任务时出错 : {response.status_code} - {response.text}")
#                 continue
#
#             data = response.json()
#
#             # 更新记录
#             updated_count = Tk_invacation.objects.filter(taskId=taskid).update(
#                 userId=data.get('userId'),
#                 taskId=data.get('taskId'),
#                 delivery_id=taskId,
#                 type=data.get('type'),
#                 region=data.get('region'),
#                 refTaskid=data.get('refTaskId'),
#                 status=data.get('status'),
#                 receivestatus=data.get('receivestatus'),
#                 message=data.get('message'),
#                 createAt=data.get('createdAt'),  # 处理时间字段
#                 complateAt=data.get('complatedAt'),  # 处理时间字段
#             )
#             print("保存成功")
#
#             if updated_count > 0:
#                 try:
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
#                     })
#                     print(f"任务{taskid}更新成功")
#                 except Tk_invacation.DoesNotExist:
#                     print(f"更新后找不到taskId为{taskId}的记录")
#             else:
#                 print(f"更新失败: taskId {taskid}")
#
#         return {"code": 200, "data": results}
#
#     except Exception as e:
#         import traceback
#         print("上传任务中出现错误:", str(e))
#         print("Traceback:", traceback.format_exc())
#         return {'code': 500, 'errmsg': str(e)}
