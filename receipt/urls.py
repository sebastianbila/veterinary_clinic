from django.urls import path
from receipt import views

urlpatterns = [
    path('create/', views.receipt, name='receipt'),
]