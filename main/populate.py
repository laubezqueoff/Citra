from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage
from datetime import date
from django.shortcuts import render, HttpResponse,redirect
from django.shortcuts import get_object_or_404

if __name__ == "__main__":
    populate()

def populate(request):

    delete_all_tables()
    number_of_user = 10
    number_of_shop = 10
    range_value = 3
    number_of_threads = 4

    populate_product_type()
    populate_shop_type()
    populate_subscription_type()
    populate_promotion_type()

    populate_person(number_of_user)
    populate_roles(number_of_user)
    
    populate_shop(number_of_shop)
    populate_chat(range_value)
    populate_chat_message(range_value)
    populate_threads(number_of_threads)
    populate_forumMessage(number_of_threads)

    personas = Person.objects.all()

    print(personas)

    return render(request, 'index.html')

   
def populate_person(number_of_user = 10):

    username = "User-" #User-N  
    password = "Pass-" #Pass-N
    phoneNumber = 121201211

    for i in range(number_of_user):

        username = username+str(i)
        password = password+str(i)
        name = username
        email = username+"@gmail.com"

        Person.objects.create(id = i,username=username,password=password,name=name,phoneNumber=phoneNumber+i,email=email,zipCode=41740,registerDate=date.today(),isBanned=False)

def populate_roles(number_of_user):
    cap1 = round(number_of_user/3)
    cap2 = cap1*2
    msg = "Funciona correctamente"
    try:
        for i in range(number_of_user):
            if i < cap1:
                person = Person.objects.filter(id=i).get()
                CustomUser.objects.create(id=i,person=person)
            elif i >= cap1 and i<cap2:
                person = Person.objects.filter(id=i).get()
                CustomAdmin.objects.create(id=i,person=person)
            elif i >= cap2:
                person = Person.objects.filter(id=i).get()
                Owner.objects.create(id=i,person=person)
    except:
        msg = "Se ha lanzado un error"
    print(msg)

def populate_shop_type():
    ShopType.objects.create(id=0,name='Alimentación')

def populate_shop(number_of_shop=10):

    name = "Shop-"  # User-N
    schedule = "Horarios de tarde de 16:00-19:00"
    description = "Tienda dedicada a "
    address = "Calle Toro numero "
    durationBooking = 30

    owner =Owner.objects.all()

    for i,o in enumerate(owner):
        

        shopType = ShopType.objects.get(id=0)
        Shop.objects.create(id=i, name=name+str(i), shopType=shopType, schedule=schedule, description=description + shopType.name,
                            address=address+str(i), owner=o, durationBooking=durationBooking)     
        populate_product(5,i)

def populate_product(range_value = 10, shop_id = 0):

    name = "Product-"
    price = 10
    description = "Descripcion de prueba"
       
    for i in range(range_value*shop_id ,range_value*(shop_id+1)):

        name = name+str(i)

        Product.objects.create(id=i, name=name, productType=ProductType.objects.get(id = 0), price=price, description=description, shop=Shop.objects.get(id = shop_id))

def populate_product_type():
    ProductType.objects.create(id=0, name="Alimentacion")


def populate_subscription_type():
    SubscriptionType.objects.create(id=0, name="Semanal")
    SubscriptionType.objects.create(id=1, name="Mensual")

def populate_promotion_type():
    PromotionType.objects.create(id=0, name="Semanal")
    PromotionType.objects.create(id=1, name="Mensual")


def populate_chat(range_value = 3):


    for i in range(3):
        shop = Shop.objects.get(id=i)
        Chat.objects.create(id= i,user=get_object_or_404(CustomUser, pk = i),shop= shop)

def populate_chat_message(range_value = 3):


    for i in range(3):
        if i%2 ==1 : 
            isSentByUser=True
        else: 
            isSentByUser=False
        ChatMessage.objects.create(id= i,text = '¿Vendeis naranjas?', chat=get_object_or_404(Chat, pk = i), date = date.today(),isSentByUser=isSentByUser)


def populate_threads(number_of_threads = 4):

    name = "Thread"
    
    for i in range(3):

        name = name
        
        Thread.objects.create(id = i, name=name+str(i))

def populate_forumMessage(number_of_threads = 4):

    text = "Soy el comentario "

    for i in range(3):

        thread = Thread.objects.get(id=i)
        user = CustomUser.objects.get(id=i)

        ForumMessage.objects.create(id = i,text=text+str(i),date=date.today(),thread=thread,user=user)

def delete_all_tables():
    Person.objects.all().delete()
    CustomUser.objects.all().delete()
    CustomAdmin.objects.all().delete()
    Owner.objects.all().delete()
    ShopType.objects.all().delete()
    ProductType.objects.all().delete()
    Shop.objects.all().delete()
    Product.objects.all().delete()
    SubscriptionType.objects.all().delete()
    PromotionType.objects.all().delete()
    Subscription.objects.all().delete()
    Promotion.objects.all().delete()
    Booking.objects.all().delete()
    Review.objects.all().delete()
    Chat.objects.all().delete()
    Thread.objects.all().delete()
    ForumMessage.objects.all().delete()