from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='user-register'),
    path('profile/', views.get_user_profile, name='user-profile'),
]