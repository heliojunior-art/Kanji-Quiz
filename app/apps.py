from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(username="admin_render").exists():
                User.objects.create_superuser("admin_render", "admin@teste.com", "SenhaMestra123!")
        except Exception:
            pass 
