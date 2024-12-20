from django.urls import path
from .views import CommunityList, BlogList, EnrolledCommunities, CommunityBlogs

urlpatterns = [
    path('communities/', CommunityList.as_view()),
    path('blogs/', BlogList.as_view()),
    path('enrolled-communities/<int:user_id>/', EnrolledCommunities.as_view()),
    path('community-blogs/<int:community_id>/', CommunityBlogs.as_view()),
]