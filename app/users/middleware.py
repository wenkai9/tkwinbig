import traceback
from datetime import datetime, timedelta
import jwt
from django.conf import settings
from django.http import JsonResponse
from .views import generate_jwt



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
                if expiration_time - datetime.utcnow() < timedelta(hours=6):
                    new_token = generate_jwt(payload['user_id'])
                    response.set_cookie('Authorization', new_token)
            except jwt.ExpiredSignatureError:
                response.delete_cookie('Authorization')
                return JsonResponse({'code': 400, 'errmsg': 'Token已过期'}, status=400)
            except jwt.InvalidTokenError:
                response.delete_cookie('Authorization')
                return JsonResponse({'code': 400, 'errmsg': '无效的Token'}, status=400)

        return response
