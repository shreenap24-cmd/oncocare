from django.urls import path
from . import views

urlpatterns = [
    path('', views.cancer_profile_list, name='cancer_profile_list'),
    path('add/', views.cancer_profile_add, name='cancer_profile_add'),
    path('delete/<int:pk>/', views.cancer_profile_delete, name='cancer_profile_delete'),
    path('<int:profile_pk>/readings/', views.biomarker_readings, name='biomarker_readings'),
    path('<int:profile_pk>/readings/add/', views.biomarker_add, name='biomarker_add'),
    path('readings/delete/<int:pk>/', views.biomarker_delete, name='biomarker_delete'),
]