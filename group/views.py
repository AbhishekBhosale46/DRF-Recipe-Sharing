from rest_framework import viewsets, generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from core.models import Recipe, Group
from group import serializers
from recipe.serializers import RecipeSerializer


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


    
class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        group = self.get_object()
        user = self.request.user
        if group.owner != user:
            raise PermissionDenied()
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.owner != user:
            raise PermissionDenied()
        instance.delete()



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def join_group(request, group_id):
    user = request.user
    group = get_object_or_404(Group, pk=group_id)

    # if user in group.users.all():
    #     return Response({'message': 'You have already joined the group'})
    
    if user.group.filter(pk=group_id).exists():
        return Response({'message': 'You have already joined the group'})

    group.users.add(user)
    group.save()
    return Response({'message': 'You have joined the group successfully'})



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def leave_group(request, group_id):
    user = request.user
    group = get_object_or_404(Group, pk=group_id)

    # if user not in group.users.all():
    #     return Response({'message': 'You are not a member of this group'})

    if not user.group.filter(pk=group_id).exists():
        return Response({'message': 'You are not a member of this group'})

    group.users.remove(user)
    group.save()
    return Response({'message': 'You have left the group successfully'})



class GroupUserRecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        group_id = self.kwargs['group_id']
        group = get_object_or_404(Group, pk=group_id)

        if not user.group.filter(pk=group_id).exists():
            raise ValidationError({'message': 'You are not a member of this group'})
        else:
            return group.recipes.filter(user=user)


    def perform_create(self, serializer):
        user = self.request.user
        group_id = self.kwargs['group_id']
        group = get_object_or_404(Group, pk=group_id)

        if not user.group.filter(pk=group_id).exists():
            raise ValidationError({'message': 'You are not a member of this group'})
        else:
            recipe = serializer.save(user=user)
            group.recipes.add(recipe)



class GroupRecipeList(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        group_id = self.kwargs['group_id']
        group = get_object_or_404(Group, pk=group_id)

        if not user.group.filter(pk=group_id).exists():
            raise ValidationError({'message': 'You are not a member of this group'})
        else:
            return group.recipes.filter(is_public=True)
