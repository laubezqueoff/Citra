# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm   
from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage
from django.core.exceptions import ValidationError

class MessageForm(forms.Form):
    text = forms.CharField(label='Mensaje')

class ReviewForm(forms.Form):
    rating = forms.IntegerField(label='Puntuación')
    title = forms.CharField(label='Título')
    description = forms.CharField()

class ProductForm(forms.Form):
    name = forms.CharField(label="Nombre")
    description = forms.CharField(label="Descripción")
    price = forms.FloatField(label="Precio")
    # productType = forms.ModelChoiceField(ProductType.objects.all(), empty_label=None)
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Inserte un nombre al producto')
        return name

    # def clean_description(self):
    #     description = self.cleaned_data.get('description')
    #     if not description:
    #         raise ValidationError('Inserte una descripción')
    #     return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError('Introduzca un precio mayor que 0')
        return price