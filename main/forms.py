# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm    

class MessageForm(forms.Form):
    text = forms.CharField(label='Mensaje')