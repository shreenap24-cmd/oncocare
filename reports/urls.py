from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('add/', views.report_add, name='report_add'),
    path('delete/<int:pk>/', views.report_delete, name='report_delete'),
]