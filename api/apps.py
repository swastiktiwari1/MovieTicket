from django.apps import AppConfig
from .models import User

class ApiConfig(AppConfig):
    name = 'api'
admin.site.register(User)