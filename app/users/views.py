from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from .models import User
import re


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 获取表单提交的数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        number = request.POST.get('number')
        company = request.POST.get('company')

        # 检查是否有任何字段缺失
        if not (username and password and email and number and company):
            return JsonResponse({'code': 1, 'errmsg': '缺少必要的参数'})

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

        return JsonResponse({'code': 0, 'errmsg': '注册成功!'})

    return JsonResponse({'code': 1, 'errmsg': '只允许POST请求'})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 获取表单提交的用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # 查询数据库中是否存在该用户
            user = User.objects.get(username=username)
            # 检查密码是否匹配
            if check_password(password, user.password):
                return JsonResponse({'code': 0, 'errmsg': '登录成功!'})
            else:
                return JsonResponse({'code': 1, 'errmsg': '用户名或密码错误。'})
        except User.DoesNotExist:
            return JsonResponse({'code': 1, 'errmsg': '用户不存在。'})

    return JsonResponse({'code': 1, 'errmsg': '只允许POST请求'})


def logout(request):
    if request.method == 'POST':
        return JsonResponse({'code': 0, 'errmsg': '退出成功!'})
