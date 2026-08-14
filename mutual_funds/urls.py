from django.urls import path
from . import views

app_name = 'mutual_funds'

urlpatterns = [
    path('', views.mutual_fund_list_view, name='fund_list'),
    path('add/', views.add_mutual_fund_view, name='add_fund'),
    path('<int:pk>/edit/', views.edit_mutual_fund_view, name='edit_fund'),
    path('<int:pk>/delete/', views.delete_mutual_fund_view, name='delete_fund'),
    path('import/', views.import_mutual_funds_view, name='import_funds'),
    path('export/', views.export_mutual_funds_view, name='export_funds'),
]
