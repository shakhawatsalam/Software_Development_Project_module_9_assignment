from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return  self.name

class Event(models.Model):
    name =  models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='event_asset', blank=True, null=True)
    date  = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, related_name='participants')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return  self.name
    


    
    
