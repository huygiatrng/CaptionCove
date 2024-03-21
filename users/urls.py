from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('create_admin/', views.create_admin_user, name='create_admin_user'),
    path('logout/', views.user_logout, name='logout')
]