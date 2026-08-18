from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contact_list_view, name='contact_list'),
    path('add/', views.add_contact_view, name='add_contact'),
    path('<int:pk>/edit/', views.edit_contact_view, name='edit_contact'),
    path('<int:pk>/delete/', views.delete_contact_view, name='delete_contact'),
    path('import/', views.import_contacts_view, name='import_contacts'),
    path('export/', views.export_contacts_view, name='export_contacts'),
]
