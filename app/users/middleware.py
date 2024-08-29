from datetime import datetime, timedelta
from django.http import JsonResponse
import jwt
from django.conf import settings
from app.users.views import generate_jwt


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 'Authorization' in request.COOKIES:
            token = request.COOKIES['Authorization']
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                expiration_time = datetime.utcfromtimestamp(payload['exp'])

                # 检查Token是否在6小时内即将过期
                if expiration_time - datetime.utcnow() < timedelta(hours=6):
                    new_token = generate_jwt(payload['user_id'])
                    response.set_cookie('Authorization', new_token)
            except jwt.ExpiredSignatureError:
                # 当 Authorization Token 过期时，清除所有 cookies
                for cookie in request.COOKIES:
                    response.delete_cookie(cookie)
                return JsonResponse({'code': 401, 'errmsg': 'Token已过期,请重新登录'}, status=400)
            except jwt.InvalidTokenError:
                # 当Token无效时，清除所有 cookies
                for cookie in request.COOKIES:
                    response.delete_cookie(cookie)
                return JsonResponse({'code': 401, 'errmsg': '无效的Token,请重新登录'}, status=400)

        return response
