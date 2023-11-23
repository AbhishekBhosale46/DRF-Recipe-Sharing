from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.UpdateUserView.as_view(), name='me'),
    path('reset-password/', views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/<int:user_id>/<str:token>/', views.PasswordResetConfirmationView.as_view()),
]

