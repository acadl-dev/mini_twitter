from rest_framework import serializers
from .models import User

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'followers', 'following']
