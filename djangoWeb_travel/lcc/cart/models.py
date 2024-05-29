from django.db import models

# Create your models here.
class OrderModel(models.Model):
    subtotal = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    grandtotal = models.IntegerField(default=0)
    customename = models.CharField(max_length=50)
    customeemail  = models.CharField(max_length=100)
    customephone  = models.CharField(max_length=20)
    customeaddress  = models.CharField(max_length=200)
    paytype  = models.CharField(max_length=10)
    bankaccount  = models.CharField(max_length=10,null=True)
    create_date  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.customename
    
class  DetailModel(models.Model):
    
    dorder = models.ForeignKey('OrderModel', on_delete=models.CASCADE)
    
    pname = models.CharField(max_length=100)
    
    unitprice = models.IntegerField(default=0)
    quantity  = models.IntegerField(default=0)
    dtotal  = models.IntegerField(default=0)
    
    def __str__(self):
        return self.pname