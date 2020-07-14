from django.urls import path
from patients import views

urlpatterns = [
    path('patients', views.patients, name='patients'),
    path('add_patients', views.add_patients, name='add_patients'),
    path('get_patient', views.get_patient, name='get_patient'),
    path('save_patient', views.save_patient, name='save_patient'),
    path('delete_patient/', views.delete_patient, name='delete_patient'),
]