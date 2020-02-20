# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist

class Category(models.Model):

    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    children_count = models.IntegerField(default=0)
    position = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    url_key = models.CharField(
        unique=True, max_length=255, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['parent_id']),
        ]

    __cached_results = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        opts = self._meta

        for field in opts.concrete_fields:
            setattr(self, '__orig_%s' %
                    field.attname, getattr(self, field.attname))

    def __get_orig_data(self, field):
        return getattr(self, '__orig_%s' % field)

    def __has_data_changed(self, field):
        orig = '__orig_%s' % field

        if getattr(self, orig) != getattr(self, field):
            return True
        return False

    def is_object_new(self):
        return self._get_pk_val() == None

    def get_products(self, is_active_flag=True):
        return self.products.filter(active=is_active_flag)

    def get_children(self, category, is_active_flag=True, recursive=True):
        children = Category.objects.all().filter(
            parent_id=category.pk, active=is_active_flag)

        if recursive == False:
            return children
        else:
            children = []
            for child in children:
                children = children + child.get_children(child, is_active_flag, recursive)
            return children

    def has_children(self, force=False):
        if force == False:
            try:
                return self.__cached_results[self.pk]['has_children']
            except:
                pass

        has_children = self.get_children_amount(self) > 0

        self.__cached_results.update({self.pk: {'has_children': has_children}})
        return self.__cached_results[self.pk]['has_children']

    def get_children_amount(self, category, is_active_flag=True):
        return Category.objects.values('id').filter(parent_id=category.pk, active=is_active_flag).count()

    def get_parent_category(self, category):
        parent = None
        if category.parent_id:
            parent = Category.objects.get(pk=category.parent_id)

        if parent == None:
            raise ObjectDoesNotExist(
                "The category that was requested doesn't exist. Verify the category and try again."
                )
        return parent

    def get_all_parent_categories(self, category):
        parents = []

        try:
            parent = self.get_parent_category(category)
            if parent.parent_id:
                parents = parents + self.get_all_parent_categories(parent)
                parents.append(parent)
            else:
                parents.append(parent)
        except ObjectDoesNotExist:
            pass

        return parents

    def get_all_child_categories(self, category): 
        children = []
        for child in Category.objects.all().filter(parent_id=category.pk):
            children = children + child.get_all_child_categories(child)
            children.append(child)

        return children

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.__before_save()
        super().save(force_insert, force_update, using, update_fields)

    def __before_save(self):
        if self.children_count is None:
            self.children_count = 0
        if self.url_key is None:
            raise ValueError('Category is missing the url key. Please add the key and try again.')

        if self.parent_id is not None:
            if self.parent_id <= 0:
                self.parent_id = None
            elif self.parent_id > 0:
                self.get_parent_category(self)

        if self.position is None:
            self.position = self.__get_max_position(self.parent_id) + 1

        if self.is_object_new(): 
            # Increase children count for all category parents
            for parent in self.get_all_parent_categories(self):
                parent.children_count += 1
                parent.save()
        else:
            if self.__has_data_changed('parent_id'):
                raise RuntimeError('Sorry, but we can\' move the category. Please delete the category and create a new instead.')

    def delete(self, using=None, keep_parents=False):
        self.__before_delete()
        super().delete(using, keep_parents)

    def __before_delete(self):
        assert self._get_pk_val() is not None, (
            "%s object can't be deleted because its %s attribute is set to None." %
            (self._meta.object_name, self._meta.pk.attname)
        )

        for child in self.get_all_child_categories(self):
            child.delete()

        # Decrease children count for all category parents
        for parent in self.get_all_parent_categories(self):
            parent.children_count -= 1
            parent.save()

    def __get_max_position(self, parent_id):
        position = Category.objects.values('position').filter(
            parent_id=parent_id).aggregate(position=Max('position'))
        position = position if isinstance(
            position, int) else position['position']

        if position == None:
            position = 0
        return position

    def __str__(self):
        return self.name
