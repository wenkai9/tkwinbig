import json

from botocore.paginate import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage

from app.task.models import Tk_Invitation, Product, Image, BaseInfo, Creator, Tk_invacation, Task
import requests

from utils.get_token import get_token


def get_rpa_creator(taskId, username, password, page=1, size=10):
    try:
        access_token = get_token(username, password)
        token = 'Bearer ' + access_token
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        url = f"https://qtoss-connect.azurewebsites.net/qtoss-connect/tiktok/creator-invitation/{taskId}/detail"
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            data = response.json()
            creators = [
                Creator(
                    product_add_cnt=item['product_add_cnt'],
                    content_posted_cnt=item['content_posted_cnt'],
                    base_info=BaseInfo(
                        creator_id=item['base_info']['creator_id'],
                        nick_name=item['base_info']['nick_name'],
                        user_name=item['base_info']['user_name'],
                        selection_region=item['base_info']['selection_region']
                    )
                ) for item in data.get('creator_id_list', [])
            ]
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
            invitation = Tk_Invitation.objects(id=taskId).first()
            creators = invitation.creator_id_list
            start = (page - 1) * size
            end = start + size
            paginated_creators = creators[start:end]

            creator_data = [
                {
                    "creator_id": creator['base_info']['creator_id'],
                    "nick_name": creator['base_info']['nick_name'],
                    "user_name": creator['base_info']['user_name'],
                    "selection_region": creator['base_info']['selection_region'],
                    "product_add_cnt": creator['product_add_cnt'],
                    "content_posted_cnt": creator['content_posted_cnt']
                }
                for creator in paginated_creators
            ]
            total_creators = len(creators)
            total_pages = (total_creators + size - 1) // size

            return {
                "code": 200,
                "creators": creator_data,
                "page": page,
                "total_pages": total_pages,
                "total_creators": total_creators
            }
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
    except Exception as e:
        print(f"发生了意外错误: {e}")
        return None
