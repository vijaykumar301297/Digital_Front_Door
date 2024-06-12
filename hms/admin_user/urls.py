from django.urls import path
from . import views


urlpatterns = [
    path('admin-list', views.admin_list, name='admin'),
    path('create-admin', views.create_user, name='admin_create'),
    path('edit-admin/<id>', views.edit_admin, name='admin_edit'),
    path('delete-admin/<id>', views.del_admin, name='admin_delete'),
    path('activate/<uidb64>/<token>', views.activate_user, name='activate'),
]
