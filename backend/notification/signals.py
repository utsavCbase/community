# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from blogs.models import Blog, UserCommunity
from .models import Notification
from datetime import timedelta


@receiver(post_save, sender=Blog)
def notify_users_on_blog_publish(sender, instance, created, **kwargs):
    if created:
        # Fetch all users enrolled in the community where the blog was published
        enrolled_users = UserCommunity.objects.filter(community=instance.community)

        # Create a notification for each user
        for user_community in enrolled_users:
            Notification.objects.create(
                user=user_community.user,
                message=f"A new blog '{instance.title}' has been published in your enrolled community '{instance.community.name}'!",
                ttl=timedelta(days=7)  # Set TTL as 7 days for example
            )
