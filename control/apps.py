from django.apps import AppConfig

from migrator.apps import post_final_migrate


class ControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'control'

@post_final_migrate.connect
def auto_create_superuser(**kwargs):
    from django.contrib.auth.models import User

    has_superuser = User.objects.filter(is_superuser=True).exists()
    print('test')
    if not has_superuser:
        User.objects.create_superuser('admin', password='password')
