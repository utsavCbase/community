from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=150, blank=True)  # Optional field for full name
    email = models.EmailField(unique=True)  # Email must be unique
    region = models.CharField(max_length=100)  # User region
    password = models.CharField(max_length=100)

    # Set email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']  # Required fields besides email and password

    def __str__(self):
        return self.email