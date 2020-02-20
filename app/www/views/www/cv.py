# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView

class CvView(TemplateView):    
    template_name = "www/cv.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Sirkka Pelkonen - Curriculum Vitae" 
        context['active_tab'] = "cv"
        return context
