from django.contrib import admin
from .models import Doctor, User, Appointment, Specialization, TimeSlot, Service, Payment

admin.site.register(Doctor)
admin.site.register(User)
admin.site.register(Appointment)
admin.site.register(Specialization)
admin.site.register(TimeSlot)
admin.site.register(Service)
admin.site.register(Payment)