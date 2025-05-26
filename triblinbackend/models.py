from django.db import models
import uuid

class PlasticItem(models.Model):
    item_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)  
    username = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100,blank=True, null=True)
    location = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    date = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.item_name} ({self.item_id})"
    
