from django.contrib import admin
from .models import User, District, Hostel, Mess, Visitor, Application

# Register your models here.
admin.site.register(User)
admin.site.register(District)
admin.site.register(Hostel)
admin.site.register(Mess)
admin.site.register(Visitor)
admin.site.register(Application)