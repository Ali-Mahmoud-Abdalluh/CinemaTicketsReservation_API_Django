from django.contrib import admin

from . import models

admin.site.register(models.Guest)
admin.site.register(models.Movie)
admin.site.register(models.Reservation)