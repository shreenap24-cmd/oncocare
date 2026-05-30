from django.urls import path
from . import views

urlpatterns = [
    path('', views.treatment_list, name='treatment_list'),
    path('add/', views.treatment_add, name='treatment_add'),
    path('edit/<int:pk>/', views.treatment_edit, name='treatment_edit'),
    path('delete/<int:pk>/', views.treatment_delete, name='treatment_delete'),
]