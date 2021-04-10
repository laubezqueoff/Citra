# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import ReportReason

class MessageForm(forms.Form):
    text = forms.CharField(label='Mensaje')

class ReviewForm(forms.Form):
    rating = forms.IntegerField(label='Puntuación')
    title = forms.CharField(label='Título')
    description = forms.CharField(label='Descripción')

class ReportForm(forms.Form):
    lista=[(r.name) for r in ReportReason.objects.all()]
    title = forms.ChoiceField(label="Título", choices=lista)
    description = forms.CharField(label='Descripción')