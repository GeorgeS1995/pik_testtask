from django.db.models import Sum
from django.db.models.functions import TruncDay
from rest_framework import serializers as s
from .models import Building, Bricklaying


class BuildingSerializer(s.HyperlinkedModelSerializer):
    class Meta:
        model = Building
        fields = ['address', 'construction_date']


class BricklayingSerializer(s.HyperlinkedModelSerializer):
    class Meta:
        model = Bricklaying
        fields = ['count', 'date']


class BricklayingSerializerGouprByDay(s.HyperlinkedModelSerializer):
    day = s.DateTimeField()
    day_count = s.IntegerField()

    class Meta:
        model = Bricklaying
        fields = ['day', 'day_count']


class StatsSerializer(BuildingSerializer):
    detail = s.SerializerMethodField()
    total_bricks_count = s.IntegerField()

    class Meta:
        model = BuildingSerializer.Meta.model
        fields = BuildingSerializer.Meta.fields + ['total_bricks_count', 'detail']

    def get_detail(self, obj):
        obj = Bricklaying.objects \
            .filter(building=obj['id']) \
            .annotate(day=TruncDay('date')) \
            .values('day') \
            .annotate(day_count=Sum('count'))
        return BricklayingSerializerGouprByDay(obj, many=True).data
