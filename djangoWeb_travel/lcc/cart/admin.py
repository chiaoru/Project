from django.contrib import admin

# Register your models here.
from cart import models

admin.site.register(models.OrderModel)
admin.site.register(models.DetailModel)