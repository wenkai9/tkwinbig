import io
import os
import oss2
import json
import csv
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from ..shops.models import Shop
from .models import base_category1, base_category2, Goods
from openpyxl import Workbook
from djangoProject1 import settings


@csrf_exempt
def add_product(request, page=None):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 检查 shop_id 是否存在
            try:
                Shop.objects.get(pk=data['shopId'])
            except ObjectDoesNotExist:
                return JsonResponse({"code": 400, 'errmsg': '无效的店铺 ID'}, status=400)
            try:
                base_category = base_category2.objects.get(pk=data['base_category2_id'])
            except ObjectDoesNotExist:
                return JsonResponse({"code": 400, 'errmsg': '无效的二级分类 ID'}, status=400)
            match_tag = f"{data['title']}_{base_category.name}"
            product = Goods.objects.create(
                title=data['title'],
                description=data['description'],
                price=data['price'],
                base_category2_id=data['base_category2_id'],
                product_link=data['product_link'],
                shop_id=data['shopId'],  # 正确的字段名
                match_tag=match_tag,
                hasFreeSample=data['hasFreeSample'],
                commissionRate=data['commissionRate'],
                CooperationFee=data['CooperationFee']
            )
            data = {
                "product_id": product.id,
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "base_category2_id": product.base_category2_id,
                "product_link": product.product_link,
                "shopId": product.shop_id,
                "match_tag": product.match_tag,
                "hasFreeSample": product.hasFreeSample,
                "commissionRate": product.commissionRate,
                "CooperationFee": product.CooperationFee,
                "createdAt": str(product.createdAt)
            }
            return JsonResponse({"code": 200, "msg": "商品添加成功", "data": data}, status=200)
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
    elif request.method == 'GET':
        try:
            category2_data = list(base_category2.objects.values('id', 'name'))
            paginate_category2 = Paginator(category2_data, request.GET.get('size', 10))
            page_number_category2 = request.GET.get('page_category2', 1)
            shop_data = list(Shop.objects.values('shopId', 'shop_name', 'location', 'description'))
            paginator_shop = Paginator(shop_data, request.GET.get('size', 10))
            page_shop_number = request.GET.get('page')
            try:
                category2_data_page = paginate_category2.page(page_number_category2)
                shop_data_page = paginator_shop.page(page_shop_number)
            except PageNotAnInteger:
                category2_data_page = paginate_category2.page(1)
                shop_data_page = paginator_shop.page(1)
            except EmptyPage:
                category2_data_page = paginate_category2.page(paginate_category2.num_pages)
                shop_data_page = paginator_shop.page(paginator_shop.num_pages)

            return JsonResponse(
                {"code": 200, 'category2_data': list(category2_data_page), 'shop_data': list(shop_data_page),
                 'total_categories': paginate_category2.count,
                 'total_shops': paginator_shop.count,
                 'page_category2': category2_data_page.number,
                 'page_shop': shop_data_page.number}, status=200)
        except ObjectDoesNotExist as e:
            return JsonResponse({"code": 400, 'errmsg': str(e)}, status=400)
    else:
        return JsonResponse({"code": 405, 'errmsg': 'Unsupported method'}, status=405)


@csrf_exempt
def list_products(request, page=None):
    if request.method == 'GET':
        try:
            size = int(request.GET.get('size', 10))  # 如果未提供，默认为 10
            all_products = Goods.objects.all().order_by('id')
            paginator = Paginator(all_products, size)
            page_number = request.GET.get('page')
            try:
                products = paginator.page(page_number)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
            serialized_products = [{
                "product_id": product.id,
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "base_category2_id": product.base_category2_id,
                "product_link": product.product_link,
                "shopId": product.shop_id,
                "match_tag": product.match_tag,
                "hasFreeSample": product.hasFreeSample,
                "commissionRate": product.commissionRate,
                "CooperationFee": product.CooperationFee,
                "createdAt": str(product.createdAt)
            } for product in products]
            return JsonResponse({
                "code": 200,
                "products": serialized_products,
                "page": products.number,
                "total_pages": paginator.num_pages,
                "total_products": paginator.count
            })
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, 'errmsg': '仅支持 GET 请求'}, status=405)


@csrf_exempt
def get_product(request, product_id):
    if request.method == 'GET':
        try:
            product = Goods.objects.get(id=product_id)
            data = {
                "product_id": product.id,
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "base_category2_id": product.base_category2_id,
                "product_link": product.product_link,
                "shopId": product.shop_id,
                "match_tag": product.match_tag,
                "hasFreeSample": product.hasFreeSample,
                "commissionRate": product.commissionRate,
                "CooperationFee": product.CooperationFee,
                "createdAt": str(product.createdAt)
            }
            return JsonResponse({"code": 200, "data": data}, status=200)
        except Goods.DoesNotExist:
            return JsonResponse({"code": 400, 'errmsg': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)


@csrf_exempt
def update_product(request, product_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            # 验证 title 和 description 是否被正确提供
            title = data.get('title')
            description = data.get('description')
            if not title or not description:
                return JsonResponse({"code": 400, 'errmsg': '标题和描述为必填项'}, status=400)

            product = Goods.objects.get(id=product_id)
            # 更新商品信息
            product.title = title
            product.description = description
            product.price = data.get('price', product.price)
            product.base_category2_id = data.get('base_category2_id', product.base_category2_id)
            product.product_link = data.get('product_link', product.product_link)
            product.match_tag = data.get('match_tag', product.match_tag)
            product.hasFreeSample = data.get('hasFreeSample', product.hasFreeSample)
            product.commissionRate = data.get('commissionRate', product.commissionRate)
            product.CooperationFee = data.get('CooperationFee', product.CooperationFee)
            product.save()
            # 返回更新后的商品信息
            data = {
                "product_id": product.id,
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "base_category2_id": product.base_category2_id,
                "product_link": product.product_link,
                "shopId": product.shop_id,
                "match_tag": product.match_tag,
                "hasFreeSample": product.hasFreeSample,
                "commissionRate": product.commissionRate,
                "CooperationFee": product.CooperationFee,
                "updatedAt": str(product.updatedAt)
            }
            return JsonResponse({"code": 200, "msg": "商品信息更新成功", "data": data}, status=200)
        except Goods.DoesNotExist:
            return JsonResponse({"code": 404, 'errmsg': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, 'errmsg': '只支持 PUT 请求'}, status=405)


@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            product = Goods.objects.get(id=product_id)
            product.delete()
            return JsonResponse({"code": 200, "msg": "删除成功"}, status=200)
        except Goods.DoesNotExist:
            return JsonResponse({"code": 404, 'errmsg': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, 'errmsg': '只支持 DELETE 请求'}, status=405)


@csrf_exempt
def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return JsonResponse({"code": 400, 'errmsg': 'File is not a CSV'}, status=400)

        csv_data = csv.reader(io.TextIOWrapper(csv_file, encoding='gb2312'))
        headers = next(csv_data)
        products = []
        for row in csv_data:
            try:
                base_category = base_category2.objects.get(pk=row[6])
            except ObjectDoesNotExist:
                return JsonResponse({"code": 400, 'errmsg': '无效的二级分类 ID'}, status=400)
            match_tag = f"{row[0]}_{base_category.name}"
            product = {
                "商品标签": row[0],
                "商品描述": row[1],
                "商品价格": row[2],
                "是否免费寄送样品": row[3],
                "佣金率": row[4],
                "合作费": row[5],
                "商品二级类目id": row[6],
                "商品链接": row[7],
                "商品的店铺id": row[8],
                "匹配标签": match_tag
            }
            products.append(product)

        # 在这里执行将数据保存到数据库的操作
        for product in products:
            try:
                Goods.objects.create(
                    title=product['商品描述'],
                    description=product['商品描述'],
                    price=product['商品价格'],
                    hasFreeSample=product['是否免费寄送样品'],
                    commissionRate=product['佣金率'],
                    CooperationFee=product['合作费'],
                    base_category2_id=product['商品二级类目id'],
                    product_link=product['商品链接'],
                    shop_id=product['商品的店铺id'],
                    match_tag=product['匹配标签']
                )
            except Exception as e:
                return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)

        return JsonResponse({"code": 200, 'success': True, 'products': products}, status=200)

    return JsonResponse({"code": 400, 'errmsg': '请求方法无效或未提供文件'}, status=400)


# @csrf_exempt
# def upload_csv(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']
#         if not csv_file.name.endswith('.csv'):
#             return JsonResponse({"code": 400, 'errmsg': '不是csv类型的文件'}, status=400)
#         csv_data = csv.reader(io.TextIOWrapper(csv_file, encoding='gb2312'))
#         headers = next(csv_data)
#         products = []
#         for row in csv_data:
#             product = {
#                 "商品标签": row[0],
#                 "商品描述": row[1],
#                 "商品价格": row[2],
#                 "商品二级类目id": row[3],
#                 "商品链接": row[4],
#                 "商品的店铺id": row[5],
#                 "匹配标签": row[0] + row[3]  # 标题+类目
#             }
#             products.append(product)
#             for product in products:
#                 try:
#                     Goods.objects.create(
#                         title=product['商品描述'],
#                         description=product['商品描述'],
#                         price=product['商品价格'],
#                         base_category2_id=product['商品二级类目id'],
#                         product_link=product['商品链接'],
#                         shop_id=product['商品的店铺id'],
#                         match_tag=product['匹配标签']
#                     )
#                 except Exception as e:
#                     return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
#         # 连接阿里云OSS
#         access_key_id = '***'
#         access_key_secret = '***'
#         bucket_name = 'tkwb-samples'
#         endpoint = 'tkwb-samples.oss-cn-shanghai.aliyuncs.com'
#         auth = oss2.Auth(access_key_id, access_key_secret)
#         print(auth)
#         bucket = oss2.Bucket(auth, endpoint, bucket_name)
#         print(bucket)
#         oss_file_name = 'cs_data/upload_csv.csv'  # 在OSS中的文件名
#         print(oss_file_name)
#         with open(csv_file.temporary_file_path(), 'rb') as f:
#             bucket.put_object(oss_file_name, f)
#             print('上传成功')
#         return JsonResponse({"code": 200, 'success': True, 'products': products, 'oss_file_name': oss_file_name},
#                             status=200)
#     return JsonResponse({"code": 400, 'errmsg': '请求方法无效或未提供文件'}, status=400)


@csrf_exempt
def download_excel(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="products.xlsx"'

        # 创建一个工作簿并添加一个工作表
        wb = Workbook()
        ws = wb.active
        ws.append(['商品ID', '标题', '描述', '价格', '是否免费寄送样品', '佣金率', '合作费', '二级类目ID', '商品链接',
                   '店铺ID', '匹配标签', '创建时间', '更新时间'])

        # 获取所有商品
        all_products = Goods.objects.all()

        # 将产品数据写入工作表
        for product in all_products:
            ws.append([product.id, product.title, product.description, str(product.price),
                       product.hasFreeSample, product.commissionRate, product.CooperationFee,
                       product.base_category2_id,
                       product.product_link, product.shop_id, product.match_tag,
                       str(product.createdAt), str(product.updatedAt)])

        # 将工作簿保存到响应中
        wb.save(response)
        return response
    else:
        return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)


def list_category_products(request):
    if request.method == 'GET':
        # 获取所有一级分类
        all_primary_categories = base_category1.objects.all()
        all_category_products = []

        # 获取每个一级分类下的二级分类及其商品信息
        for primary_category in all_primary_categories:
            category_data = {
                "primary_category_id": primary_category.id,
                "primary_category_name": primary_category.name,
                "secondary_categories": []
            }
            secondary_categories = base_category2.objects.filter(category1=primary_category)
            for secondary_category in secondary_categories:
                category_products = Goods.objects.filter(base_category2=secondary_category)

                # 分页逻辑
                page_number = int(request.GET.get('page', 1))
                page_size = 20
                start_index = (page_number - 1) * page_size
                end_index = start_index + page_size

                serialized_products = [{
                    "id": product.id,
                    "title": product.title,
                    "description": product.description,
                    "price": str(product.price),
                    "match_tag": product.match_tag,
                } for product in category_products[start_index:end_index]]

                # 构建二级分类数据
                secondary_category_data = {
                    "category_id": secondary_category.id,
                    "category_name": secondary_category.name,
                    "products": serialized_products
                }
                category_data["secondary_categories"].append(secondary_category_data)

            all_category_products.append(category_data)

        return JsonResponse({"code": 200, 'category_products': all_category_products})
    else:
        return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)


