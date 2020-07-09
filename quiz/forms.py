from django import forms
from .models import Correction


class CorrectionForm(forms.ModelForm):
    class Meta():
        model = Correction
        fields = ('name', 'type', 'text', 'desc')

