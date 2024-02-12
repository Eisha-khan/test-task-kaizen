
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, null=True,blank=True,unique=True)


class Item(models.Model):
    sku = models.CharField(max_length=30, null=True,blank=True)
    name = models.CharField(max_length=60,null=True, blank=True)
    tags = models.CharField(max_length=800,null=True, blank=True)
    category = models.ForeignKey(Category,to_field="name", on_delete=models.CASCADE)
    in_stock = models.IntegerField(blank=True, null=True,default=0)
    availble_stock = models.IntegerField(blank=True, null=True,default=0)


