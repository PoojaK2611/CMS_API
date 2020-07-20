from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from .validators import ValidateFileExtension
from .validators import UppercaseValidator, LowercaseValidator, MinimumLengthValidator, OnlyNumberValidator

class MyUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    """
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not password:
            raise ValueError("User must have a password")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=13)
    pincode = models.CharField(max_length=6,validators=[OnlyNumberValidator])
    is_active = models.BooleanField(default =True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager

    def __str__(self):
        return self.email

    def has_perm(self,perm, obj=None):
        """ Does the user have specific permission? """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True


class Content(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    title = models.CharField(max_length=30, blank=False)
    body = models.CharField(max_length=300, blank=False)
    summary = models.CharField(max_length=60, blank=False)
    category = models.CharField(max_length=300)
    document = models.FileField(validators=[ValidateFileExtension],
                                upload_to='upload_content_doc/', blank=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content'

