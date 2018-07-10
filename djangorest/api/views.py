from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .serializers import RecommendationSerializer, UserSerializer, ProfileSerializer, FriendSerializer
from .models import Recommendation, Profile, Friend
from .permissions import IsOwner, IsIdentifiedUser

from django.contrib.auth.models import User

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner) #This could be permissions.IsAuthenticatedOrReadOnly for GET, HEAD and OPTIONS


    def get_queryset(self):    
        """Only return recommendation items owned by the currently authenticated user."""

        user = self.request.user
        return Recommendation.objects.filter(owner=user)

    def perform_create(self, serializer):
        """Save the post data when creating a new Recommendation."""
        print(self.request.POST["source"])
        #source = Profile.objects.get(pk=self.request.POST["source"])
        #destination = Profile.objects.get(pk=self.request.POST["destination"])
        serializer.save(owner=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class ProfileView(generics.RetrieveAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsIdentifiedUser)
        #"""View to list the user queryset."""

class ProfileViewFriends(generics.ListAPIView):
    """View to list the user queryset."""
    #queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsIdentifiedUser)


    def get_queryset(self):    
        """Only return recommendation items owned by the currently authenticated user."""

        user = self.request.user
        profile = Profile.objects.get(user=User.objects.get(username=user))
        friends = Friend.objects.filter(to_user=profile)
        custom_list = [friend.to_user.id for friend in friends]
        querset = Profile.objects.filter(id__in=custom_list)
        return querset

class ProfileDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = Profile.objects.all()    
    serializer_class = ProfileSerializer
