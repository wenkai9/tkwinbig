import json

import jwt
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from .models import Shop

'''
需要用户去填写tk的店铺id
'''


@csrf_exempt
@require_http_methods(["POST"])
def create_shop(request):
    try:
        shopId = request.POST.get('shopId')
        shop_name = request.POST.get('shop_name')
        location = request.POST.get('location')
        description = request.POST.get('description')

        shop = Shop.objects.create(
            shopId=shopId,
            shop_name=shop_name,
            location=location,
            description=description,
            createAt=datetime.now()
        )

        return JsonResponse({"code": 200,
                             "shopId": shop.shopId,
                             "shop_name": shop.shop_name,
                             "location": shop.location,
                             "description": shop.description,
                             "createAt": shop.createAt.strftime("%Y-%m-%d %H:%M:%S")
                             }, status=200)
    except Exception as e:
        # 发生异常时返回错误响应
        return JsonResponse({"code": 400, "error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def list_shops(request, page=None):
    try:
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        # user_id = "20"
        # all_shops = Shop.objects.all().order_by('shopId')
        all_shops = Shop.objects.filter(user_id=user_id).order_by('shopId')

        size = int(request.GET.get('size', 10))

        paginator = Paginator(all_shops, size)

        page_number = request.GET.get('page')
        if page_number is None:
            page_number = 1
        else:
            page_number = int(page_number)

        try:
            shops = paginator.page(page_number)
        except PageNotAnInteger:
            shops = paginator.page(1)
        except EmptyPage:
            # 如果页码超出范围（例如9999），则返回最后一页的结果
            shops = paginator.page(paginator.num_pages)

        # 序列化数据
        serialized_shops = [{
            "shopId": shop.shopId,
            "shop_name": shop.shop_name,
            "location": shop.location,
            "description": shop.description,
            "user_id": shop.user_id,
            "createAt": shop.createAt.strftime("%Y-%m-%d %H:%M:%S")
        } for shop in shops]

        return JsonResponse(
            {"code": 200, "shops": serialized_shops, "page": shops.number, "total_pages": paginator.num_pages,
             "total_shops": paginator.count},
            status=200)
    except Exception as e:
        return JsonResponse({"code": 500, "error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def view_shop(request, shopId):
    try:
        shop = Shop.objects.get(shopId=shopId)
        return JsonResponse({"code": 200,
                             "shopId": shop.shopId,
                             "shop_name": shop.shop_name,
                             "location": shop.location,
                             "description": shop.description,
                             "createAt": shop.createAt.strftime("%Y-%m-%d %H:%M:%S")
                             }, status=200)
    except Shop.DoesNotExist:
        return JsonResponse({"code": 404, "errmsg": "店铺不存在"}, status=404)


@csrf_exempt
@require_http_methods(["PUT"])
def update_shop(request, shopId):
    try:
        shop = Shop.objects.get(shopId=shopId)

        # 检查请求体是否为空
        if request.body:
            # 解析 JSON 数据
            data = json.loads(request.body)

            # 更新店铺信息
            shop.shop_name = data.get('shop_name')
            shop.location = data.get('location')
            shop.description = data.get('description')

            shop.save()

            return JsonResponse({"code": 200, 'msg': '成功更新店铺信息'}, status=200)
        else:
            return JsonResponse({"code": 400, 'errmsg': '请求体为空'}, status=400)
    except Shop.DoesNotExist:
        return JsonResponse({"code": 404, 'errmsg': '未找到店铺'}, status=404)
    except json.decoder.JSONDecodeError:
        return JsonResponse({"code": 400, 'errmsg': '请求体中包含无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_shop(request, shopId):
    try:
        shop = Shop.objects.get(shopId=shopId)
        shop.delete()
        return JsonResponse({"code": 200, "msg": "成功删除店铺"}, status=200)
    except Shop.DoesNotExist:
        return JsonResponse({"code": 404, "errmsg": "店铺不存在"}, status=404)
