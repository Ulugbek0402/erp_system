from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username kiritilishi shart!")

        extra_fields.setdefault("is_active", True)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff=True bo‘lishi kerak!")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser=True bo‘lishi kerak!")

        return self.create_user(username, password, **extra_fields)


# class User(AbstractBaseUser, PermissionsMixin):
#
#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(unique=True, null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_student = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.username


class Teacher(models.Model):


    name = models.CharField(max_length=80)
    subject = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Student(models.Model):


    name = models.CharField(max_length=80)
    grade = models.IntegerField()

    def __str__(self):
        return self.name
