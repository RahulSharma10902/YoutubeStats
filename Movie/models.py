from django.db import models
# from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(models.Model):
    username=models.CharField(primary_key=True,max_length=20)
    fullname=models.CharField(max_length=20)
    gmail=models.EmailField(unique=True)
    password=models.CharField(max_length=400)
