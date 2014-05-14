from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_staff=False, is_active=True, is_superuser=False, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_('email'))
    date_joined = models.DateTimeField(default=timezone.now, verbose_name=_('date joined'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('staff status'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-date_joined']
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.__unicode__()

    def get_full_name(self):
        return self.__unicode__()
