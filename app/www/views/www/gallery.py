# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect

from www.models.www.category import Category


class GalleryListView(ListView):
    default_template = "www/categories.html"
    products_template = "www/products.html"
    default_max_results_amount = 12
    products_max_results_amount = 24

    template_name = default_template
    ordering = 'position'
    paginate_by = default_max_results_amount
    category = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['page_heading'] = "Galleria"
        context['page_title'] = "Sirkka Pelkonen - Galleria"
        context['active_tab'] = "gallery"
        
        if self.category != None:
            context['page_heading'] = self.category.name
            context['page_title'] = "Sirkka Pelkonen - " + self.category.name
            context['category'] = self.category
            context['parent_category'] = self.__get_parent_category(self.category)
        
        return context

    def get(self, request, *args, **kwargs):
        try:
            category = self.__init_category()
        except ObjectDoesNotExist:
            raise Http404('Category does not exist')

        if category:
            self.queryset = self.__get_queryset_type(category)
            self.template_name = self.__get_template_type(category)
            self.paginate_by = self.__get_results_max_amount(category)

            # Add category into class variables so we can use it later to add data into context
            self.category = category
        else:
            # List root level categories
            self.queryset = Category.objects.all().filter(parent_id=None, active=True)

        return super().get(request, args, kwargs)

    '''
    Initialize requested category object
    '''
    def __init_category(self):
        url_key = self.__get_url_key()
        if url_key is None:
            return None
        
        return Category.objects.get(url_key=url_key, active=True)

    '''
    Get page template type based on category
    '''
    def __get_template_type(self, category):
        has_children = category.has_children()
        return self.default_template if has_children else self.products_template

    '''
    Get page queryset type based on category
    '''
    def __get_queryset_type(self, category):
        if category.has_children():
            return category.get_children(category, True, False)
        else:
            return category.get_products()  

    '''
    Get page max results amount based on category
    '''
    def __get_results_max_amount(self, category):
        if category.has_children():
            return self.default_max_results_amount
        else:
            return self.products_max_results_amount

    '''
    Get parent category of requested category
    '''
    def __get_parent_category(self, category):
        try: 
            return category.get_parent_category(category)
        except ObjectDoesNotExist:
            return None   

    '''
    Get url key of requested category from request
    '''
    def __get_url_key(self):
        path_parts = list(filter(None, self.request.path.split('/')))

        if len(path_parts) == 2:
            return path_parts[1]
        return None