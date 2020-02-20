# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView

class ExhibitionsView(TemplateView):    
    template_name = "www/exhibitions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Sirkka Pelkonen - Näyttelyt" 
        context['active_tab'] = "exhibitions"
        return context
