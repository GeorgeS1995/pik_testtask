from datetime import date
from django.utils import timezone
from django.db import models


# Create your models here.


class Building(models.Model):
    address = models.CharField(max_length=255)
    construction_date = models.DateField(default=date.today)


class Bricklaying(models.Model):
    count = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    building = models.ForeignKey(Building, on_delete=models.DO_NOTHING)
