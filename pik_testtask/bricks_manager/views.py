from django.db.models import Sum
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from .serializers import BuildingSerializer, BricklayingSerializer, StatsSerializer
from .models import Bricklaying, Building
from django.db.utils import DatabaseError


# Create your views here.


class BuildingView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = BuildingSerializer

    @action(detail=True, methods=['post'], url_path="add-bricks")
    def add_bricks(self, request, pk=None):
        serializer = BricklayingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                kwargs = serializer.data
                kwargs['building_id'] = pk
                new_bricklaying = Bricklaying.objects.create(**kwargs)
                new_bricklaying.save()
                serialized_db = BricklayingSerializer(new_bricklaying)
            except DatabaseError as err:
                return Response({'status': f'Can\'t insert to db: {err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serialized_db.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Stats(mixins.ListModelMixin, GenericViewSet):
    serializer_class = StatsSerializer
    queryset = Building.objects.values('address', 'construction_date', 'id'). \
                                annotate(total_bricks_count=Sum('bricklaying__count')). \
                                order_by('-construction_date')

