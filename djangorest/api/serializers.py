
from rest_framework import serializers
from .models import Recommendation, Profile, Friend

from django.contrib.auth.models import User

class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    owner = serializers.ReadOnlyField(source='owner.username') # ADD THIS LINE

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Recommendation
        # Some fields are missing...
        fields = ('id', 'title', 'owner', 'comment', 'source', 'destination','reference', 'state', 'rating','date_created', 'date_modified') 
        read_only_fields = ('date_created', 'date_modified')



class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    recommendation = serializers.PrimaryKeyRelatedField(
    	many=True, queryset=Recommendation.objects.all())

    class Meta:
        """Map this serializer to the default django user model."""
        model = User
        fields = ('id', 'username', 'recommendation')


class FriendSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""
    to_user = serializers.ReadOnlyField(source='profile.id')
    from_user = serializers.ReadOnlyField(source='profile.id')
    class Meta:
        """Map this serializer to the default django user model."""
        model = Friend
        fields = ('to_user', 'from_user', 'created')




class ProfileSerializer(serializers.ModelSerializer):
    """A profile serializer to aid in authentication and authorization."""
    #friends = FriendSerializer(source='friend_set', many=True)
    class Meta:
        """Map this serializer to the default django user model."""
        model = Profile
        fields = ('user', 'friends')
