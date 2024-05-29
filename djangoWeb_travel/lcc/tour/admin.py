from django.contrib import admin

# Register your models here.
from .models import Travel

class ToursAdmin(admin.ModelAdmin):
    list_display = ('platform', 'depDate', 'title')

admin.site.register(Travel, ToursAdmin)