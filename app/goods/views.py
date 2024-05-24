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
                CooperationFee=data['CooperationFee'],
                product_status=0  # 商品默认状态为0，表示未建联

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
                "product_status": product.product_status,
                "raidsysrule_id": product.raidsysrule_id,
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
                "product_status": product.product_status,
                "raidsysrule_id": product.raidsysrule_id,
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
            # try:
            #     RaidsysRule.objects.get(pk=data['id'])
            # except ObjectDoesNotExist:
            #     return JsonResponse({"code": 400, 'errmsg': '建联规则不存在'}, status=400)
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
            # product.product_status = 1  # 商品状态改为1，表示已建联
            # product.raidsysrule_id = data['id']
            product.save()
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
                # "product_status": product.product_status,
                # "raidsysrule_id": product.raidsysrule_id,
                "updatedAt": str(product.updatedAt)
            }
            return JsonResponse({"code": 200, "msg": "商品信息更新成功", "data": data}, status=200)
        except Goods.DoesNotExist:
            return JsonResponse({"code": 404, 'errmsg': '商品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)


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


@csrf_exempt
def list_category_products(request):
    if request.method == 'GET':
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
                    "id": product.id,
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
                "id": product.id,
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
        category_id = request.GET.get('id')  # 获取请求中的 id 参数
        category_type = request.GET.get('type')  # 获取请求中的 type 参数

        try:
            if category_type == 'lv_1':
                # 查询一级分类下的二级分类下的商品
                secondary_categories = base_category2.objects.filter(category1_id=category_id)
                data = Goods.objects.filter(base_category2__in=secondary_categories).values('id', 'title',
                                                                                            'description', 'price',
                                                                                            'base_category2_id',
                                                                                            'product_link', 'match_tag',
                                                                                            'hasFreeSample',
                                                                                            'commissionRate',
                                                                                            'CooperationFee')
            elif category_type == 'lv_2':
                # 查询二级分类下的商品
                data = Goods.objects.filter(base_category2_id=category_id).values('id', 'title', 'description', 'price',
                                                                                  'base_category2_id',
                                                                                  'product_link', 'match_tag',
                                                                                  'hasFreeSample', 'commissionRate',
                                                                                  'CooperationFee')
            else:
                # 如果没有提供类别类型，则返回所有商品
                data = Goods.objects.all().values('id', 'title', 'description', 'price', 'base_category2_id',
                                                  'product_link', 'match_tag', 'hasFreeSample', 'commissionRate',
                                                  'CooperationFee')

            return JsonResponse({"code": 200, "data": list(data)}, status=200)
        except Exception as e:
            return JsonResponse({"code": 500, 'errmsg': str(e)}, status=500)
    else:
        return JsonResponse({"code": 405, 'errmsg': '只支持 GET 请求'}, status=405)


# from .models import RaidsysRule
#
#
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
