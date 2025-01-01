from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import UserSerializer
from blogs.serializers import BlogSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from blogs.models import Community, UserCommunity, Blog
from notification.models import Notification
from notification.serializers import NotificationSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class UserList(APIView):
    def get_permissions(self):
        return [AllowAny()]

    def get(self, request):
        # Handle authentication by email and password via GET request
        email = request.GET.get('email')
        password = request.GET.get('password')

        if not email or not password:
            return Response({"error": "Both email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user:
            serializer = UserSerializer(user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                'user': serializer.data,
                'access_token': access_token,
                'refresh_token': str(refresh)  # Optionally include refresh token as well
            }, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        # Handle user signup: create a new user and hash the password
        data = request.data
        data['password'] = make_password(data['password'])  # Secure password before saving
        
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()  # Save the user instance

            # Generate a token for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Include the token in the response
            return Response({
                'user': serializer.data,
                'access_token': access_token,
                'refresh_token': str(refresh)  # Optionally include refresh token as well
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogPost(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can post blogs
    parser_classes = (MultiPartParser, FormParser)  # To handle file uploads

    def post(self, request):
        # Prepare the blog post data
        data = request.data.copy()  # Copy data to ensure we can modify it
        data['created_by'] = request.user.id  # Set the created_by field with the current user's ID
        
        # Check if community exists
        community_name = data.get('community')
        try:
            community = Community.objects.get(name=community_name)  # Search for community by name
            data['community'] = community.id  # Set the community ID in the blog post data
        except Community.DoesNotExist:
            return Response({"error": "Community not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize the serializer with request context
        serializer = BlogSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()  # Save the blog post with the created_by field populated
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollInCommunity(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can enroll

    def post(self, request):
        # Extract community name from request data
        community_name = request.data.get('community')
        
        # Validate if community name is provided
        if not community_name:
            return Response({"error": "Community name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the community exists
        try:
            community = Community.objects.get(name=community_name)  # Query community by name
        except Community.DoesNotExist:
            return Response({"error": "Community not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get the authenticated user
        user = request.user
        
        # Check if user is already enrolled in the community
        if UserCommunity.objects.filter(user=user, community=community).exists():
            return Response({"error": "User is already enrolled in this community"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new UserCommunity instance to enroll the user in the community
        user_community = UserCommunity(user=user, community=community)
        user_community.save()
        
        # Return success response with community enrollment details
        return Response({"message": "Successfully enrolled in the community", "community": community_name}, status=status.HTTP_201_CREATED)
    

class ViewAllBlogsInEnrolledCommunity(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can view blogs

    def get(self, request):
        # Get the authenticated user
        user = request.user
        
        # Fetch the communities the user is enrolled in
        enrolled_communities = UserCommunity.objects.filter(user=user)
        
        if not enrolled_communities.exists():
            return Response({"error": "User is not enrolled in any community"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the IDs of the communities the user is enrolled in
        community_ids = [user_community.community.id for user_community in enrolled_communities]
        
        # Fetch all blogs belonging to those communities
        blogs = Blog.objects.filter(community__in=community_ids).order_by('-created_at')  # Order by creation date (most recent first)
        
        # If no blogs found in enrolled communities
        if not blogs.exists():
            return Response({"message": "No blogs found in the communities you're enrolled in."}, status=status.HTTP_200_OK)
        
        # Serialize the blog data
        blog_serializer = BlogSerializer(blogs, many=True)
        
        return Response(blog_serializer.data, status=status.HTTP_200_OK)
    


class GetUserNotifications(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user, read=False)

        # Check if notifications are expired and mark them as read
        for notification in notifications:
            if notification.is_expired():
                notification.read = True
                notification.save()

        # Serialize the notifications
        notification_serializer = NotificationSerializer(notifications, many=True)
        return Response(notification_serializer.data, status=200)


class MarkNotificationAsRead(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        user = request.user
        try:
            notification = Notification.objects.get(id=notification_id, user=user)
            notification.read = True
            notification.save()
            return Response({"message": "Notification marked as read"}, status=200)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=404)
