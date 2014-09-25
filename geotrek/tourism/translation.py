from django.conf import settings

from modeltranslation.translator import translator, TranslationOptions

from geotrek.tourism.models import DataSource, TouristicContent, TouristicContentCategory


class DataSourceTO(TranslationOptions):
    fields = ('title',)


class TouristicContentTO(TranslationOptions):
    fields = ('name',) + (('published',) if settings.PUBLISHED_BY_LANG else tuple())
    fallback_undefined = {'published': None}


class TouristicContentCategoryTO(TranslationOptions):
    fields = ('label',)


translator.register(DataSource, DataSourceTO)
translator.register(TouristicContent, TouristicContentTO)
translator.register(TouristicContentCategory, TouristicContentCategoryTO)
