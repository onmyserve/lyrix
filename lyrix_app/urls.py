from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'), # Add this for home page
    path('add-user/', views.add_user_view, name='add_user'),
]