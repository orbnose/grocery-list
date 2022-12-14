from concurrent.futures import process
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.forms import HiddenInput, ValidationError

from nltk.corpus import words

from .models import List, Entry, Item, Group, SortOrder
from .forms import NewListForm, DeleteForm, EntryForm

# Create your views here.

def index(request):
    lists = List.objects.all()
    return render(request, 'grocerylist/index.html', {'lists': lists})

def new_list(request):

    if request.method == 'POST':
        form = NewListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('grocerylist:index'))

    else:
        form = NewListForm()
    

    return render(request, 'grocerylist/new_list.html', {'form': form})

def delete_list(request, grocList_pk):
    grocList = get_object_or_404(List, pk=grocList_pk)

    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['confirm_delete'] == True:
                grocList.delete()
                return HttpResponseRedirect(reverse('grocerylist:index'))
    else:
        form = DeleteForm()
    
    context = {
            'list': grocList,
            'form': form
        }

    return render(request, 'grocerylist/delete_list.html', context)

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

def process_entry_form(entry_form, grocList):
    # Return a tuple of (success (Bool) , entry_form (EntryForm obj) )
    # If success is false, the EntryForm object will have the appropriate errors.

    # Correct form type?
    if not type(entry_form) == EntryForm:
        return False, entry_form

    # Valid submission?
    if not entry_form.is_valid():
        return False, entry_form

    #lowercase the item name
    entry_form.cleaned_data['item'] = entry_form.cleaned_data['item'].lower()

    # Check if the item already exists. If not, create one.
    submitted_item = entry_form.cleaned_data['item']
    try:
        item = Item.objects.get(name = submitted_item)     
        
        # Check if item is already on the list
        entries = grocList.entry_set.all()
        if entries.filter(item=item):
                entry_form.add_error('item', "This item is already on this list!")
                return False, entry_form

    except Item.DoesNotExist:
        # Grab the chosen group for a new item, or give an error if blank
        group = entry_form.cleaned_data['section']
        if not group:
            entry_form.add_error('item', "This item is not yet saved in the database. Please choose a section to go with it.")
            return False, entry_form

        # Spellcheck - Check to see if this spells a word according to nltk
        ignore_spelling = entry_form.cleaned_data['ignore_spelling']
        wordlist = words.words()
        if not submitted_item in wordlist and ignore_spelling is not True:
            entry_form.add_error('item', "This spelling is not recognized as a valid word. Would you like to ignore spelling?")
            return False, entry_form
        
        # Save new item into the db
        item = Item(
            group = group,
            name = submitted_item,
        )
        item.save()
    
    # grab the quantity
    quantity = entry_form.cleaned_data['quantity']

    # Create new entry
    new_entry = Entry(
        list = grocList,
        item = item,
        quantity = quantity
    )
    new_entry.save()

    # Successful new entry!
    return True, entry_form

def edit_list(request, grocList_pk):
    grocList = get_object_or_404(List, pk=grocList_pk)
    entries = grocList.entry_set.all()

    if request.method == 'POST':
        entry_form = EntryForm(request.POST)
        success, entry_form = process_entry_form(entry_form, grocList)
        if success:
            return HttpResponseRedirect(reverse('grocerylist:edit_list', args=[grocList_pk]))
    else:
        entry_form = EntryForm()
        #entry_form.fields['section'].widget = HiddenInput
    
    context = {
        'list': grocList,
        'entries': entries,
        'entry_form': entry_form.render("grocerylist/new_entry_form.html"),
    }
    return render(request, 'grocerylist/edit_list.html', context)

def sort(request, grocList_pk):
    grocList = get_object_or_404(List, pk=grocList_pk)
    sort_order = SortOrder.objects.get(name='default')
    sort_order_list = sort_order.sortorderslot_set.all().order_by('order_num')
    sorted_entries = []

    group_list = [slot.group for slot in sort_order_list]
    for group in group_list:
        entries = grocList.entry_set.filter(item__group=group)
        sorted_entries.append({
            'group': group,
            'entries': entries
        })
    
    context = {
        'list': grocList,
        'sorted_entries': sorted_entries,
    }
    return render(request, 'grocerylist/sort.html', context)

def delete_entry(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk)
    entry.delete()
    return HttpResponseRedirect(reverse('grocerylist:edit_list', args=[entry.list.pk]))
