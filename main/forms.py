# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm    

class MessageForm(forms.Form):
    text = forms.CharField(label='Mensaje')

class ReviewForm(forms.Form):
    rating = forms.IntegerField(label='Puntuación')
    title = forms.CharField(label='Título')
    description = forms.CharField()
class UserSearchForm(forms.Form):
    username = forms.CharField(label='Username')
class UserBannedForm(forms.Form):
    isBanned = forms.BooleanField(label='Esta Banneado', required=False)