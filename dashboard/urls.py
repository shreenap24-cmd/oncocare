from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
    path('<int:pk>/complete/', views.appointment_mark_complete, name='appointment_mark_complete'),
]