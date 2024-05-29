from django.db import models

# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=50) 
    content = models.TextField(null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "contact"