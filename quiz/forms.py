from django import forms
from .models import Correction


class CorrectionForm(forms.ModelForm):
    class Meta():
        model = Correction
        fields = '__all__'

    categories=(
        ('1', 'hahah'),
        ('2','hehe'),
   )
