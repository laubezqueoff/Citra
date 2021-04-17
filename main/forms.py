# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm   
from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage
from django.core.exceptions import ValidationError
from main.models import Shop

class MessageForm(forms.Form):
    text = forms.CharField(label='Mensaje')

class NameShopForm(forms.Form):
    shop_name = forms.CharField(label='Nombre')

class ReviewForm(forms.Form):
    rating = forms.IntegerField(label='Puntuación')
    title = forms.CharField(label='Título')
    description = forms.CharField()

class UserSearchForm(forms.Form):
    username = forms.CharField(label='Username', required= True)
class UserBannedForm(forms.Form):
    isBanned = forms.BooleanField(label='Esta Banneado', required=False)


class ProductForm(forms.Form):
    name = forms.CharField(label="Nombre")
    description = forms.CharField(label="Descripción")
    price = forms.FloatField(label="Precio")
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Inserte un nombre al producto')
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Introduzca un precio mayor que 0')
        return price


class FormShop(forms.Form):
    name = forms.CharField(label="Nombre")
    schedule = forms.CharField(label="Horario")
    description = forms.CharField(label="Descripción")
    address = forms.CharField(label="Direción")
    durationBooking = forms.IntegerField(label="Duración")

