from django.urls import path
from .views import GetUserNotifications, MarkNotificationAsRead

urlpatterns = [
    path('notifications/', GetUserNotifications.as_view(), name='get_user_notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', MarkNotificationAsRead.as_view(), name='mark_notification_as_read'),
]
