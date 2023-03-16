from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

from ..models import List
from ..forms import DeleteForm

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