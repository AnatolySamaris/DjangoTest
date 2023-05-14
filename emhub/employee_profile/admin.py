from django.contrib import admin
from .models import Employee, Payment, Dayoff

admin.site.register(Employee)
admin.site.register(Payment)
admin.site.register(Dayoff)
