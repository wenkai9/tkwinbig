import os
import django
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.get_token import get_token

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
django.setup()
from app.task.models import Creators


def fetch_creator_data(keyword, headers, url):
    """单个请求的处理函数"""
    params = {"keywords": keyword}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get("isSuccess"):
            count = response_data["result"].get("count", 0)
            items = response_data["result"].get("items", [])
            return [{"count": count, "userName": item.get("userName"), "keyword": keyword} for item in items]
        else:
            print(f"请求返回失败的响应: {response_data}")
    except requests.exceptions.RequestException as e:
        print(f"请求出现异常: {e}")
    return []


def is_creator(taskId, username, password):
    creators = Creators.objects.filter(taskId=taskId).values('product')
    crt_list = [i['product'] for i in creators]
    access_token = get_token(username, password)
    token = "Bearer " + access_token
    headers = {"Content-Type": "application/json", "Authorization": token}

    url = "https://qtoss-crawling-proxy.azurewebsites.net/qtoss-crawling-proxy/tiktok/affiliate-center/creator/search/suggestion"

    start_time = time.time()

    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_keyword = {executor.submit(fetch_creator_data, keyword, headers, url): keyword for keyword in
                             crt_list}

        for future in as_completed(future_to_keyword):
            result = future.result()
            if result:
                results.extend(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"耗费的时间: {elapsed_time:.2f} 秒")

    return results


# 示例使用
username = "song"
password = "306012"
tasks = "454723797"
results = is_creator(tasks, username, password)
print(results)
