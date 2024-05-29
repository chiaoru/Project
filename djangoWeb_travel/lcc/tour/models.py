from django.db import models

# Create your models here.

class Travel(models.Model):
    platform =models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    depDate = models.CharField(max_length=30)
    img = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    createDate = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table='tours'