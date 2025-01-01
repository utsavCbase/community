from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Community, Blog, UserCommunity
from .serializers import CommunitySerializer, BlogSerializer, UserCommunitySerializer
from rest_framework import status

class CommunityList(APIView):
    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data)


class BlogList(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Add parsers to handle file uploads

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        image = request.FILES.get('image')

        # Check if the image is provided
        if not image:
            return Response({'error': 'Image is required for creating a blog post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the blog object with the provided data
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save(image=image)  # Save the image along with the blog
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    
class BlogDetail(APIView):
    def get(self, request, id):
        try:
            # Try to get the blog by ID
            blog = Blog.objects.get(id=id)
            print("--------------------------------------------")
            print(blog)
            print("--------------------------------------------")
            serializer = BlogSerializer(blog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
