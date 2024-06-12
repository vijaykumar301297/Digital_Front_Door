from django.urls import path
from . import views

urlpatterns = [
    path('staff/staff-list/', views.staff_list, name='stafflist'),
    path('staff/create-staff/', views.create_staff_user, name="addstaff"),
    path('staff/edit-staff/<id>', views.edit_staff, name="editstaff"),
    path('staff/delete-staff/<id>', views.del_staff, name="del_staff"),
    path('staff/appointment/', views.patient_appointment, name="appoinment-list"),
    path('staff/patients/', views.patient, name="patient-list"),
    path('staff/Doctor-schedule/', views.schedule_list, name="sechedule-list"),
    path('staff/add-patient/', views.book_patient_offline, name="add_patient"),
]