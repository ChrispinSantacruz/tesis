from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission


from django.contrib.auth.models import Group


class Thesis(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='theses')
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='thesis_files/')  # Agregar esta línea

    def __str__(self):
        return self.title

class Approval(models.Model):
    thesis = models.OneToOneField(Thesis, on_delete=models.CASCADE, related_name='approval')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approvals')
    approved_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField()

    def __str__(self):
        return f"{self.thesis.title} - {'Approved' if self.is_approved else 'Rejected'}"


class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    # Agregar related_name personalizado para evitar conflictos con el modelo de usuario predeterminado
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')



