from django.urls import path
from .views import CommunityList, BlogList, EnrolledCommunities, CommunityBlogs, BlogDetail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('communities/', CommunityList.as_view()),
    path('blogs/', BlogList.as_view()),
    path('enrolled-communities/<int:user_id>/', EnrolledCommunities.as_view()),
    path('community-blogs/<int:community_id>/', CommunityBlogs.as_view()),
    path('<int:id>/', BlogDetail.as_view(), name='blog-detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)