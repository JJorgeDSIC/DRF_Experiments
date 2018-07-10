from django.contrib.auth.models import User


print("Creating super user")

user=User.objects.create_user('admin', password='bar')
user.is_superuser=True
user.is_staff=True
user.save()


print("Creating fake users")

users = []

for i in range(11):

	user=User.objects.create_user('FakeUser' + str(i), password='bar')
	users.append(user)

print("Creating fake friendships")


from api.models import Profile
from api.models import Friend
from api.models import Recommendation


for i in range(5):
	friendship = Friend(to_user=Profile.objects.get(pk=2),from_user=Profile.objects.get(pk=i+1+2))
	friendship.save()


for i in range(2,5):
	friendship = Friend(to_user=Profile.objects.get(pk=i+1),from_user=Profile.objects.get(pk=i+2))
	friendship.save()


print("Creating fake recommendations")


for i in range(5):

	recommendation = Recommendation(
		title="title" + str(i), 
		comment="comment" + str(i), 
		reference="www.reference."+ str(i) + ".com",
		owner=users[i], 
		source=Profile.objects.get(pk=i+1), 
		destination=Profile.objects.get(pk=i+2), 
		state=1)
	recommendation.save()
