from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.profile, name='profile'),
    path('payments', views.payments),
    path('dayoff', views.dayoff, name='dayoff'),
    path('dayoff/application_form', views.application_form)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
