from modeltranslation.translator import translator, TranslationOptions

from geotrek.tourism.models import DataSource, TouristicContent


class DataSourceTO(TranslationOptions):
    fields = ('title',)


class TouristicContentTO(TranslationOptions):
    fields = ('name',)


translator.register(DataSource, DataSourceTO)
translator.register(TouristicContent, TouristicContentTO)
