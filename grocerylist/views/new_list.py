from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from ..forms import NewListForm

def new_list(request):

    if request.method == 'POST':
        form = NewListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('grocerylist:index'))
    else:
        form = NewListForm()
    return render(request, 'grocerylist/new_list.html', {'form': form})