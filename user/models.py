from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework import serializers, status, views, viewsets, permissions
from rest_framework.decorators import action
from django_rq import job  # For background email sending
import redis

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    is_verified = models.BooleanField(default=False)
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    verification_token = models.CharField(max_length=50, null=True, blank=True)







