# -*- coding: utf-8 -*-
import csv
import os
from www.models.www.category import Category

class CategoryDataInstaller:
    apps = None
    category_ids = {}

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
                        value = row[key].strip() if row[key].strip() != '' else None
                        if value:
                            data.update({header[key]: value})

                    if 'position' not in data:
                        data.update({'position': index})

                    self.__create_category(data)
                    index += 1

    def __create_category(self, row):
        Category = self.__get_category_model()

        category = Category()
        category.name = row.get('name')
        category.image = row.get('image')
        category.position = row.get('position', 0)
        category.active = row.get('active', True)
        category.url_key = row.get('url_key')
        
        parent = row.get('parent_category_url_key')
        if parent != None:
            category.parent_id = self.__get_category_id_by_url_key(parent)

        if self.__is_existing_category(category) == False:
            category.save()

    def __is_existing_category(self, category):
        return self.__get_category_model().objects.filter(name=category.name, image=category.image,
                      parent_id=category.parent_id).count() > 0

    def __get_category_id_by_url_key(self, url_key):
        Category = self.apps.get_model('www', 'Category')
        
        if url_key not in self.category_ids:
            category = Category.objects.get(url_key=url_key)
            self.category_ids.update({url_key: category.id})

        if url_key in self.category_ids:
            return self.category_ids.get(url_key)
        return None

    def __get_category_model(self):
        return self.apps.get_model('www', 'Category')    