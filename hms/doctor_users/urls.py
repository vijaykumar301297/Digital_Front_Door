from django.urls import path
from . import views


urlpatterns = [
    path('create-doctor/', views.create_user, name='addDoctor'),
    path('doctor-list/', views.doctor_list, name='doctor'),
    path('edit-doctor/<id>', views.edit_doctor, name='edit_doctor'),
    path('delete-doctor/<id>', views.del_doctor, name='del_doctor'),
    path('schedule-session/<id>', views.schedule_day, name='session'),
    path('schedule-list/<id>', views.schedule_list, name='list'),
    path('edit-schedule/<id>', views.edit_schedule, name='edit'),
    path('del-schedule/<id>', views.delete_schedule, name='delete_schedule'),
    path('doctor/appointment/<id>', views.patient_appointment, name='doctor_appointment'),
    path('doctor/patients/<id>', views.patient, name='patients'),
]

