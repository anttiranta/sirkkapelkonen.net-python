from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_site_info():
    return {
        'site_name': settings.SITE_NAME,
        'site_description': settings.SITE_DESCRIPTION,
        'site_keywords': ', '.join(settings.SITE_KEYWORDS),
    }