from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
import bcrypt


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email      = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name  = models.CharField(max_length=150, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    is_active  = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        if raw_password:
            self.password = bcrypt.hashpw(
                raw_password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
        else:
            self.password = ''

    def check_password(self, raw_password):
        if not self.password:
            return False
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password.encode('utf-8')
        )
