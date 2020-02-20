#-*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max
from .category import Category

class Product(models.Model):
    
    category = models.ForeignKey(Category, related_name="products", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(db_index=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255,  null=True, blank=True)
    thumbnail = models.CharField(max_length=255, null=True, blank=True)
    position = models.IntegerField(default=0)
    active = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
            update_fields=None):
        self.__before_save(force_insert, force_update, using, update_fields)

        super().save(force_insert, force_update, using, update_fields)

    def __before_save(self, force_insert=False, force_update=False, using=None,
            update_fields=None):
        if self.position is None:
            self.position = self.__get_max_position(self.category) + 1

    def __get_max_position(self, category):
        category_id = None
        if isinstance(category, int):
            category_id = category
        elif isinstance(category, Category): 
            category_id = category.pk
        else:
            raise ValueError('Unsupported category value given.')

        position = Product.objects.values('position').filter(
            category=category_id).aggregate(Max('position'))
        position = position if isinstance(position, int) else position['position']

        if position == None:
            position = 0
        return position

    def __str__(self):
        return self.name