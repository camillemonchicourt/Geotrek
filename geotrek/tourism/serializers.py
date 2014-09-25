from geotrek.common.serializers import PublishableSerializerMixin, TranslatedModelSerializer
from geotrek.tourism import models as tourism_models


class TouristicContentSerializer(PublishableSerializerMixin, TranslatedModelSerializer):
    class Meta:
        model = tourism_models.TouristicContent
        fields = ('id', ) + PublishableSerializerMixin.Meta.fields
