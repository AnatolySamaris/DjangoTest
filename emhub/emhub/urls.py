from django.contrib import admin, auth
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
    path('admin/', admin.site.urls),
    path('', include('employee_profile.urls'))
]