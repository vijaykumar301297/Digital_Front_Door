from django.urls import path
from . import views

urlpatterns = [
    path('edit-account-info/', views.account_setting, name='account'),
    path('account-info/', views.account_info, name='account_info'),
    path('change-password/', views.password_update, name='password_change'),
]
