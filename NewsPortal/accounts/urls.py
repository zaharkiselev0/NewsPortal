from django.urls import path
from .views import subscribe, profile, change_user_info, UserDetail

urlpatterns = [
    path('subscribe/', subscribe, name='subscribe'),
    path('profile/', profile, name='profile'),
    path('change_user_info/', change_user_info, name='change_user_info'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user'),
]
