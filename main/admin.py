from django.contrib import admin
from django.contrib import admin
from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage

# Register your models here.
admin.site.register(Person)
admin.site.register(CustomUser)
admin.site.register(CustomAdmin)
admin.site.register(Owner)
admin.site.register(ShopType)
admin.site.register(ProductType)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(SubscriptionType)
admin.site.register(PromotionType)
admin.site.register(Subscription)
admin.site.register(Promotion)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(Thread)
admin.site.register(ForumMessage)
