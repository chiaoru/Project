from django.db import models

# Create your models here.
class travelNews(models.Model):
    platform = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    content = models.TextField()
    img = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    createDate = models.CharField(max_length=12)
    
    class Meta:
        db_table = 'news'