from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Building, Bricklaying
from .serializers import BuildingSerializer, BricklayingSerializer

# Create your tests here.


class SetUpTestData(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.new_building_full_param = {
            "address": "москва проспект вернадского дом 64 а",
            "construction_date": "1968-10-25"
        }

        cls.new_building_only_address = {
            "address": "москва проспект вернадского дом 32"
        }

        cls.new_building_only_date = {
            "construction_date": "1968-10-25"
        }

        cls.new_bricklaying_full_param = {
            "count": 100,
            "date": "2020-02-25 14:30:59"
        }

        cls.new_bricklaying_only_count = {
            "count": 100,
        }

        cls.new_bricklaying_only_date = {
            "date": "2020-02-25 14:30:59"
        }

        cls.stats_page = [
            {
                "address": "москва проспект вернадского дом 32",
                "construction_date": "2020-02-26",
                "total_bricks_count": 3000,
                "detail": [
                    {
                        "day": "2020-02-25T00:00:00Z",
                        "day_count": 1000
                    },
                    {
                        "day": "2020-02-26T00:00:00Z",
                        "day_count": 1000
                    },
                    {
                        "day": "2020-02-27T00:00:00Z",
                        "day_count": 1000
                    }
                ]
            },{
                "address": "москва проспект вернадского дом 64 а",
                "construction_date": "1968-10-25",
                "total_bricks_count": 300,
                "detail": [
                    {
                        "day": "2020-02-25T00:00:00Z",
                        "day_count": 100
                    },
                    {
                        "day": "2020-02-26T00:00:00Z",
                        "day_count": 100
                    },
                    {
                        "day": "2020-02-27T00:00:00Z",
                        "day_count": 100
                    }
                ]
            }

        ]


class BuildingViewTestCase(SetUpTestData):

    def test_not_allowed_method(self):
        response = self.client.get(reverse('building-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(reverse('building-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(reverse('building-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(reverse('building-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_add_full_info(self):
        response = self.client.post(reverse('building-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        db = Building.objects.get(id=1)
        serialized_db = BuildingSerializer(db)
        self.assertEqual(serialized_db.data, response.data)

    def test_only_address(self):
        response = self.client.post(reverse('building-list'), self.new_building_only_address)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        db = Building.objects.get(id=1)
        serialized_db = BuildingSerializer(db)
        self.assertEqual(serialized_db.data, response.data)

    def test_only_date(self):
        response = self.client.post(reverse('building-list'), self.new_building_only_date)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bricklaying_full_info(self):
        response = self.client.post(reverse('building-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('building-add-bricks', args=[1]), self.new_bricklaying_full_param)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        db = Bricklaying.objects.get(building_id=1)
        serialized_db = BricklayingSerializer(db)
        self.assertEqual(serialized_db.data, response.data)

    def test_bricklaying_only_count(self):
        response = self.client.post(reverse('building-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('building-add-bricks', args=[1]), self.new_bricklaying_only_count)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        db = Bricklaying.objects.get(building_id=1)
        serialized_db = BricklayingSerializer(db)
        self.assertEqual(serialized_db.data, response.data)

    def test_bricklaying_only_date(self):
        response = self.client.post(reverse('building-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('building-add-bricks', args=[1]), self.new_bricklaying_only_date)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StatsTestCase(SetUpTestData):

    def setUp(self) -> None:
        new_building = Building.objects.create(address="москва проспект вернадского дом 64 а",
                                               construction_date="1968-10-25")
        new_building.save()
        bricks_add_date = ["2020-02-25", "2020-02-26", "2020-02-27"]
        for i in bricks_add_date:
            new_building_brick = Bricklaying.objects.create(count=100, date=i, building_id=1)
            new_building_brick.save()

        new_building = Building.objects.create(address="москва проспект вернадского дом 32",
                                               construction_date="2020-02-26")
        new_building.save()

        for i in bricks_add_date:
            new_building_brick = Bricklaying.objects.create(count=1000, date=i, building_id=2)
            new_building_brick.save()

    def test_not_allowed_method(self):
        response = self.client.post(reverse('stats-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(reverse('stats-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(reverse('stats-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(reverse('stats-list'), self.new_building_full_param)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_output(self):
        response = self.client.get(reverse('stats-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], self.stats_page)
