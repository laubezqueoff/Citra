# -*- encoding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm   
from main.models import ReportReason, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage
from django.core.exceptions import ValidationError
from main.models import Shop

class MessageForm(forms.Form):
    text = forms.CharField(label='Mensaje',max_length=60,required=True,
    error_messages={'required': 'Introduce un mensaje, por favor', 'max_length':'El mensaje no debe tener más de 60 caracteres'})

class NameShopForm(forms.Form):
    shop_name = forms.CharField(label='Nombre')


class ShopForm(forms.Form):
    lista=[(r.id,r.name) for r in ShopType.objects.all()]
    username = forms.CharField(label='Username',max_length=20,required=True,
        error_messages={'required': 'Introduce un username, por favor', 'max_length':'El username no debe tener más de 20 caracteres'})
    password = forms.CharField(label='Contraseña',max_length=20,required=True,
        error_messages={'required': 'Introduce una contraseña, por favor', 'max_length':'La contraseña no debe tener más de 20 caracteres'})
    name = forms.CharField(label='Nombre',max_length=40,required=True,
        error_messages={'required': 'Introduce un nombre, por favor', 'max_length':'El nombre no debe tener más de 40 caracteres' })
    phoneNumber =forms.IntegerField(label='Teléfono', min_value=100000000, max_value=999999999,required=True,
        error_messages={'required': 'Introduce un número de teléfono, por favor','min_value':'El número de teléfono debe tener 9 cifras','max_value':'El número de teléfono debe tener 9 cifras'})
    zipCode = forms.IntegerField(label='Código postal',min_value=41000, max_value=41093,required=True,
        error_messages={'required': 'Introduce un código postal, por favor','min_value':'El código postal no puede ser menor que 41000','max_value':'El código postal no puede ser mayor que 41093'})
    email = forms.EmailField(label='Email', max_length=30,required=True, 
        error_messages={'required': 'Introduce un email, por favor', 'invalid':'El email introducido no es válido', 'max_length':'El email no debe tener más de 30 caracteres'})
    shopName=forms.CharField(label='Nombre de la tienda',max_length=60,required=True,
        error_messages={'required': 'Introduce el nombre de la tienda, por favor', 'max_length':'El nombre de la tienda no debe tener más de 60 caracteres'})
    select = forms.ChoiceField(label="Tipo de tienda", choices=lista,required=True,
        error_messages={'required': 'Introduce el tipo de la tienda, por favor', 'invalid_choice':'Debe escoger una opción válida como tipo de tienda'})
    schedule = forms.CharField(label='Horario',max_length=50,required=True, 
        error_messages={'required': 'Introduce un horario, por favor', 'max_length':'El horario no debe tener más de 50 caracteres'})
    description = forms.CharField(label='Descripción',max_length=120,required=True,
        error_messages={'required': 'Introduce una descripción, por favor', 'max_length':'La descripción no debe tener más de 120 caracteres'})
    address = forms.CharField(label='Dirección',max_length=60,required=True,
        error_messages={'required': 'Introduce una dirección, por favor', 'max_length':'La dirección no debe tener más de 60 caracteres'})
    durationBooking = forms.IntegerField(label='Duración de las reservas',min_value=1,required=True, max_value=23,
        error_messages={'required': 'Introduce una duración para las reservas, por favor','min_value':'La duración para las reservas no puede ser menor que 1','max_value':'La duración de las reservas no puede ser mayor que 23'})
    # def username_val(self):
    #     username = self.cleaned_data.get('username')
    #     if len(username) > 20:
    #         raise ValidationError('El username no debe tener más de 20 caracteres')
    #     if not username:
    #         raise ValidationError('Inserte un nombre de usuario')
    #     return username
    # def password_val(self):
    #     password = self.cleaned_data.get('password')
    #     if len(password) > 20:
    #         raise ValidationError('La contraseña no debe tener más de 20 caracteres')
    #     if not password:
    #         raise ValidationError('Inserte una contraseña')
    #     return password
    # def name_val(self):
    #     name = self.cleaned_data.get('name')
    #     if len(name) > 40:
    #         raise ValidationError('El nombre no debe tener más de 40 caracteres')
    #     if not name:
    #         raise ValidationError('Inserte un nombre')
    #     return name
    # def phoneNumber_val(self):
    #     phoneNumber = self.cleaned_data.get('phoneNumber')
    #     if phoneNumber > 999999999 or phoneNumber < 100000000:
    #         raise ValidationError('El número de teléfono debe estar entre 100000000 y 999999999')
    #     if not phoneNumber:
    #         raise ValidationError('Inserte un número de teléfono')
    #     return phoneNumber
    # def zipCode_val(self):
    #     zipCode = self.cleaned_data.get('zipCode')
    #     if zipCode > 41093 or zipCode < 41000:
    #         raise ValidationError('El código postal no debe tener más de 40 caracteres')
    #     if not zipCode:
    #         raise ValidationError('Inserte un código postal')
    #     return zipCode


class CustomUserForm(forms.Form):
    username = forms.CharField(label='Username',max_length=20,required=True,
        error_messages={'required': 'Introduce un username, por favor', 'max_length':'El username no debe tener más de 20 caracteres'})
    password = forms.CharField(label='Contraseña',max_length=20,required=True,
        error_messages={'required': 'Introduce una contraseña, por favor', 'max_length':'La contraseña no debe tener más de 20 caracteres'})
    name = forms.CharField(label='Nombre',max_length=40,required=True,
        error_messages={'required': 'Introduce un nombre, por favor', 'max_length':'El nombre no debe tener más de 40 caracteres' })
    phoneNumber =forms.IntegerField(label='Teléfono', min_value=100000000, max_value=999999999,required=True,
        error_messages={'required': 'Introduce un número de teléfono, por favor','min_value':'El número de teléfono debe tener 9 cifras','max_value':'El número de teléfono debe tener 9 cifras'})
    zipCode = forms.IntegerField(label='Código postal',min_value=41000, max_value=41093,required=True,
        error_messages={'required': 'Introduce un código postal, por favor','min_value':'El código postal no puede ser menor que 41000','max_value':'El código postal no puede ser mayor que 41093'})
    email = forms.EmailField(label='Email', max_length=30,required=True, 
        error_messages={'required': 'Introduce un email, por favor', 'invalid':'El email introducido no es válido', 'max_length':'El email no debe tener más de 30 caracteres'})

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=20,required=True,
        error_messages={'required': 'Introduce un usuario, por favor', 'max_length':'El usuario no debe tener más de 20 caracteres'})
    password = forms.CharField(label='Contraseña',max_length=20,required=True,
        error_messages={'required': 'Introduce una contraseña, por favor', 'max_length':'La contraseña no debe tener más de 20 caracteres'})

class ReviewForm(forms.Form):
    rating = forms.IntegerField(label='Puntuación',min_value=1, max_value=5,required=True,
        error_messages={'required': 'Introduce una puntuación, por favor','min_value':'La puntuación debe estar entre 1 y 5','max_value':'La puntuación debe estar entre 1 y 5'})
    title = forms.CharField(label='Título',max_length=30,required=True,
        error_messages={'required': 'Introduce un título, por favor', 'max_length':'El título no debe tener más de 30 caracteres' })
    description = forms.CharField(label='Descripción',max_length=60,required=True,
        error_messages={'required': 'Introduce una descripción, por favor', 'max_length':'La descripción no debe tener más de 60 caracteres' })
    
class CustomUserUpdateForm(forms.Form):
    password = forms.CharField(label='Contraseña',max_length=20,required=True,
        error_messages={'required': 'Introduce una contraseña, por favor', 'max_length':'La contraseña no debe tener más de 20 caracteres'})
    name = forms.CharField(label='Nombre',max_length=40,required=True,
        error_messages={'required': 'Introduce un nombre, por favor', 'max_length':'El nombre no debe tener más de 40 caracteres' })
    phoneNumber =forms.IntegerField(label='Teléfono', min_value=100000000, max_value=999999999,required=True,
        error_messages={'required': 'Introduce un número de teléfono, por favor','min_value':'El número de teléfono debe tener 9 cifras','max_value':'El número de teléfono debe tener 9 cifras'})
    zipCode = forms.IntegerField(label='Código postal',min_value=41000, max_value=41093,required=True,
        error_messages={'required': 'Introduce un código postal, por favor','min_value':'El código postal no puede ser menor que 41000','max_value':'El código postal no puede ser mayor que 41093'})
   
class ReportForm(forms.Form):
    lista=[(r.id,r.name) for r in ReportReason.objects.all()]
    title = forms.ChoiceField(label="Título", choices=lista,required=True,
        error_messages={'required': 'Introduce el título, por favor', 'invalid_choice':'Debe escoger una opción válida como título'})
    description = forms.CharField(label='Descripción',max_length=60,required=True,
        error_messages={'required': 'Introduce una descripción, por favor', 'max_length':'La descripción no debe tener más de 60 caracteres'})

class UserSearchForm(forms.Form):
    username = forms.CharField(label='Username', required= True,max_length=20,
        error_messages={'required': 'Introduce un username, por favor', 'max_length':'El username no debe tener más de 20 caracteres o no encontrará ninguna coincidencia'})

class UserBannedForm(forms.Form):
    isBanned = forms.BooleanField(label='Esta Baneado', required=False)


class ProductForm(forms.Form):
    name = forms.CharField(label="Nombre",max_length=60,required=True,
        error_messages={'required': 'Inserte un nombre al producto','max_length':'El nombre no debe tener más de 60 caracteres'})
    description = forms.CharField(label="Descripción",max_length=120,required=True,
        error_messages={'required': 'Introduce una descripción, por favor','max_length':'La descripción no debe tener más de 120 caracteres'})
    price = forms.FloatField(label="Precio",required=True,
        error_messages={'required': 'Introduce un precio, por favor'})
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
    name = forms.CharField(label="Nombre",max_length=60,required=True,
        error_messages={'required': 'Introduce un nombre, por favor', 'max_length':'El nombre no debe tener más de 60 caracteres'})
    schedule = forms.CharField(label="Horario",max_length=50,required=True,
        error_messages={'required': 'Introduce un horario, por favor', 'max_length':'El horario no debe tener más de 50 caracteres'})
    description = forms.CharField(label="Descripción",max_length=120,required=True,
        error_messages={'required': 'Introduce una descripción, por favor', 'max_length':'La descripción no debe tener más de 120 caracteres'})
    address = forms.CharField(label="Direción",max_length=60,required=True,
        error_messages={'required': 'Introduce un nombre, por favor', 'max_length':'El nombre no debe tener más de 60 caracteres'})
    durationBooking = forms.IntegerField(label='Duración de las reservas',min_value=1,required=True, max_value=23,
        error_messages={'required': 'Introduce una duración para las reservas, por favor','min_value':'La duración para las reservas no puede ser menor que 1','max_value':'La duración de las reservas no puede ser mayor que 23'})
