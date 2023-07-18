from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
import json


from .models import BomComponent, FieldPermission
from .serializers import ComponentSerializer, FieldPermissionSerializer
from ..core.permissions import IsGod


class Component(ModelViewSet):
    queryset = BomComponent.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        groups = user.groups.all()
        # permission to create a new object
        permissions = FieldPermission.objects.filter(group__in=groups, method='create')
        if not permissions:
            return Response({"message": "you don't have access to create a new component"})
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=201)   
        return Response(serialized_data.errors, status=400)
    
    def retrieve(self, request, pk=None):
        user = request.user
        groups = user.groups.all()
        permissions = FieldPermission.objects.filter(group__in=groups, method='retrieve', instance_id=pk)
        if not permissions:
            return Response({"message": "You don't have access to see this particular component"})
        obj = self.get_object()
        fields = [permission.field for permission in permissions]
        serialized_data = {field: getattr(obj, field) for field in fields}
        return Response(serialized_data)
    
    def partial_update(self, request, pk=None):
        user = request.user
        groups = user.groups.all()
        permissions = FieldPermission.objects.filter(group__in=groups, method='partial_update', instance_id=pk)
        if not permissions:
            return Response({"message": "You don't have access to edit this particular cell"})
        obj = self.get_object()
        fields = [permission.field for permission in permissions]
        filtered_dict = {k: v for k, v in request.data.items() if k in fields}
        serialized_data = self.serializer_class(obj, data=filtered_dict, partial=True)
        if serialized_data.is_valid():
            serialized_data.save()
            serialized_data = {k: v for k, v in serialized_data.data.items() if k in fields}
            return Response(serialized_data)
        return Response(serialized_data.errors, status=400)
    
    def destroy(self, request, pk=None):
        user = request.user
        groups = user.groups.all()
        permission = FieldPermission.objects.filter(group__in=groups, method='')
        queryset = self.get_queryset()
        obj = self.get_object()
        obj.delete()
        return Response(status=204)


class FieldPermissionView(ModelViewSet):
    queryset = FieldPermission.objects.all()
    serializer_class = FieldPermissionSerializer
    permission_classes = [IsAuthenticated, IsGod]