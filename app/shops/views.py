import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Shop


@csrf_exempt
@require_http_methods(["POST"])
def create_shop(request):
    shopId = int(request.POST.get('shopId'))
    shop_name = request.POST.get('shop_name')
    location = request.POST.get('location')
    description = request.POST.get('description')

    # 创建店铺
    shop = Shop.objects.create(
        shop_name=shop_name,
        location=location,
        description=description,
        shopId=shopId,
        createAt=datetime.now()
    )

    # 返回创建成功的响应
    return JsonResponse({
        "shopId": shop.shopId,
        "shop_name": shop.shop_name,
        "location": shop.location,
        "description": shop.description,
        "createAt": shop.createAt.strftime("%Y-%m-%d %H:%M:%S")
    }, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def view_shop(request, shopId):
    try:
        shop = Shop.objects.get(shopId=shopId)
        return JsonResponse({
            "shopId": shop.shopId,
            "shop_name": shop.shop_name,
            "location": shop.location,
            "description": shop.description,
            "createAt": shop.createAt.strftime("%Y-%m-%d %H:%M:%S")
        })
    except Shop.DoesNotExist:
        return JsonResponse({"error": "店铺不存在"}, status=404)


# @csrf_exempt
# @require_http_methods(["PUT"])
# def update_shop(request, shopId):
#     try:
#         shop = Shop.objects.get(shopId=shopId)
#         shop.shop_name = request.POST.get('shop_name')
#         shop.location = request.POST.get('location')
#         shop.description = request.POST.get('description')
#         shop.save()
#
#         return JsonResponse({
#             "shopId": shop.shopId,
#             "shop_name": shop.shop_name,
#             "location": shop.location,
#             "description": shop.description,
#             "updateAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         })
#     except Shop.DoesNotExist:
#         return JsonResponse({"error": "店铺不存在"}, status=404)

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

            return JsonResponse({'message': '成功更新店铺信息'})
        else:
            return JsonResponse({'error': '请求体为空'}, status=400)
    except Shop.DoesNotExist:
        return JsonResponse({'error': '未找到店铺'}, status=404)
    except json.decoder.JSONDecodeError:
        return JsonResponse({'error': '请求体中包含无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_shop(request, shopId):
    try:
        shop = Shop.objects.get(shopId=shopId)
        shop.delete()
        return JsonResponse({"message": "成功删除店铺"}, status=200)
    except Shop.DoesNotExist:
        return JsonResponse({"error": "店铺不存在"}, status=404)
