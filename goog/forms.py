from goog.models import *
from django import forms


class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=150)