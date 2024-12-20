from django.urls import path
from .views import UserList, BlogPost, EnrollInCommunity, ViewAllBlogsInEnrolledCommunity, GetUserNotifications, MarkNotificationAsRead
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('signup/', UserList.as_view()),
    path('login/', UserList.as_view()),
    path('blogPost/', BlogPost.as_view()),
    path('enrollInCommunity/', EnrollInCommunity.as_view()),
    path('viewAllPosts/', ViewAllBlogsInEnrolledCommunity.as_view()),
    path('notifications/', GetUserNotifications.as_view()),
    path('notifications/mark-as-read/<int:notification_id>/', MarkNotificationAsRead.as_view(), name='mark_notification_as_read'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login and obtain token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]