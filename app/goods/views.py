from openpyxl import Workbook
import io
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
                primary_category=data['primary_category'],
                secondary_category=data['secondary_category'],
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
                "primary_category": product.primary_category,
                "secondary_category": product.secondary_category,
                "product_link": product.product_link,
                "shopId": product.shop_id,
                "match_tag": product.match_tag,
                "createdAt": str(product.createdAt)
            }, status=200)
        except Exception as e:
            return JsonResponse({'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({'errmsg': '只支持 POST 请求'}, status=405)


@csrf_exempt
def list_products(request):
    if request.method == 'GET':
        # 检索所有商品并按照商品ID排序
        all_products = Goods.objects.all().order_by('id')

        # 分页
        paginator = Paginator(all_products, 3)  # 每页显示3个商品
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # 如果页码不是整数，则返回第一页
            products = paginator.page(1)
        except EmptyPage:
            # 如果页码超出范围（例如9999），则返回最后一页的结果
            products = paginator.page(paginator.num_pages)

        # 序列化数据
        serialized_products = [{
            "product_id": product.id,
            "title": product.title,
            "description": product.description,
            "price": str(product.price),
            "category_id": product.category_id,
            "primary_category": product.primary_category,
            "secondary_category": product.secondary_category,
            "product_link": product.product_link,
            "shopId": product.shop_id,
            "match_tag": product.match_tag,
            "createdAt": str(product.createdAt)
        } for product in products]

        return JsonResponse({"products": serialized_products, "page": products.number, "total_pages": paginator.num_pages})
    else:
        return JsonResponse({'errmsg': '只支持 GET 请求'}, status=405)




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
                "primary_category": product.primary_category,
                "secondary_category": product.secondary_category,
                "product_link": product.product_link,
                "shopId": product.shop_id,
                "match_tag": product.match_tag,
                "createdAt": str(product.createdAt)
            })
        except Goods.DoesNotExist:
            return JsonResponse({'errmsg': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({'errmsg': '只支持 GET 请求'}, status=405)


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
            product.primary_category = data.get('primary_category', product.primary_category)
            product.secondary_category = data.get('secondary_category', product.secondary_category)
            product.product_link = data.get('product_link', product.product_link)
            product.match_tag = data.get('match_tag', product.match_tag)
            product.save()
            return JsonResponse({
                "product_id": product.id,
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "category_id": product.category_id,
                "primary_category": product.primary_category,
                "secondary_category": product.secondary_category,
                "product_link": product.product_link,
                "shopId": product.shop_id,
                "match_tag": product.match_tag,
                "updatedAt": str(product.updatedAt)
            })
        except Goods.DoesNotExist:
            return JsonResponse({'errmsg': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({'errmsg': '只支持 PUT 请求'}, status=405)


@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            product = Goods.objects.get(id=product_id)
            product.delete()
            return JsonResponse({"msg": "删除成功"}, status=204)
        except Goods.DoesNotExist:
            return JsonResponse({'errmsg': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({'errmsg': '只支持 DELETE 请求'}, status=405)


@csrf_exempt
def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'errmsg': 'File is not a CSV'}, status=400)

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
                "一级分类": row[4],
                "二级分类": row[5],
                "商品链接": row[6],
                "商品的店铺id": row[7],
                "匹配标签": row[0] + row[4]  # 标题+类目
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
                    primary_category=product['一级分类'],
                    secondary_category=product['二级分类'],
                    product_link=product['商品链接'],
                    shop_id=product['商品的店铺id'],
                    match_tag=product['匹配标签']
                )
            except Exception as e:
                return JsonResponse({'errmsg': str(e)}, status=500)

        return JsonResponse({'success': True, 'products': products}, status=200)

    return JsonResponse({'errmsg': 'Invalid request method or file not provided'}, status=400)


@csrf_exempt
def download_excel(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="products.xlsx"'

        # 创建一个工作簿并添加一个工作表
        wb = Workbook()
        ws = wb.active
        ws.append(['商品ID', '标题', '描述', '价格', '类目ID',
                   '一级分类', '二级分类', '商品链接',
                   '店铺ID', '匹配标签', '创建时间', '更新时间'])

        # 获取所有商品
        all_products = Goods.objects.all()

        # 将产品数据写入工作表
        for product in all_products:
            ws.append([product.id, product.title, product.description, str(product.price),
                       product.category_id, product.primary_category, product.secondary_category,
                       product.product_link, product.shop_id, product.match_tag,
                       str(product.createdAt), str(product.updatedAt)])

        # 将工作簿保存到响应中
        wb.save(response)
        return response
    else:
        return JsonResponse({'errmsg': '只支持 GET 请求'}, status=405)