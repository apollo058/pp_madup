from rest_framework.test import APITestCase
from rest_framework import status

from .models import Amount
from clients.models import Client

class AcountTestCase(APITestCase):
    def setUp(self):
        self.client_data = Client.objects.create(
            name = "test_name_01",
            manager = "test_manage_01",
            contact = "test_contact_01",
            address_code = "test_code_01",
            address_detail = "test_detail_01"
        )
        Amount.objects.create(
            advertiser = self.client_data,
            uid	= "test-uid-001",
            media = "naver",
            date = "2021-12-01",
            cost = 	1105,
            impression = 10001,
            click = 103,
            conversion = 2,	
            cv = 10007,
        )

        Amount.objects.create(
            advertiser = self.client_data,
            uid	= "test-uid-002",
            media = "naver",
            date = "2021-12-02",
            cost = 	1103,
            impression = 10002,
            click = 107,
            conversion = 3,	
            cv = 10001,
        )

        Amount.objects.create(
            advertiser = self.client_data,
            uid	= "test-uid-003",
            media = "facebook",
            date = "2021-12-03",
            cost = 	1102,
            impression = 10012,
            click = 207,
            conversion = 4,	
            cv = 10023,
        )

    def test_amounts_get(self):
        response = self.client.get(f"/amounts/client?id={self.client_data.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {
                'naver': {'ctr': 1.04, 'cpc': 10.51, 'roas': 906.15, 'cvr': 2.38, 'cpa': 441.6}, 
                'facebook': {'ctr': 2.06, 'cpc': 5.32, 'roas': 909.52, 'cvr': 1.93, 'cpa': 275.5}
                })

        response = self.client.get(f"/amounts/client?id={self.client_data.id}&start-date=2021-12-01&end-date=2021-12-02")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {
                'naver': {'ctr': 1.04, 'cpc': 10.51, 'roas': 906.15, 'cvr': 2.38, 'cpa': 441.6}
                })

        response = self.client.get(f"/amounts/client?id={self.client_data.id}&start-date=2021-12-03")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'facebook': {'ctr': 2.06, 'cpc': 5.32, 'roas': 909.52, 'cvr': 1.93, 'cpa': 275.5}
            })

        response = self.client.get(f"/amounts/client?id={self.client_data.id}&end-date=2021-12-03")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get("/amounts/client")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
