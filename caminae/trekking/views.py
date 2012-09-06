from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic.edit import CreateView

from caminae.authent.decorators import trekking_manager_required
from caminae.mapentity.views import (MapEntityLayer, MapEntityList, MapEntityJsonList, 
                                MapEntityDetail, MapEntityCreate, MapEntityUpdate, MapEntityDelete)
from .models import Trek, POI, WebLink
from .filters import TrekFilter, POIFilter
from .forms import TrekForm, POIForm, WebLinkCreateFormPopup


class TrekLayer(MapEntityLayer):
    model = Trek


class TrekList(MapEntityList):
    model = Trek
    filterform = TrekFilter
    columns = ['id', 'name', 'departure', 'arrival']


class TrekJsonList(MapEntityJsonList, TrekList):
    pass


class TrekDetail(MapEntityDetail):
    model = Trek

    def can_edit(self):
        return self.request.user.profile.is_trekking_manager()


class TrekCreate(MapEntityCreate):
    model = Trek
    form_class = TrekForm

    @method_decorator(trekking_manager_required('trekking:trek_list'))
    def dispatch(self, *args, **kwargs):
        return super(TrekCreate, self).dispatch(*args, **kwargs)


class TrekUpdate(MapEntityUpdate):
    model = Trek
    form_class = TrekForm

    @method_decorator(trekking_manager_required('trekking:trek_detail'))
    def dispatch(self, *args, **kwargs):
        return super(TrekUpdate, self).dispatch(*args, **kwargs)


class TrekDelete(MapEntityDelete):
    model = Trek

    @method_decorator(trekking_manager_required('trekking:trek_detail'))
    def dispatch(self, *args, **kwargs):
        return super(TrekDelete, self).dispatch(*args, **kwargs)


class POILayer(MapEntityLayer):
    model = POI


class POIList(MapEntityList):
    model = POI
    filterform = POIFilter
    columns = ['id', 'name', 'type']


class POIJsonList(MapEntityJsonList, POIList):
    pass


class POIDetail(MapEntityDetail):
    model = POI

    def can_edit(self):
        return self.request.user.profile.is_trekking_manager()


class POICreate(MapEntityCreate):
    model = POI
    form_class = POIForm

    @method_decorator(trekking_manager_required('trekking:poi_list'))
    def dispatch(self, *args, **kwargs):
        return super(POICreate, self).dispatch(*args, **kwargs)


class POIUpdate(MapEntityUpdate):
    model = POI
    form_class = POIForm

    @method_decorator(trekking_manager_required('trekking:poi_detail'))
    def dispatch(self, *args, **kwargs):
        return super(POIUpdate, self).dispatch(*args, **kwargs)


class POIDelete(MapEntityDelete):
    model = POI

    @method_decorator(trekking_manager_required('trekking:poi_detail'))
    def dispatch(self, *args, **kwargs):
        return super(POIDelete, self).dispatch(*args, **kwargs)



class WebLinkCreatePopup(CreateView):
    model = WebLink
    form_class = WebLinkCreateFormPopup

    def form_valid(self, form):
        self.object = form.save()
        print form.instance
        return HttpResponse("""
            <script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>
        """ % (escape(form.instance._get_pk_val()), escape(form.instance)))