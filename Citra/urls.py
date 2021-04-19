from django.contrib import admin
from django.urls import path
from main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("search_shop/", views.search_shop, name="search_shop"),
    path("threads/", views.threads_list, name="threads"),
    path('threads/<id_thread>', views.forumMessages_list),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('product/<id_shop>/create', views.product_create, name="product_create"),
    path('product/<id_product>/delete', views.product_delete, name="product_delete"),
    path('product/<id_product>/promotionweekproduct', views.promotion_week_product, name="promotion_week_product"),
    path('product/<id_product>/promotionmonthproduct', views.promotion_month_product, name="promotion_month_product"),
    path("products/<id_product>", views.product_details, name="products"),
    path('shops/<id_shop>/promotionweekshop',
         views.promotion_week_shop, name="promotion_week_shop"),
    path('shops/<id_shop>/promotionmonthshop',
         views.promotion_month_shop, name="promotion_month_shop"),
    path('shops/<id_shop>/activateshop',
         views.activate_shop, name="activate_shop"),
    path('shops/', views.list_shop, name="shops"),
    path('shop/bookings/acceptbookings/', views.accept_booking),
    path('shops/<id_shop>/', views.shop_details, name="shop"),
    path('shop/chat_new/<id_shop>/', views.get_chat_new, name='newChat'),
    path('chats/', views.get_chats_list, name='chats'),
    path('shop/chat/<id_chat>/', views.get_chat, name='chat'),
    path('shops/booking/', views.booking),
    path('error/', views.error),
    path('forbidden/', views.forbidden),
    path('booking/', views.booking),
    path('shops/<id_shop>/reviews/', views.review_list, name='reviews'),
    path('shops/<id_shop>/reviews/new/', views.review_form, name='review'),
    path('shop/bookings/',views.list_booking_owner,name="list_booking_owner"),
    path('user/bookings/',views.list_booking_user,name="list_booking_user"),
    path('owners/',views.get_owners,name="list_owners"),
    path('users/',views.get_users,name="list_users"),
    path('owners/<id_user>',views.get_owner,name="list_owners"),
    path('users/<id_user>',views.get_user,name="list_users"),
    path('about/',views.about,name="about"),
    path('shops/<id_shop>/report/', views.report_shop_form, name="report_shop"),
    path('shop/bookings/<id_booking>/report/', views.report_user_form, name="report_user"),
    path('shop/chat/<id_chat>/report/', views.report_from_chat_form, name='report_chat'),
    path('register/',views.register,name="register"),
    path('registerShop/',views.registerShop,name="registerShop"),
    path('shops/<id_shop>/edit', views.updateShop, name='update_shop'),
    path('updateUser/',views.updateUser,name="updateUser"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'main.views.error_404'
