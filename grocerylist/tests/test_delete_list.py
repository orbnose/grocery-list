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
        self.assertEqual(List.objects.get(pk=2).shopping_date.year, 2023) # the list still exists