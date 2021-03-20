from main.models import Person, CustomUser, CustomAdmin, Owner, ShopType, ProductType, Shop, Product, SubscriptionType, PromotionType, Subscription, Promotion, Booking, Review, Chat, ChatMessage, Thread, ForumMessage
from django.shortcuts import render
import requests


def login(request):
    ''' Logea una persona en la aplicación.\n
        POST    -> Lleva la inicio con el contexto actualizado \n
        GET     -> Lleva al formulario de login
    '''
    if request.method == 'POST': #Si es un POST redirijimos a la vista de index con el context actualizado
        try:
            username = request.POST['username']             #Sacamos el valor de la propiedad 'name' del formulario
            password = request.POST['password']         #Sacamos el valor de la propiedad 'password' del formulario

            person = Person.objects.get(username=username,password=password)        #Buscamos el usuario por su contraseña y nombre
            rol_and_id = whoIsWho(person)
            
            update_context(request,person.id,rol_and_id[0],rol_and_id[1],True)

        except Exception as e:
            print(e)
    
    else: #Si es un GET redirijimos a la vista de login
        return render(request, 'login.html')

def logout(request):
    ''' Deslogea una persona en la aplicación.\n
        POST    -> None \n
        GET     -> Lleva al formulario de login
    '''
    if request.method == 'GET': #Si es un GET redirijimos a la vista de index con el context actualizado
        try:
            
           person_id,rol,rol_id,is_active = get_context()

           update_context(person_id,rol,rol_id,False)

        except Exception as e:
            print(e)
        
        return render(request, 'index.html')
        
def whoIsWho(person):
    ''' Identifica el rol e id de una persona\n
        In: Person\n
        Out: List[rol,rol_id]
    '''
    res = []
    try:
        cu = CustomUser.objects.get(person=person).id
        continue_searching = False
        res=["User",cu]
    except:
        continue_searching = True
    print("==========================================================")
    print(continue_searching)
    if continue_searching:
        try:
            ca = CustomAdmin.objects.get(person=person).id
            res=["Admin",ca]
        except:
            continue_searching = True
    
    if continue_searching:
        try:
            o = Owner.objects.get(person=person).id
            res=["Owner",o]
        except:
            continue_searching = True
    
    return res

def update_context(request,person_id,rol,rol_id,is_active):
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

def delete_context():
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
    print("***************")
    print(person_id)
    person_id   =   request.session['person_id'] 
    rol         =   request.session['rol']
    rol_id      =   request.session['rol_id']
    is_active   =   request.session['is_active']

    return person_id,rol,rol_id,is_active


def promotion_product(request):
    product = Product.objects.get(id=1)
    person_id,rol,rol_id,is_active = get_context(request)
    print(person_id)
    promotion = Promotion.obj
    person = Person.objects.get(username=username,password=password)        #Buscamos el usuario por su contraseña y nombre
    rol_and_id = whoIsWho(person)
    
    update_context(person.id,rol_and_id[0],rol_and_id[1],True)