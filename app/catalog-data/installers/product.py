# -*- coding: utf-8 -*-
import csv
import os
from django.core.exceptions import ObjectDoesNotExist

from www.models.www.product import Product
from www.models.www.category import Category


class ProductDataInstaller:
    categories = {}
    apps = None

    def __init__(self, apps):
        self.apps = apps

    def install(self, fixtures):
        for file_name in fixtures:
            if os.path.exists(file_name) == False:
                continue

            with open(file_name, encoding='utf-8') as csv_file:
                rows = list(csv.reader(csv_file, delimiter=','))
                header = rows.pop(0)
                index = 0

                for row in rows:
                    data = {}

                    for key in range(len(row)):
                        value = row[key].strip(
                        ) if row[key].strip() != '' else None
                        if value:
                            data.update({header[key]: value})

                    if 'position' not in data:
                        data.update({'position': index})
                    
                    self.__create_product(data)
                    index += 1

    def __create_product(self, row):
        Product = self.__get_product_model()

        product = Product()
        product.name = row.get('name')
        product.description = row.get('description')
        product.image = row.get('image')
        product.thumbnail = row.get('thumbnail')
        product.position = row.get('position', 0)
        product.active = row.get('active', True)

        category = row.get('category_url_key')
        if category != None:
            product.category = self.__get_category_by_url_key(category)

        if self.__is_existing_product(product) == False:
            product.save()

    def __is_existing_product(self, product):
        category_id = product.category.id if product.category != None else None

        return self.__get_product_model().objects.filter(name=product.name, image=product.image,
                      category_id=category_id).count() > 0

    def __get_category_by_url_key(self, url_key):
        Category = self.__get_category_model()

        if url_key not in self.categories:
            try:
                category = Category.objects.get(url_key=url_key)
                self.categories.update({url_key: category})
            except ObjectDoesNotExist:
                pass

        if url_key in self.categories:
            return self.categories.get(url_key)
        return None

    def __get_product_model(self):
        return self.apps.get_model('www', 'Product')

    def __get_category_model(self):
        return self.apps.get_model('www', 'Category')
