from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Account)
admin.site.register(Favourites)
admin.site.register(Requests)
admin.site.register(Notifications)