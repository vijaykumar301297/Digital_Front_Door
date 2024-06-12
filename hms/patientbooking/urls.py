from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book, name='book'),
    path('books/', views.ajax_call, name='books'),
    path('book/patient-details/', views.book_patient, name='patient_book'),
    path('appointments/appointmets-lists/', views.patient_appointment, name='appointment'),
    path('patient/patient-lists/', views.patient, name='patient'),
    path('patient/book/', views.book_patient_offline, name='patient-book'),
    path('appointments/delete/<id>', views.del_appointment, name='appointment_delete'),
    path('patient/delete/<id>', views.del_patient, name='patient_delete'),

]
