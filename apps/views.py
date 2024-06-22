from django.shortcuts import render

from apps.models import RegisterUser


# Create your views here.

def index(request):
    login_msg = '恭喜！登录成功'
    return render(request, 'index.html', {'login_msg': login_msg})

def register(request):
    if request.method == 'POST':
        userEmail = request.POST.get('usermail')
        userPassword = request.POST.get('userPassword')
        userrePassword = request.POST.get('userrePassword')
    try:
        user = RegisterUser.objects.get(userEmail=userEmail)
        if user:
            msg = '该邮箱已被注册，请更换邮箱！'
            return render(request, 'register.html', {'msg': msg})
    except:
        if userPassword != userrePassword:
            errmsg = '两次密码输入不一致，请重新输入！'
            return render(request,'register.html', {'errmsg': errmsg})
        else:
            user = RegisterUser()
            user.userEmail = userEmail
            user.userPassword = userPassword
            user.save()
            return render(request, 'login.html')

    else:
        return render(request,'register.html')
