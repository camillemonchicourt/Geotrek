# -*- coding: utf-8 -*-
import factory

from geotrek.common.utils.testdata import get_dummy_uploaded_image

from . import models


class DataSourceFactory(factory.Factory):
    FACTORY_FOR = models.DataSource

    title = factory.Sequence(lambda n: u"DataSource %s" % n)
    url = factory.Sequence(lambda n: u"http://%s.com" % n)
    type = models.DATA_SOURCE_TYPES.GEOJSON
    pictogram = get_dummy_uploaded_image()


class TouristicContentCategoryFactory(factory.Factory):
    FACTORY_FOR = models.TouristicContentCategory

    label = factory.Sequence(lambda n: u"TouristicContentCategory %s" % n)


class TouristicContentFactory(factory.Factory):
    FACTORY_FOR = models.TouristicContent

    name = factory.Sequence(lambda n: u"TouristicContent %s" % n)
    category = factory.SubFactory(TouristicContentCategoryFactory)
    geom = 'POINT(0 0)'
