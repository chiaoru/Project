from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)
    sex  = models.CharField(max_length=2)
    birthday = models.DateField()
    email  = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    address  = models.CharField(max_length=200)
    password  = models.CharField(max_length=200)
    
    c_date  = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'customer'