from django.db import models


## MODELOS DE TIPOS DE USUARIO ##############################################

class Person(models.Model):
    username = models.TextField(max_length=20,unique=True)
    password = models.TextField(max_length=20)
    name = models.TextField(max_length=40)
    phoneNumber = models.IntegerField()
    email = models.TextField(max_length=30,unique=True)
    zipCode = models.IntegerField()
    registerDate = models.DateField()
    isBanned = models.BooleanField()


class CustomUser(models.Model):
    picture = models.ImageField(upload_to='users')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class CustomAdmin(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Owner(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


## MODELO DE REPORTE ########################################################

class ReportReason(models.Model):
    name = models.CharField(max_length=40)

class Report(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=60)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


## MODELOS DE TIENDA Y PRODUCTOS ############################################

class ShopType(models.Model):
    name = models.CharField(max_length=40)


class ProductType(models.Model):
    name = models.CharField(max_length=40)


class Shop(models.Model):
    name = models.CharField(max_length=60)
    shopType = models.ForeignKey(ShopType, on_delete=models.CASCADE)
    schedule = models.TextField(max_length=50)
    description = models.TextField(max_length=120)
    picture = models.ImageField(upload_to='shops')
    address = models.CharField(max_length=60)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    durationBooking = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=60)
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='products')
    price = models.FloatField()
    description = models.TextField(max_length=120)
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
    promotionType = models.ForeignKey(
        PromotionType, on_delete=models.SET_NULL, null=True)
    startDate = models.DateField()
    endDate = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)


## MODELOS DE RESERVAS Y REVIEWS ############################################

class Booking(models.Model):
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    title = models.CharField(max_length=20)
    quantity = models.IntegerField()
    isAccepted = models.BooleanField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Review(models.Model):
    rating = models.IntegerField(range(1, 5))
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=60)
    date = models.DateField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


## MODELOS DE CHAT Y MENSAJES ###############################################

class Chat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)


class ChatMessage(models.Model):
    text = models.TextField(max_length=60)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    isSentByUser = models.BooleanField()
    date = models.DateField(null=True)


## MODELOS DE FORO Y MENSAJES ###############################################

class Thread(models.Model):
    name = models.CharField(max_length=40)


class ForumMessage(models.Model):
    text = models.TextField(max_length=60)
    date = models.DateField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

## MODELO DE NOTIFICACIONES ########################################################

class Notification(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=60)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)