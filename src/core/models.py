from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.utils import translation
from ModelTracker import Tracker


class BomBaseManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def archive(self):
        return super().get_queryset()


# class BomBaseModel(Tracker.ModelTracker):
class BomBaseModel(models.Model):  # Just for test for not saving logs
    deleted = models.BooleanField(default=False)
    deletable = models.BooleanField(default=True)
    editable = models.BooleanField(default=True)

    class Meta:
        abstract = True

    objects = BomBaseManger()
    indexes = [models.Index(fields=["deleted"])]


