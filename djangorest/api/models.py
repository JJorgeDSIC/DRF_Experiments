from django.db import models
# Create your models here.

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)    
    friends = models.ManyToManyField('Profile', through = 'Friend')

    def __str__(self):
        return "%s" % (self.user.username)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Friend(models.Model):
    """ Model to represent Friendships """
    to_user = models.ForeignKey(Profile, models.CASCADE, related_name='profile_to')
    from_user = models.ForeignKey(Profile, models.CASCADE, related_name='profile_from')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User #%s is friends with #%s" % (self.to_user_id, self.from_user_id)

#    def save(self, *args, **kwargs):
#        # Ensure users can't be friends with themselves
#        if self.to_user == self.from_user:
#            raise ValidationError("Users cannot be friends with themselves.")
    

# class User(models.Model):
# 	username = models.CharField(max_length=255, blank=False, unique=True)
# 	profile_image = models.ImageField(upload_to = 'user_pic_folder/', blank=True, null=True, default = 'pic_folder/None/no-img.jpg')
# 	def __str__(self):
# 		"""Return a human readable representation of the model instance."""
# 		return "{}".format(self.username)

class Recommendation(models.Model):
	"""This class represents the Recommendation model."""
	title = models.CharField(max_length=255, blank=False)
	comment = models.CharField(max_length=255, blank=False)
	reference = models.CharField(max_length=255, blank=False)
	picture = models.ImageField(upload_to = 'recomm_pic_folder/', blank=True, null=True, default = 'pic_folder/None/no-img.jpg')

	owner = models.ForeignKey('auth.User', related_name='recommendation', on_delete=models.CASCADE) 

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	#source = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=False, null=True, related_name="recommended_by")
	#destination = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=False, null=True, related_name="recommended_to")
	source = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name="recommended_by")
	destination = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name="recommended_to")

	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)

	STATUS = (
		(1, 'pending'),
		(2, 'rated'),
		(3, 'deleted')
		)

	state = models.PositiveSmallIntegerField(choices=STATUS, null=True)

	RATE = (
		(0, 'bad'),
		(1, 'good')
		)
	rating = models.PositiveSmallIntegerField(choices=RATE, blank=True, null=True)

	def __str__(self):
		"""Return a human readable representation of the model instance."""
		return "{}".format(self.title)


# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
