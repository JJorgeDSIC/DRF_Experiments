from django.contrib import admin

# Register your models here.
from .models import Recommendation, Profile, Friend

#admin.site.register(User)
admin.site.register(Recommendation)
admin.site.register(Profile)
admin.site.register(Friend)