from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def assign_group(sender, instance, created, **kwargs):
    if created:
        # Verificar el tipo de usuario y asignar al grupo correspondiente
        if instance.is_teacher:
            group = Group.objects.get(name='teachers')
            instance.groups.add(group)
        else:
            group = Group.objects.get(name='students')
            instance.groups.add(group)
