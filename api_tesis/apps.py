from django.apps import AppConfig


class ApiTesisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_tesis'

def ready(self):
    import api_tesis.signals