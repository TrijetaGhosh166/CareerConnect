from django.contrib import admin
from .models import Profile, RecruiterProfile, SeekerProfile

admin.site.register(Profile)
admin.site.register(SeekerProfile)
admin.site.register(RecruiterProfile)
