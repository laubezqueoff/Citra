from django.db import models


## MODELOS DE TIPOS DE USUARIO ##############################################

class Person(models.Model):
    username = models.TextField(max_length=20)
    password = models.TextField(max_length=20)
    name = models.TextField(max_length=40)
    phoneNumber = models.IntegerField(max_length=9)
    email = models.TextField(max_length=30)
    zipCode = models.IntegerField(max_length=5)
    registerDate = models.DateField()
    isBanned = models.BooleanField()


class User(models.Model):
    picture = models.URLField(max_length=100)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Admin(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Owner(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


## MODELOS DE TIENDA Y PRODUCTOS ############################################

# Yo pondria unos tipos de tienda estandar y que el usuario elija el que mas se adapte
# a su negocio, y lo mismo para los productos

class ShopType(models.Model):
    name = models.CharField()


class ProductType(models.Model):
    name = models.CharField()


class Shop(models.Model):
    name = models.CharField(max_length=20)
    shopType = models.ForeignKey(ShopType, on_delete=models.CASCADE)
    schedule = models.TextField(max_length=50)
    description = models.TextField(max_length=60)
    picture = models.URLField(max_length=100)
    address = models.CharField(max_length=40)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    duration_booking = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=20)
    productType = models.CharField(max_length=20)
    picture = models.URLField(max_length=100)
    price = models.FloatField
    description = models.TextField(max_length=60)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


## MODELOS DE SUSCRIPCION Y PROMOCIONES #####################################
class SubscriptionType(models.Model):
    name = models.CharField(max_length=20)


class PromotionType(models.Model):
    name = models.CharField(max_length=20)


class Subscription(models.Model):
    subscriptionType = models.ForeignKey(
        SubscriptionType, on_delete=models.SET_NULL, null=True)
    startDate = models.DateField()
    endDate = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


class Promotion(models.Model):
    #promotionType = models.CharField(max_length=20)
    promotionType = models.ForeignKey(
        PromotionType, on_delete=models.SET_NULL, null=True)
    startDate = models.DateField()
    endDate = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


# Los tipos de suscripcion y promocion los dejo así de momento para implementarlos
# mas adelante


## MODELOS DE RESERVAS Y REVIEWS ############################################

class Booking(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    description = models.CharField(max_length=20)
    title = models.CharField(max_length=20)


class Review(models.Model):
    rating = models.IntegerField(range(1, 5))
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=60)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


## MODELOS DE CHAT Y MENSAJES ###############################################

# este modelo es lo que se me ocurre para diferenciar quien envió el mensaje
# para ponerlos de distinto color/distinto lado de la pantalla


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


class ChatMessage(models.Model):
    text = models.TextField(max_length=60)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    isSentByUser = models.BooleanField()


## MODELOS DE FORO Y MENSAJES ###############################################

class Thread(models.Model):
    name = models.CharField()


class ForumMessage(models.Model):
    text = models.TextField(max_length=60)
    date = models.DateField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
