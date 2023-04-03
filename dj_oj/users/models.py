from core.models import BaseModel
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self.create_user(email, password, **extra_fields)
        return user

    def with_score(self):
        return self.annotate(
            score=Coalesce(
                Sum('passed_problems__difficulty__score'),
                0,
            ),
        )


class User(BaseModel, AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='이메일',
        unique=True,
    )

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
