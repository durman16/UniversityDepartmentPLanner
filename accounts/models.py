from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

class Account(AbstractUser):
    university = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'username'
