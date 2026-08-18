from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.customer_list_view, name='customer_list'),
    path('add-user/', views.add_user_view, name='add_user'),
    path('customer-list', views.customer_list_view, name='customer_list'),
    path('add-customer/', views.add_customer_view, name='add_customer'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]
