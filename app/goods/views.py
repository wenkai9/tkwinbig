import io
import os
import oss2
import json
import csv
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from ..shops.models import Shop
from .models import base_category1, base_category2, Goods, RaidsysRule
from openpyxl import Workbook
from djangoProject1 import settings


@csrf_exempt
def add_product(request, page=None):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 检查 shop_id 是否存在
            try:
                Shop.objects.get(shopId=data['shopId'])
            except ObjectDoesNotExist:
                return JsonResponse({"code": 400, 'errmsg': '无效的店铺 ID'}, status=400)
            match_tag = f"{data['title']}"

            try:
                Goods.objects.get(product_id=data['product_id'])
                return JsonResponse({"code": 409, 'errmsg': '产品ID已存在'}, status=409)
            except Goods.DoesNotExist:
                pass  # 继续流程
            except Goods.MultipleObjectsReturned:
                return JsonResponse({"code": 400, 'errmsg': '产品ID重复'}, status=400)

            product = Goods.objects.create(
                product_id=data['product_id'],
                title=data['title'],
                description=data['description'],
                price=data['price'],
                base_category2_id=data['base_category2_id'],
                product_link=data['product_link'],
                shop_id=data['shopId'],  # 正确的字段名
                match_tag=match_tag,
                hasFreeSample=data['hasFreeSample'],
                commissionRate=data['commissionRate'],
                CooperationFee=data['CooperationFee'],
                product_status=0  # 商品默认状态为0，表示未建联

            )
            data = {
                "product_id": product.product_id,
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
                "product_status": product.product_status,
                "raidsysrule_id": product.raidsysrule_id,
                "createdAt": str(product.createdAt)
            }
            return JsonResponse({"code": 200, "msg": "商品添加成功", "data": data}, status=200)
        except KeyError as e:
            return JsonResponse({"code": 400, 'errmsg': f"缺少必要的字段: {str(e)}"}, status=400)
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
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
        try:
            size = int(request.GET.get('size', 10))  # 如果未提供，默认为 10
            all_products = Goods.objects.all().order_by('product_id')
            paginator = Paginator(all_products, size)
            page_number = request.GET.get('page')
            try:
                products = paginator.page(page_number)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            # 根据 raidsysrule_id 获取任务名称
            for product in products:
                raidsysrule_id = product.raidsysrule_id
                try:
                    rule = RaidsysRule.objects.get(id=raidsysrule_id)
                    rule_name = rule.name
                except RaidsysRule.DoesNotExist:
                    rule_name = None

                # 将任务名称添加到 serialized_products 中
                product.rule_name = rule_name

            serialized_products = [{
                "product_id": product.product_id,
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
                "product_status": product.product_status,
                "rule_name": product.rule_name,
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
def get_products(request, shop_id):
    if request.method == 'GET':
        try:
            products = Goods.objects.filter(shop_id=shop_id)
            data = []
            for product in products:
                product_data = {
                    "product_id": product.product_id,
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
                    "product_status": product.product_status,
                    "raidsysrule_id": product.raidsysrule_id,
                    "createdAt": str(product.createdAt)
                }
                data.append(product_data)
            return JsonResponse({"code": 200, "data": data}, status=200)
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)


@csrf_exempt
def update_product(request, product_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)

            # 获取指定的商品
            try:
                product = Goods.objects.get(product_id=product_id)
            except Goods.DoesNotExist:
                return JsonResponse({"code": 404, 'errmsg': '商品不存在'}, status=404)

            # 更新允许的字段，如果未提供则保留原有的值
            product.title = data.get('title', product.title)
            product.description = data.get('description', product.description)
            product.price = data.get('price', product.price)
            product.hasFreeSample = data.get('hasFreeSample', product.hasFreeSample)
            product.commissionRate = data.get('commissionRate', product.commissionRate)
            product.CooperationFee = data.get('CooperationFee', product.CooperationFee)
            product.product_link = data.get('product_link', product.product_link)
            product.save()

            response_data = {
                "product_id": product.product_id,
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "hasFreeSample": product.hasFreeSample,
                "commissionRate": str(product.commissionRate),
                "CooperationFee": str(product.CooperationFee),
                "product_link": product.product_link,
                "updatedAt": str(product.updatedAt)
            }

            return JsonResponse({"code": 200, "msg": "商品信息更新成功", "data": response_data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"code": 400, 'errmsg': '无效的JSON数据'}, status=400)
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)

    return JsonResponse({"code": 405, 'errmsg': '请求方法无效'}, status=405)


@csrf_exempt
def bind_rule(request, product_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            # 验证提供的 raidsysrule_id 是否有效
            raidsysrule_id = data.get('raidsysrule_id')
            raidsysrule = get_object_or_404(RaidsysRule, pk=raidsysrule_id)

            # 获取商品
            product = Goods.objects.get(product_id=product_id)

            # 更新商品信息
            product.raidsysrule = raidsysrule  # 更新 raidsysrule_id
            product.product_status = True  # 更新商品状态

            product.save()

            return JsonResponse({"code": 200, "msg": "建联规则修改成功"}, status=200)

        except Goods.DoesNotExist:
            return JsonResponse({"code": 404, 'errmsg': '商品不存在'}, status=404)

        except RaidsysRule.DoesNotExist:
            return JsonResponse({"code": 404, 'errmsg': '建联规则不存在'}, status=404)

        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)


@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            product = Goods.objects.get(product_id=product_id)
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
            match_tag = f"{row[0]}{base_category.name}"
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
                "匹配标签": match_tag,
                "物品状态": False
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
                    match_tag=product['匹配标签'],
                    product_status=0  # 商品默认状态为0，表示未建联
                )
            except Exception as e:
                return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)

        return JsonResponse({"code": 200, 'success': True, 'products': products}, status=200)

    return JsonResponse({"code": 400, 'errmsg': '请求方法无效或未提供文件'}, status=400)


# @csrf_exempt
# def upload_csv(request):
#     if request.method == 'POST' and request.FILES.get('csv_file'):
#         csv_file = request.FILES['csv_file']
#
#         if not csv_file.name.endswith('.csv'):
#             return JsonResponse({"code": 400, 'errmsg': 'File is not a CSV'}, status=400)
#
#         # 读取 CSV 文件内容
#         csv_data = csv.reader(io.TextIOWrapper(csv_file, encoding='gb2312'))
#         headers = next(csv_data)
#         products = []
#
#         for row in csv_data:
#             try:
#                 base_category = base_category2.objects.get(pk=row[6])
#             except ObjectDoesNotExist:
#                 return JsonResponse({"code": 400, 'errmsg': '无效的二级分类 ID'}, status=400)
#
#             match_tag = f"{row[0]}{base_category.name}"
#             product = {
#                 "商品标签": row[0],
#                 "商品描述": row[1],
#                 "商品价格": row[2],
#                 "是否免费寄送样品": row[3],
#                 "佣金率": row[4],
#                 "合作费": row[5],
#                 "商品二级类目id": row[6],
#                 "商品链接": row[7],
#                 "商品的店铺id": row[8],
#                 "匹配标签": match_tag,
#                 "物品状态": False
#             }
#             products.append(product)
#
#         # 保存数据到数据库
#         for product in products:
#             try:
#                 Goods.objects.create(
#                     title=product['商品描述'],
#                     description=product['商品描述'],
#                     price=product['商品价格'],
#                     hasFreeSample=product['是否免费寄送样品'],
#                     commissionRate=product['佣金率'],
#                     CooperationFee=product['合作费'],
#                     base_category2_id=product['商品二级类目id'],
#                     product_link=product['商品链接'],
#                     shop_id=product['商品的店铺id'],
#                     match_tag=product['匹配标签'],
#                     product_status=0  # 商品默认状态为0，表示未建联
#                 )
#             except Exception as e:
#                 return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
#
#         # 从 settings 中读取 OSS 配置
#         oss_config = settings.ALIYUN_OSS
#         access_key_id = oss_config['ACCESS_KEY_ID']
#         access_key_secret = oss_config['ACCESS_KEY_SECRET']
#         endpoint = oss_config['ENDPOINT']
#         bucket_name = oss_config['BUCKET_NAME']
#
#         # 上传文件到阿里云 OSS
#         try:
#             # 初始化 OSS 连接
#             auth = oss2.Auth(access_key_id, access_key_secret)
#             bucket = oss2.Bucket(auth, endpoint, bucket_name)
#
#             # 上传文件
#             csv_file.seek(0)  # 将文件指针重置到开头
#             bucket.put_object(csv_file.name, csv_file.read())
#         except Exception as e:
#             return JsonResponse({"code": 500, 'errmsg': f'上传文件到 OSS 失败: {str(e)}'}, status=500)
#
#         return JsonResponse({"code": 200, 'success': True, 'products': products}, status=200)
#
#     return JsonResponse({"code": 400, 'errmsg': '请求方法无效或未提供文件'}, status=400)

'''
导出文件
'''


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
            ws.append([product.product_id, product.title, product.description, str(product.price),
                       product.hasFreeSample, product.commissionRate, product.CooperationFee,
                       product.base_category2_id,
                       product.product_link, product.shop_id, product.match_tag,
                       str(product.createdAt), str(product.updatedAt)])

        # 将工作簿保存到响应中
        wb.save(response)
        return response
    else:
        return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)


@csrf_exempt
def download_sample_csv(request):
    if request.method == 'GET':
        # 创建一个 HTTP 响应对象，设置为 CSV 文件类型
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sample_product_format.csv"'

        # 创建 CSV 写入器
        writer = csv.writer(response)

        # 写入 CSV 文件头
        writer.writerow([
            '商品标签', '商品描述', '商品价格', '是否免费寄送样品',
            '佣金率', '合作费', '商品二级类目id', '商品链接', '商品的店铺id',
            '物品标签', '物品状态'
        ])

        # 写入一行示例数据，以帮助用户理解格式
        writer.writerow([
            '示例标签', '示例描述', '123.45', '是',
            '10%', '100.00', '123', 'http://example.com', '456',
            '示例物品标签', '在售'
        ])

        return response


@csrf_exempt
def list_category_products(request):
    if request.method == 'GET':
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
        category_id = request.GET.get('id')
        category_type = request.GET.get('type')

        if category_type == '1':
            # 查询一级分类下的二级分类和商品
            primary_category = base_category1.objects.get(id=category_id)
            secondary_categories = base_category2.objects.filter(category1=primary_category)
            all_category_products = []

            for secondary_category in secondary_categories:
                category_products = Goods.objects.filter(base_category2=secondary_category)

                # 序列化商品信息
                serialized_products = [{
                    "id": product.product_id,
                    "title": product.title,
                    "description": product.description,
                    "price": str(product.price),
                    "match_tag": product.match_tag,
                } for product in category_products]

                all_category_products.extend(serialized_products)

            return JsonResponse({"code": 200, 'sub': all_category_products})


        elif category_type == '2':
            # 查询二级分类下的商品
            category_products = Goods.objects.filter(base_category2_id=category_id)

            # 序列化商品信息
            serialized_products = [{
                "id": product.product_id,
                "title": product.title,
                "description": product.description,
                "price": str(product.price),
                "match_tag": product.match_tag,
            } for product in category_products]

            return JsonResponse({"code": 200, 'products': serialized_products})

        else:
            # 如果既没有提供一级分类ID也没有提供二级分类ID，则返回参数错误提示
            all_primary_categories = base_category1.objects.all()
            all_category_products = []

            for primary_category in all_primary_categories:
                secondary_categories = base_category2.objects.filter(category1=primary_category)
                primary_category_data = {
                    "id": primary_category.id,
                    "name": primary_category.name,
                    "sub": []
                }

                for secondary_category in secondary_categories:
                    category_products = Goods.objects.filter(base_category2=secondary_category)

                    # 构建二级分类数据
                    secondary_category_data = {
                        "id": secondary_category.id,
                        "name": secondary_category.name,
                    }
                    primary_category_data["sub"].append(secondary_category_data)

                all_category_products.append(primary_category_data)

            return JsonResponse({"code": 200, 'sub': all_category_products})

    else:
        return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)


@csrf_exempt
def list_products_all(request):
    if request.method == 'GET':
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
        category_id = request.GET.get('id')  # 获取请求中的 id 参数
        category_type = request.GET.get('type')  # 获取请求中的 type 参数

        try:
            if category_type == 'lv_1':
                # 查询一级分类下的二级分类下的商品
                secondary_categories = base_category2.objects.filter(category1_id=category_id)
                data = Goods.objects.filter(base_category2__in=secondary_categories).values('product_id', 'title',
                                                                                            'description', 'price',
                                                                                            'base_category2_id',
                                                                                            'product_link', 'match_tag',
                                                                                            'hasFreeSample',
                                                                                            'commissionRate',
                                                                                            'CooperationFee')
            elif category_type == 'lv_2':
                # 查询二级分类下的商品
                data = Goods.objects.filter(base_category2_id=category_id).values('product_id', 'title', 'description',
                                                                                  'price',
                                                                                  'base_category2_id',
                                                                                  'product_link', 'match_tag',
                                                                                  'hasFreeSample', 'commissionRate',
                                                                                  'CooperationFee')
            else:
                # 如果没有提供类别类型，则返回所有商品
                data = Goods.objects.all().values('product_id', 'title', 'description', 'price', 'base_category2_id',
                                                  'product_link', 'match_tag', 'hasFreeSample', 'commissionRate',
                                                  'CooperationFee')

            return JsonResponse({"code": 200, "data": list(data)}, status=200)
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)


@csrf_exempt
def add_rule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rule = RaidsysRule.objects.create(
                name=data['name'],
                requirement=data['requirement'],
                commission=data.get('commission'),
                shop_info=data.get('shop_info', '')
            )
            response_data = {
                "id": rule.id,
                "name": rule.name,
                "requirement": rule.requirement,
                "commission": str(rule.commission) if rule.commission is not None else None,
                "shop_info": str(rule.shop_info) if rule.shop_info is not None else None,
                "createdAt": str(rule.createdAt)
            }
            return JsonResponse({"code": 200, "msg": "规则添加成功", "data": response_data}, status=200)
        except KeyError as e:
            return JsonResponse({"code": 400, "errmsg": f"缺少必要字段: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "只允许POST请求"}, status=405)


@csrf_exempt
def list_rule(request, page=None):
    if request.method == 'GET':
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})
        try:
            size = int(request.GET.get('size', 10))  # 如果未提供，默认为 10
            all_rules = RaidsysRule.objects.all().order_by('id')
            paginator = Paginator(all_rules, size)
            page_number = request.GET.get('page')
            try:
                rules = paginator.page(page_number)
            except PageNotAnInteger:
                rules = paginator.page(1)
            except EmptyPage:
                rules = paginator.page(paginator.num_pages)
            serialized_rules = [{
                "id": rule.id,
                "name": rule.name,
                "requirement": rule.requirement,
                "commission": rule.commission,
                "shop_info": rule.shop_info,
                "createdAt": str(rule.createdAt)
            } for rule in rules]
            return JsonResponse({
                "code": 200,
                "rules": serialized_rules,
                "page": rules.number,
                "total_pages": paginator.num_pages,
                "total_rules": paginator.count
            })
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, 'errmsg': '仅支持 GET 请求'}, status=405)


@csrf_exempt
def update_rule(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            rule = RaidsysRule.objects.get(id=id)
            rule.name = data['name']
            rule.requirement = data['requirement']
            rule.commission = data.get('commission')
            rule.shop_info = data.get('shop_info', '')
            rule.save()
            response_data = {
                "id": rule.id,
                "name": rule.name,
                "requirement": rule.requirement,
                "commission": str(rule.commission) if rule.commission is not None else None,
                # "shop_info": rule.shop_info,
                "createdAt": str(rule.createdAt)
            }
            return JsonResponse({"code": 200, "msg": "规则更新成功", "data": response_data}, status=200)
        except KeyError as e:
            return JsonResponse({"code": 400, "errmsg": f"缺少必要字段: {str(e)}"}, status=400)
        except RaidsysRule.DoesNotExist:
            return JsonResponse({"code": 404, "errmsg": "规则不存在"}, status=404)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "只允许PUT请求"}, status=405)


@csrf_exempt
def delete_rule(request, rule_id):
    if request.method == 'DELETE':
        try:
            rule = RaidsysRule.objects.get(id=rule_id)
            rule.delete()
            return JsonResponse({"code": 200, "msg": "规则删除成功"}, status=200)
        except RaidsysRule.DoesNotExist:
            return JsonResponse({"code": 404, "errmsg": "规则不存在"}, status=404)
        except Exception as e:
            return JsonResponse({"code": 500, "errmsg": str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, "errmsg": "只允许DELETE请求"}, status=405)
