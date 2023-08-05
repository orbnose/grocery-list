from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from ..forms import RecipeEntryForm

def new_recipe(request):
    valid_flag = None
    if request.method == 'POST':
        form = RecipeEntryForm(request.POST)
        if form.is_valid():
            valid_flag = True
        else:
            valid_flag = False
    else:
        form = RecipeEntryForm()
    return render(request, 'grocerylist/new_recipe.html', {'form': form, 'valid_flag': valid_flag})