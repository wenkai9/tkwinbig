from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Goods
import json

@csrf_exempt
def upload_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = Goods.objects.create(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                category_id=data['category_id'],
                product_link=data['product_link'],
                shop_id=data['shopId'],  # 正确的字段名
                match_tag=data['match_tag']
            )
            return JsonResponse({
                "product_id": product.id,
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "category_id": product.category_id,
                "product_link": product.product_link,
                "shopId": product.shop_id,
                "match_tag": product.match_tag,
                "createdAt": str(product.createdAt)
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': '只支持 POST 请求'}, status=405)

@csrf_exempt
def get_product(request, product_id):
    if request.method == 'GET':
        try:
            product = Goods.objects.get(id=product_id)
            return JsonResponse({
                "product_id": product.id,
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "category_id": product.category_id,
                "product_link": product.product_link,
                "shopId": product.shop_id,
                "createdAt": str(product.createdAt)
            })
        except Goods.DoesNotExist:
            return JsonResponse({'error': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': '只支持 GET 请求'}, status=405)

@csrf_exempt
def update_product(request, product_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            product = Goods.objects.get(id=product_id)
            product.title = data.get('title', product.title)
            product.description = data.get('description', product.description)
            product.price = data.get('price', product.price)
            product.category_id = data.get('category_id', product.category_id)
            product.product_link = data.get('product_link', product.product_link)
            product.match_tag = data.get('match_tag', product.match_tag)
            product.save()
            return JsonResponse({
                "product_id": product.id,
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "category_id": product.category_id,
                "product_link": product.product_link,
                "shopId": product.shop_id,
                "updatedAt": str(product.updatedAt)
            })
        except Goods.DoesNotExist:
            return JsonResponse({'error': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': '只支持 PUT 请求'}, status=405)

@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            product = Goods.objects.get(id=product_id)
            product.delete()
            return JsonResponse({"message": "删除成功"}, status=204)
        except Goods.DoesNotExist:
            return JsonResponse({'error': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': '只支持 DELETE 请求'}, status=405)

