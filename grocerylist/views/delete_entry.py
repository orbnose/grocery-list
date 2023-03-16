from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

from ..models import Entry

def delete_entry(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk)
    entry.delete()
    return HttpResponseRedirect(reverse('grocerylist:edit_list', args=[entry.list.pk]))