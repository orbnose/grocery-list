from email.policy import default
from django import forms
from django.forms import Form, ModelForm
from .models import List, Entry, Group

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