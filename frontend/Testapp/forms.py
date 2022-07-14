from django import forms
from .models import Information


class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ('families', 'chromosomes', 'colors')
