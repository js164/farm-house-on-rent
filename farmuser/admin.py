from django.contrib import admin
from farmuser.models import Farm,FarmImage,FarmAvailble,FarmBooking

# Register your models here.

admin.site.register(Farm)
admin.site.register(FarmImage)
admin.site.register(FarmAvailble)
admin.site.register(FarmBooking)
