from modeltranslation.translator import translator, TranslationOptions

from geotrek.tourism.models import DataSource, TouristicContent, TouristicContentCategory


class DataSourceTO(TranslationOptions):
    fields = ('title',)


class TouristicContentTO(TranslationOptions):
    fields = ('name',)


class TouristicContentCategoryTO(TranslationOptions):
    fields = ('label',)


translator.register(DataSource, DataSourceTO)
translator.register(TouristicContent, TouristicContentTO)
translator.register(TouristicContentCategory, TouristicContentCategoryTO)
