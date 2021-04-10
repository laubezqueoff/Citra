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
    path("home/", views.home, name="home"),
    path("threads/", views.threads_list, name="threads"),
    path('threads/<id_thread>', views.forumMessages_list),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('product/<id_product>/promotionweekproduct', views.promotion_week_product, name="promotion_week_product"),
    path('product/<id_product>/promotionmonthproduct', views.promotion_month_product, name="promotion_month_product"),
    path("products/<id_product>", views.product_details, name="products"),
    path('shops/<id_shop>/promotionweekshop', views.promotion_week_shop, name="promotion_week_shop"),
    path('shops/<id_shop>/promotionmonthshop', views.promotion_month_shop, name="promotion_month_shop"),
    path('shops/', views.list_shop, name="shops"),
    path('shop/bookings/acceptbookings/', views.accept_booking),
    path('shops/<id_shop>', views.shop_details, name="shop"),
    path('shop/chat_new/<id_shop>', views.get_chat_new, name='newChat'),
    path('chats/', views.get_chats_list, name='chats'),
    path('shop/chat/<id_chat>', views.get_chat, name='chat'),
    path('shops/booking/', views.booking),
    path('error/', views.error),
    path('forbidden/', views.forbidden),
    path('booking/',views.booking),
    path('shops/<id_shop>/reviews/', views.review_list, name='reviews'),
    path('shops/<id_shop>/reviews/new/', views.review_form, name='review'),
    path('shop/bookings/',views.list_booking_owner,name="list_booking_owner"),
    path('user/bookings/',views.list_booking_user,name="list_booking_user"),
    path('about/',views.about,name="about"),
    path('shops/<id_shop>/report/', views.report_shop_form, name="report_shop"),
    # path('shops/<id_shop>/report/', views.report_user_form, name="report_user"),
    path('shop/chat/<id_chat>/report/', views.report_from_chat_form, name='report_chat'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'main.views.error_404'
