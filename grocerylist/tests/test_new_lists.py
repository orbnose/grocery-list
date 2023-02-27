from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

class NewListViewTests(TestCase):

    def test_newlist_get(self):
        response = self.client.get(reverse('grocerylist:new_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response,'Creating a new grocery list')
    
    def test_submit_valid_date(self):
        response = self.client.post(reverse('grocerylist:new_list'), data={"shopping_date": "1/1/2023"})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/")
