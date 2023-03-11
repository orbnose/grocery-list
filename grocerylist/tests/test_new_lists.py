from http import HTTPStatus
import datetime

from django.test import TestCase
from django.urls import reverse

from ..models import List

class NewListViewTests(TestCase):

    def test_newlist_get(self):
        response = self.client.get(reverse('grocerylist:new_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response,'Creating a new grocery list')
    
    def test_submit_valid_date(self):
        response = self.client.post(reverse('grocerylist:new_list'), data={"shopping_date": "1/1/2023"})
        
        # valid redirect
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/")

        # object exists
        grocList = List.objects.get(pk=1)
        self.assertEqual(grocList.shopping_date, datetime.date(2023, 1, 1))

    def test_submit_invalid_date(self):
        response = self.client.post(reverse('grocerylist:new_list'), data={"shopping_date": "30/1/2023"})
        
        # reload with form error message
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Enter a valid date.")

        # object does not exist
        with self.assertRaises(List.DoesNotExist):
            List.objects.get(pk=1)
