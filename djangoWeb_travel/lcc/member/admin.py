from django.contrib import admin

# Register your models here.
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','mobile','email')
    
    
admin.site.register(Customer,CustomerAdmin)    