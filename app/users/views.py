import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
import jwt
from django.conf import settings
import re


# def generate_jwt(user_id):
#     payload = {
#         'user_id': user_id,
#         'exp': datetime.utcnow() + timedelta(days=1)  # 设置过期时间为1天
#     }
#     return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def generate_jwt(user_id):
    expiration_time = datetime.utcnow() + timedelta(days=1)  # 设置过期时间为1天
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        # 获取表单提交的数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        number = request.POST.get('number')
        company = request.POST.get('company')

        # 检查是否有任何字段缺失
        if not (username and password and email and number and company):
            return JsonResponse({'code': 400, 'errmsg': '缺少必要的参数'})

        # 检查用户名是否已被注册
        if User.objects.filter(username=username).exists():
            return JsonResponse({'code': 400, 'errmsg': '用户名已存在'})

        # 判断参数是否有效
        if not re.match(r'^\w{5,20}$', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名5-20位数字字母下划线'})

        if not re.match(r'^.{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': '密码长度必须在8到20位之间'})

        if not re.match(r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', email):
            return JsonResponse({'code': 400, 'errmsg': '邮箱格式不正确'})

        if not re.match(r'^1[3-9]\d{9}$', number):
            return JsonResponse({'code': 400, 'errmsg': '手机号格式不正确'})

        if not re.match('^.{1,20}$', company):
            return JsonResponse({'code': 400, 'errmsg': '公司名称不能超过20个字符'})

        # 对密码进行哈希处理
        hashed_password = make_password(password)

        # 创建用户对象并保存到数据库
        user = User(username=username, password=hashed_password, email=email, number=number, company=company)
        user.save()

        # 生成 JWT
        token = generate_jwt(user.user_id)

        # 设置JWT的Cookie
        response = JsonResponse({'code': 200, 'msg': '注册成功!'})
        response.set_cookie('Authorization', token)

        return response

    return JsonResponse({'code': 400, 'errmsg': '只允许POST请求'})


# @csrf_exempt
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         print(username, password)
#
#         if not username or not password:
#             return JsonResponse({'code': 400, 'errmsg': '用户名和密码不能为空。'})
#
#         try:
#             user = User.objects.get(username=username)
#             if check_password(password, user.password):
#                 data = {
#                     "user_id": user.user_id,
#                     "username": user.username,
#                     "number": user.number,
#                     "email": user.email,
#                     "company": user.company
#                 }
#                 # 生成 JWT
#                 token = generate_jwt(user.user_id)
#                 # print('token:', token)
#
#                 # 设置JWT的Cookie
#                 response = JsonResponse({'code': 200, 'msg': '登录成功！', 'data': data, 'token': token}, status=200)
#                 response.set_cookie('Authorization', token)
#
#                 return response
#             else:
#                 return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误。'})
#         except User.DoesNotExist:
#             return JsonResponse({'code': 400, 'errmsg': '用户不存在。'})
#         except Exception as e:
#             traceback.print_exc()
#             return JsonResponse({'code': 500, 'errmsg': '服务器内部错误。'})
#
#     return JsonResponse({'code': 400, 'errmsg': '只允许POST请求'})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'code': 400, 'errmsg': '用户名和密码不能为空。'})

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                data = {
                    "user_id": user.user_id,
                    "username": user.username,
                    "number": user.number,
                    "email": user.email,
                    "company": user.company
                }
                # 生成 JWT
                token = generate_jwt(user.user_id)

                # 删除旧的 token（如果存在）
                response = JsonResponse({'code': 200, 'msg': '登录成功！', 'data': data, 'token': token}, status=200)
                response.delete_cookie('Authorization')

                # 设置JWT的Cookie
                response.set_cookie('Authorization', token)

                return response
            else:
                return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误。'})
        except User.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '用户不存在。'})
        except Exception as e:
            return JsonResponse({'code': 500, 'errmsg': '服务器内部错误。'})

    return JsonResponse({'code': 400, 'errmsg': '只允许POST请求'})


def user_profile(request):
    if request.method == 'GET':
        # 从请求头中获取 JWT
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证,请重新登录'})

        try:
            # 解码 JWT
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']

            # 查询用户信息
            user = User.objects.get(user_id=user_id)
            user_info = {
                'username': user.username,
                'number': user.number,
                'email': user.email
            }
            return JsonResponse({'code': 200, 'data': user_info})
        except jwt.ExpiredSignatureError:
            traceback.print_exc()
            return JsonResponse({'code': 401, 'errmsg': 'Token已过期'})
        except jwt.InvalidTokenError:
            traceback.print_exc()
            return JsonResponse({'code': 401, 'errmsg': '无效的Token'})
        except User.DoesNotExist:
            traceback.print_exc()
            return JsonResponse({'code': 400, 'errmsg': '用户不存在。'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'code': 500, 'errmsg': '服务器内部错误。'})

    return JsonResponse({'code': 400, 'errmsg': '只允许GET请求'})


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        # 从请求头中获取 JWT
        token = request.COOKIES.get('Authorization')
        if not token:
            return JsonResponse({'code': 401, 'errmsg': '未提供有效的身份认证'})

        try:
            # 解码 JWT
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']

            # 查询用户信息
            user = User.objects.get(user_id=user_id)

            # 获取表单提交的旧密码、新密码和确认密码
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # 检查是否缺少必要的参数
            if not (old_password and new_password and confirm_password):
                return JsonResponse({'code': 400, 'errmsg': '缺少必要的参数'})

            # 检查旧密码是否正确
            if not check_password(old_password, user.password):
                return JsonResponse({'code': 400, 'errmsg': '旧密码不正确'})

            # 检查新密码长度是否在8到20位之间
            if not re.match(r'^.{8,20}$', new_password):
                return JsonResponse({'code': 400, 'errmsg': '新密码长度必须在8到20位之间'})

            # 检查新密码和确认密码是否一致
            if new_password != confirm_password:
                return JsonResponse({'code': 400, 'errmsg': '两次密码不一致'})

            # 对新密码进行哈希处理
            hashed_password = make_password(new_password)
            user.password = hashed_password
            user.save()

            return JsonResponse({'code': 200, 'msg': '密码修改成功'})
        except jwt.ExpiredSignatureError:
            return JsonResponse({'code': 401, 'errmsg': 'Token已过期'})
        except jwt.InvalidTokenError:
            traceback.print_exc()
            return JsonResponse({'code': 401, 'errmsg': '无效的Token'})
        except User.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '用户不存在。'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'code': 500, 'errmsg': '服务器内部错误。'})

    return JsonResponse({'code': 400, 'errmsg': '只允许POST请求'})


def user_logout(request):
    if request.method == 'POST':
        response = JsonResponse({'code': 200, 'msg': '退出成功！'})
        response.delete_cookie('Authorization')  # 删除 JWT 的 Cookie

        return response

    return JsonResponse({'code': 400, 'errmsg': '只允许POST请求'})
