from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class PlasticItem(models.Model):
    item_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)  
    username = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100,blank=True, null=True)
    location = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    replace = models.JSONField(default=list,blank=True)



class Program(models.Model):
    program_id = models.CharField(max_length=100, default=uuid.uuid4,unique=True)
    program_name = models.CharField(max_length=100)
    program_description = models.TextField(blank=True, null=True)
    program_start_date = models.DateField()
    program_end_date = models.DateField()


class Programusers(models.Model):
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    userid = models.CharField(max_length=100)


class Messages(models.Model):
    message_id = models.CharField(max_length=100, default=uuid.uuid4,unique=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)


class Blogs(models.Model):
    Blog_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    Blog_title = models.CharField(max_length=100)
    Blog_description = models.CharField(max_length=1000)
    Blog_Content = models.TextField(max_length=50000)


class Location(models.Model):
    location_id = models.CharField(max_length=100, default= uuid.uuid4, unique=True)
    location_name = models.CharField(max_length=100)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)


class Plastic_Item(models.Model):
    item_id = models.CharField(max_length=100, default= uuid.uuid4, unique=True)
    location_name = models.ForeignKey(Location,on_delete= models.CASCADE)
    plastic_type = models.CharField(max_length=100)
    plastic_name = models.CharField(max_length=100)
    date = models.DateField(max_length=100)
    quantity = models.IntegerField()
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)


class Plastic_Item_Replacement(models.Model):
    replacement_id = models.CharField(max_length=100, default= uuid.uuid4, unique=True)
    plastic_name = models.ForeignKey(Plastic_Item,on_delete=models.CASCADE)
    location_name = models.ForeignKey(Location,on_delete= models.CASCADE)
    replaced_with = models.CharField(max_length=100)
    quantity = models.IntegerField()
    date = models.DateField(max_length=100)
    disposed_type = models.CharField(max_length=100)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)


class location_count(models.Model):
    location_name = models.CharField(max_length=100)
    location_count = models.IntegerField()
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
