from models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, Thread, ForumMessage
from datetime import date


if __name__ == "__main__":
    populate()

def populate():

    delete_all_tables()
    number_of_user = 10
    populate_person(number_of_user)

    personas = Person.objects.all()

    print(personas)

   
def populate_person(range_value = 10):

    username = "User-" #User-N  
    password = "Pass-" #Pass-N
    phoneNumber = 121201211

    for i in range(number_of_user):

        username = username+str(i)
        password = password+str(i)
        name = username
        email = username+"@gmail.com"

        Person.objects.create(username=username,password=password,name=name,phoneNumber=phoneNumber+i,email=email,zipCode=phoneNumber[0:4],registerDate=date.today(),isBanned=False)


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