from django.apps import AppConfig


class CelerydummyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celerydummyapp'
    
    def ready(self):
        import celerydummyapp.signals 