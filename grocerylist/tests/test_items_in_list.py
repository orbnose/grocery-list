from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from ..models import List, SortOrder

NO_DEFAULT_SORT_ORDER_MESSAGE = "There is no default sort order defined. Please contact the system administrator."

def set_up_expected_defaults():
    SortOrder.objects.create(name="default")

class TestEditListView(TestCase):
    
    def setUp(self):
        # List pk=1
        List.objects.create(shopping_date="2023-01-01")

        # List pk=2
        List.objects.create(shopping_date="2023-01-02")
    
    def test_no_default_sort_order(self):
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertContains(response, NO_DEFAULT_SORT_ORDER_MESSAGE)
    
    def test_with_default_sort_order(self):
        set_up_expected_defaults()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, NO_DEFAULT_SORT_ORDER_MESSAGE)
    
    def test_no_sort_order_slots(self):
        assert "To be done" == "Done"

    def test_with_at_least_one_sort_order_slot(self):
        assert "To be done" == "Done"