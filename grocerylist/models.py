from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models

# --- --- --- Shopping List Models --- --- ---
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

# --- --- --- Recipe Models --- --- ---
class Recipe(models.Model):
    name = models.CharField(max_length=200)

class Unit(models.Model):
    MEASUREMENT_CHOICES = [
        ('weight',  'Weight'),
        ('volume',  'Volume'),
        ('count',   'Count'),
    ]
    name = models.CharField(max_length=200)
    measurement_type = models.CharField(max_length=6, choices=MEASUREMENT_CHOICES)

class Ingredient(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    item = models.ForeignKey(to=Item, on_delete=models.SET_NULL, null=True)    
    quantity = models.DecimalField(max_digits=9, decimal_places=3)
    unit = models.ForeignKey(to=Unit, on_delete=models.SET_NULL, null=True)