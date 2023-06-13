from rest_framework import viewsets, generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import get_object_or_404
from core.models import Recipe, Comment
from recipe import serializers



class UserRecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class RecipeList(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.exclude(group__isnull=False)
        return queryset.filter(is_public=True)



class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        recipe_id = self.kwargs['recipe_id']
        try:
            recipe = Recipe.objects.get(pk=recipe_id, is_public=True, group__isnull=True)
            return Comment.objects.filter(recipe=recipe)
        except ObjectDoesNotExist:
            raise ValidationError({"detail": "recipe not found"})

    def perform_create(self, serializer):
        recipe_id = self.kwargs['recipe_id']
        recipe = Recipe.objects.get(pk=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)
    


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        recipe_id = self.kwargs['recipe_id']
        comment_id = self.kwargs['pk']
        queryset = queryset.filter(recipe=recipe_id, pk=comment_id)
        return queryset

    def perform_update(self, serializer):
        comment = self.get_object()
        user = self.request.user
        if comment.user != user:
            raise PermissionDenied()
        serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        if instance.user != user:
            raise PermissionDenied()
        instance.delete()



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_unlike(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.likes.filter(pk=request.user.id).exists():
        recipe.likes.remove(request.user)
        return Response({'message': 'Unliked the recipe'})
    else:
        recipe.likes.add(request.user)
        return Response({'message': 'Liked the recipe'})
