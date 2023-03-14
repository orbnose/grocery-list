from http import HTTPStatus
import datetime

from django.test import TestCase
from django.urls import reverse

from ..models import List

from .test_items_in_list import set_up_lists

class TestDeleteListView(TestCase):
    def setUp(self):
        set_up_lists()
    
    def test_get_delete_list_page(self):
        response = self.client.get(reverse("grocerylist:delete_list", args=[2])) # the delete page for the list for 1/02/2023
        self.assertContains(response, "Are you sure you want to delete this grocery list?")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(List.objects.get(pk=2).shopping_date.year, 2023) # the list still exists
    
    def test_delete_list_true_post(self):
        response = self.client.post(reverse("grocerylist:delete_list", args=[2]), data={"confirm_delete": True})
        
        # valid redirect
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/")

        # this list no longer exists
        with self.assertRaises(List.DoesNotExist):
            List.objects.get(pk=2)

        # the other list still exists
        List.objects.get(pk=1)
    
    def test_delete_list_string_post(self):
        response = self.client.post(reverse("grocerylist:delete_list", args=[2]), data={"confirm_delete": "random_post_value"})
        # The form should clean the string in the boolean field to True, meaning this will be a valid delete.

        # valid redirect
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], "/")

        # this list no longer exists
        with self.assertRaises(List.DoesNotExist):
            List.objects.get(pk=2)

        # the other list still exists
        List.objects.get(pk=1)
    
    def test_delete_list_false_post(self):
        response = self.client.post(reverse("grocerylist:delete_list", args=[2]), data={"confirm_delete": "false"})
        self.assertContains(response, "Are you sure you want to delete this grocery list?")
        self.assertEqual(List.objects.get(pk=2).shopping_date.year, 2023) # the list still exists