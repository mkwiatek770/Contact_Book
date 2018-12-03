from django import forms
from .models import Person, Group, CHOICES


class CreatePersonForm(forms.Form):

    # fields
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    phone_num = forms.RegexField(regex=r'\d{9}|\d{3} \d{3} \d{3}')
    phone_type = forms.ChoiceField(choices=CHOICES)
    email = forms.EmailField()
    email_type = forms.ChoiceField(choices=CHOICES)
