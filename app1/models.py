from django.contrib.auth import *
from django.contrib.auth.models import *


User = get_user_model()

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username kiritilishi shart!")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser is_admin=True bo'lishi shart!")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff=True bo'lishi shart!")

        return self.create_user(username, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def is_superuser(self):
        return self.is_admin

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Sarlavha')
    content = models.TextField(blank=True, null=True, verbose_name='Text')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    bool = models.BooleanField(default=False, verbose_name='Bool')
    views = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Category')

    def __str__(self):
        return self.title


class Commit(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="commits")
    news = models.ForeignKey("News", on_delete=models.CASCADE, related_name="commits")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.news.title} ({self.created_at:%Y-%m-%d})"