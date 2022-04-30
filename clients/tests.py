from rest_framework.test import APITestCase
from rest_framework import status

from .models import Client


class AcountTestCase(APITestCase):
    def test_clients(self):
        data = {
            "name" : "test_name_01",
            "manager" : "test_manage_01",
            "contact"  : "test_contact_01",
            "address_code" : "test_code_01",
            "address_detail" : "test_detail_01"
        }
        create_response = self.client.post('/clients', data=data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        # test_clients_get_list
        response = self.client.get('/clients')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test_clients_get_detail
        response = self.client.get(f"/clients/{create_response.data['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/clients/100')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # test_clients_patch
        update_data = {
            "name" : "test_patch_name"
        }
        response = self.client.patch(f"/clients/{create_response.data['id']}", update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test_clients_put
        put_data = {
            "name" : "test_name_02",
            "manager" : "test_manage_02",
            "contact"  : "test_contact_02",
            "address_code" : "test_code_02",
            "address_detail" : "test_detail_02"
        }
        response = self.client.put(f"/clients/{create_response.data['id']}", put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        put_error_data = {
            "name" : "test_name_02",
        }
        response = self.client.put(f"/clients/{create_response.data['id']}", put_error_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test_clients_delete
        response = self.client.delete(f"/clients/{create_response.data['id']}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0)