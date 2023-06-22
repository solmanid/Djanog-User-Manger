from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    email_active_code = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class OtpCode(models.Model):
    email = models.CharField(max_length=200)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.code} - {self.created}"