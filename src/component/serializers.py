from rest_framework import serializers

from .models import BomComponent


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BomComponent
        fields = '__all__'