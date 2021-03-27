from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage
import requests
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
import urllib.request
from main.forms import MessageForm




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


def promotion_product(request):
    if request.method == 'GET':
        return render(request, 'index.html') # redirección del botón
    product = Product.objects.get(id=1)
    person_id,rol,rol_id,is_active = get_context(request)
    promotionType = PromotionType.objects.get(id=0) # semanal
    shop = Shop.objects.filter(owner = rol_id)
    tienda = shop[0]
    owner = Owner.objects.get(person = person_id)
    time = date.today()

    promocion = Promotion.objects.create(owner= owner,shop=  None,startDate = time, endDate = time.replace(day=time.day+ 7),promotionType = promotionType, product = product)


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

def promotion_shop(request):
    if request.method == 'GET':
        return render(request, 'index.html') # redirección del botón
    product = Product.objects.get(id=1)
    person_id,rol,rol_id,is_active = get_context(request)
    promotionType = PromotionType.objects.get(id=0) # semanal
    shop = Shop.objects.filter(owner = rol_id)
    tienda = shop[0]
    owner = Owner.objects.get(person = person_id)
    time = date.today()

    promocion = Promotion.objects.create(owner= owner,shop =  tienda,startDate = time, endDate = time.replace(day=time.day+ 7),promotionType = promotionType, product = None)



def list_shop(request):
    shops = Shop.objects.all()
    return render(request, 'shops.html', {'shops': shops})


def list_shop_details(request, id_shop):
    shop = get_object_or_404(Shop, pk=id_shop)
    return render(request, 'shopDetail.html', {'shop': shop})

def get_chats_list(request):
    ''' Muestra una lista de todos los chats que el usuario activo, sea user u owner, tenga. \n
        POST    -> None \n
        GET     -> Proporciona un listado de los chats del usuario/dueño
    '''
    person_id,rol,rol_id,is_active = get_context(request)
    context = [person_id,rol,rol_id,is_active]

    chats= []

    if context.rol=='user':

        chats= Chat.objects.filter(user=get_object_or_404(CustomUser, pk= context.person_id))

    elif context.rol=='owner':

        shops= Shop.objects.filter(owner= get_object_or_404(Owner, pk=context.person_id))

        for s in shops:

            chats.append(Chat.objects.filter(shop=s))

    return render(request, 'chats_list.html', {"context" : context, "chats" : chats})


def get_chat(request, id_chat):
    ''' Muesta los mensajes del chat y prepara el imputo para enviar mensajes.\n
        POST    -> None \n
        GET     -> Muestra los mensajes del chat, de las dos partes
    '''
    person_id,rol,rol_id,is_active= get_context(request)
    context = [person_id,rol,rol_id,is_active]
    chat= get_object_or_404(Chat, pk= id_chat)
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            shop= chat.shop
            isSendByUser= False
            print(rol)
            if rol== 'User':
                isSendByUser=True
            ChatMessage.objects.create(text=text, chat= chat, isSentByUser=isSendByUser).save()
            return redirect('/shop/chat/'+str(chat.id))
    # TODO: if para comprobar que el usuario forma parte de ese chat
    chat_message = ChatMessage.objects.filter(chat=chat)
    form = MessageForm()
    return render(request, 'chat.html', {"context" : context, "messages" : chat_message, 'form': form})


def get_chat_new(request, id_shop):
    ''' Muesta los mensajes del chat y prepara el imputo para enviar mensajes.\n
        POST    -> Envia un mensaje al chat de la tienda \n
        GET     -> Muestra los mensajes del chat, de las dos partes
    '''

    person_id,rol,rol_id,is_active= get_context(request)
    context = [person_id,rol,rol_id,is_active]
    shop=get_object_or_404(Shop, pk= id_shop)
    chat=Chat.objects.filter(shop = shop)
    if chat.exists:
        return redirect('/shop/chat'+chat.id)
    chat_message=[]
    form = MessageForm()
    form.cleaned_data['shop_id'] = id_shop
    return render(request, 'show_chat.html', {"context" : context, "messages" : chat_message, 'form': form,'shop_id' : id_shop})


def send_message(request,id_chat):
    ''' Envia un mensaje al chat de usuario-tienda.\n
        POST    -> Envia un mensaje al chat de la tienda \n
        GET     -> None
    '''
    person_id,rol,rol_id,is_active= get_context(request)
    context = [person_id,rol,rol_id,is_active]

    if request.method == 'POST':

        form = MessageForm(data=request.POST)
        if form.is_valid():
            chat= Chat.objects.filter(user= CustomUser.objects.filter(person=person_id),shop=shop)
            if not chat.exists():
                chat_id= Chat.objects.create(user= CustomUser.objects.filter(person=person_id),shop=shop).save().id
                chat = get_object_or_404(Chat,pk=chat_id)
            text = form.cleaned_data['text']
            shop_id = form.cleaned_data['shop_id']
            shop= get_object_or_404(Shop,pk=shop_id)
            ChatMessage.objects.create(text=text, chat= chat, shop=shop).save()
            return redirect('/shop/chat'+chat.id)
    return render(request, 'Error.html', {'form': form})


def home(request):
    try:
        person_id, rol, rol_id, is_active = get_context(request)
        context = [person_id, rol, rol_id, is_active]
        return render(request, 'home.html',{"context" : context})
    except:
        return render(request, 'home.html')


def error(request):
    return render(request, 'error.html')

def forbidden(request):
    return render(request, 'prohibido.html')
