from django.apps import apps
from django.contrib import admin

from ..log.Tracker import TrackerAdmin
from .models import BomUser, HiddenColumns

admin.site.register(BomUser, TrackerAdmin)
admin.site.register(HiddenColumns)
