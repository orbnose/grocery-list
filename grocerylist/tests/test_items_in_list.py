from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from ..models import List, SortOrder, SortOrderSlot, Group, Entry, Item
from ..views.edit_list import     (NO_DEFAULT_SORT_ORDER_MESSAGE, 
                         NO_SORT_ORDER_SLOTS_MESSAGE, 
                         NO_GROUPS_MESSAGE, 
                         COMMON_ITEMS_GROUPS_MISSING_MESSAGE)

from ..views.edit_list import     (ITEM_NOT_IN_DB_FORM_ERROR,
                         NOT_VALID_SPELLING_FORM_ERROR,
                         ALREADY_ON_LIST_FORM_ERROR)

def set_up_lists():
    # List pk=1
    List.objects.create(shopping_date="2023-01-01")

    # List pk=2
    List.objects.create(shopping_date="2023-01-02")

def set_up_all_groups_and_sort_orders():
    produce_front_group = Group.objects.create(name="Produce Front")
    produce_front_group.save()
    dairy_group = Group.objects.create(name="Dairy")
    dairy_group.save()
    bulk_group = Group.objects.create(name="Bulk")
    bulk_group.save()
    canned_group = Group.objects.create(name="Canned Aisle")
    canned_group.save()

    default_sort_order = SortOrder.objects.create(name="default")
    default_sort_order.save()

    slot1 = SortOrderSlot.objects.create(sort_order=default_sort_order, group=produce_front_group, order_num=1)
    slot1.save()
    slot2 = SortOrderSlot.objects.create(sort_order=default_sort_order, group=dairy_group, order_num=2)
    slot2.save()
    slot3 = SortOrderSlot.objects.create(sort_order=default_sort_order, group=bulk_group, order_num=3)
    slot3.save()
    slot4 = SortOrderSlot.objects.create(sort_order=default_sort_order, group=canned_group, order_num=4)
    slot4.save()

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
        set_up_all_groups_and_sort_orders()

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
    
    def test_add_item_not_in_db(self):
        testlist = List.objects.get(pk=1)
        bulk_group_id = Group.objects.get(name="Bulk").id

        # Submit new item without section - Raises no section error
        response = self.client.post(reverse("grocerylist:edit_list", args=[1]), 
                                    data={
                                        'item': 'rolled oats',
                                        'quantity': '',
                                        'section': '',
                                        'ignore_spelling': '',
                                    })
        self.assertContains(response, ITEM_NOT_IN_DB_FORM_ERROR)
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(name="rolled oats")
        self.assertEqual(Entry.objects.filter(list=testlist).count(), 0)

        # Submit new item without spelling choice - Raises not valid spelling error
        response = self.client.post(reverse("grocerylist:edit_list", args=[1]), 
                                    data={
                                        'item': 'rolled oats',
                                        'quantity': '',
                                        'section': bulk_group_id,
                                        'ignore_spelling': '',
                                    })
        self.assertContains(response, NOT_VALID_SPELLING_FORM_ERROR)
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(name="rolled oats")
        self.assertEqual(Entry.objects.filter(list=testlist).count(), 0)

        # Submit new item with section and spelling - Creates item and entry objects
        response = self.client.post(reverse("grocerylist:edit_list", args=[1]), 
                                    data={
                                        'item': 'rolled oats',
                                        'quantity': '',
                                        'section': bulk_group_id,
                                        'ignore_spelling': True,
                                    })
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        oats_item = Item.objects.get(name="rolled oats")
        Entry.objects.get(list=testlist, item=oats_item)

        # Submit the same item - Raises already on list error
        response = self.client.post(reverse("grocerylist:edit_list", args=[1]), 
                                    data={
                                        'item': 'rolled oats',
                                        'quantity': '',
                                        'section': '',
                                        'ignore_spelling': '',
                                    })
        self.assertContains(response, ALREADY_ON_LIST_FORM_ERROR)
        self.assertEqual(Entry.objects.filter(list=testlist).count(), 1)

    def test_delete_entry(self):
        #add new item
        response = self.client.post(reverse("grocerylist:edit_list", args=[1]), 
                                    data={
                                        'item': 'rolled oats',
                                        'quantity': '',
                                        'section': Group.objects.get(name="Bulk").id,
                                        'ignore_spelling': True,
                                    })
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # delete the item
        new_entry_id = 1
        response = self.client.get(reverse("grocerylist:delete_entry", args=[new_entry_id]))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        with self.assertRaises(Entry.DoesNotExist):
            Entry.objects.get(pk=new_entry_id)
        
        # get 404 when trying to delete again
        response = self.client.get(reverse("grocerylist:delete_entry", args=[new_entry_id]))
        self.assertEqual(response.status_code, 404)

class TestEditListViewWithMissingModels(TestCase):
    
    def setUp(self):
        set_up_lists()
    
    def test_no_default_sort_order(self):
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertContains(response, NO_DEFAULT_SORT_ORDER_MESSAGE)
    
    def test_with_default_sort_order(self):
        set_up_all_groups_and_sort_orders()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, NO_DEFAULT_SORT_ORDER_MESSAGE)
    
    def test_no_sort_order_slots(self):
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertContains(response, NO_SORT_ORDER_SLOTS_MESSAGE)

    def test_with_at_least_one_sort_order_slot(self):
        set_up_all_groups_and_sort_orders()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, NO_SORT_ORDER_SLOTS_MESSAGE)
    
    def test_no_groups(self):
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertContains(response, NO_GROUPS_MESSAGE)

    def test_with_at_least_one_group(self):
        set_up_all_groups_and_sort_orders()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, NO_GROUPS_MESSAGE)
    
    def test_add_common_items_without_all_groups_set_up(self):
        set_up_one_group_and_sort_order()
        response = self.client.get(reverse("grocerylist:edit_list", args=[1]))
        self.assertNotContains(response, "Add Common Weekly Items") # This button should not be available if the groups are not yet set up.
        self.assertContains(response, COMMON_ITEMS_GROUPS_MISSING_MESSAGE)