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

        except Exception as e:
            print(e)

        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]

        # Es importante pasar el context en todas las vistas.
        # Cambiar index.html por tu vista en tu método

        return render(request, 'home.html',{"context" : context})
    else: #Si es un GET redirijimos a la vista de login
        return render(request, 'login.html')


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

        return render(request, 'home.html')


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
    print("==========================================================")
    print(continue_searching)
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
    print(person_id)
    print(rol)
    print(rol_id)
    print(is_active)

    try:
        request.session['person_id'] = str(person_id)
        request.session['rol'] = str(rol)
        request.session['rol_id'] = str(rol_id)
        request.session['is_active'] = str(is_active)
    except:
        res = False

    print(res)

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
    person_id = request.session['person_id']
    rol = request.session['rol']
    rol_id = request.session['rol_id']
    is_active = request.session['is_active']

    return person_id, rol, rol_id, is_active


def promotion_product(request, id_product):

    product = get_object_or_404(Product, pk=id_product) 
    person_id,rol,rol_id,is_active = get_context(request)
    promotionType = PromotionType.objects.get(id=0) # semanal
    owner = Owner.objects.get(person = person_id)
    time = date.today()
    endtime = (time + timedelta(days=7))

    promocion = Promotion.objects.create(owner= owner,shop=  None,startDate = time, endDate = endtime,promotionType = promotionType, product = product)
    return render(request, 'promotionproduct.html', {'promocion':promocion})


def threads_list(request):
    rol = get_context(request)[1]
    if rol == "User":
        threads = Thread.objects.all
        return render(request, 'threads.html', {'threads':threads})

def forumMessages_list(request,id_thread):
    rol,rol_id = get_context(request)[1:3]
    thread= get_object_or_404(Thread, pk= id_thread)
    if rol == "User":
        if request.method == 'POST':
            text = request.POST['text']
            ForumMessage.objects.create(text = text, date = date.today(), thread = thread, user = CustomUser.objects.get(id=rol_id))
        
        threadName = thread.name
        forumMessages = []
        for m in thread.forummessage_set.all():
            forumMessages.append(m)
        return render(request, 'thread.html', {'forumMessages':forumMessages,'threadName':threadName})

def promotion_shop(request, id_shop):

    shop = get_object_or_404(Shop, pk=id_shop) 
    person_id,rol,rol_id,is_active = get_context(request)
    promotionType = PromotionType.objects.get(id=0) # semanal HABRIA QUE MODIFICAR ESTO PARA QUE SE SELECCIONE EL TIPO DE LA PRMOCION
    owner = Owner.objects.get(person = person_id)
    time = date.today()
    endtime = (time + timedelta(days=7))
    
    promocion = Promotion.objects.create(owner= owner,shop =  shop,startDate = time, endDate = endtime,promotionType = promotionType, product = None)
    return render(request, 'promotionshop.html', {'promocion':promocion})

def list_shop(request):
    shops = Shop.objects.all()
    return render(request, 'shops.html', {'shops': shops})


def shop_details(request, id_shop):

    shop = get_object_or_404(Shop, pk=id_shop)
    products = Product.objects.filter(shop=shop)
    try:
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
    except:
        person_id = 0
        rol = 'User no registrado'
        context = [person_id, rol]

    return render(request, 'shop_detail.html', {'shop': shop, 'products': products, 'context': context})

def get_chats_list(request):
    ''' Muestra una lista de todos los chats que el usuario activo, sea user u owner, tenga. \n
        POST    -> None \n
        GET     -> Proporciona un listado de los chats del usuario/dueño
    '''
    person_id,rol,rol_id,is_active = get_context(request)
    context = [person_id,rol,rol_id,is_active]

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
        return render(request,'error.html', {"context" : context}, status=403)

    print(chats)
    return render(request, "chatList.html", {"context" : context, "chats" : chats}, status=200)


def get_chat(request, id_chat):
    ''' Muesta los mensajes del chat y prepara el imputo para enviar mensajes.\n
        POST    -> None \n
        GET     -> Muestra los mensajes del chat, de las dos partes
    '''
    person_id,rol,rol_id,is_active= get_context(request)
    context = [person_id,rol,rol_id,is_active]
    chat= get_object_or_404(Chat, pk= id_chat)
    print(context)
    print(chat.user.id)
    # TODO: if para comprobar que el usuario forma parte de ese chat
    if str(rol) == 'User':
        if not (int(chat.user.id) == int(person_id)):
            print(True)
            return render(request,'error.html', {"context" : context},status=403)
    elif str(rol) == 'Owner':
        if not(int(chat.shop.owner.id) == int(person_id)):
            print(False)
            return render(request,'error.html', {"context" : context},status=403)
    else:
        return render(request,'error.html', {"context" : context},status=403)

    # if not(str(rol) == 'User' and int(chat.user.id) == int(person_id)):
    #     print(True)
    #     return render(request,'error.html', {"context" : context})

    # elif not((str(rol) == 'User') and (int(chat.shop.owner.id) == int(person_id))):
    #     print(False)
    #     return render(request,'error.html', {"context" : context})

    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            shop= chat.shop
            isSentByUser= False
            if rol== 'User':
                isSendByUser=True
            ChatMessage.objects.create(text=text, chat= chat, date=date.today(), isSentByUser=isSentByUser).save()
            return redirect('/shop/chat/'+str(chat.id))
    chat_message = ChatMessage.objects.filter(chat=chat)
    form = MessageForm()
    return render(request, 'chat.html', {"context" : context, "messages" : chat_message, 'form': form})


def get_chat_new(request, id_shop):
    ''' Muesta los mensajes del chat y prepara el imputo para enviar mensajes.\n
        POST    -> Envia un mensaje a la tienda si lo envia un usuario y a un usuario si lo envia una tienda \n
        GET     -> Muestra los mensajes del chat, de las dos partes
    '''

    person_id,rol,rol_id,is_active= get_context(request)
    context = [person_id,rol,rol_id,is_active]
    print(rol)
    if rol =='Admin' or rol=='Owner':
        return render(request,'error.html', {"context" : context}, status=403)
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
    return render(request, 'chat.html', {"context" : context, "messages" : chat_message, 'form': form,'shop_id' : id_shop})


# def send_message(request,id_chat):
#     ''' Envia un mensaje al chat de usuario-tienda.\n
#         POST    -> Envia un mensaje al chat de la tienda \n
#         GET     -> None
#     '''
#     person_id,rol,rol_id,is_active= get_context(request)
#     context = [person_id,rol,rol_id,is_active]

#     if request.method == 'POST':

#         form = MessageForm(data=request.POST)
#         if form.is_valid():
#             chat= Chat.objects.filter(user= CustomUser.objects.filter(person=person_id),shop=shop)
#             if not chat.exists():
#                 chat_id= Chat.objects.create(user= CustomUser.objects.filter(person=person_id),shop=shop).save().id
#                 chat = get_object_or_404(Chat,pk=chat_id)
#             text = form.cleaned_data['text']
#             shop_id = form.cleaned_data['shop_id']
#             shop= get_object_or_404(Shop,pk=shop_id)
#             ChatMessage.objects.create(text=text, chat= chat,date=date.today(), shop=shop).save()
#             return redirect('/shop/chat'+chat.id)
#     return render(request, 'error.html', {'form': form})


def home(request):
    try:
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
        return render(request, 'home.html',{"context" : context})
    except:
        return render(request, 'home.html')

def booking(request):
    try:
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
        user = CustomUser.objects.get(id=person_id)
        print(json.loads(request.POST.get('key_1_string')))
        for reserva in json.loads(request.POST.get('key_1_string')):
            product = Product.objects.get(id=reserva['id'])
            Booking.objects.create(startDate=date.today(),endDate=date.today(), product=product,title='Prueba',quantity=reserva['cantidad'], isAccepted=False, user=user)

        data = {
            'url': "user/bookings/"
        }
        return JsonResponse(data)
    except:
        data = {
            'url': "/prohibido/"
        }
        return JsonResponse(data)

        

def list_booking_user(request):
    try:
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
        user = CustomUser.objects.get(id=person_id)
        bookings = Booking.objects.filter(user=user).filter(isAccepted=False)
        return render(request, 'bookings_user.html', {'bookings': bookings, 'context': context})
    except:
        return render(request, 'prohibido.html')

def list_booking_owner(request):
    try:
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
        owner = Owner.objects.get(id=person_id)
        bookings = Booking.objects.filter(isAccepted=False)
        reservas = []
        for book in bookings:
            if book.product.shop.owner.id == owner.id:
                reservas.append(book)
        return render(request, 'bookings_owner.html', {'bookings': reservas, 'context': context})
    except:
        return render(request, 'prohibido.html')

def accept_booking(request):
    print(request.POST.get('id'))
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
    try:
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
        user = CustomUser.objects.get(id=person_id)
        for reserva in json.loads(request.POST.get('key_1_string')):
            product = Product.objects.get(id=reserva['id'])
            Booking.objects.create(startDate=date.today(),endDate=date.today(), product=product,title='Prueba',quantity=reserva['cantidad'], isAccepted=False, user=user)

        data = {
            'url': "/user/bookings/"
        }
        return JsonResponse(data)
    except:
        data = {
            'url': "/prohibido/"
        }
        return JsonResponse(data)


def review_list(request, id_shop):
    rol = get_context(request)[1]
    shop = get_object_or_404(Shop, pk= id_shop)
    if rol == "User":

        reviews = []
        for m in shop.review_set.all():
            reviews.append(m)

        return render(request, 'reviews.html', {'reviews':reviews}) #a la vista de todas las reviews
    else:
        return render(request, 'prohibido.html')

def review_form(request, id_shop):
    rol,rol_id = get_context(request)[1:3]
    shop = get_object_or_404(Shop, pk= id_shop)
    if rol == "User":
        if request.method == 'GET':
            form = ReviewForm()
            return render(request, 'review.html', {'form':form}) #al formulario vacio
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
                return render(request, 'reviews.html', {'reviews':reviews}) #a la vista las reviews de la tienda
            else:
                return render(request, 'review.html', {'form':form}) #de vuelta al formulario a rellenarlo correctamente
    else:
        return render(request, 'prohibido.html')
        

# def list_booking_user(request):
#     try:
#         person_id, rol, rol_id, is_active = get_context(request)
#         context = [person_id, rol, rol_id, is_active]
#         user = CustomUser.objects.get(id=person_id)
#         bookings = Booking.objects.filter(user=user).filter(isAccepted=False)
#         return render(request, 'bookings_user.html', {'bookings': bookings})
#     except:
#         return render(request, 'prohibido.html')

# def list_booking_owner(request):
#     try:
#         person_id, rol, rol_id, is_active = get_context(request)
#         context = [person_id, rol, rol_id, is_active]
#         owner = Owner.objects.get(id=person_id)
#         bookings = Booking.objects.filter(isAccepted=False)
#         reservas = []
#         for book in bookings:
#             kk = book.product.shop.owner.id
#             kk2 = owner.id
#             if book.product.shop.owner.id == owner.id:
#                 reservas.append(book)
#         return render(request, 'bookings_owner.html', {'bookings': bookings})
#     except:
#        return render(request, 'prohibido.html') 

# def accept_booking(request):
#     booking = Booking.objects.filter(id=request.POST.get('id')).update(isAccepted=True)
#     data = {
#             'url': "/shop/bookings/accepted"
#         }
#     return JsonResponse(data)