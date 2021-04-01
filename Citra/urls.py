"""Citra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import populate, views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('populate/', populate.populate),
    path("", views.home, name="home"),
    path("threads/", views.threads_list, name="threads"),
    path('threads/<id_thread>', views.forumMessages_list),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('promotionproduct/', views.promotion_product),
    path('promotionshop/', views.promotion_shop),
    path('shops/', views.list_shop),
    path('chatList/', views.chat_list),
    # path('bookings_user/', views.list_booking_user),
    # path('bookings_owner/', views.list_booking_owner),
    path('shop/bookings/acceptbookings/', views.accept_booking),
    path('shops/<id_shop>', views.shop_details),
    path('shop/chat/<id_chat>', views.get_chat),
    path('shops/booking/', views.booking),
    path('error/', views.error),
    path('forbidden/', views.forbidden),
    path('booking/',views.booking),
    path('shop/bookings/',views.list_booking_owner),
    path('user/bookings/',views.list_booking_user),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
