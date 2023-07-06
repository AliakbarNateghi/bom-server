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

    def list(self, request):
        user = request.user
        groups = user.groups.all()
        # permission to see all the objects
        permissions = FieldPermission.objects.filter(group__in=groups, method='list')
        if not permissions:
            return Response({"message": "you don't have access to the list of components"})
        fields = [permission.field for permission in permissions]
        queryset = self.get_queryset()
        serialized_data = self.serializer_class(queryset, many=True)
        # permission to see all objects with all fields
        if 'all' in fields:
            return Response(serialized_data.data)
        # permission to see all objects but fields that has been allowed
        else:
            filtered_data = []
            for item in serialized_data.data:
                filtered_item = {}
                for field in fields:
                    filtered_item[field] = item.get(field)
                filtered_data.append(filtered_item)
            return Response(filtered_data)

    def create(self, request):
        user = request.user
        groups = user.groups.all()
        # permission to create a new object
        permissions = FieldPermission.objects.filter(group__in=groups, method='create')
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            if permissions:
                serialized_data.save()
                return Response(serialized_data.data, status=201)
            else: 
                return Response({"message": "you don't have access to create a new component"})
        return Response(serialized_data.errors, status=400)
    
    def retrieve(self, request, pk=None):
        user = request.user
        groups = user.groups.all()
        permissions = FieldPermission.objects.filter(group__in=groups, method='retrieve', instance_id=pk)
        if not permissions:
            return Response({"message": "You don't have access to see this particular component"})
        obj = self.get_object()
        fields = [permission.field for permission in permissions]
        # if 'all' that means the user has permission to the whole object
        if 'all' in fields:
            serialized_data = self.serializer_class(obj)
            return Response(serialized_data.data)
        """
            permission to see only a field of only one object:
            all fields from the allowed object will be append to a list
            to return
        """ 
        serialized_data = {field: getattr(obj, field) for field in fields}
        return Response(serialized_data)

    # For updating only an object --> The permission of a whole object is given
    # def update(self, request, pk=None):
    #     user = request.user
    #     groups = user.groups.all()
    #     permissions = FieldPermission.objects.filter(group__in=groups, method='update', instance_id=pk)
    #     if not permissions:
    #         return Response({"message": "You don't have access to edit this particular component"})
    #     queryset = self.get_queryset()
    #     obj = self.get_object()
    #     serialized_data = self.serializer_class(obj, data=request.data)
    #     if serialized_data.is_valid():
    #         serialized_data.save()
    #         return Response(serialized_data.data)
    #     return Response(serialized_data.errors, status=400)
    
    def partial_update(self, request, pk=None):
        user = request.user
        groups = user.groups.all()
        # Permission to edit only the fields of an instance that GOD allowed
        permissions = FieldPermission.objects.filter(group__in=groups, method='partial_update', instance_id=pk)
        if not permissions:
            return Response({"message": "You don't have access to edit this particular cell"})
        obj = self.get_object()
        fields = [permission.field for permission in permissions]
        filtered_dict = {k: v for k, v in request.data.items() if k in fields}
        # The following that have been commented do the update action job
        if 'all' in fields:
            serialized_data = self.serializer_class(obj, data=request.data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response(serialized_data.data)
            return Response(serialized_data.errors, status=400)
        else:
            serialized_data = self.serializer_class(obj, data=filtered_dict, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response(serialized_data.data)
            return Response(serialized_data.errors, status=400)
        # return Response(serialized_data.errors, status=400)
    
    @action(detail=True, methods=['patch'])
    def update_column(self, request, field=None):
        pass
    
    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        obj = self.get_object()
        obj.delete()
        return Response(status=204)


class FieldPermissionView(ModelViewSet):
    queryset = FieldPermission.objects.all()
    serializer_class = FieldPermissionSerializer
    permission_classes = [IsAuthenticated, IsGod]