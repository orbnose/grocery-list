from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from ..models import List, SortOrder, SortOrderSlot, Group, Entry, Item
from ..views import sort

from .test_items_in_list import set_up_lists, set_up_all_groups_and_sort_orders

class TestSortView(TestCase):

    def setUp(self):
        set_up_lists()
        set_up_all_groups_and_sort_orders()
    
    def test_sort_view(self):
    
        # add common weekly items
        self.client.get(reverse("grocerylist:add_common_items", args=[1]))

        response = self.client.get(reverse("grocerylist:sort", args=[1]))

        self.assertContains(response, "Grocery List for Jan. 1, 2023")
        self.assertContains(response, "Produce Front")
        self.assertContains(response, "blueberries")
        self.assertContains(response, "Dairy")
        self.assertContains(response, "yogurt")

    def test_sort(self):
        testlist = List.objects.get(pk=1)

        # add common weekly items
        self.client.get(reverse("grocerylist:add_common_items", args=[1]))

        # add other items
        self.client.post(reverse("grocerylist:edit_list", args=[1]),
                         data = {
                            'item': 'coconut milk',
                            'quantity': '12 oz',
                            'section': Group.objects.get(name='Canned Aisle').id,
                            'ignore_spelling': True
                         })
        self.client.post(reverse("grocerylist:edit_list", args=[1]),
                         data = {
                            'item': 'oats',
                            'quantity': '3 cups',
                            'section': Group.objects.get(name='Bulk').id,
                            'ignore_spelling': True
                         })
        self.client.post(reverse("grocerylist:edit_list", args=[1]),
                         data = {
                            'item': 'lentils',
                            'quantity': '12 oz',
                            'section': Group.objects.get(name='Bulk').id,
                            'ignore_spelling': True
                         })
        self.client.post(reverse("grocerylist:edit_list", args=[1]),
                         data = {
                            'item': 'feta',
                            'quantity': '12 oz',
                            'section': Group.objects.get(name='Dairy').id,
                            'ignore_spelling': True
                         })
        self.client.post(reverse("grocerylist:edit_list", args=[1]),
                         data = {
                            'item': 'bananas',
                            'quantity': '12 oz',
                            'section': Group.objects.get(name='Produce Front').id,
                            'ignore_spelling': True
                         })
        
        proper_sorted_entries = [
            {
                'group': Group.objects.get(name='Produce Front'),
                'entries': [
                    Entry.objects.get(list=testlist, item=Item.objects.get(name='blueberries')),
                    Entry.objects.get(list=testlist, item=Item.objects.get(name='apples')),
                    Entry.objects.get(list=testlist, item=Item.objects.get(name='bananas')),
                    ],
            },
            {
                'group': Group.objects.get(name='Dairy'),
                'entries': [
                    Entry.objects.get(list=testlist, item=Item.objects.get(name='yogurt')),
                    Entry.objects.get(list=testlist, item=Item.objects.get(name='oat milk')), 
                    Entry.objects.get(list=testlist, item=Item.objects.get(name='feta')),
                    ],
            },
            {
                'group': Group.objects.get(name='Bulk'),
                'entries': [
                    Entry.objects.get(list=testlist, item=Item.objects.get(name='oats')),
                    Entry.objects.get(list=testlist, item=Item.objects.get(name='lentils')),
                    ],
            },
            {
                'group': Group.objects.get(name='Canned Aisle'),
                'entries': [
                    Entry.objects.get(list=testlist, item=Item.objects.get(name='coconut milk')),
                    ],
            },
        ]

        self.assertEqual(
            sort(List.objects.get(pk=1), SortOrder.objects.get(name="default")),
            proper_sorted_entries
            )
