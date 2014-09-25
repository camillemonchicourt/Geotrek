from django.contrib.gis.db import models as gis_models
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import lazy

from mapentity import registry
from mapentity.models import MapEntityMixin

from geotrek.authent.models import StructureRelated
from geotrek.common.mixins import (NoDeleteMixin, TimeStampedModelMixin,
                                   PictogramMixin, PublishableMixin)

from extended_choices import Choices
from multiselectfield import MultiSelectField


DATA_SOURCE_TYPES = Choices(
    ('GEOJSON', 'GEOJSON', _("GeoJSON")),
    ('TOURINFRANCE', 'TOURINFRANCE', _("TourInFrance")),
    ('SITRA', 'SITRA', _("Sitra")),
)


def _get_target_choices():
    """ Populate choices using installed apps names.
    """
    apps = [('public', _("Public website"))]
    for model, entity in registry.registry.items():
        if entity.menu:
            appname = model._meta.app_label.lower()
            apps.append((appname, unicode(entity.label)))
    return tuple(apps)


class DataSource(models.Model):
    title = models.CharField(verbose_name=_(u"Title"),
                             max_length=128, db_column='titre')
    url = models.URLField(max_length=400, db_column='url')
    pictogram = models.FileField(verbose_name=_(u"Pictogram"),
                                 upload_to=settings.UPLOAD_DIR,
                                 db_column='picto', max_length=512)
    type = models.CharField(db_column="type", max_length=32,
                            choices=DATA_SOURCE_TYPES)
    targets = MultiSelectField(verbose_name=_(u"Display"),
                               max_length=512,
                               choices=lazy(_get_target_choices, tuple)(), null=True, blank=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('tourism:datasource_geojson', [str(self.id)])

    def pictogram_img(self):
        return u'<img src="%s" />' % (self.pictogram.url if self.pictogram else "")
    pictogram_img.short_description = _("Pictogram")
    pictogram_img.allow_tags = True

    class Meta:
        db_table = 't_t_source_donnees'
        verbose_name = _(u"External data source")
        verbose_name_plural = _(u"External data sources")
        ordering = ['title', 'url']


class TouristicContentCategory(PictogramMixin):

    label = models.CharField(verbose_name=_(u"Label"), max_length=128, db_column='nom')

    class Meta:
        db_table = 't_b_touristic_content'
        verbose_name = _(u"Touristic Content Category")
        verbose_name_plural = _(u"Touristic Content Categories")
        ordering = ['label']

    def __unicode__(self):
        return self.label


class TouristicContent(MapEntityMixin, PublishableMixin, StructureRelated,
                       TimeStampedModelMixin, NoDeleteMixin):
    """ A generic touristic content (accomodation, museum, etc.) in the park
    """
    geom = gis_models.PointField(srid=settings.SRID)
    category = models.ForeignKey(TouristicContentCategory, related_name='contents',
                                 verbose_name=_(u"Category"), db_column='category')

    objects = NoDeleteMixin.get_manager_cls(gis_models.GeoManager)()

    class Meta:
        db_table = 't_t_touristic_content'

    def __unicode__(self):
        return self.name

    @property
    def name_display(self):
        return '<a href="%s" title="%s" >%s</a>' % (self.get_detail_url(),
                                                    self,
                                                    self)

    @property
    def name_csv_display(self):
        return unicode(self)
