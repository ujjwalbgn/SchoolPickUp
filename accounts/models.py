from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.

class SchoolUserManager(BaseUserManager):

    # def create_user(self, email,first_name,last_name, password=None):
    def create_user(self, email, password=None):  # first, last name removed
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # first_name=first_name,
            # last_name=last_name,
        )
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, first_name, last_name, password=None):
    def create_superuser(self, email, password=None): # first, last name removed
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            # first_name=first_name,
            # last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class SchoolUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # first_name = models.CharField(max_length=64)
    # last_name = models.CharField(max_length=64)
    # date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SchoolUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created=False, **kwargs):
    if created:
        Token.objects.create(user = instance)