from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)  # Nome de usuário único
    email = models.EmailField(unique=True)  # Email único
    password = models.CharField(max_length=128)  # Senha (armazenada como hash)

    def save(self, *args, **kwargs):
        # Use o hash para armazenar a senha
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

