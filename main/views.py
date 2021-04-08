from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage
import requests
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
import urllib.request
from main.forms import MessageForm, ReviewForm
from django.http import Http404
import json
from django.http import JsonResponse
from datetime import timedelta


def login(request):
    ''' Logea una persona en la aplicación.\n
        POST    -> Lleva la inicio con el contexto actualizado \n
        GET     -> Lleva al formulario de login
    '''
    #msg_success = "Bienvenido a la aplicación"
    msg_error  = "El nombre y la contraseña no coinciden"


    if request.method == 'POST': #Si es un POST redirijimos a la vista de index con el context actualizado
        try:
            username = request.POST['username']             #Sacamos el valor de la propiedad 'name' del formulario
            password = request.POST['password']             #Sacamos el valor de la propiedad 'password' del formulario

            person = Person.objects.get(username=username,password=password)        #Buscamos el usuario por su contraseña y nombre
            rol_and_id = whoIsWho(person)
            
            update_context(request,person.id,rol_and_id[0],rol_and_id[1],True)
            #msg = msg_success

            person_id,rol,rol_id,is_active = get_context(request)
            context = [person_id,rol,rol_id,is_active]

            promotions_shops = Promotion.objects.filter(product=None)
            promotions_products = Promotion.objects.filter(shop=None)

            tienda = miTienda(person_id)

            return render(request, 'home.html', {"context" : context, 'promotions_shops': promotions_shops, 'promotions_products': promotions_products, 'tienda': tienda})
        except:
            # Es importante pasar el context en todas las vistas.
            # Cambiar index.html por tu vista en tu método
            msg = msg_error
            return render(request, 'login.html',{"msg":msg, 'tienda': ''})
         
    else: #Si es un GET redirijimos a la vista de login
        return render(request, 'login.html', {'tienda': ''})

def register(request):
    ''' Logea una persona en la aplicación.\n
        POST    -> Lleva la inicio con el contexto actualizado \n
        GET     -> Lleva al formulario de login
    '''
    #msg_success = "Bienvenido a la aplicación"
    msg_error  = "El nombre y la contraseña no coinciden"


    if request.method == 'POST': #Si es un POST redirijimos a la vista de index con el context actualizado

        rol = request.POST['rol'] 
        
        try:
            #Parametros tomados del post
                username        =   request.POST['username']             
                password        =   request.POST['password']            
                name            =   request.POST['name']                
                phoneNumber     =   request.POST['phoneNumber'] 
                zipCode         =   request.POST['zipCode']              
                email           =   request.POST['email'] 
                   
                #Parámetros autogenerados   
                registerDate = date.today()
                isBanned = False

                p = Person(username=username, password=password, name=name, phoneNumber=phoneNumber, email=email, zipCode=zipCode, registerDate=registerDate, isBanned=isBanned)
                p.save()

                p = Person.objects.get(username=username,password=password)

                if rol == "Owner":
                    co = Owner(person=p)
                    co.save()

                    shopName        =   request.POST['shopName']
                    shopType        =   request.POST['shopType']
                    schedule        =   request.POST['schedule']
                    description     =   request.POST['description']
                    picture         =   request.POST['picture']
                    address         =   request.POST['address']
                    owner           =   request.POST['owner']
                    durationBooking =   request.POST['durationBooking']
                    address         =   request.POST['address']
                    
                    co = Owner.objects.get(person=p)
                    shopType = ShopType.objects.get(id=int(shopType))
                    shop = Shop.objects.get(name=name,shopType=null,schedule=schedule,description=description,picture=picture,address=address,owner=co,durationBooking=durationBooking)




                if rol == "User":
                    cu = CustomUser(person=p)
                    cu.save()

                print(p)  
                print(cu)
                rol_and_id = whoIsWho(p)

                update_context(request,p.id,rol_and_id[0],rol_and_id[1],True)
                person_id,rol,rol_id,is_active = get_context(request)
                context = [person_id,rol,rol_id,is_active]

                if rol == "Owner": return render(request, 'home.html', {"context" : context})
                if rol == "User": return render(request, 'home.html', {"context" : context})

        except:
            msg = msg_error
            return render(request, 'login.html',{"msg":msg})
         
    else: #Si es un GET redirijimos a la vista de login
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


def promotion_week_product(request, id_product):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    if (is_active):
        product = get_object_or_404(Product, pk=id_product) 
        promotion = Promotion.objects.filter(product=product).exists()
        if (not(promotion) and str(product.shop.owner.person.id) == person_id):
            promotionType = PromotionType.objects.get(id=0) # semanal
            owner = Owner.objects.get(person = person_id)
            time = date.today()
            endtime = (time + timedelta(days=7))
            promocion = Promotion.objects.create(owner= owner,shop=  None,startDate = time, endDate = endtime,promotionType = promotionType, product = product)
            # return render(request, 'promotionproduct.html', {'promocion':promocion, 'context':context})
            data = {
                    'url': ""
                }
            return JsonResponse(data)
        else:
            tienda = miTienda(person_id)
            return render(request, 'prohibido.html', {'context':context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')

def promotion_month_product(request, id_product):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    if (is_active):
        product = get_object_or_404(Product, pk=id_product) 
        promotion = Promotion.objects.filter(product=product).exists()
        if (not(promotion) and str(product.shop.owner.person.id) == person_id):
            promotionType = PromotionType.objects.get(id=1) # mensual
            owner = Owner.objects.get(person = person_id)
            time = date.today()
            endtime = (time + timedelta(days=30))

            promocion = Promotion.objects.create(owner= owner,shop=  None,startDate = time, endDate = endtime,promotionType = promotionType, product = product)
            data = {
                    'url': ""
                }
            return JsonResponse(data)
        else:
            tienda = miTienda(person_id)
            return render(request, 'prohibido.html', {'context':context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')

def threads_list(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    if rol == "User":
        threads = Thread.objects.all
        return render(request, 'threads.html', {'threads':threads, 'context':context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html', {'context':context, 'tienda': tienda})

def forumMessages_list(request,id_thread):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    thread= get_object_or_404(Thread, pk= id_thread)
    tienda = miTienda(person_id)
    if rol == "User":
        if request.method == 'POST':
            text = request.POST['text']
            ForumMessage.objects.create(text = text, date = date.today(), thread = thread, user = CustomUser.objects.get(id=rol_id))
        
        threadName = thread.name
        forumMessages = []
        for m in thread.forummessage_set.all():
            forumMessages.append(m)
        return render(request, 'thread.html', {'forumMessages':forumMessages,'threadName':threadName, 'context':context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html', {'context':context, 'tienda': tienda})

def promotion_week_shop(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    if (is_active):
        shop = get_object_or_404(Shop, pk=id_shop)
        promotion = Promotion.objects.filter(shop=shop).exists()
        
        if (not(promotion) and str(shop.owner.person.id) == person_id):
            # person_id, rol, rol_id, is_active = get_context(request)
            # context = [person_id, rol, rol_id, is_active]
            promotionType = PromotionType.objects.get(id=0)
            owner = Owner.objects.get(person = person_id)
            time = date.today()
            endtime = (time + timedelta(days=7))
            print(promotionType)
            promocion = Promotion.objects.create(owner= owner,shop =  shop,startDate = time, endDate = endtime,promotionType = promotionType, product = None)
            data = {
                    'url': ""
                }
            return JsonResponse(data)
        else:
            tienda = miTienda(person_id)
            return render(request, 'prohibido.html', {'context':context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')


def promotion_month_shop(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    if (is_active):
        shop = get_object_or_404(Shop, pk=id_shop)
        promotion = Promotion.objects.filter(shop=shop).exists()
        
        if (not(promotion) and str(shop.owner.person.id) == person_id):
        # shop = get_object_or_404(Shop, pk=id_shop) 
        # person_id, rol, rol_id, is_active = get_context(request)
        # context = [person_id, rol, rol_id, is_active]
            promotionType = PromotionType.objects.get(id=1)
            owner = Owner.objects.get(person = person_id)
            time = date.today()
            endtime = (time + timedelta(days=30))
            print(promotionType)
            promocion = Promotion.objects.create(owner= owner,shop =  shop,startDate = time, endDate = endtime,promotionType = promotionType, product = None)
            data = {
                    'url': ""
                }
            return JsonResponse(data)
        else:
            tienda = miTienda(person_id)
            return render(request, 'prohibido.html', {'context':context, 'tienda': tienda})
    else:
        return render(request, 'prohibido.html')

def product_details(request, id_product):
    product = get_object_or_404(Product, pk=id_product)
    types = ProductType.objects.all()   
    productType = []
    for ty in types:
        productType.append(ty)
    
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    promotionProduct = Promotion.objects.filter(product=product).exists()
    tienda = miTienda(person_id)
    return render(request, 'products.html', {'product': product, 'types' : productType, "context" : context, "promotionProduct" : not(promotionProduct), 'tienda': tienda})

def list_shop(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    shops = Shop.objects.all()
    tienda = miTienda(person_id)
    return render(request, 'shops.html', {'shops': shops,'context':context, 'tienda': tienda})


def shop_details(request, id_shop):
    shop = get_object_or_404(Shop, pk=id_shop)
    products = Product.objects.filter(shop=shop)
    promotionShop = Promotion.objects.filter(shop=shop).exists()
    # productsPromotion = {}
    # for prod in products:
    #     productsPromotion[prod] = not(Promotion.objects.filter(product=prod).exists())
    try:
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
    except:
        person_id = 0
        rol = 'User no registrado'
        context = [person_id, rol]
    tienda = miTienda(person_id)
    return render(request, 'shop_detail.html', {'shop': shop, 'products': products, 'context': context, 'promotionShop': not(promotionShop), 'tienda': tienda})

def get_chats_list(request):
    ''' Muestra una lista de todos los chats que el usuario activo, sea user u owner, tenga. \n
        POST    -> None \n
        GET     -> Proporciona un listado de los chats del usuario/dueño
    '''
    person_id,rol,rol_id,is_active = get_context(request)
    context = [person_id,rol,rol_id,is_active]
    tienda = miTienda(person_id)

    chats= []

    if rol=='User':

        chats= Chat.objects.filter(user=get_object_or_404(CustomUser, pk= person_id))

    elif rol=='Owner':

        shops= Shop.objects.filter(owner= get_object_or_404(Owner, pk=person_id))
        i = 0
        for s in shops:
            if i == 0:
                chats= Chat.objects.filter(shop=s)
            else:
                chats = chats | Chat.objects.filter(shop=s)
                
            i+= 1
    else: 
        return render(request,'error.html', {"context" : context, 'tienda': tienda}, status=403)

    print(chats)
    return render(request, "chatList.html", {"context" : context, "chats" : chats, 'tienda': tienda}, status=200)


def get_chat(request, id_chat):
    ''' Muesta los mensajes del chat y prepara el imputo para enviar mensajes.\n
        POST    -> None \n
        GET     -> Muestra los mensajes del chat, de las dos partes
    '''
    person_id,rol,rol_id,is_active= get_context(request)
    context = [person_id,rol,rol_id,is_active]
    tienda = miTienda(person_id)
    if (is_active):
        chat= get_object_or_404(Chat, pk= id_chat)
        # TODO: if para comprobar que el usuario forma parte de ese chat
        if str(rol) == 'User':
            if not (int(chat.user.id) == int(person_id)):
                print(True)
                return render(request,'prohibido.html', {"context" : context, 'tienda': tienda},status=403)
        elif str(rol) == 'Owner':
            if not(int(chat.shop.owner.id) == int(person_id)):
                print(False)
                return render(request,'prohibido.html', {"context" : context, 'tienda': tienda},status=403)
        else:
            return render(request,'prohibido.html', {"context" : context, 'tienda': tienda},status=403)

        if request.method == 'POST':
            form = MessageForm(data=request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                shop= chat.shop
                isSentByUser= False
                if rol== 'User':
                    isSentByUser=True
                ChatMessage.objects.create(text=text, chat= chat, date=date.today(), isSentByUser=isSentByUser).save()
                return redirect('/shop/chat/'+str(chat.id))
        chat_message = ChatMessage.objects.filter(chat=chat)
        form = MessageForm()
        return render(request, 'chat.html', {"context" : context, "messages" : chat_message, 'form': form, 'tienda': tienda})
    else:
        return render(request,'prohibido.html',status=403)

def get_chat_new(request, id_shop):
    ''' Muesta los mensajes del chat y prepara el imputo para enviar mensajes.\n
        POST    -> Envia un mensaje a la tienda si lo envia un usuario y a un usuario si lo envia una tienda \n
        GET     -> Muestra los mensajes del chat, de las dos partes
    '''

    person_id,rol,rol_id,is_active = get_context(request)
    context = [person_id,rol,rol_id,is_active]
    tienda = miTienda(person_id)
    print(rol)
    if rol =='Admin' or rol=='Owner':
        return render(request,'error.html', {"context" : context, 'tienda':tienda}, status=403)
    shop=get_object_or_404(Shop, pk= id_shop)
    user= get_object_or_404(CustomUser, pk=person_id)
    try:
        chat = Chat.objects.filter(shop = shop, user= user)[0]
    except:
        chat=None
    print(chat)
    if chat!=None:
        return redirect('/shop/chat/'+str(chat.id))
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            newChat = Chat.objects.create(shop= shop, user= user)
            newChat.save()
            print('new chat')
            print(newChat.pk)
            isSentByUser= False
            if rol== 'User':
                isSendByUser=True
            ChatMessage.objects.create(text=text, chat= newChat,date=date.today(), isSentByUser=isSentByUser).save()
            return redirect('/shop/chat/'+str(newChat.pk))

    chat_message=[]
    form = MessageForm()
    return render(request, 'chat.html', {"context" : context, "messages" : chat_message, 'form': form,'shop_id' : id_shop, 'tienda': tienda})


def home(request):
    promotions_shops = Promotion.objects.filter(product=None)
    promotions_products = Promotion.objects.filter(shop=None)
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    return render(request, 'home.html', {"context": context, 'promotions_shops': promotions_shops, 'promotions_products': promotions_products, 'tienda': tienda})

def booking(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    if (is_active):
        user = CustomUser.objects.get(id=person_id)
        for reserva in json.loads(request.POST.get('key_1_string')):
            product = Product.objects.get(id=reserva['id'])
            Booking.objects.create(startDate=date.today(),endDate=date.today(), product=product,title='Prueba',quantity=reserva['cantidad'], isAccepted=False, user=user)

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
    booking = Booking.objects.filter(id=request.POST.get('id')).update(isAccepted=True)
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
            Booking.objects.create(startDate=date.today(),endDate=date.today(), product=product,title='Prueba',quantity=reserva['cantidad'], isAccepted=False, user=user)

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
    shop = get_object_or_404(Shop, pk= id_shop)
    tienda = miTienda(person_id)
    if rol == "User":

        reviews = []
        for m in shop.review_set.all():
            reviews.append(m)

        return render(request, 'reviews.html', {'reviews':reviews, 'context':context, 'tienda': tienda}) #a la vista de todas las reviews
    else:
        return render(request, 'prohibido.html', {'context':context, 'tienda': tienda})

def review_form(request, id_shop):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    shop = get_object_or_404(Shop, pk= id_shop)
    tienda = miTienda(person_id)
    if rol == "User":
        if request.method == 'GET':
            form = ReviewForm()
            return render(request, 'review.html', {'form':form, 'context':context, 'tienda': tienda}) #al formulario vacio
        if request.method == 'POST':  
            form = ReviewForm(data=request.POST)         
            if form.is_valid():
                rating = form.cleaned_data['rating']
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                Review.objects.create(rating = rating, title = title, description = description, date = date.today(), user = CustomUser.objects.get(id=rol_id), shop = shop)
                reviews = []
                for m in shop.review_set.all():
                    reviews.append(m)
                return redirect('../', {'reviews':reviews, 'context':context, 'tienda': tienda}) #a la vista las reviews de la tienda
            else:
                return render(request, 'review.html', {'form':form, 'context':context, 'tienda': tienda}) #de vuelta al formulario a rellenarlo correctamente
    else:
        return render(request, 'prohibido.html', {'context':context, 'tienda': tienda})

def about(request):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    return render(request, 'about.html', {"context": context, 'tienda': tienda})

def error_404(request, exception):
    person_id, rol, rol_id, is_active = get_context(request)
    context = [person_id, rol, rol_id, is_active]
    tienda = miTienda(person_id)
    return render(request,'error.html', {'context': context, "tienda":tienda})

def miTienda(person_id):
    try:
        person = Person.objects.get(id=person_id)
        owner = Owner.objects.get(person=person)
        shop = Shop.objects.get(owner=owner)
    except:
        shop = ''

    return shop
