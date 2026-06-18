from django.urls import path
from . import views

urlpatterns = [
    path('', views.assistant_view, name='assistant'),
    path('ask/', views.ask_question, name='ask_question'),
]