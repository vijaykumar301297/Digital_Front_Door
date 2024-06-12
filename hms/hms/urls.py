
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('department.urls')),
    path('', include('admin_user.urls')),
    path('', include('doctor_users.urls')),
    path('', include('staff.urls')),
    path('', include('patientbooking.urls')),
    path('', include('settings.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
