from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ttl = models.DurationField(default=timedelta(days=7))  # Default TTL is 7 days
    read = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + self.ttl

    def __str__(self):
        return f"Notification for {self.user.email} - {self.message}"
