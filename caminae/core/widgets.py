"""

    We distinguish two types of widgets : Geometry and Topology.
    
    Geometry widgets receive a WKT string, deserialized by GEOS.
    Leaflet.Draw is used for edition.
    
    Topology widgets receive a JSON string, deserialized by Topology.deserialize().
    Caminae custom code is used for edition.

    :notes:

        The purpose of floppyforms is to use Django templates for widget rendering.

"""
from django.conf import settings

import floppyforms as forms

from caminae.common.utils import wkt_to_geom
from .models import TopologyMixin


class LeafletMapWidget(forms.gis.BaseGeometryWidget):
    template_name = 'core/fieldgeometry_fragment.html'
    display_wkt = settings.DEBUG

    def get_context(self, name, value, attrs=None, extra_context={}):
        context = super(LeafletMapWidget, self).get_context(name, value, attrs, extra_context)
        context['update'] = bool(value)
        context['field'] = value
        return context


class GeometryWidget(LeafletMapWidget):
    path_snapping = True

    def value_from_datadict(self, data, files, name):
        wkt = super(GeometryWidget, self).value_from_datadict(data, files, name)
        return None if not wkt else wkt_to_geom(wkt)

    def get_context(self, name, value, attrs=None, extra_context={}):
        context = super(GeometryWidget, self).get_context(name, value, attrs, extra_context)
        # Be careful, on form error, value is not a GEOSGeometry
        if value and not isinstance(value, basestring):
            value.transform(settings.API_SRID)
        context['path_snapping'] = self.path_snapping
        # TODO: this should come from context processor !
        context['MIN_SNAP_ZOOM'] = settings.MIN_SNAP_ZOOM
        context['SNAP_DISTANCE'] = settings.SNAP_DISTANCE
        return context


class PointWidget(GeometryWidget,
                  forms.gis.PointWidget):
    pass


class LineStringWidget(GeometryWidget,
                       forms.gis.LineStringWidget):
    pass


class BaseTopologyWidget(forms.Textarea):
    """ A widget allowing to create topologies on a map.
    """
    template_name = 'core/fieldtopology_fragment.html'
    display_json = settings.DEBUG
    is_multipath = False
    is_point = False

    def value_from_datadict(self, data, files, name):
        return data.get(name)

    def get_context(self, name, value, *args, **kwargs):
        topologyjson = ''
        if value:
            if isinstance(value, basestring):
                topologyjson = value
            else:
                if isinstance(value, int):
                    value = TopologyMixin.objects.get(pk=value)
                topologyjson = value.serialize()
        context = super(BaseTopologyWidget, self).get_context(name, topologyjson, *args, **kwargs)
        context['module'] = 'map_%s' % name.replace('-', '_')
        context['display_json'] = self.display_json
        context['is_multipath'] = self.is_multipath
        context['is_point'] = self.is_point
        context['update'] = bool(value)
        context['topology'] = value
        context['topologyjson'] = topologyjson
        context['path_snapping'] = True
        # TODO: this should come from context processor !
        context['MIN_SNAP_ZOOM'] = settings.MIN_SNAP_ZOOM
        context['SNAP_DISTANCE'] = settings.SNAP_DISTANCE
        return context


class LineTopologyWidget(BaseTopologyWidget):
    """ A widget allowing to select a list of paths. 
    """
    is_multipath = True

class PointTopologyWidget(BaseTopologyWidget):
    """ A widget allowing to point a position with a marker. 
    """
    is_point = True


class PointLineTopologyWidget(PointTopologyWidget, LineTopologyWidget):
    """ A widget allowing to point a position with a marker or a list of paths.
    """
    pass


class TopologyReadonlyWidget(BaseTopologyWidget):
    template_name = 'core/fieldtopologyreadonly_fragment.html'
    
    def get_context(self, *args, **kwargs):
        context = super(TopologyReadonlyWidget, self).get_context(*args, **kwargs)
        topology =  context['topology']
        if topology:
            context['object'] = topology.geom
        context['mapname'] = context['module']
        return context