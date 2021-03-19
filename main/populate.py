from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, Thread, ForumMessage

def populate():
    Person.objects.all().delete()
    for i in range(10):
        Person.objects.get_or_create(titulo=elemento[0],up_votes=elemento[1],licencia=elemento[2],descripcion = elemento[4],url="https://www.kaggle.com/" + elemento[5])