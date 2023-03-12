from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from ..models import List, SortOrder, SortOrderSlot, Group
from ..views import NO_DEFAULT_SORT_ORDER_MESSAGE, NO_SORT_ORDER_SLOTS_MESSAGE, NO_GROUPS_MESSAGE

def set_up_expected_defaults():
    produce_front_group = Group.objects.create(name="Produce Front")
    produce_front_group.save()
    dairy_group = Group.objects.create(name="Dairy")
    dairy_group.save()

    default_sort_order = SortOrder.objects.create(name="default")
    default_sort_order.save()

    slot1 = SortOrderSlot.objects.create(sort_order=default_sort_order, group=produce_front_group, order_num=1)
    slot1.save()
    slot2 = SortOrderSlot.objects.create(sort_order=default_sort_order, group=dairy_group, order_num=2)
    slot2.save()


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
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertContains(response, NO_SORT_ORDER_SLOTS_MESSAGE)

    def test_with_at_least_one_sort_order_slot(self):
        set_up_expected_defaults()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, NO_SORT_ORDER_SLOTS_MESSAGE)
    
    def test_no_groups(self):
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertContains(response, NO_GROUPS_MESSAGE)

    def test_with_at_least_one_group(self):
        set_up_expected_defaults()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, NO_GROUPS_MESSAGE)