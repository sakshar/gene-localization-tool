from django import forms
from .models import Information
import os
from django.core.exceptions import ValidationError


class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ('families', 'chromosomes', 'colors')
