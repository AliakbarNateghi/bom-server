from django.contrib import admin
from django.contrib.auth.models import Permission
from ModelTracker.Tracker import TrackerAdmin

admin.site.register(Permission, TrackerAdmin)