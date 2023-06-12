from django.contrib import admin
from .models import client, adventure, schedule, ContactUSData, packages

# Register your models here.

admin.site.register(client)
admin.site.register(adventure)
admin.site.register(schedule)
admin.site.register(packages)
# admin.site.register(ContactUSData)
