from django.contrib import admin
from django.contrib import admin
from main.models import Person,CustomUser,CustomAdmin,Owner,ShopType,ProductType,Shop

# Register your models here.
admin.site.register(Person)
admin.site.register(CustomUser)
admin.site.register(CustomAdmin)
admin.site.register(Owner)
admin.site.register(ShopType)
admin.site.register(ProductType)
admin.site.register(Shop)
