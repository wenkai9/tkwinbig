from django.apps import AppConfig
from mongoengine import connect
from django.conf import settings


class TaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.task'


def connect_to_mongo():
    connect(
        db=settings.MONGODB_DATABASES['default']['NAME'],
        host=settings.MONGODB_DATABASES['default']['HOST'],
        port=settings.MONGODB_DATABASES['default']['PORT'],
        username=settings.MONGODB_DATABASES['default']['USERNAME'],
        password=settings.MONGODB_DATABASES['default']['PASSWORD']
    )
