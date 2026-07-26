# recommender/forms.py
from django import forms


class SongSearchForm(forms.Form):
    q = forms.CharField(
        label="Search",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by track or artist..."}),
    )