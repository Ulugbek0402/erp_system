from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

class SomeModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='something',
    )

User = get_user_model()


class Actor(models.Model):
    name = models.CharField(max_length=150)
    birthdate = models.DateField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField()
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True)
    genre = models.CharField(max_length=50)
    actor = models.ManyToManyField(Actor)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Movie.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class CommitMovie(models.Model):
    title = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_ed = models.DateField(auto_now_add=True)
    update_ed = models.DateTimeField(auto_now=True)