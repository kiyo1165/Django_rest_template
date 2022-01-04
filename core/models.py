from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from djangoProject1228 import settings
# Create your models here.


def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['image'], str(instance.user.id)+str(instance.nickname)+str(".")+str(ext))


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Emailアドレスは必須です。')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # デフォルトの入力をemailに変更
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name


class Profile(models.Model):
    nickname = models.CharField(max_length=20)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='user',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='friends',
        on_delete=models.CASCADE
    )

    img = models.ImageField(blank=True, null=True, upload_to=upload_path)

    def __str__(self):
        return self.nickname
