from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from geotrek.tourism.models import DataSource, TouristicContentCategory


class DataSourceAdmin(TranslationAdmin):
    list_display = ('title', 'pictogram_img')
    search_fields = ('title',)


class TouristicContentCategoryAdmin(TranslationAdmin):
    list_display = ('label', 'pictogram_img')
    search_fields = ('label',)


admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(TouristicContentCategory, TouristicContentCategoryAdmin)
