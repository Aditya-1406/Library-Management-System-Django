from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Member(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    name = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='member')
    created_at = models.DateTimeField(auto_now_add=True)

    
    def set_password(self, raw_password: str):
        self.password = make_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)


    def __str__(self):
        return self.name + " " + self.role