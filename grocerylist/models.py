from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Item(models.Model):
    group = models.ForeignKey(to=Group,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class List(models.Model):
    shopping_date = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.shopping_date)

class Entry(models.Model):
    list = models.ForeignKey(to=List,on_delete=models.CASCADE)
    item = models.ForeignKey(to=Item,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.item.name

class SortOrder(models.Model):
    name = models.CharField(max_length = 50)

class SortOrderSlot(models.Model):
    sort_order = models.ForeignKey(to=SortOrder, on_delete=models.CASCADE)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    order_num = models.IntegerField()