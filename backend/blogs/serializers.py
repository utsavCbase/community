from rest_framework import serializers
from .models import Community, Blog, UserCommunity

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

    def create(self, validated_data):
        # Automatically set the 'created_by' field to the authenticated user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class UserCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCommunity
        fields = '__all__'