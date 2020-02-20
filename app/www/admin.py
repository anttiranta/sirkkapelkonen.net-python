#-*- coding: utf-8 -*-
from django.contrib import admin

from www.models.www.category import Category
from www.models.www.product import Product

admin.site.register(Category)
admin.site.register(Product)