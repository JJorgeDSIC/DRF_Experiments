
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView, ProfileView, ProfileDetailsView, ProfileViewFriends
from rest_framework.authtoken.views import obtain_auth_token # add this import

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls',
                               namespace='rest_framework')), 
    url(r'^recommendation/$', CreateView.as_view(), name="create"),
    url(r'^recommendation/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name="details"),
    #url(r'^users/$', ProfileView.as_view(), name="users"),
    url(r'users/(?P<pk>[0-9]+)/$',
        ProfileView.as_view(), name="user_details"),
    url(r'users/(?P<pk>[0-9]+)/friends$',
        ProfileViewFriends.as_view(), name="user_friend_details"),
    url(r'^get-token/', obtain_auth_token), # Add this line
}

urlpatterns = format_suffix_patterns(urlpatterns)