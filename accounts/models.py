from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

class Account(AbstractUser):
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")

    USERNAME_FIELD = 'username'
