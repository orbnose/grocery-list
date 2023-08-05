from email.policy import default
from typing import Any, Optional
from django import forms
from django.forms import Form, ModelForm
from django.core.validators import RegexValidator

from .models import List, Entry, Group
from .recipe_entry.ingredients import regex_combined_ingredient_pattern_without_capture

class DateInput(forms.DateInput):
    input_type = 'date'

class NewListForm(ModelForm):
    class Meta:
        model = List
        fields = ['shopping_date']
        widgets = {
            'shopping_date': DateInput
        }

class DeleteForm(Form):
    confirm_delete = forms.BooleanField(initial=True, widget=forms.HiddenInput)

class EntryForm(Form):
    item = forms.CharField(max_length=50)
    quantity = forms.CharField(max_length=50, required=False)
    section = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    ignore_spelling = forms.BooleanField(initial=False, required=False)


validate_ingredient = RegexValidator(regex=regex_combined_ingredient_pattern_without_capture)

class IngredientsField(forms.Field):
    widget=forms.Textarea
    def to_python(self, value):
        if not value:
            return []
        return value.split("\n")

    def validate(self, value):
        super().validate(value)
        for ingredient_line in value:
            validate_ingredient(ingredient_line)


class RecipeEntryForm(Form):
    ingredients = IngredientsField()





