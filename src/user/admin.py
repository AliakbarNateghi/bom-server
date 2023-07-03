from django.apps import apps
from django.contrib import admin

from .models import BomUser

admin.site.register(BomUser)