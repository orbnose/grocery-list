from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from ..models import List, SortOrder, SortOrderSlot, Group, Entry, Item
from ..views import     (NO_DEFAULT_SORT_ORDER_MESSAGE, 
                         NO_SORT_ORDER_SLOTS_MESSAGE, 
                         NO_GROUPS_MESSAGE, 
                         COMMON_ITEMS_GROUPS_MISSING_MESSAGE)

def set_up_lists():
    # List pk=1
    List.objects.create(shopping_date="2023-01-01")

    # List pk=2
    List.objects.create(shopping_date="2023-01-02")

def set_up_two_groups_and_sort_orders():
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
    

def set_up_one_group_and_sort_order():
    dairy_group = Group.objects.create(name="Dairy")
    dairy_group.save()

    default_sort_order = SortOrder.objects.create(name="default")
    default_sort_order.save()

    slot1 = SortOrderSlot.objects.create(sort_order=default_sort_order, group=dairy_group, order_num=1)
    slot1.save()

class TestEditListView(TestCase):
    
    def setUp(self):
        set_up_lists()
        set_up_two_groups_and_sort_orders()

    def test_add_common_items_with_proper_setup(self):
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertContains(response, "Add Common Weekly Items")

        # get link for adding common items
        response = self.client.get(reverse("grocerylist:add_common_items", args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND) # response redirects

        # The four common items and entries exist
        testlist = List.objects.get(pk=1)

        blueberries = Item.objects.get(name="blueberries")
        apples = Item.objects.get(name="apples")
        yogurt = Item.objects.get(name="yogurt")
        oat_milk = Item.objects.get(name="oat milk")
        Entry.objects.get(list=testlist, item=blueberries)
        Entry.objects.get(list=testlist, item=apples)
        Entry.objects.get(list=testlist, item=yogurt)
        Entry.objects.get(list=testlist, item=oat_milk)

        #try adding common items 3 more times
        response = self.client.get(reverse("grocerylist:add_common_items", args=[1]))
        response = self.client.get(reverse("grocerylist:add_common_items", args=[1]))
        response = self.client.get(reverse("grocerylist:add_common_items", args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        #there are still only 4 total entries
        self.assertEqual(Entry.objects.all().count(), 4)

class TestEditListViewWithMissingModels(TestCase):
    
    def setUp(self):
        set_up_lists()
    
    def test_no_default_sort_order(self):
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertContains(response, NO_DEFAULT_SORT_ORDER_MESSAGE)
    
    def test_with_default_sort_order(self):
        set_up_two_groups_and_sort_orders()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, NO_DEFAULT_SORT_ORDER_MESSAGE)
    
    def test_no_sort_order_slots(self):
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertContains(response, NO_SORT_ORDER_SLOTS_MESSAGE)

    def test_with_at_least_one_sort_order_slot(self):
        set_up_two_groups_and_sort_orders()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, NO_SORT_ORDER_SLOTS_MESSAGE)
    
    def test_no_groups(self):
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertContains(response, NO_GROUPS_MESSAGE)

    def test_with_at_least_one_group(self):
        set_up_two_groups_and_sort_orders()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, NO_GROUPS_MESSAGE)
    
    def test_add_common_items_without_all_groups_set_up(self):
        set_up_one_group_and_sort_order()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, "Add Common Weekly Items") # This button should not be available if the groups are not yet set up.
        self.assertContains(response, COMMON_ITEMS_GROUPS_MISSING_MESSAGE)