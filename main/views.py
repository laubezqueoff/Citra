from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage, ReportReason, Report, Notification
import requests
from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import MessageForm, ReviewForm, UserSearchForm, CustomUserUpdateForm, LoginForm, ShopForm, CustomUserForm,UserBannedForm, ProductForm, FormShop, NameShopForm, ReportForm
from django.http import Http404
import json
from django.http import JsonResponse
from datetime import timedelta
import stripe
from Citra import settings
from django.db import transaction


def login(request):
    '''
    Logea una persona en la aplicación.\n
        POST    -> Lleva la inicio con el contexto actualizado \n
        GET     -> Lleva al formulario de login
    '''
    # msg_success = "Bienvenido a la aplicación"
    msg_error = "El nombre y la contraseña no coinciden"
    msg_error_is_banned = "El usuario esta suspendido"
    if request.method == 'POST':  # Si es un POST redirijimos a la vista de index con el context actualizado

        form = LoginForm(data=request.POST)
        if form.is_valid():
            try:
                # Sacamos el valor de la propiedad 'name' del formulario
                username = form.cleaned_data['username']
                # Sacamos el valor de la propiedad 'password' del formulario
                password = form.cleaned_data['password']
                # Buscamos el usuario por su contraseña y nombre
                person = Person.objects.get(username=username, password=password)
                rol_and_id = whoIsWho(person)

                update_context(request, person.id,
                            rol_and_id[0], rol_and_id[1], True)
                # msg = msg_success

                person_id, rol, rol_id, is_active = get_context(request)
                context = [person_id, rol, rol_id, is_active]

                today = date.today()
                promotions_shops = Promotion.objects.filter(product=None, endDate__gte = today)
                promotions_products = Promotion.objects.filter(shop=None, endDate__gte = today)

                promotions_shops_subscription = {}
                promotions_products_subscription = {}
                for promo in promotions_shops:
                    person = Person.objects.get(id=promo.shop.owner.person.id)
                    if not person.isBanned:
                        sus = Subscription.objects.filter(endDate__gte = today, shop = promo.shop).exists()
                        promotions_shops_subscription[promo] = sus

                for promo in promotions_products:
                    person = Person.objects.get(id=promo.product.shop.owner.person.id)
                    if not person.isBanned:
                        sus = Subscription.objects.filter(endDate__gte = today, shop = promo.product.shop).exists()
                        promotions_products_subscription[promo] = sus

                tienda = miTienda(person_id)
                person = get_object_or_404(Person, pk=person_id)
                if person.isBanned:
                    msg = msg_error_is_banned
                    request.session['person_id']= '0'
                    request.session['rol']= 'Usuario no registrado'
                    request.session['rol_id']= '0'
                    request.session['is_active']= False
                    
                    return render(request, 'login.html', {"msg": msg, 'tienda': ''})
                return render(request, 'home.html', {"context": context, 'promotions_shops_subscription': promotions_shops_subscription, 'promotions_products_subscription': promotions_products_subscription, 'tienda': tienda})
            except:
                # Es importante pasar el context en todas las vistas.
                # Cambiar index.html por tu vista en tu método
                msg = msg_error
                return render(request, 'login.html', {"msg": msg, 'tienda': '','form':form})
        else:
                return render(request, 'login.html',{'form': form})

    else:  # Si es un GET redirijimos a la vista de login
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
        tienda = miTienda(person_id)
        if is_active:
            return redirect('/home')
        else:
            form = LoginForm()
            return render(request, 'login.html', {'tienda': '', 'form':form})

def registerShop(request):

    error_log=["",""]
    shopType = ShopType.objects.all()

    if request.method == 'POST': #Si es un POST redirijimos a la vista de index con el context actualizado  
        form = ShopForm(data=request.POST)
        if form.is_valid():
            try:
                # Parametros tomados del post
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                name = form.cleaned_data['name']
                phoneNumber = form.cleaned_data['phoneNumber']
                zipCode = form.cleaned_data['zipCode']
                email = form.cleaned_data['email']

                error_log,is_wrong_user = assert_username_unique(username,error_log)
                error_log,is_wrong_email = assert_email_unique(email,error_log)

                if(is_wrong_user or is_wrong_email):
                    shopType = ShopType.objects.all()
                    return render(request, 'register_shop.html',{"error_log":error_log,"types":shopType})
                # ParÃ¡metros autogenerados
                registerDate = date.today()
                isBanned = False

                p = Person(username=username, password=password, name=name, phoneNumber=phoneNumber,
                        email=email, zipCode=zipCode, registerDate=registerDate, isBanned=isBanned)
                p.save()


                p = Person.objects.get(username=username,password=password)
                #Assertions
                

                co = Owner(person=p)
                co.save()


                shopName = form.cleaned_data['shopName']
                shopType = form.cleaned_data['select']
                schedule = form.cleaned_data['schedule']
                description = form.cleaned_data['description']
                picture = request.FILES.get('picture')
                address = form.cleaned_data['address']
                durationBooking = form.cleaned_data['durationBooking']
                print(shopName,shopType,schedule,description,address,durationBooking)
                co = Owner.objects.get(person=p)
                shopType = ShopType.objects.get(id=int(shopType))
                shop = Shop.objects.create(name=shopName, shopType=shopType, schedule=schedule, description=description,
                                        picture=picture, address=address, owner=co, durationBooking=durationBooking)

                update_context(request, p.id, "Owner", co.id, True)
                person_id, rol, rol_id, is_active = get_context(request)
                context = [person_id, rol, rol_id, is_active]
                print('llegó')
                return redirect('/home/')

            except:
                print("------------------------------")
                return render(request, 'register_shop.html',{"error":error,'form': form, "types":shopType})
        else:
            return render(request, 'register_shop.html',{'form': form, "types":shopType})
    else:
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
        tienda = miTienda(person_id)
        if is_active:
            return redirect('/home')
        shopType = ShopType.objects.all()
        form = ShopForm()
        return render(request, 'register_shop.html',{'form': form, "types":shopType})


def register(request):
    ''' Logea una persona en la aplicación.\n
        POST    -> Lleva la inicio con el contexto actualizado \n
        GET     -> Lleva al formulario de login
    '''
    # msg_success = "Bienvenido a la aplicación"
    error_log = ["", ""]

    if request.method == 'POST':  # Si es un POST redirijimos a la vista de index con el context actualizado

        form = CustomUserForm(data=request.POST)
        if form.is_valid():
            try:
                # Parametros tomados del post
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                name = form.cleaned_data['name']
                phoneNumber = form.cleaned_data['phoneNumber']
                zipCode = form.cleaned_data['zipCode']
                email = form.cleaned_data['email']

                # Parámetros autogenerados
                registerDate = date.today()
                isBanned = False

                #Assertions
                error_log,is_wrong_user = assert_username_unique(username,error_log)
                error_log,is_wrong_email = assert_email_unique(email,error_log)

                if(is_wrong_user or is_wrong_email):
                    return render(request, 'register_user.html',{"error_log":error_log})

                p = Person(username=username, password=password, name=name, phoneNumber=phoneNumber, email=email, zipCode=zipCode, registerDate=registerDate, isBanned=isBanned)
                p.save()


                p = Person.objects.get(username=username, password=password)

                cu = CustomUser(person=p)
                cu.save()

                rol_and_id = whoIsWho(p)


                update_context(request,p.id,rol_and_id[0],rol_and_id[1],True)
                person_id,rol,rol_id,is_active = get_context(request)
                context = [person_id,rol,rol_id,is_active]
                
                return redirect('/home')

            except:
                return render(request, 'register_user.html',{'form': form})
        else:
            return render(request, 'register_user.html',{'form': form})
    else: #Si es un GET redirijimos a la vista de login
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
        tienda = miTienda(person_id)
        if is_active:
            return redirect('/home')
        return render(request, 'register_user.html')


def updateUser(request):

    error_log = ["", ""]


    if request.method == 'POST': #Si es un POST redirijimos a la vista de index con el context actualizado
        form = CustomUserUpdateForm(data=request.POST)
        if form.is_valid():
            try:
                #Parametros tomados del post
                    #username        =   request.POST['username']             
                    password        =   form.cleaned_data['password']            
                    name            =   form.cleaned_data['name']                
                    phoneNumber     =   form.cleaned_data['phoneNumber'] 
                    zipCode         =   form.cleaned_data['zipCode']              
                    #email           =   request.POST['email']   


                    person_id,rol,rol_id,is_active = get_context(request)

                    p = Person.objects.get(id=person_id)

                    #vamoaver(p,email,username)

                    p.password=password
                    p.name=name
                    p.phoneNumber=int(phoneNumber)
                    p.zipCode=int(zipCode)
                    p.save()

                    context = [person_id,rol,rol_id,is_active]

                    return redirect('/home')


            except:
                person_id, rol, rol_id, is_active = get_context(request)
                context = [person_id,rol,rol_id,is_active]
                p = Person.objects.get(id=person_id)
                return render(request, 'home.html', {"context" : context,"person":p,"editMode":True})
        else:
            person_id, rol, rol_id, is_active = get_context(request)
            context = [person_id, rol, rol_id, is_active]
            p = Person.objects.get(id=person_id)

            tienda = miTienda(person_id)
            return render(request, 'register_user.html',{"context" : context,"person":p,'form': form,"editMode":True, 'tienda': tienda})
    else: #Si es un GET redirijimos a la vista de login


        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
        p = Person.objects.get(id=person_id)
        tienda = miTienda(person_id)

        form = CustomUserUpdateForm()
        
        return render(request, 'register_user.html',{'form': form, "context" : context,"person":p,"editMode":True, 'tienda': tienda})


        return render(request, 'register_user.html', {"context": context, "person": p, "editMode": True, 'tienda': tienda})


def assert_email_unique(email, error_log):

    p = Person.objects.filter(email=email).exists()
    print(p)
    is_wrong = p

    if p:
        error_msg = "Este email ya se encuentra en uso, introduce uno nuevo."
        error_log[0] = error_msg
    else:
        error_msg = ""
        error_log[0] = error_msg

    return error_log, is_wrong


def assert_username_unique(username, error_log):

    p = Person.objects.filter(username=username).exists()

    is_wrong = p

    if p:
        error_msg = "Este username ya se encuentra en uso, introduce uno nuevo."
        error_log[1] = error_msg
    else:
        error_msg = ""
        error_log[1] = error_msg

    return error_log, is_wrong


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

        today = date.today()
        promotions_shops = Promotion.objects.filter(
            product=None, endDate__gte=today)
        promotions_products = Promotion.objects.filter(
            shop=None, endDate__gte=today)

        promotions_shops_subscription = {}
        promotions_products_subscription = {}
        for promo in promotions_shops:
            person = Person.objects.get(id=promo.shop.owner.person.id)
            if not person.isBanned:
                sus = Subscription.objects.filter(endDate__gte = today, shop = promo.shop).exists()
                promotions_shops_subscription[promo] = sus

        for promo in promotions_products:
            person = Person.objects.get(id=promo.product.shop.owner.person.id)
            if not person.isBanned:
                sus = Subscription.objects.filter(endDate__gte = today, shop = promo.product.shop).exists()
                promotions_products_subscription[promo] = sus

        return render(request, 'home.html', {'promotions_shops_subscription': promotions_shops_subscription, 'promotions_products_subscription': promotions_products_subscription})


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
        try:
            product = get_object_or_404(Product, pk=id_product)
        except:
             return render(request, 'error.html',{'context': context, 'tienda': tienda}, status=404)
       
        time = date.today()

        product = get_object_or_404(Product, pk=id_product)
        sus = Subscription.objects.filter(
            endDate__gte=time, shop=product.shop).exists()

        promotion = Promotion.objects.filter(product=product).exists()
        promotionweek = Promotion.objects.filter(
            endDate__gte=time, product=product).exists()
        if (not(promotion) and str(product.shop.owner.person.id) == person_id and sus and request.method == 'POST'):
            promotionType = PromotionType.objects.get(id=0)  # semanal
            owner = Owner.objects.get(person=person_id)
            time = date.today()
            endtime = (time + timedelta(days=7))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=300, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.create(
                owner=owner, shop=None, startDate=time, endDate=endtime, promotionType=promotionType, product=product)
            
            Notification.objects.create(title="Producto promocionado con éxito", description="El producto " + product.name + " estará promocionado hasta el dia " + endtime.strftime("%d/%m/%Y"),
                person=person)
            return redirect("home")
        elif (promotion and str(product.shop.owner.person.id) == person_id and sus and not promotionweek and request.method == 'POST'):
            time = date.today()
            endtime = (time + timedelta(days=7))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=300, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.filter(product = product).update(startDate=time, endDate=endtime)
            Notification.objects.create(title="Producto promocionado con éxito", description="El producto " + product.name + " estará promocionado hasta el dia " + endtime.strftime("%d/%m/%Y"),
                person=person)
            return redirect("home")
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda}, status=403)
    else:
        return render(request, 'prohibido.html')


def promotion_month_product(request, id_product):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        try:
            product = get_object_or_404(Product, pk=id_product)
        except:
             return render(request, 'error.html',{'context': context, 'tienda': tienda}, status=404)
        promotion = Promotion.objects.filter(product=product).exists()
        time = date.today()
        sus = Subscription.objects.filter(
            endDate__gte=time, shop=product.shop).exists()
        promotionmonth = Promotion.objects.filter(
            endDate__gte=time, product=product).exists()
        if (not(promotion) and str(product.shop.owner.person.id) == person_id and sus and request.method == 'POST'):
            promotionType = PromotionType.objects.get(id=1)  # mensual
            owner = Owner.objects.get(person=person_id)
            time = date.today()
            endtime = (time + timedelta(days=30))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=500, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.create(
                owner=owner, shop=None, startDate=time, endDate=endtime, promotionType=promotionType, product=product)
            Notification.objects.create(title="Producto promocionado con éxito", description="El producto " + product.name + " estará promocionado hasta el dia " + endtime.strftime("%d/%m/%Y"),
                person=person)
            return redirect("home")
        elif (promotion and str(product.shop.owner.person.id) == person_id and sus and not promotionmonth and request.method == 'POST'):
            time = date.today()
            endtime = (time + timedelta(days=30))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=500, source=request.POST.get('stripeToken'))
            promocion = Promotion.objects.filter(product = product).update(startDate=time, endDate=endtime)
            Notification.objects.create(title="Producto promocionado con éxito", description="El producto " + product.name + " estará promocionado hasta el dia " + endtime.strftime("%d/%m/%Y"),
                person=person)
            return redirect("home")
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda}, status=403)
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
        threadName = thread.name
        forumMessages = []
        for m in thread.forummessage_set.all():
            forumMessages.append(m)
        if request.method == 'POST':
            form = MessageForm(data=request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                ForumMessage.objects.create(text=text, date=date.today(
                ), thread=thread, user=CustomUser.objects.get(id=rol_id))
                return redirect("/threads/"+id_thread)
            else:
                return render(request, 'thread.html', {'form':form, 'forumMessages': forumMessages, 'threadName': threadName, 'context': context, 'tienda': tienda})
        else:
            form= MessageForm()
            return render(request, 'thread.html', {'form':form, 'forumMessages': forumMessages, 'threadName': threadName, 'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})


def promotion_week_shop(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    time = date.today()
    if (is_active):
        try:
            shop = get_object_or_404(Shop, pk=id_shop)
        except:
             return render(request, 'error.html',{'context': context, 'tienda': tienda}, status=404)
        time = date.today()

        sus = Subscription.objects.filter(endDate__gte = time,shop=shop).exists()
        promotion = Promotion.objects.filter(shop=shop).exists()
        promotionweek = Promotion.objects.filter(endDate__gte = time,shop=shop).exists()
        if (str(shop.owner.person.id) == person_id):
            if(request.method == 'POST'and sus):
                if (not(promotion)):
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
                elif (promotion and not promotionweek):
                    time = date.today()
                    endtime = (time + timedelta(days=7))
                    person = Person.objects.get(id=person_id)
                    get_or_create_customer(email=person.email, source=None)
                    charge(amount=500, source=request.POST.get('stripeToken'))
                    promocion = Promotion.objects.filter(shop = shop).update(startDate=time, endDate=endtime)
                    return redirect("home")
                else:
                    print("existe")
                    return render(request, 'prohibido.html',{'context': context, 'tienda': tienda}, status=403)
            else:
                return render(request, 'prohibido.html',{'context': context, 'tienda': tienda}, status=403)

        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')


def promotion_month_shop(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    time = date.today()
    if (is_active):

        try:
            shop = get_object_or_404(Shop, pk=id_shop)
        except:
             return render(request, 'error.html',{'context': context, 'tienda': tienda}, status=404)
        sus = Subscription.objects.filter(endDate__gte = time,shop=shop).exists()
        promotion = Promotion.objects.filter(shop=shop).exists()
        time = date.today()
        promotionmonth = Promotion.objects.filter(endDate__gte = time, shop=shop).exists()
        if (str(shop.owner.person.id) == person_id):
            if(request.method == 'POST' and sus):
                if (not(promotion)):
                    print("nueva mensual")
                    promotionType = PromotionType.objects.get(id=1)
                    owner = Owner.objects.get(person=person_id)
                    time = date.today()
                    endtime = (time + timedelta(days=30))
                    person = Person.objects.get(id=person_id)
                    get_or_create_customer(email=person.email, source=None)
                    charge(amount=1000, source=request.POST.get('stripeToken'))
                    promocion = Promotion.objects.create(
                        owner=owner, shop=shop, startDate=time, endDate=endtime, promotionType=promotionType, product=None)
                    return redirect("home")
                elif (promotion and not promotionmonth):
                    print("actualiza mensual")
                    time = date.today()
                    endtime = (time + timedelta(days=30))
                    person = Person.objects.get(id=person_id)
                    get_or_create_customer(email=person.email, source=None)
                    charge(amount=1000, source=request.POST.get('stripeToken'))
                    promocion = Promotion.objects.filter(shop = shop).update(startDate=time, endDate=endtime)
                    return redirect("home")
                else:
                    print("existe")
                    return render(request, 'prohibido.html',{'context': context, 'tienda': tienda}, status=403)
            else:
                return render(request, 'prohibido.html',{'context': context, 'tienda': tienda}, status=403)

        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda}, status=403)
    else:
        return render(request, 'prohibido.html')


def activate_shop(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        try:
            shop = get_object_or_404(Shop, pk=id_shop)
        except:
             return render(request, 'error.html',{'context': context, 'tienda': tienda}, status=404)
        subscription = Subscription.objects.filter(shop=shop).exists()
        time = date.today()
        activate = Subscription.objects.filter(endDate__gte = time).exists()
        if (str(shop.owner.person.id) == person_id):
            if(request.method == 'POST'):
                if (not(subscription)):
                    print("no suscrita")
                    subscriptionType = SubscriptionType.objects.get(id=0)
                    owner = Owner.objects.get(person=person_id)
                    time = date.today()
                    endtime = (time + timedelta(days=30))
                    person = Person.objects.get(id=person_id)
                    get_or_create_customer(email=person.email, source=None)
                    charge(amount=1000, source=request.POST.get('stripeToken'))
                    suscripcion = Subscription.objects.create(
                        subscriptionType=subscriptionType, startDate=time, endDate=endtime, owner=owner, shop=shop)
                    return redirect("home")
                elif (subscription and not activate):
                    print(update)
                    time = date.today()
                    endtime = (time + timedelta(days=30))
                    person = Person.objects.get(id=person_id)
                    get_or_create_customer(email=person.email, source=None)
                    charge(amount=1000, source=request.POST.get('stripeToken'))
                    promocion = Subscription.objects.filter(shop = shop).update(startDate=time, endDate=endtime)
                    return redirect("home")
                else:
                    print("existe")
                    return render(request, 'prohibido.html',{'context': context, 'tienda': tienda}, status=403)
            else:
                return render(request, 'prohibido.html',{'context': context, 'tienda': tienda}, status=403)
        else:
            return render(request, 'prohibido.html',{'context': context, 'tienda': tienda}, status=403)
    else:
        return render(request, 'prohibido.html')



def activate_shop_three_months(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        try:
            shop = get_object_or_404(Shop, pk=id_shop)
        except:
             return render(request, 'error.html',{'context': context, 'tienda': tienda}, status=404)
        subscription = Subscription.objects.filter(shop=shop).exists()
        time = date.today()
        activate = Subscription.objects.filter(endDate__gte=time).exists()
        if (not(subscription) and str(shop.owner.person.id) == person_id and request.method == 'POST'):
            subscriptionType = SubscriptionType.objects.get(id=0)
            owner = Owner.objects.get(person=person_id)
            time = date.today()
            endtime = (time + timedelta(days=90))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=1000, source=request.POST.get('stripeToken'))
            suscripcion = Subscription.objects.create(
                subscriptionType=subscriptionType, startDate=time, endDate=endtime, owner=owner, shop=shop)
            Notification.objects.create(title="Tienda dada de alta", description="La tienda " + shop.name + " estará activa hasta el dia " + endtime.strftime("%d/%m/%Y"),
                person=person)
            return redirect("home")
        elif (subscription and str(shop.owner.person.id) == person_id and not activate and request.method == 'POST'):
            time = date.today()
            endtime = (time + timedelta(days=30))
            person = Person.objects.get(id=person_id)
            get_or_create_customer(email=person.email, source=None)
            charge(amount=1000, source=request.POST.get('stripeToken'))
            promocion = Subscription.objects.filter(shop = shop).update(startDate=time, endDate=endtime)
            Notification.objects.create(title="Tienda dada de alta", description="La tienda " + shop.name + " estará activa hasta el dia " + endtime.strftime("%d/%m/%Y"),
                person=person)
            return redirect("home")
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda}, status=403)
    else:
        return render(request, 'prohibido.html')

def activate_shop_one_year(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        try:
            shop = get_object_or_404(Shop, pk=id_shop)
        except:
             return render(request, 'error.html',{'context': context, 'tienda': tienda}, status=404)
        subscription = Subscription.objects.filter(shop=shop).exists()
        time = date.today()
        activate = Subscription.objects.filter(endDate__gte = time).exists()
        if (str(shop.owner.person.id) == person_id):
            if(request.method == 'POST'):
                if (not(subscription)):
                    subscriptionType = SubscriptionType.objects.get(id=0)
                    owner = Owner.objects.get(person=person_id)
                    time = date.today()
                    endtime = (time + timedelta(days=365))
                    person = Person.objects.get(id=person_id)
                    get_or_create_customer(email=person.email, source=None)
                    charge(amount=1000, source=request.POST.get('stripeToken'))
                    suscripcion = Subscription.objects.create(
                        subscriptionType=subscriptionType, startDate=time, endDate=endtime, owner=owner, shop=shop)
                    return redirect("home")
                elif (subscription and not activate ):
                    time = date.today()
                    endtime = (time + timedelta(days=30))
                    person = Person.objects.get(id=person_id)
                    get_or_create_customer(email=person.email, source=None)
                    charge(amount=1000, source=request.POST.get('stripeToken'))
                    promocion = Subscription.objects.filter(shop = shop).update(startDate=time, endDate=endtime)
                    return redirect("home")
                else:
                    print("existe")
                    return render(request, 'prohibido.html',{'context': context, 'tienda': tienda}, status=403)
            else:
                return render(request, 'prohibido.html',{'context': context, 'tienda': tienda}, status=403)
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda}, status=403)
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
                    product = Product.objects.create(name=form.cleaned_data['name'], price=price, description=form.cleaned_data['description'], productType=ProductType.objects.get(
                        id=form.cleaned_data['select']), picture=picture, shop=shop)
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
        return render(request, 'prohibido.html', {"context": context, 'tienda': tienda}, status=403)


def product_delete(request, id_product):
    product = get_object_or_404(Product, pk=id_product)
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
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
        return JsonResponse(data, status=403)


def product_details(request, id_product):
    product = get_object_or_404(Product, pk=id_product)
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    today = date.today()
    promotionProduct = Promotion.objects.filter(
        product=product, endDate__gte=today).exists()
    tienda = miTienda(person_id)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if  str(product.shop.owner.person.id) == person_id:
            if form.is_valid():
                product.name = form.cleaned_data['name']
                product.price = form.cleaned_data['price']
                product.description = form.cleaned_data['description']
                product.productType = ProductType.objects.get(
                    name=request.POST['select'])
                if request.FILES.get('picture') != None:
                    if request.FILES.get('picture').size > 5000000:
                        msg = 'El tamaño máximo de la imagen no puede superar 5 MB'
                        types = ProductType.objects.all()
                        productType = []
                        for ty in types:
                            productType.append(ty)
                        return render(request, 'products.html', {'form': form, 'product': product, 'types': productType, "context": context, "promotionProduct": not(promotionProduct), 'tienda': tienda, 'msg': msg})
                    else:
                        product.picture = request.FILES.get('picture')
                product.save()
                return redirect('/shops/'+str(product.shop.id))
            else:
                types = ProductType.objects.all()
                productType = []
                for ty in types:
                    productType.append(ty)
                return render(request, 'products.html', {'form': form, 'product': product, 'types': productType, "context": context, "promotionProduct": not(promotionProduct), 'tienda': tienda})
        else:
            return render(request, 'prohibido.html', {"context": context, 'tienda': tienda}, status=403)

    form = ProductForm()
    types = ProductType.objects.all()
    productType = []
    for ty in types:
        productType.append(ty)
    sus = Subscription.objects.filter(
        endDate__gte=today, shop=product.shop).exists()
    return render(request, 'products.html', {'stripe_key': settings.STRIPE_PUBLISHABLE_KEY, 'form': form, 'product': product, 'types': productType, "context": context, "promotionProduct": not(promotionProduct), 'tienda': tienda, 'sus': sus})


def list_shop(request):
    today = date.today()
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    shops = Shop.objects.all()
    shop_subscription = {}
    for promo in shops:
        person = Person.objects.get(id=promo.owner.person.id)
        if not person.isBanned:
            a = Subscription.objects.filter(endDate__gte = today, shop = promo).exists()
            shop_subscription[promo] = a
    tienda = miTienda(person_id)
    return render(request, 'shops.html', {'shop_subscription': shop_subscription, 'context': context, 'tienda': tienda})


def shop_details(request, id_shop):
    shop = get_object_or_404(Shop, pk=id_shop)
    products = Product.objects.filter(shop=shop)
    today = date.today()
    promotionShop = Promotion.objects.filter(
        shop=shop, endDate__gte=today).exists()
    subscriptionShop = Subscription.objects.filter(
        shop=shop, endDate__gte=today).exists()
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
        print('Chats de usuario logeado con otras tiendas')
        chats = Chat.objects.filter(
            user=get_object_or_404(CustomUser, pk=rol_id))

    elif rol == 'Owner':
        print('Chats de owner logeado con usuarios')

        shops = Shop.objects.filter(
            owner=get_object_or_404(Owner, pk=rol_id))
        i = 0
        for s in shops:
            if i == 0:
                chats = Chat.objects.filter(shop=s)
            else:
                chats = chats | Chat.objects.filter(shop=s)

            i += 1
    else:
        print('Es admin o no está logeado, por lo tanto no tiene acceso a chats')
        return render(request, 'prohibido.html', {"context": context, 'tienda': tienda}, status=403)

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
        try:
            chat = get_object_or_404(Chat, pk=id_chat)
        except:
            print('No existe el chat')
            return render(request, 'error.html', {"context": context, 'tienda': tienda}, status=404)
        # TODO: if para comprobar que el usuario forma parte de ese chat
        if str(rol) == 'User':
            if not (int(chat.user.id) == int(rol_id)):
                return render(request, 'prohibido.html', {"context": context, 'tienda': tienda}, status=403)
        elif str(rol) == 'Owner':
            if not(int(chat.shop.owner.id) == int(rol_id)):
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
                if isSentByUser:
                    Notification.objects.create(title="Un usuario te ha mandado un mensaje", description="El usuario " + chat.user.person.name + " quiere hablar contigo",
                        person=shop.owner.person)
                else:
                    Notification.objects.create(title="Una tienda te ha respondido", description="La tienda " + shop.owner.person.name + " te ha respondido",
                        person=chat.user.person)
                ChatMessage.objects.create(
                    text=text, chat=chat, date=date.today(), isSentByUser=isSentByUser).save()
                return redirect('/shop/chat/'+str(chat.id))
            else:
                chat_message = ChatMessage.objects.filter(chat=chat)
                return render(request, 'chat.html', {"context": context, "messages": chat_message, 'form': form, 'tienda': tienda, 'shop': chat.shop, 'user': chat.user})
        chat_message = ChatMessage.objects.filter(chat=chat)
        form = MessageForm()
        return render(request, 'chat.html', {"context": context, "messages": chat_message, 'form': form, 'tienda': tienda, 'shop': chat.shop, 'user': chat.user})
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
    if rol == 'Admin' or rol == 'Owner':
        return render(request, 'prohibido.html', {"context": context, 'tienda': tienda}, status=403)
    if rol != 'User':
        print('No está logeado')
        return render(request, 'prohibido.html', {"context": context, 'tienda': tienda}, status=403)
    try:
        shop = get_object_or_404(Shop, pk=id_shop)
    except:
        print('No existe la tienda')
        return render(request, 'error.html', {"context": context, 'tienda': tienda}, status=404)
    user = get_object_or_404(CustomUser, pk=rol_id)
    try:
        chat = Chat.objects.filter(shop=shop, user=user)[0]
    except:
        chat = None
    if chat != None:
        return redirect('/shop/chat/'+str(chat.id))
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            newChat = Chat.objects.create(shop=shop, user=user)
            newChat.save()
            isSentByUser = False
            if rol == 'User':
                isSentByUser = True
            ChatMessage.objects.create(
                text=text, chat=newChat, date=date.today(), isSentByUser=isSentByUser).save()

            Notification.objects.create(title="Un usuario te ha mandado un mensaje", description="El usuario " + user.person.name + " quiere hablar contigo",
                person=shop.owner.person)
                
            return redirect('/shop/chat/'+str(newChat.pk))
        else:
            chat_message = []
            return render(request, 'chat.html', {"context": context, "messages": chat_message, 'form': form, 'shop_id': id_shop, 'tienda': tienda})

    chat_message = []
    form = MessageForm()
    return render(request, 'chat.html', {"context": context, "messages": chat_message, 'form': form, 'shop_id': id_shop, 'tienda': tienda})


def search_shop(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    today = date.today()
    if request.method == 'POST':
        form = NameShopForm(data=request.POST)
        if form.is_valid():
            shop_name = form.cleaned_data['shop_name']
            shops = Shop.objects.filter(name__contains=shop_name)
            shopType = ShopType.objects.all()
            shop_subscription = {}
            for promo in shops:
                person = Person.objects.get(id=promo.owner.person.id)
                if not person.isBanned:
                    a = Subscription.objects.filter(
                        endDate__gte=today, shop=promo).exists()
                    shop_subscription[promo] = a
            return render(request, 'search_shop.html', {'context': context, 'tienda': tienda, 'shop_subscription': shop_subscription, 'shopType': shopType, "shop_name": shop_name})

    form = NameShopForm()
    shops = Shop.objects.all()
    shopType = ShopType.objects.all()
    shop_subscription = {}
    for promo in shops:
        person = Person.objects.get(id=promo.owner.person.id)
        if not person.isBanned:
            a = Subscription.objects.filter(
                endDate__gte=today, shop=promo).exists()
            shop_subscription[promo] = a
    return render(request, 'search_shop.html', {'context': context, 'tienda': tienda, 'shop_subscription': shop_subscription, 'shopType': shopType, "shop_name": ''})


def home(request):
    today = date.today()
    promotions_shops = Promotion.objects.filter(
        product=None, endDate__gte=today)
    promotions_products = Promotion.objects.filter(
        shop=None, endDate__gte=today)
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    promotions_shops_subscription = {}
    promotions_products_subscription = {}
    for promo in promotions_shops:
        person = Person.objects.get(id=promo.shop.owner.person.id)
        if not person.isBanned:
            sus = Subscription.objects.filter(
                endDate__gte=today, shop=promo.shop).exists()
            promotions_shops_subscription[promo] = sus

    for promo in promotions_products:
        person = Person.objects.get(id=promo.product.shop.owner.person.id)
        if not person.isBanned:
            sus = Subscription.objects.filter(
                endDate__gte=today, shop=promo.product.shop).exists()
            promotions_products_subscription[promo] = sus

    return render(request, 'shop_prueba.html', {"context": context, 'promotions_shops_subscription': promotions_shops_subscription, 'promotions_products_subscription': promotions_products_subscription, 'tienda': tienda})


def list_booking_user(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        user = CustomUser.objects.get(id=rol_id)
        bookings = Booking.objects.filter(user=user).filter(isAccepted=True)
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
        owner = Owner.objects.get(id=rol_id)
      #  bookings = Booking.objects.filter(isAccepted=False)
        bookings = Booking.objects.all()

        factoresConfianza = {}
        for book in bookings:
            if book.product.shop.owner.id == owner.id:
                factoresConfianza[book] = factor_confianza(book.user.id)
        return render(request, 'bookings_owner.html', {'context': context, 'tienda': tienda, 'factoresConfianza': factoresConfianza})
    else:
        return render(request, 'prohibido.html')


def accept_booking(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    dur = tienda.durationBooking
    now = datetime.now()
    finishBooking = now + timedelta(hours=dur)
    booking = Booking.objects.filter(
        id=request.POST.get('id')).update(isAccepted=True, endDate=finishBooking)
    data = {
        'url': "/shop/bookings/"
    }
    return JsonResponse(data)


def delete_booking(request):

    booking = Booking.objects.filter(
        id=request.POST.get('id')).delete()
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

@transaction.atomic
def booking(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]

    if is_active:
        user = CustomUser.objects.get(id=rol_id)
        for reserva in json.loads(request.POST.get('key_1_string')):
            product = Product.objects.get(id=reserva['id'])
            person = Person.objects.get(id=product.shop.owner.person.id)
            if not person.isBanned:
                data = {
                    'url': "/error/"
                }
                return JsonResponse(data)
            shop = product.shop.durationBooking
            now = datetime.now()
            finishBooking = now + timedelta(hours=shop)
            b = Booking.objects.create(startDate=now, endDate=finishBooking, product=product,
                                       title='Prueba', quantity=reserva['cantidad'], isAccepted=False, user=user)
            b.save()
            Notification.objects.create(title="Te han hecho una reserva", description="El producto " + product.name + " ha sido reservado por " + user.person.name
            + ". La reserva estará activa hasta " + finishBooking.strftime("%d/%m/%Y, %H:%M:%S"),
                person=product.shop.owner.person)
            Notification.objects.create(title="Has reservado un producto", description="El producto " + product.name + " de la tienda " + product.shop.name + 
            " estará reservado hasta " + finishBooking.strftime("%d/%m/%Y, %H:%M:%S"), person=user.person)
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
    sus = Subscription.objects.get(shop=shop).exists()
    if rol == "User" and sus:

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
    person = Person.objects.get(id=shop.owner.person.id)
    sus = Subscription.objects.get(shop=shop).exists()
    if person.isBanned or not(sus):
        return render(request, 'error.html', {'context': context, 'tienda': tienda})
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
    return render(request, 'error.html', {'context': context, "tienda": tienda}, status=404)


def miTienda(person_id):
    try:
        person = Person.objects.get(id=person_id)
        owner = Owner.objects.get(person=person)
        shop = Shop.objects.get(owner=owner)
    except:
        shop = ''

    return shop


def report_shop_form(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    shop = get_object_or_404(Shop, pk=id_shop)
    reportReason = ReportReason.objects.all()

    person = Person.objects.get(id=shop.owner.person.id)
    if person.isBanned:
        return render(request, 'error.html', {'context': context})

    if rol == "User":
        if request.method == 'GET':
            form = ReportForm()
            return render(request, 'report.html', {'form':form, 'context':context, 'reportReason' : reportReason})
        if request.method == 'POST':  
            owner = Owner.objects.get(id = shop.owner.id)
            id_reported_person = owner.person.id

            form = ReportForm(data=request.POST)

            if form.is_valid():
                title = form['title'].data
                description = form['description'].data
                Report.objects.create(title = title, description = description, person = Person.objects.get(id=id_reported_person))
                return redirect('/shops/'+str(shop.id))
            else:
                return render(request, 'report.html', {'form':form, 'context':context, 'reportReason' : reportReason})


    else:
        return render(request, 'prohibido.html', {'context': context})


def report_user_form(request, id_booking):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    booking = get_object_or_404(Booking, pk=id_booking)
    tienda = miTienda(person_id)
    reportReason = ReportReason.objects.all()

    if rol == "Owner":
        if request.method == 'GET':
            form = ReportForm()
            return render(request, 'report.html', {'form': form, 'context': context, 'reportReason': reportReason, 'tienda': tienda})

        if request.method == 'POST':

            user = CustomUser.objects.get(id=booking.user.id)
            id_reported_person = user.person.id

            form = ReportForm(data=request.POST)

            if form.is_valid():
                title = form['title'].data
                description = form['description'].data
                Report.objects.create(title = title, description = description, person = Person.objects.get(id=id_reported_person))
                return redirect('/shop/bookings/')
            else:
                return render(request, 'report.html', {'form':form, 'context':context, 'reportReason' : reportReason})


    else:
        return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})


def report_from_chat_form(request, id_chat):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    chat = get_object_or_404(Chat, pk=id_chat)
    reportReason = ReportReason.objects.all()
    tienda = miTienda(person_id)
    person = Person.objects.get(id=chat.shop.owner.person.id)
    if person.isBanned:
        return render(request, 'error.html', {'context': context, 'tienda': tienda})
    if request.method == 'GET':
        form = ReportForm()
        return render(request, 'report.html', {'form': form, 'context': context, 'reportReason': reportReason, 'tienda': tienda})

    if request.method == 'POST':

        if rol == "User":
            shop = Shop.objects.get(id=chat.shop.id)
            owner = Owner.objects.get(id=shop.owner.id)
            reported_person = owner.person
        elif rol == "Owner":
            user = CustomUser.objects.get(id=chat.user.id)
            reported_person = user.person
        else:
            return render(request, 'prohibido.html', {'context': context, 'tienda': tienda})

        form = ReportForm(data=request.POST)

        if form.is_valid():
            title = form['title'].data
            description = form['description'].data
            Report.objects.create(title = title, description = description, person = reported_person)
            return redirect('/shop/chat/' + str(chat.id))
        else:
            return render(request, 'report.html', {'form':form, 'context':context, 'reportReason' : reportReason})



# 0: Datos insuficientes, 1: Poco fiable, 2: Medianamente fiable, 3: Cliente fiable
def factor_confianza(id_user):
    res = 0
    user = CustomUser.objects.get(id=id_user)
    npedidos = Booking.objects.filter(user=user, isAccepted=True).count()
    if(npedidos > 4):
        nreportes = Report.objects.filter(
            person=Person.objects.get(id=user.person.id)).count()
        if (nreportes == 0):
            res = 3
        elif(nreportes < 5):
            res = 2
        else:
            res = 1
    return res


def get_owners(request):
    ''' Muestra un listado con todos los owners que hay registrados.\n
        POST    -> Filtra en función del username \n
        GET     -> Muestra los owners listados.
    '''
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        if str(rol) == 'Admin':
            if request.method == 'POST':
                form = UserSearchForm(data=request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    person_list = Person.objects.filter(
                        username__icontains=username)
                    i = 0
                    if len(person_list) > 0:
                        for p in person_list:
                            owners = Owner.objects.filter(person=p)
                            if(i > 0):
                                owners = owners | Owner.objects.filter(
                                    person=p)
                            i = +1
                    else:
                        owners = []


                    print('Método post exitoso, get_owners')
                    return render(request, 'ownerListAdmin.html', {"context" : context, "owners" : owners, 'form': form, 'tienda': tienda})

                else:
                    print('Error en el formulario')
                    form = UserSearchForm()
                    owners = Owner.objects.all()
                    return render(request, 'ownerListAdmin.html', {"context": context, "owners": owners, 'form': form, 'tienda': tienda})
            else:
                print('Método get exitoso, get_owners')
                form = UserSearchForm()
                owners = Owner.objects.all()
                return render(request, 'ownerListAdmin.html', {"context": context, "owners": owners, 'form': form, 'tienda': tienda})
        else:

            print('No está logueado como Admin')
            return render(request,'prohibido.html',{"context" : context, 'tienda': tienda},status=403)
    else:
        print('No está logueado')
        return render(request,'prohibido.html',status=403)


def get_users(request):
    ''' Muestra un listado con todos los usuarios que hay registrados.\n
        POST    -> Filtra en función del username \n
        GET     -> Muestra los usuarios registrados en una lista.
    '''
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        if str(rol) == 'Admin':
            if request.method == 'POST':
                form = UserSearchForm(data=request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    person_list = Person.objects.filter(
                        username__icontains=username)
                    i = 0
                    if len(person_list) > 0:
                        for p in person_list:
                            users = CustomUser.objects.filter(person=p)
                            if(i > 0):
                                users = users | CustomUser.objects.filter(
                                    person=p)
                            i = +1
                    else:
                        users = []

                    print('Método post exitoso, get_users')
                    return render(request, 'userListAdmin.html', {"context" : context, "users" : users, 'form': form, 'tienda': tienda})

                else:
                    print('Error en el formulario')
                    users = CustomUser.objects.all()
                    return render(request, 'userListAdmin.html', {"context": context, "users": users, 'form': form, 'tienda': tienda})
            else:
                print('Método get exitoso, get_users')
                form = UserSearchForm()
                users = CustomUser.objects.all()
                return render(request, 'userListAdmin.html', {"context": context, "users": users, 'form': form, 'tienda': tienda})
        else:

            print('No está logueado como Admin')
            return render(request,'prohibido.html',{"context" : context, 'tienda': tienda},status=403)
    else:
        print('No está logueado')
        return render(request,'prohibido.html',status=403)


def get_user(request, id_user):
    ''' Muestra los datos de un usuario registrado.\n
        POST    -> Suspende la cuenta del usuario en cuestion, o la activa en caso de estarlo \n
        GET     -> Muestra los datos del usuario.
    '''
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        if str(rol) == 'Admin':

            try:
                user = get_object_or_404(CustomUser,pk=id_user)
            except:
                print('No existe el user')
                return render(request, 'error.html', {"context": context, 'tienda': tienda}, status=404)
            if request.method == 'POST': 

                form = UserBannedForm(data=request.POST)
                if form.is_valid():
                    # Debe pasarse el valor original de isBanned negado
                    isBanned = form.cleaned_data['isBanned']
                    person = user.person
                    person.isBanned = isBanned
                    person.save()
                    reports = Report.objects.filter(person=user.person)

                    print('Método post exitoso, get_user')
                    return render(request, 'userDetailsAdmin.html', {"context" : context, "user" : user, 'form': form, 'tienda': tienda, 'reports': reports})

            else:
                print('Método get exitoso, get_user')
                form = UserBannedForm()
                reports = Report.objects.filter(person=user.person)
                return render(request, 'userDetailsAdmin.html', {"context": context, "user": user, 'form': form, 'tienda': tienda, 'reports': reports})
        else:

            print('No esta logueado como Admin')
            return render(request,'prohibido.html',{"context" : context, 'tienda': tienda},status=403)
    else:
        print('No esta logueado')
        return render(request,'prohibido.html',status=403)



def get_owner(request, id_user):
    ''' Muestra los datos de un owner registrado.\n
        POST    -> Suspende la cuenta del owner en cuestión, o la activa en caso de estarlo \n
        GET     -> Muestra los datos del owner.
    '''
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if (is_active):
        if str(rol) == 'Admin':

            try:
                owner = get_object_or_404(Owner,pk=id_user)
            except:
                print('No existe el owner')
                return render(request, 'error.html', {"context": context, 'tienda': tienda}, status=404)
            if request.method == 'POST': 

                form = UserBannedForm(data=request.POST)
                if form.is_valid():
                    # Debe pasarse el valor original de isBanned negado
                    isBanned = form.cleaned_data['isBanned']
                    person = owner.person
                    person.isBanned = isBanned
                    person.save()
                    reports = Report.objects.filter(person=owner.person)

                    print('Método post exitoso, get_owner')
                    return render(request, 'ownerDetailsAdmin.html', {"context" : context, "owner" : owner, 'form': form, 'tienda': tienda, 'reports': reports})

            else:
                print('Método get exitoso, get_owner')
                form = UserBannedForm()
                reports = Report.objects.filter(person=owner.person)
                return render(request, 'ownerDetailsAdmin.html', {"context": context, "owner": owner, 'form': form, 'tienda': tienda, 'reports': reports})
        else:

            print('No esta logueado como Admin')
            return render(request,'prohibido.html',{"context" : context, 'tienda': tienda},status=403)
    else:
        print('No esta logueado')
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
                if request.FILES.get('picture') != None:
                    if request.FILES.get('picture').size > 5000000:
                        msg = 'El tamaño máximo de la imagen no puede superar 5 MB'
                        return render(request, 'shop_edit.html', {'tienda': tienda, 'context': context, 'form': form, 'shop': shop, 'msg': msg})
                    else:
                        shop.picture = request.FILES.get('picture')
                shop.save()
                return redirect('/shops/'+str(shop.id))
            else:
                return render(request, 'shop_edit.html', {'tienda': tienda, 'context': context, 'form': form, 'shop': shop})

        form = FormShop()
        
        return render(request, 'shop_edit.html', {'tienda': tienda, 'context': context, 'form': form, 'shop': shop})
    else:
        return render(request, 'prohibido.html', {'tienda': tienda, 'context': context, 'shop': shop}, status=403)

def GDPR(request):
    return render(request, 'GDPR.html')
    
def notificationList(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if is_active:
        person = Person.objects.get(id=person_id)
        notifications = Notification.objects.filter(person=person).order_by('-id')
        return render(request, "notification_list.html", {'tienda': tienda, 'context': context, 'notifications': notifications})
    else:
        return render(request, "prohibido.html", status=403)