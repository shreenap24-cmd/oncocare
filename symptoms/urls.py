from django.urls import path
from . import views

urlpatterns = [
    path('', views.symptom_list, name='symptom_list'),
    path('add/', views.symptom_add, name='symptom_add'),
    path('edit/<int:pk>/', views.symptom_edit, name='symptom_edit'),
    path('delete/<int:pk>/', views.symptom_delete, name='symptom_delete'),
]