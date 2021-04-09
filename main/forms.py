# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import Shop


class MessageForm(forms.Form):
    text = forms.CharField(label='Mensaje')


class ReviewForm(forms.Form):
    rating = forms.IntegerField(label='Puntuación')
    title = forms.CharField(label='Título')
    description = forms.CharField()


# class FormShop(forms.Form):
#     name = forms.CharField(label='Nombre')
#     schedule = forms.CharField(label='Horario')
#     description = forms.CharField(label='Descripción')
#     address = forms.CharField(label='Dirección')


class FormShop(forms.Form):
    name = forms.CharField(label="Nombre")
    schedule = forms.CharField(label="Horario")
    description = forms.CharField(label="Descripción")
    address = forms.CharField(label="Direción")
    durationBooking = forms.IntegerField(label="Duración")
