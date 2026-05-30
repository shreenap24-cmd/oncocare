from django.urls import path
from . import views

urlpatterns = [
    path('', views.medication_list, name='medication_list'),
    path('add/', views.medication_add, name='medication_add'),
    path('edit/<int:pk>/', views.medication_edit, name='medication_edit'),
    path('delete/<int:pk>/', views.medication_delete, name='medication_delete'),
]