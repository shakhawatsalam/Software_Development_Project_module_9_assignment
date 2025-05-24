from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
   
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default.png')
    phone = models.CharField(blank=True,max_length=15, null=True)
    
    def __str__(self):
        return self.username
