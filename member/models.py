from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('superuser', 'Superuser'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.BigIntegerField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
