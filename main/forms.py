# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm   
from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage

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