from django import forms
from mainapp.models import Schema, Column
from django.forms import modelformset_factory


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ['title']


ColumnFormSet = modelformset_factory(Column, fields=("name", "type", 'order'), extra=1)
