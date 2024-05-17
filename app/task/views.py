# from openpyxl import Workbook
# import io
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.core.exceptions import ObjectDoesNotExist
# from ..shops.models import Shop
# from .models import base_category1, base_category2, Goods
# import json
# import csv
#
#
# # from django.conf import settings
# # from aliyunsdkcore.client import AcsClient
# # from aliyunsdkoss.request.v20140501 import PutObjectRequest # 需要降级python版本Python版本（3.12.2）不被支持 osscmd要求使用的Python版本在2.4到3.0之间
#
#
# @csrf_exempt
# def add_product(request, page=None):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             # 检查 shop_id 是否存在
#             try:
#                 Shop.objects.get(pk=data['shopId'])
#             except ObjectDoesNotExist:
#                 return JsonResponse({"code": 400, 'errmsg': '无效的店铺 ID'}, status=400)
#
#             # 检查 base_category2_id 是否存在
#             try:
#                 base_category = base_category2.objects.get(pk=data['base_category2_id'])
#             except ObjectDoesNotExist:
#                 return JsonResponse({"code": 400, 'errmsg': '无效的二级分类 ID'}, status=400)
#
#             # 自动生成 match_tag
#             match_tag = f"{data['title']}_{base_category.name}"
#
#             product = Goods.objects.create(
#                 title=data['title'],
#                 description=data['description'],
#                 price=data['price'],
#                 base_category2_id=data['base_category2_id'],
#                 product_link=data['product_link'],
#                 shop_id=data['shopId'],  # 正确的字段名
#                 match_tag=match_tag
#             )
#             return JsonResponse({"code": 200,
#                                  "product_id": product.id,
#                                  "title": product.title,
#                                  "description": product.description,
#                                  "price": str(product.price),
#                                  "base_category2_id": product.base_category2_id,
#                                  "product_link": product.product_link,
#                                  "shopId": product.shop_id,
#                                  "match_tag": product.match_tag,
#                                  "createdAt": str(product.createdAt)
#                                  }, status=200)
#         except Exception as e:
#             return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
#     elif request.method == 'GET':
#         try:
#             category2_data = list(base_category2.objects.values('id', 'name'))
#             paginate_category2 = Paginator(category2_data, request.GET.get('size', 10))
#             page_number_category2 = request.GET.get('page_category2', 1)
#             shop_data = list(Shop.objects.values('shopId', 'shop_name', 'location', 'description'))
#             paginator_shop = Paginator(shop_data, request.GET.get('size', 10))
#             page_shop_number = request.GET.get('page')
#
#             try:
#                 category2_data_page = paginate_category2.page(page_number_category2)
#                 shop_data_page = paginator_shop.page(page_shop_number)
#             except PageNotAnInteger:
#                 category2_data_page = paginate_category2.page(1)
#                 shop_data_page = paginator_shop.page(1)
#             except EmptyPage:
#                 category2_data_page = paginate_category2.page(paginate_category2.num_pages)
#                 shop_data_page = paginator_shop.page(paginator_shop.num_pages)
#
#             return JsonResponse(
#                 {"code": 200, 'category2_data': list(category2_data_page), 'shop_data': list(shop_data_page),
#                  'total_categories': paginate_category2.count,
#                  'total_shops': paginator_shop.count,
#                  'page_category2': category2_data_page.number,
#                  'page_shop': shop_data_page.number}, status=200)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({"code": 400, 'errmsg': str(e)}, status=400)
#     else:
#         return JsonResponse({"code": 405, 'errmsg': 'Unsupported method'}, status=405)
#
#
# @csrf_exempt
# def list_products(request, page=None):
#     if request.method == 'GET':
#         try:
#             size = int(request.GET.get('size', 10))  # 如果未提供，默认为 10
#             all_products = Goods.objects.all().order_by('id')
#             paginator = Paginator(all_products, size)
#             page_number = request.GET.get('page')
#             try:
#                 products = paginator.page(page_number)
#             except PageNotAnInteger:
#                 products = paginator.page(1)
#             except EmptyPage:
#                 products = paginator.page(paginator.num_pages)
#             serialized_products = [{
#                 "product_id": product.id,
#                 "title": product.title,
#                 "description": product.description,
#                 "price": str(product.price),
#                 "base_category2_id": product.base_category2_id,
#                 "product_link": product.product_link,
#                 "shopId": product.shop_id,
#                 "match_tag": product.match_tag,
#                 "createdAt": str(product.createdAt)
#             } for product in products]
#             return JsonResponse({
#                 "code": 200,
#                 "products": serialized_products,
#                 "page": products.number,
#                 "total_pages": paginator.num_pages,
#                 "total_products": paginator.count
#             })
#         except Exception as e:
#             return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
#     else:
#         return JsonResponse({"code": 405, 'errmsg': '仅支持 GET 请求'}, status=405)
#
#
# @csrf_exempt
# def get_product(request, product_id):
#     if request.method == 'GET':
#         try:
#             product = Goods.objects.get(id=product_id)
#             return JsonResponse({"code": 200,
#                                  "product_id": product.id,
#                                  "title": product.title,
#                                  "description": product.description,
#                                  "price": str(product.price),
#                                  "base_category2_id": product.base_category2_id,
#                                  "product_link": product.product_link,
#                                  "shopId": product.shop_id,
#                                  "match_tag": product.match_tag,
#                                  "createdAt": str(product.createdAt)
#                                  })
#         except Goods.DoesNotExist:
#             return JsonResponse({"code": 400, 'errmsg': '商品不存在'}, status=404)
#         except Exception as e:
#             return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
#     else:
#         return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)
#
#
# @csrf_exempt
# def update_product(request, product_id):
#     if request.method == 'PUT':
#         try:
#             data = json.loads(request.body)
#             # 验证 title 和 description 是否被正确提供
#             title = data.get('title')
#             description = data.get('description')
#             if not title or not description:
#                 return JsonResponse({"code": 400, 'errmsg': '标题和描述为必填项'}, status=400)
#
#             product = Goods.objects.get(id=product_id)
#             # 更新商品信息
#             product.title = title
#             product.description = description
#             product.price = data.get('price', product.price)
#             product.base_category2_id = data.get('base_category2_id', product.base_category2_id)
#             product.product_link = data.get('product_link', product.product_link)
#             product.match_tag = data.get('match_tag', product.match_tag)
#             product.save()
#             # 返回更新后的商品信息
#             return JsonResponse({"code": 200,
#                                  "product_id": product.id,
#                                  "title": product.title,
#                                  "description": product.description,
#                                  "price": str(product.price),
#                                  "base_category2_id": product.base_category2_id,
#                                  "product_link": product.product_link,
#                                  "shopId": product.shop_id,
#                                  "match_tag": product.match_tag,
#                                  "updatedAt": str(product.updatedAt)
#                                  })
#         except Goods.DoesNotExist:
#             return JsonResponse({"code": 404, 'errmsg': '商品不存在'}, status=404)
#         except Exception as e:
#             return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
#     else:
#         return JsonResponse({"code": 405, 'errmsg': '只支持 PUT 请求'}, status=405)
#
#
# @csrf_exempt
# def delete_product(request, product_id):
#     if request.method == 'DELETE':
#         try:
#             product = Goods.objects.get(id=product_id)
#             product.delete()
#             return JsonResponse({"code": 200, "msg": "删除成功"}, status=200)
#         except Goods.DoesNotExist:
#             return JsonResponse({"code": 404, 'errmsg': '商品不存在'}, status=404)
#         except Exception as e:
#             return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
#     else:
#         return JsonResponse({"code": 405, 'errmsg': '只支持 DELETE 请求'}, status=405)
#
#
# @csrf_exempt
# def upload_csv(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']
#
#         if not csv_file.name.endswith('.csv'):
#             return JsonResponse({"code": 400, 'errmsg': 'File is not a CSV'}, status=400)
#
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
#
#         # 在这里执行将数据保存到数据库的操作
#         for product in products:
#             try:
#                 Goods.objects.create(
#                     title=product['商品描述'],
#                     description=product['商品描述'],
#                     price=product['商品价格'],
#                     base_category2_id=product['商品二级类目id'],
#                     product_link=product['商品链接'],
#                     shop_id=product['商品的店铺id'],
#                     match_tag=product['匹配标签']
#                 )
#             except Exception as e:
#                 return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
#
#         return JsonResponse({"code": 200, 'success': True, 'products': products}, status=200)
#
#     return JsonResponse({"code": 400, 'errmsg': 'Invalid request method or file not provided'}, status=400)
#
#
# # @csrf_exempt
# # def upload_csv(request):
# #     if request.method == 'POST' and request.FILES['csv_file']:
# #         csv_file = request.FILES['csv_file']
# #
# #         if not csv_file.name.endswith('.csv'):
# #             return JsonResponse({'errmsg': 'File is not a CSV'}, status=400)
# #
# #         csv_data = csv.reader(io.TextIOWrapper(csv_file, encoding='gb2312'))
# #         headers = next(csv_data)
# #         products = []
# #         for row in csv_data:
# #             product = {
# #                 "商品标签": row[0],
# #                 "商品描述": row[1],
# #                 "商品价格": row[2],
# #                 "商品二级类目id": row[3],
# #                 "商品链接": row[4],
# #                 "商品的店铺id": row[5],
# #                 "匹配标签": row[0] + row[3]  # 标题+类目
# #             }
# #             products.append(product)
# #
# #         for product in products:
# #             try:
# #                 Goods.objects.create(
# #                     title=product['商品描述'],
# #                     description=product['商品描述'],
# #                     price=product['商品价格'],
# #                     base_category2_id=product['商品二级类目id'],
# #                     product_link=product['商品链接'],
# #                     shop_id=product['商品的店铺id'],
# #                     match_tag=product['匹配标签']
# #                 )
# #             except Exception as e:
# #                 return JsonResponse({'errmsg': str(e)}, status=500)
# #
# #         # 上传文件到阿里云OSS
# #         try:
# #             client = AcsClient(settings.ALIYUN_ACCESS_KEY_ID, settings.ALIYUN_ACCESS_KEY_SECRET, 'cn-hangzhou')
# #             request = PutObjectRequest.PutObjectRequest()
# #             request.set_BucketName(settings.ALIYUN_OSS_BUCKET_NAME)
# #             request.set_Key(csv_file.name)
# #             request.set_ObjectBody(csv_file.read())
# #             response = client.do_action_with_exception(request)
# #         except Exception as e:
# #             return JsonResponse({'errmsg': str(e)}, status=500)
# #
# #         return JsonResponse({'success': True, 'products': products}, status=200)
# #
# #     return JsonResponse({'errmsg': 'Invalid request method or file not provided'}, status=400)
#
#
# @csrf_exempt
# def download_excel(request):
#     if request.method == 'GET':
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
#
#         # 创建一个工作簿并添加一个工作表
#         wb = Workbook()
#         ws = wb.active
#         ws.append(['商品ID', '标题', '描述', '价格', '二级类目ID', '商品链接',
#                    '店铺ID', '匹配标签', '创建时间', '更新时间'])
#
#         # 获取所有商品
#         all_products = Goods.objects.all()
#
#         # 将产品数据写入工作表
#         for product in all_products:
#             ws.append([product.id, product.title, product.description, str(product.price),
#                        product.base_category2_id,
#                        product.product_link, product.shop_id, product.match_tag,
#                        str(product.createdAt), str(product.updatedAt)])
#
#         # 将工作簿保存到响应中
#         wb.save(response)
#         return response
#     else:
#         return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)
#
#
# def list_category_products(request):
#     if request.method == 'GET':
#         # 获取所有一级分类
#         all_primary_categories = base_category1.objects.all()
#         all_category_products = []
#
#         # 获取每个一级分类下的二级分类及其商品信息
#         for primary_category in all_primary_categories:
#             category_data = {
#                 "primary_category_id": primary_category.id,
#                 "primary_category_name": primary_category.name,
#                 "secondary_categories": []
#             }
#             secondary_categories = base_category2.objects.filter(category1=primary_category)
#             for secondary_category in secondary_categories:
#                 category_products = Goods.objects.filter(base_category2=secondary_category)
#
#                 # 分页逻辑
#                 page_number = int(request.GET.get('page', 1))
#                 page_size = 20
#                 start_index = (page_number - 1) * page_size
#                 end_index = start_index + page_size
#
#                 serialized_products = [{
#                     "id": product.id,
#                     "title": product.title,
#                     "description": product.description,
#                     "price": str(product.price),
#                     "match_tag": product.match_tag,
#                 } for product in category_products[start_index:end_index]]
#
#                 # 构建二级分类数据
#                 secondary_category_data = {
#                     "category_id": secondary_category.id,
#                     "category_name": secondary_category.name,
#                     "products": serialized_products
#                 }
#                 category_data["secondary_categories"].append(secondary_category_data)
#
#             all_category_products.append(category_data)
#
#         return JsonResponse({"code": 200, 'category_products': all_category_products})
#     else:
#         return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)
#
