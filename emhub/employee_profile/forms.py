from typing import Any, Dict
from django import forms


class ApplicationForm(forms.Form):
    date_from = forms.DateField(input_formats=["%d.%m.%Y"], label='Дата от')
    date_to = forms.DateField(label='Дата до')
    reason = forms.CharField(widget=forms.Textarea, max_length=320, label='Причина')
