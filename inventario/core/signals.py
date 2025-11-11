from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Crea los grupos predeterminados después de las migraciones.
    """
    grupos = {
        'administradores': {
            'permissions': Permission.objects.all(),  # todos los permisos
        },
        'stock': {
            'permissions': Permission.objects.filter(content_type__app_label__in=['productos']),
        },
        'ventas': {
            'permissions': Permission.objects.filter(content_type__app_label__in=['clientes', 'ventas']),
        },
    }

    for nombre, data in grupos.items():
        group, created = Group.objects.get_or_create(name=nombre)
        group.permissions.set(data['permissions'])
        group.save()
