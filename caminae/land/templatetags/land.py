from django import template
from django.conf import settings

from caminae.land.models import District, City

register = template.Library()

# Here, register is a django.template.Library instance, as before


def get_bbox_cities():
    return [
        (city.name or city.pk, city.geom.transform(settings.API_SRID, clone=True).extent)
        for city in City.objects.all()
    ]

def get_bbox_districts():
    return [
        (district.name or district.pk, district.geom.transform(settings.API_SRID, clone=True).extent)
        for district in District.objects.all()
    ]

def combobox_bbox_land():
    return { 'bbox_cities': get_bbox_cities(), 'bbox_districts': get_bbox_districts() }

register.inclusion_tag('land/bbox.html')(combobox_bbox_land)

