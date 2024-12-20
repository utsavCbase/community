from django.conf import settings
from django.db import models

class Community(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.region})"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='blogs')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use settings.AUTH_USER_MODEL
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

class UserCommunity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name='enrolled_communities'
    )
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='members'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
