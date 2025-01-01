from django.conf import settings
from django.db import models
import os

class Community(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.region})"

def blog_image_upload_path(instance, filename):
    # Upload the images to a subdirectory 'blog_images' within your media folder
    return filename

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='blogs')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=blog_image_upload_path, default="def.jpg")  # New field

    def __str__(self):
        return self.title

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
