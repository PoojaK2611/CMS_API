from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, is_active=True):
        if not email:
            raise ValueError("The email must be set.")
        if not password:
            raise ValueError("The password must be set.")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.is_active = is_active

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user=self.create_user(
            email,
            password=password
        )
        user.is_admin=True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=13)
    pincode= models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    object = MyUserManager


"""
    Validator for document only .pdf file
"""


def ValidateFileExtension(document):
    if not document.name.endswith('.pdf'):
        raise ValidationError("Only PDF file is accepted")


class Content(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False)
    body = models.CharField(max_length=300, blank=False)
    summary = models.CharField(max_length=60, blank=False)
    category = models.CharField(max_length=300)
    document = models.FileField(upload_to='upload_content_doc/', blank=False, validators=[ValidateFileExtension])

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content'
