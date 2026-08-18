from django.urls import path
from . import views

app_name = 'bank_details'

urlpatterns = [
    path('', views.bank_detail_list_view, name='list'),
    path('add/', views.add_bank_detail_view, name='add'),
    path('<int:pk>/edit/', views.edit_bank_detail_view, name='edit'),
    path('<int:pk>/delete/', views.delete_bank_detail_view, name='delete'),
    path('import/', views.import_bank_details_view, name='import'),
    path('export/', views.export_bank_details_view, name='export'),
    path('api/lookup/', views.bank_detail_lookup_api, name='api_lookup'),
]
