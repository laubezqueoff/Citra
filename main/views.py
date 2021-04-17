from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage
import requests
from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
import urllib.request
from main.forms import MessageForm, ReviewForm, UserSearchForm, UserBannedForm, ProductForm, FormShop, NameShopForm
from django.http import Http404
import json
from django.http import JsonResponse
from datetime import timedelta
from datetime import datetime
import stripe
from Citra import settings


def login(request):
    ''' Logea una persona en la aplicación.\n
        POST    -> Lleva la inicio con el contexto actualizado \n
        GET     -> Lleva al formulario de login
    '''
    # msg_success = "Bienvenido a la aplicación"
    msg_error = "El nombre y la contraseña no coinciden"

    if request.method == 'POST':  # Si es un POST redirijimos a la vista de index con el context actualizado
        try:
            # Sacamos el valor de la propiedad 'name' del formulario
            username = request.POST['username']
            # Sacamos el valor de la propiedad 'password' del formulario
            password = request.POST['password']

            # Buscamos el usuario por su contraseña y nombre
            person = Person.objects.get(username=username, password=password)
            rol_and_id = whoIsWho(person)

            update_context(request, person.id,
                           rol_and_id[0], rol_and_id[1], True)
            # msg = msg_success

            person_id, rol, rol_id, is_active = get_context(request)
            context = [person_id, rol, rol_id, is_active]

            promotions_shops = Promotion.objects.filter(product=None)
            promotions_products = Promotion.objects.filter(shop=None)

            tienda = miTienda(person_id)

            return render(request, 'home.html', {"context": context, 'promotions_shops': promotions_shops, 'promotions_products': promotions_products, 'tienda': tienda})
        except:
            # Es importante pasar el context en todas las vistas.
            # Cambiar index.html por tu vista en tu método
            msg = msg_error
            return render(request, 'login.html', {"msg": msg, 'tienda': ''})

    else:  # Si es un GET redirijimos a la vista de login
        return render(request, 'login.html', {'tienda': ''})


def registerShop(request):
    if request.method == 'POST':  # Si es un POST redirijimos a la vista de index con el context actualizado
        try:
            # Parametros tomados del post
            username = request.POST['username']
            password = request.POST['password']
            name = request.POST['name']
            phoneNumber = request.POST['phoneNumber']
            zipCode = request.POST['zipCode']
            email = request.POST['email']

            # Parámetros autogenerados
            registerDate = date.today()
            isBanned = False

            p = Person(username=username, password=password, name=name, phoneNumber=phoneNumber,
                       email=email, zipCode=zipCode, registerDate=registerDate, isBanned=isBanned)
            p.save()

            p = Person.objects.get(username=username, password=password)

            co = Owner(person=p)
            co.save()

            shopName = request.POST['shopName']
            shopType = request.POST['shopType']
            schedule = request.POST['schedule']
            description = request.POST['description']
            picture = request.FILES.get('picture')
            address = request.POST['address']
            durationBooking = request.POST['durationBooking']

            co = Owner.objects.get(person=p)
            shopType = ShopType.objects.get(id=int(shopType))
            shop = Shop.objects.create(name=name, shopType=shopType, schedule=schedule, description=description,
                                       picture=picture, address=address, owner=co, durationBooking=durationBooking)

            update_context(request, p.id, "Owner", co.id, True)
            person_id, rol, rol_id, is_active = get_context(request)
            context = [person_id, rol, rol_id, is_active]

            return redirect('/home/')

        except:
            print("------------------------------")
            return render(request, 'login.html')

    else:
        return render(request, 'register_shop.html')


def register(request):
    ''' Logea una persona en la aplicación.\n
        POST    -> Lleva la inicio con el contexto actualizado \n
        GET     -> Lleva al formulario de login
    '''
    #msg_success = "Bienvenido a la aplicación"
    msg_error = "El nombre y la contraseña no coinciden"

    if request.method == 'POST':  # Si es un POST redirijimos a la vista de index con el context actualizado
        try:
            # Parametros tomados del post
            username = request.POST['username']
            password = request.POST['password']
            name = request.POST['name']
            phoneNumber = request.POST['phoneNumber']
            zipCode = request.POST['zipCode']
            email = request.POST['email']

            # Parámetros autogenerados
            registerDate = date.today()
            isBanned = False

            p = Person(username=username, password=password, name=name, phoneNumber=phoneNumber,
                       email=email, zipCode=zipCode, registerDate=registerDate, isBanned=isBanned)
            p.save()

            p = Person.objects.get(username=username, password=password)

            cu = CustomUser(person=p)
            cu.save()

            rol_and_id = whoIsWho(p)

            update_context(request, p.id, rol_and_id[0], rol_and_id[1], True)
            person_id, rol, rol_id, is_active = get_context(request)
            context = [person_id, rol, rol_id, is_active]

            return render(request, 'home.html', {"context": context})

        except:
            msg = msg_error
            return render(request, 'login.html', {"msg": msg})

    else:  # Si es un GET redirijimos a la vista de login
        return render(request, 'register_user.html')


def logout(request):
    ''' Deslogea una persona en la aplicación.\n
        POST    -> None \n
        GET     -> Lleva al formulario de login
    '''
    if request.method == 'GET':  # Si es un GET redirijimos a la vista de index con el context actualizado
        try:

            person_id, rol, rol_id, is_active = get_context(request)

            update_context(request, person_id, rol, rol_id, False)
            delete_context(request)

        except Exception as e:
            print(e)

        promotions_shops = Promotion.objects.filter(product=None)
        promotions_products = Promotion.objects.filter(shop=None)

        return render(request, 'home.html', {'promotions_shops': promotions_shops, 'promotions_products': promotions_products})


def whoIsWho(person):
    ''' Identifica el rol e id de una persona\n
        In: Person\n
        Out: List[rol,rol_id]
    '''
    res = []
    try:
        cu = CustomUser.objects.get(person=person).id
        continue_searching = False
        res = ["User", cu]
    except:
        continue_searching = True

    if continue_searching:
        try:
            ca = CustomAdmin.objects.get(person=person).id
            res = ["Admin", ca]
        except:
            continue_searching = True

    if continue_searching:
        try:
            o = Owner.objects.get(person=person).id
            res = ["Owner", o]
        except:
            continue_searching = True

    return res


def update_context(request, person_id, rol, rol_id, is_active):
    ''' Actualiza el context en función de los parámetros de entrada\n
        In: person_id (id de la persona), rol (String, puede ser Owner,Admin o User),rol_id (id de la persona en su rol), is_active (se encuentra usando la web)\n
        Out: Bool. True si todo va bien, False si algo falla
    '''
    res = True

    try:
        request.session['person_id'] = str(person_id)
        request.session['rol'] = str(rol)
        request.session['rol_id'] = str(rol_id)
        request.session['is_active'] = str(is_active)
    except:
        print("---------")
        res = False

    return res


def delete_context(request):
    ''' Elimina el context\n
        In: None \n
        Out: Bool. True si todo va bien, False si algo falla
    '''

    res = True
    try:
        del request.session['person_id']
        del request.session['rol']
        del request.session['person_id']
        del request.session['is_active']

    except:
        res = False

    return res


def get_context(request):
    ''' Actualiza el context en función de los parámetros de entrada\n
        In: None \n
        Out: person_id (id de la persona), rol (String, puede ser Owner,Admin o User),rol_id (id de la persona en su rol), is_active (se encuentra usando la web)
    '''
    try:
        person_id = request.session['person_id']
        rol = request.session['rol']
        rol_id = request.session['rol_id']
        is_active = request.session['is_active']
    except:
        person_id = '0'
        rol = 'Usuario no registrado'
        rol_id = '0'
        is_active = False

    return person_id, rol, rol_id, is_active


def get_or_create_customer(email: str, source: str) -> stripe.Customer:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    connected_customers = stripe.Customer.list()
    for customer in connected_customers:
        if customer.email == email:
            return customer
    return stripe.Customer.create(
        email=email,
        source=source
    )


def is_customer(email: str) -> bool:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    connected_customers = stripe.Customer.list()
    for customer in connected_customers:
        if customer.email == email:
            return True

    return False

# Amount x100 = centimos


def charge(amount: int, source: str) -> None:
    stripe.Charge.create(
        amount=amount,
        currency='eur',
        description='A event payment',
        source=source)


def promotion_week_product(request, id_product):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        time = date.today()
        product = get_object_or_404(Product, pk=id_product)
        promotion = Promotion.objects.filter(product=product).exists()
        promotionweek = Promotion.objects.filter(endDate__gte = time).exists()
        if (not(promotion) and str(product.shop.owner.person.id) == person_id):
            promotionType = PromotionType.objects.get(id=0)  # semanal
            owner = Owner.objects.get(person=person_id)
            time = date.today()
            endtime = (time + timedelta(days=7))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=300, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.create(
                owner=owner, shop=None, startDate=time, endDate=endtime, promotionType=promotionType, product=product)
            return redirect("home")
        elif (promotion and str(product.shop.owner.person.id) == person_id and not promotionweek):
            time = date.today()
            endtime = (time + timedelta(days=7))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=300, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.filter(product = product).update(startDate=time, endDate=endtime)
            return redirect("home")
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')


def promotion_month_product(request, id_product):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        product = get_object_or_404(Product, pk=id_product)
        promotion = Promotion.objects.filter(product=product).exists()
        time = date.today()
        promotionmonth = Promotion.objects.filter(endDate__gte = time).exists()
        if (not(promotion) and str(product.shop.owner.person.id) == person_id):
            promotionType = PromotionType.objects.get(id=1)  # mensual
            owner = Owner.objects.get(person=person_id)
            time = date.today()
            endtime = (time + timedelta(days=30))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=500, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.create(
                owner=owner, shop=None, startDate=time, endDate=endtime, promotionType=promotionType, product=product)
            return redirect("home")
        elif (promotion and str(product.shop.owner.person.id) == person_id and not promotionmonth):
            time = date.today()
            endtime = (time + timedelta(days=30))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=500, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.filter(product = product).update(startDate=time, endDate=endtime)
            return redirect("home")
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')


def threads_list(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if rol == "User":
        threads = Thread.objects.all
        return render(request, 'threads.html', {'threads': threads, 'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})


def forumMessages_list(request, id_thread):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    thread = get_object_or_404(Thread, pk=id_thread)
    tienda = miTienda(person_id)
    if rol == "User":
        if request.method == 'POST':
            text = request.POST['text']
            ForumMessage.objects.create(text=text, date=date.today(
            ), thread=thread, user=CustomUser.objects.get(id=rol_id))

        threadName = thread.name
        forumMessages = []
        for m in thread.forummessage_set.all():
            forumMessages.append(m)
        return render(request, 'thread.html', {'forumMessages': forumMessages, 'threadName': threadName, 'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})


def promotion_week_shop(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    time = date.today()
    sus = Subscription.objects.filter(endDate__gte = time).exists()
    if (is_active):
        time = date.today()
        shop = get_object_or_404(Shop, pk=id_shop)
        promotion = Promotion.objects.filter(shop=shop).exists()
        promotionweek = Promotion.objects.filter(endDate__gte = time).exists()
        print(promotionweek)
        if (not(promotion) and str(shop.owner.person.id) == person_id and sus):
            promotionType = PromotionType.objects.get(id=0)
            owner = Owner.objects.get(person=person_id)
            time = date.today()
            endtime = (time + timedelta(days=7))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=500, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.create(
                owner=owner, shop=shop, startDate=time, endDate=endtime, promotionType=promotionType, product=None)
            return redirect("home")
        elif (promotion and str(shop.owner.person.id) == person_id and sus):
            time = date.today()
            endtime = (time + timedelta(days=7))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=500, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.filter(shop = shop).update(startDate=time, endDate=endtime)
            return redirect("home")
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')


def promotion_month_shop(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    time = date.today()
    sus = Subscription.objects.filter(endDate__gte = time).exists()
    if (is_active):
        shop = get_object_or_404(Shop, pk=id_shop)
        promotion = Promotion.objects.filter(shop=shop).exists()
        time = date.today()
        promotionmonth = Promotion.objects.filter(endDate__gte = time).exists()
        if (not(promotion) and str(shop.owner.person.id) == person_id and sus):
            promotionType = PromotionType.objects.get(id=1)
            owner = Owner.objects.get(person=person_id)
            time = date.today()
            endtime = (time + timedelta(days=30))
            person = Person.objects.get(id=person_id)
            print(promotionType)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=1000, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.create(
                owner=owner, shop=shop, startDate=time, endDate=endtime, promotionType=promotionType, product=None)
            return redirect("home")
        elif (promotion and str(shop.owner.person.id) == person_id and not promotionmonth and sus):
            time = date.today()
            endtime = (time + timedelta(days=30))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=1000, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.filter(shop = shop).update(startDate=time, endDate=endtime)
            return redirect("home")
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')


def activate_shop(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        shop = get_object_or_404(Shop, pk=id_shop)
        subscription = Subscription.objects.filter(shop=shop).exists()
        time = date.today()
        activate = Subscription.objects.filter(endDate__gte = time).exists()
        if (not(subscription) and str(shop.owner.person.id) == person_id):
            subscriptionType = SubscriptionType.objects.get(id=0)
            owner = Owner.objects.get(person=person_id)
            time = date.today()
            endtime = (time + timedelta(days=30))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=1000, source=request.POST.get('stripeToken'))
            suscripcion = Subscription.objects.create(
                subscriptionType=subscriptionType, startDate=time, endDate=endtime, owner=owner, shop=shop)
            return render(request, "home.html", {'suscripcion': suscripcion, 'context': context, 'stripe_key': settings.STRIPE_PUBLISHABLE_KEY, 'tienda': tienda})
        elif (subscription and str(shop.owner.person.id) == person_id and not activate):
            time = date.today()
            endtime = (time + timedelta(days=30))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=1000, source=request.POST.get('stripeToken'))
            promocion = Subscription.objects.filter(shop = shop).update(startDate=time, endDate=endtime)
            return redirect("home")
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')


def product_create(request, id_shop):
    shop = get_object_or_404(Shop, pk=id_shop)
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active and rol == "Owner" and str(shop.owner.person.id) == person_id):
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                price = form.cleaned_data['price']
                picture = request.FILES.get('picture')
                if picture.size > 5000000:
                    msg = 'El tamaño máximo de la imagen no puede superar 5 MB'
                    types = ProductType.objects.all()
                    productType = []
                    for ty in types:
                        productType.append(ty)
                    return render(request, 'create_product.html', {'form': form, 'types': productType, "context": context, 'tienda': tienda, 'msg': msg})
                else:
                    product = Product.objects.create(name=request.POST['name'], price=price, description=request.POST['description'], productType=ProductType.objects.get(
                        name=request.POST['select']), picture=picture, shop=shop)
                    return redirect('/shops/'+str(shop.id))
            else:
                types = ProductType.objects.all()
                productType = []
                for ty in types:
                    productType.append(ty)
                return render(request, 'create_product.html', {'form': form, 'types': productType, "context": context, 'tienda': tienda})

        form = ProductForm()
        types = ProductType.objects.all()
        productType = []
        for ty in types:
            productType.append(ty)
        return render(request, 'create_product.html', {'shop': shop, 'types': productType, "context": context, 'tienda': tienda, 'form': form})
    else:
        return render(request, 'prohibido.html', {"context": context, 'tienda': tienda})


def product_delete(request, id_product):
    product = get_object_or_404(Product, pk=request.POST.get('id_product'))
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    shop_id = product.shop.id
    if (is_active and rol == "Owner" and str(product.shop.owner.person.id) == person_id):
        product.delete()
        data = {
            'url': "/shops/" + str(product.shop.id)
        }
        return JsonResponse(data)

    else:
        data = {
            'url': "/prohibido/"
        }
        return JsonResponse(data)


def product_details(request, id_product):
    product = get_object_or_404(Product, pk=id_product)
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    today = date.today()
    promotionProduct = Promotion.objects.filter(product=product, endDate__gte = today).exists()
    tienda = miTienda(person_id)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.price = form.cleaned_data['price']
            product.description = form.cleaned_data['description']
            product.productType = ProductType.objects.get(
                name=request.POST['select'])
            if request.FILES.get('picture').size > 5000000:
                msg = 'El tamaño máximo de la imagen no puede superar 5 MB'
                types = ProductType.objects.all()
                productType = []
                for ty in types:
                    productType.append(ty)
                return render(request, 'products.html', {'form': form, 'product': product, 'types': productType, "context": context, "promotionProduct": not(promotionProduct), 'tienda': tienda, 'msg': msg})
            else:
                if request.FILES.get('picture') != None:
                    product.picture = request.FILES.get('picture')
                product.save()
                return redirect('/shops/'+str(product.shop.id))
        else:
            types = ProductType.objects.all()
            productType = []
            for ty in types:
                productType.append(ty)
            return render(request, 'products.html', {'form': form, 'product': product, 'types': productType, "context": context, "promotionProduct": not(promotionProduct), 'tienda': tienda})

    form = ProductForm()
    types = ProductType.objects.all()
    productType = []
    for ty in types:
        productType.append(ty)
    print(product.picture)
    return render(request, 'products.html', {'stripe_key': settings.STRIPE_PUBLISHABLE_KEY, 'form': form, 'product': product, 'types': productType, "context": context, "promotionProduct": not(promotionProduct), 'tienda': tienda})


def list_shop(request):
    today = date.today()
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    shops = Shop.objects.all()
    shop_subscription = {}
    for promo in shops:
        a = Subscription.objects.filter(endDate__gte = today, shop = promo).exists()
        shop_subscription[promo] = a
    tienda = miTienda(person_id)
    return render(request, 'shops.html', {'shop_subscription': shop_subscription, 'context': context, 'tienda': tienda})


def shop_details(request, id_shop):
    shop = get_object_or_404(Shop, pk=id_shop)
    products = Product.objects.filter(shop=shop)
    today = date.today()
    promotionShop = Promotion.objects.filter(shop=shop, endDate__gte = today).exists()
    subscriptionShop = Subscription.objects.filter(shop=shop, endDate__gte = today).exists()
    productType = []
    for prod in products:
        productType.append(prod.productType)
    try:
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
    except:
        person_id = 0
        rol = 'User no registrado'
        context = [person_id, rol]
    tienda = miTienda(person_id)
    return render(request, 'shop_detail.html', {'shop': shop, 'productType': set(productType), 'subscriptionShop': subscriptionShop, 'products': products, 'context': context, 'promotionShop': not(promotionShop), 'tienda': tienda, 'stripe_key': settings.STRIPE_PUBLISHABLE_KEY})


def get_chats_list(request):
    ''' Muestra una lista de todos los chats que el usuario activo, sea user u owner, tenga. \n
        POST    -> None \n
        GET     -> Proporciona un listado de los chats del usuario/dueño
    '''
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)

    chats = []

    if rol == 'User':

        chats = Chat.objects.filter(
            user=get_object_or_404(CustomUser, pk=person_id))

    elif rol == 'Owner':

        shops = Shop.objects.filter(
            owner=get_object_or_404(Owner, pk=person_id))
        i = 0
        for s in shops:
            if i == 0:
                chats = Chat.objects.filter(shop=s)
            else:
                chats = chats | Chat.objects.filter(shop=s)

            i += 1
    else:
        return render(request, 'error.html', {"context": context, 'tienda': tienda}, status=403)

    print(chats)
    return render(request, "chatList.html", {"context": context, "chats": chats, 'tienda': tienda}, status=200)


def get_chat(request, id_chat):
    ''' Muesta los mensajes del chat y prepara el imputo para enviar mensajes.\n
        POST    -> None \n
        GET     -> Muestra los mensajes del chat, de las dos partes
    '''
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        chat = get_object_or_404(Chat, pk=id_chat)
        # TODO: if para comprobar que el usuario forma parte de ese chat
        if str(rol) == 'User':
            if not (int(chat.user.id) == int(person_id)):
                print(True)
                return render(request, 'prohibido.html', {"context": context, 'tienda': tienda}, status=403)
        elif str(rol) == 'Owner':
            if not(int(chat.shop.owner.id) == int(person_id)):
                print(False)
                return render(request, 'prohibido.html', {"context": context, 'tienda': tienda}, status=403)
        else:
            return render(request, 'prohibido.html', {"context": context, 'tienda': tienda}, status=403)

        if request.method == 'POST':
            form = MessageForm(data=request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                shop = chat.shop
                isSentByUser = False
                if rol == 'User':
                    isSentByUser = True
                ChatMessage.objects.create(
                    text=text, chat=chat, date=date.today(), isSentByUser=isSentByUser).save()
                return redirect('/shop/chat/'+str(chat.id))
        chat_message = ChatMessage.objects.filter(chat=chat)
        form = MessageForm()
        return render(request, 'chat.html', {"context": context, "messages": chat_message, 'form': form, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html', status=403)


def get_chat_new(request, id_shop):
    ''' Muesta los mensajes del chat y prepara el imputo para enviar mensajes.\n
        POST    -> Envia un mensaje a la tienda si lo envia un usuario y a un usuario si lo envia una tienda \n
        GET     -> Muestra los mensajes del chat, de las dos partes
    '''

    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    print(rol)
    if rol == 'Admin' or rol == 'Owner':
        return render(request, 'error.html', {"context": context, 'tienda': tienda}, status=403)
    shop = get_object_or_404(Shop, pk=id_shop)
    user = get_object_or_404(CustomUser, pk=person_id)
    try:
        chat = Chat.objects.filter(shop=shop, user=user)[0]
    except:
        chat = None
    print(chat)
    if chat != None:
        return redirect('/shop/chat/'+str(chat.id))
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            newChat = Chat.objects.create(shop=shop, user=user)
            newChat.save()
            print('new chat')
            print(newChat.pk)
            isSentByUser = False
            if rol == 'User':
                isSentByUser = True
            ChatMessage.objects.create(
                text=text, chat=newChat, date=date.today(), isSentByUser=isSentByUser).save()
            return redirect('/shop/chat/'+str(newChat.pk))

    chat_message = []
    form = MessageForm()
    return render(request, 'chat.html', {"context": context, "messages": chat_message, 'form': form, 'shop_id': id_shop, 'tienda': tienda})

def search_shop(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if request.method == 'POST':
        form = NameShopForm(data=request.POST)
        if form.is_valid():
            shop_name = form.cleaned_data['shop_name']
            shops = Shop.objects.filter(name__contains=shop_name)
            shopType = ShopType.objects.all()
            return render(request, 'search_shop.html', {'context': context, 'tienda': tienda, 'shops': shops, 'shopType': shopType, "shop_name": shop_name})

    form = NameShopForm()
    promotions_shops = Promotion.objects.filter(product=None)
    promotions_products = Promotion.objects.filter(shop=None)
    return render(request, 'home.html', {"context": context, 'promotions_shops': promotions_shops, 'promotions_products': promotions_products, 'tienda': tienda, 'form': form})

def home(request):
    today = date.today()
    promotions_shops = Promotion.objects.filter(product=None, endDate__gte = today)
    promotions_products = Promotion.objects.filter(shop=None, endDate__gte = today)
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    promotions_shops_subscription = {}
    promotions_products_subscription = {}
    for promo in promotions_shops:
        sus = Subscription.objects.filter(endDate__gte = today, shop = promo.shop).exists()
        promotions_shops_subscription[promo] = sus

    for promo in promotions_products:
        sus = Subscription.objects.filter(endDate__gte = today, shop = promo.product.shop).exists()
        promotions_products_subscription[promo] = sus

    return render(request, 'home.html', {"context": context, 'promotions_shops_subscription': promotions_shops_subscription, 'promotions_products_subscription': promotions_products_subscription, 'tienda': tienda})


def booking(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    if (is_active):
        user = CustomUser.objects.get(id=person_id)
        for reserva in json.loads(request.POST.get('key_1_string')):
            product = Product.objects.get(id=reserva['id'])

            Booking.objects.create(startDate=date.today(), endDate=date.today(
            ), product=product, title='Prueba', quantity=reserva['cantidad'], isAccepted=False, user=user)

        data = {
            'url': "user/bookings/"
        }
        return JsonResponse(data)
    else:
        data = {
            'url': "/prohibido/"
        }
        return JsonResponse(data)


def list_booking_user(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        user = CustomUser.objects.get(id=person_id)
        bookings = Booking.objects.filter(user=user).filter(isAccepted=False)
        bookingsQuantity = {}
        for book in bookings:
            bookingsQuantity[book] = book.product.price * book.quantity
        return render(request, 'bookings_user.html', {'bookingsQuantity': bookingsQuantity, 'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')


def list_booking_owner(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        owner = Owner.objects.get(id=person_id)
        bookings = Booking.objects.filter(isAccepted=False)
        reservas = []
        for book in bookings:
            if book.product.shop.owner.id == owner.id:
                reservas.append(book)
        return render(request, 'bookings_owner.html', {'bookings': reservas, 'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')


def accept_booking(request):
    booking = Booking.objects.filter(
        id=request.POST.get('id')).update(isAccepted=True)
    data = {
        'url': "/shop/bookings/"
    }
    return JsonResponse(data)


def error(request):
    return render(request, 'error.html')


def chat_list(request):
    return render(request, 'chatList.html')


def forbidden(request):
    return render(request, 'prohibido.html')


def booking(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]

    if (is_active):
        user = CustomUser.objects.get(id=person_id)
        for reserva in json.loads(request.POST.get('key_1_string')):
            product = Product.objects.get(id=reserva['id'])
            shop = product.shop.durationBooking
            now = datetime.now()
            print(now + timedelta(minutes=shop))
            finishBooking = now + timedelta(minutes=shop)
            print(finishBooking)
            b = Booking.objects.create(startDate=now, endDate=finishBooking, product=product,
                                       title='Prueba', quantity=reserva['cantidad'], isAccepted=False, user=user)
            b.save()
            print(type(b.endDate))

        data = {
            'url': "/user/bookings/"
        }
        return JsonResponse(data)
    else:
        data = {
            'url': "/prohibido/"
        }
        return JsonResponse(data)


def review_list(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    shop = get_object_or_404(Shop, pk=id_shop)
    tienda = miTienda(person_id)
    if rol == "User":

        reviews = []
        for m in shop.review_set.all():
            reviews.append(m)
        # a la vista de todas las reviews
        return render(request, 'reviews.html', {'reviews': reviews, 'context': context, 'tienda': tienda})

    if rol == "Owner":
        if(shop.id == tienda.id):
            reviews = []
            for m in tienda.review_set.all():
                reviews.append(m)
            return render(request, 'reviews.html', {'reviews': reviews, 'context': context, 'tienda': tienda})
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})

    else:
        return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})


def review_form(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    shop = get_object_or_404(Shop, pk=id_shop)
    tienda = miTienda(person_id)
    if rol == "User":
        if request.method == 'GET':
            form = ReviewForm()
            # al formulario vacio
            return render(request, 'review.html', {'form': form, 'context': context, 'tienda': tienda})
        if request.method == 'POST':
            form = ReviewForm(data=request.POST)
            if form.is_valid():
                rating = form.cleaned_data['rating']
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                Review.objects.create(rating=rating, title=title, description=description, date=date.today(
                ), user=CustomUser.objects.get(id=rol_id), shop=shop)
                reviews = []
                for m in shop.review_set.all():
                    reviews.append(m)
                # a la vista las reviews de la tienda
                return redirect('../', {'reviews': reviews, 'context': context, 'tienda': tienda})
            else:
                # de vuelta al formulario a rellenarlo correctamente
                return render(request, 'review.html', {'form': form, 'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})


def about(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    return render(request, 'about.html', {"context": context, 'tienda': tienda})


def error_404(request, exception):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    return render(request, 'error.html', {'context': context, "tienda": tienda})


def miTienda(person_id):
    try:
        person = Person.objects.get(id=person_id)
        owner = Owner.objects.get(person=person)
        shop = Shop.objects.get(owner=owner)
    except:
        shop = ''

    return shop

def get_owners(request):
    ''' Muestra un listado con todos los owners que hay registrados.\n
        POST    -> Filtra en función del username \n
        GET     -> Muestra los owners listados.
    '''
    person_id,rol,rol_id,is_active= get_context(request)
    context = [person_id,rol,rol_id,is_active]
    tienda = miTienda(person_id)
    if (is_active):
        if str(rol) == 'Admin':
            if request.method == 'POST': 
                form = UserSearchForm(data=request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    person_list= Person.objects.filter(username__icontains=username)
                    i=0
                    for p in person_list:
                        owners = Owner.objects.filter(person=p)
                        if(i>0):
                            owners = owners | Owner.objects.filter(person=p)
                        i=+1
                        print(owners)
                    return render(request, 'ownerListAdmin.html', {"context" : context, "owners" : owners, 'form': form, 'tienda': tienda})
            else:
                form = UserSearchForm()
                owners = Owner.objects.all()
                print(owners)
                return render(request, 'ownerListAdmin.html', {"context" : context, "owners" : owners, 'form': form, 'tienda': tienda})
        else:
            return render(request,'prohibido.html',{"context" : context, 'tienda': tienda},status=403)
    else:
        return render(request,'prohibido.html',status=403)

def get_users(request):
    ''' Muestra un listado con todos los usuarios que hay registrados.\n
        POST    -> Filtra en función del username \n
        GET     -> Muestra los usuarios registrados en una lista.
    '''
    person_id,rol,rol_id,is_active= get_context(request)
    context = [person_id,rol,rol_id,is_active]
    tienda = miTienda(person_id)
    if (is_active):
        if str(rol) == 'Admin':
            if request.method == 'POST': 
                form = UserSearchForm(data=request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    person_list= Person.objects.filter(username__icontains=username)
                    i=0
                    for p in person_list:
                        users = CustomUser.objects.filter(person=p)
                        if(i>0):
                            users = users | CustomUser.objects.filter(person=p)
                        i=+1
                        print(users)

                    return render(request, 'userListAdmin.html', {"context" : context, "users" : users, 'form': form, 'tienda': tienda})
            else:
                form = UserSearchForm()
                users = CustomUser.objects.all()
                print(users)
                return render(request, 'userListAdmin.html', {"context" : context, "users" : users, 'form': form, 'tienda': tienda})
        else:
            return render(request,'prohibido.html',{"context" : context, 'tienda': tienda},status=403)
    else:
        return render(request,'prohibido.html',status=403)

def get_user(request ,id_user):
    ''' Muestra los datos de un usuario registrado.\n
        POST    -> Suspende la cuenta del usuario en cuestion, o la activa en caso de estarlo \n
        GET     -> Muestra los datos del usuario.
    '''
    person_id,rol,rol_id,is_active= get_context(request)
    context = [person_id,rol,rol_id,is_active]
    tienda = miTienda(person_id)
    if (is_active):
        if str(rol) == 'Admin':
            user = get_object_or_404(CustomUser,pk=id_user)
            # user = CustomUser.objects.filter(id=id_user)
            if request.method == 'POST': 
                form = UserBannedForm(data=request.POST)
                if form.is_valid():
                    isBanned = form.cleaned_data['isBanned'] #Debe pasarse el valor original de isBanned negado
                    print(isBanned)
                    person = user.person
                    person.isBanned = isBanned
                    person.save()
                    print(user.person.isBanned)
                    return render(request, 'userDetailsAdmin.html', {"context" : context, "user" : user, 'form': form, 'tienda': tienda})
            else:
                form = UserBannedForm()
                return render(request, 'userDetailsAdmin.html', {"context" : context, "user" : user, 'form': form, 'tienda': tienda})
        else:
            return render(request,'prohibido.html',{"context" : context, 'tienda': tienda},status=403)
    else:
        return render(request,'prohibido.html',status=403)


def get_owner(request ,id_user):
    ''' Muestra los datos de un owner registrado.\n
        POST    -> Suspende la cuenta del owner en cuestión, o la activa en caso de estarlo \n
        GET     -> Muestra los datos del owner.
    '''
    person_id,rol,rol_id,is_active= get_context(request)
    context = [person_id,rol,rol_id,is_active]
    tienda = miTienda(person_id)
    if (is_active):
        if str(rol) == 'Admin':
            owner = get_object_or_404(Owner,pk=id_user)
            # user = CustomUser.objects.filter(id=id_user)
            if request.method == 'POST': 
                form = UserBannedForm(data=request.POST)
                if form.is_valid():
                    isBanned = form.cleaned_data['isBanned'] #Debe pasarse el valor original de isBanned negado
                    person = owner.person
                    person.isBanned = isBanned
                    person.save()
                    return render(request, 'ownerDetailsAdmin.html', {"context" : context, "owner" : owner, 'form': form, 'tienda': tienda})
            else:
                form = UserBannedForm()
                
                return render(request, 'ownerDetailsAdmin.html', {"context" : context, "owner" : owner, 'form': form, 'tienda': tienda})
        else:
            return render(request,'prohibido.html',{"context" : context, 'tienda': tienda},status=403)
    else:
        return render(request,'prohibido.html',status=403)

def updateShop(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    shop = get_object_or_404(Shop, pk=id_shop)
    tienda = miTienda(person_id)

    if (is_active and rol == "Owner" and str(shop.owner.person.id) == person_id):
        if request.method == 'POST':
            form = FormShop(request.POST)
            if form.is_valid():
                shop.name = form.cleaned_data['name']
                shop.schedule = form.cleaned_data['schedule']
                shop.description = form.cleaned_data['description']
                shop.address = form.cleaned_data['address']
                shop.durationBooking = form.cleaned_data['durationBooking']
            else:
                if request.FILES.get('picture') != None:
                    if request.FILES.get('picture').size > 5000000:
                        msg = 'El tamaño máximo de la imagen no puede superar 5 MB'
                        return render(request, 'shop_edit.html', {'tienda': tienda, 'context': context, 'form': form, 'shop': shop, 'msg': msg})
                    else:
                        shop.picture = request.FILES.get('picture')
                shop.save()
                return redirect('/shops/'+str(shop.id))

        form = FormShop()

    return render(request, 'shop_edit.html', {'tienda': tienda, 'context': context, 'form': form, 'shop': shop})

