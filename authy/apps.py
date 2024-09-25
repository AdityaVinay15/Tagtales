# from django.apps import AppConfig


# class AuthyConfig(AppConfig):
#     name = "authy"
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'authy'

    def ready(self):
        import authy.models