import io

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Goods
import json
import csv


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


@csrf_exempt
def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'File is not a CSV'}, status=400)

        # Assuming the CSV file has headers: "商品标签", "商品描述", "商品价格", "商品类目id", "商品链接", "商品的店铺id"
        csv_data = csv.reader(io.TextIOWrapper(csv_file, encoding='gb2312'))
        headers = next(csv_data)
        products = []
        for row in csv_data:
            product = {
                "商品标签": row[0],
                "商品描述": row[1],
                "商品价格": row[2],
                "商品类目id": row[3],
                "商品链接": row[4],
                "商品的店铺id": row[5],
                "匹配标签": row[0] + row[3]  # 标题+类目
            }
            products.append(product)

        # 在这里执行将数据保存到数据库的操作
        for product in products:
            try:
                Goods.objects.create(
                    title=product['商品描述'],
                    description=product['商品描述'],
                    price=product['商品价格'],
                    category_id=product['商品类目id'],
                    product_link=product['商品链接'],
                    shop_id=product['商品的店铺id'],
                    match_tag=product['匹配标签']
                )
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'success': True, 'products': products}, status=200)

    return JsonResponse({'error': 'Invalid request method or file not provided'}, status=400)
