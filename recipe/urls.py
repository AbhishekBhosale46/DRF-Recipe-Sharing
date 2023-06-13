from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe.views import RecipeList, UserRecipeViewSet, CommentList, CommentDetail, like_unlike


router = DefaultRouter()
router.register('me', UserRecipeViewSet)
router.register('all', RecipeList)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
    path('all/<int:recipe_id>/comments/', CommentList.as_view(), name='all-comments'),
    path('all/<int:recipe_id>/comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
    path('all/<int:recipe_id>/like', like_unlike, name='like-unlike')
]
