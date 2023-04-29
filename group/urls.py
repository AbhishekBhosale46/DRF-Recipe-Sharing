from django.urls import path, include
from rest_framework.routers import DefaultRouter
from group.views import GroupList, GroupDetail, join_group, leave_group, GroupUserRecipeViewSet, GroupRecipeList


router = DefaultRouter()
router.register('me', GroupUserRecipeViewSet)
router.register('all', GroupRecipeList)

app_name = 'group'

urlpatterns = [
    path('', GroupList.as_view(), name='all-groups'),
    path('<int:pk>', GroupDetail.as_view(), name='group-detail'),
    path('<int:group_id>/join', join_group),
    path('<int:group_id>/leave', leave_group),
    path('<int:group_id>/recipes/', include(router.urls)),

]
