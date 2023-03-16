from django.shortcuts import render, get_object_or_404

from ..models import List, SortOrder

from .edit_list import get_default_sort_order

def sorted_view(request, grocList_pk):
    grocList = get_object_or_404(List, pk=grocList_pk)
    sort_order = get_default_sort_order()
    
    sorted_entries = sort(grocList, sort_order)
    
    context = {
        'list': grocList,
        'sorted_entries': sorted_entries,
    }
    return render(request, 'grocerylist/sort.html', context)

def sort(grocList: List, sort_order: SortOrder):
    sorted_entries = []
    sort_order_slot_list = sort_order.sortorderslot_set.all().order_by('order_num')
    group_list = [slot.group for slot in sort_order_slot_list]

    for group in group_list:
        entries = grocList.entry_set.filter(item__group=group)
        sorted_entries.append({
            'group': group,
            'entries': list(entries),
        })
    
    return sorted_entries