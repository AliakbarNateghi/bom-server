from django.apps import apps
from django.contrib import admin
from ModelTracker.Tracker import TrackerAdmin

from .models import BomComponent, FieldPermission

admin.site.register(BomComponent, TrackerAdmin)
admin.site.register(FieldPermission)