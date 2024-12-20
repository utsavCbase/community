from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Community, Blog, UserCommunity
from .serializers import CommunitySerializer, BlogSerializer, UserCommunitySerializer

class CommunityList(APIView):
    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data)

class BlogList(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class EnrolledCommunities(APIView):
    def get(self, request, user_id):
        user_communities = UserCommunity.objects.filter(user_id=user_id)
        serializer = UserCommunitySerializer(user_communities, many=True)
        return Response(serializer.data)

class CommunityBlogs(APIView):
    def get(self, request, community_id):
        blogs = Blog.objects.filter(community_id=community_id)
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)