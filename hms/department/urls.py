from django.urls import path
from . import views

urlpatterns = [
    path('department/department-list/', views.department_list, name='department_list'),
    path('department/create-department/', views.create_department, name="add_department"),
    path('department/edit-department/<id>', views.edit_department, name="edit_department"),
    path('department/delete-department/<id>', views.del_department, name="delete"),
]
