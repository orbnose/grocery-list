from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

from ..models import List, Group
from ..forms import EntryForm

from .edit_list import process_entry_form

def add_common_items(request, grocList_pk):
    grocList = get_object_or_404(List, pk=grocList_pk)
    
    data_to_submit = [
        # blueberries
        {
            'item': 'blueberries',
            'quantity': '',
            'section': Group.objects.get(name='Produce Front'),
            'ignore_spelling': True
        },
        # apples
        {
            'item': 'apples',
            'quantity': '',
            'section': Group.objects.get(name='Produce Front'),
            'ignore_spelling': True
        },
        # yogurt
        {
            'item': 'yogurt',
            'quantity': '',
            'section': Group.objects.get(name='Dairy'),
            'ignore_spelling': True
        },
        # oat milk
        {
            'item': 'oat milk',
            'quantity': '',
            'section': Group.objects.get(name='Dairy'),
            'ignore_spelling': True
        },
    ]

    for data in data_to_submit:
        new_entry_form = EntryForm(data)
        success, _ = process_entry_form(new_entry_form, grocList)

    return HttpResponseRedirect(reverse('grocerylist:edit_list', args=[grocList_pk]))