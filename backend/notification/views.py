from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

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
