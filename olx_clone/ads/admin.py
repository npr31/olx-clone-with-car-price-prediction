from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import VehicleAd
from .models import Feedback

admin.site.register(Feedback)
admin.site.register(VehicleAd)
