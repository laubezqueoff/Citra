from django.test import TestCase, Client
import unittest
import requests
import json
import sys
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from main.forms import ProductForm, FormShop



class TestMethods(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

    # Es importante que se ejecute primero este test. Los test se ejecutan por orden alfabéico.

    def test_login(self):
        # Probamos que el usuario se puede registrar de forma correcta.

        credentials = {"username": 'USER-0', "password": 'PASS-0'}

        url = "http://127.0.0.1:9000/login/"
        # url = "https://citra-ispp.herokuapp.com/login/"

        c = Client()
        r = c.post(url, credentials)

        self.assertEqual(r.status_code, 200)

    def test_logout(self):
        # Probamos que el usuario puede hacer logout de forma correcta.

        credentials = {"username": 'USER-0', "password": 'PASS-0'}

        url = "http://127.0.0.1:9000/login/"

        c = Client()
        r = c.post(url, credentials)

        self.assertEqual(r.status_code, 200)


 ########################################################    TEST DE CHATS    ####################################################
    def test_new_chat_get(self):
        # Probamos que se puede acceder a un chat con una tienda con la que todavia no ha hablado
        print('test_new_chat_get')

        credentials = {'username': 'User-0', 'password': 'Pass-0'}

        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)


        response = self.client.get(reverse('newChat', args=(1,)), follow=True)   
        self.assertEqual(response.status_code, 200)

    def test_new_chat_post(self):
        #Probamos que se puede enviar un mensaje a un chat con una tienda con la que NO se ha hablado antes
        print('test_chat_post')
        
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        data={'text': 'Hola'}
        response = self.client.post(reverse('newChat', args=(1,)), data=data, follow=True)    
        self.assertEqual(response.status_code, 200)
    
    def test_new_chat_get_404(self):
        #Probamos que NO se puede acceder a un chat con una tienda que no existe
        print('test_new_chat_get_404')

        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('newChat', args=(12345678,)), follow=True)   
        self.assertEqual(response.status_code, 404)

    def test_new_chat_get_403_owner(self):
        #Probamos que NO se puede acceder a un chat con una tienda desde un owner
        print('test_new_chat_get_403_owner')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('newChat', args=(0,)), follow=True)    
        self.assertEqual(response.status_code, 403)

    def test_new_chat_get_403_admin(self):
        #Probamos que NO se puede acceder a un chat con una tienda desde un usuario admin
        print('test_new_chat_get_403_admin')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('newChat', args=(0,)), follow=True)    
        self.assertEqual(response.status_code, 403)

    def test_new_chat_get_403_no_login(self):
        #Probamos que NO se puede acceder a un chat con una tienda sin haberse logueado antes
        print('test_new_chat_get_403_no_login')
        
        
        response = self.client.get(reverse('newChat', args=(0,)), follow=True)    
        self.assertEqual(response.status_code, 403)

    def test_chat_post(self):
        #Probamos que se puede enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_chat_post')

        credentials = {'username': 'User-0', 'password': 'Pass-0'}

        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        data={'text': 'Hola'}
        response = self.client.post(reverse('chat', args=(0,)), data=data, follow=True)    

        self.assertEqual(response.status_code, 200)

    def test_chat_get(self):

        #Probamos que se puede acceder acceder a un chat con una tienda con la que ha hablado antes

        print('test_chat_get')

        credentials = {'username': 'User-0', 'password': 'Pass-0'}

        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('chat', args=(0,)), follow=True)    
        self.assertEqual(response.status_code, 200)

    def test_chat_get_403_user(self):
        #Probamos que NO se puede acceder a un chat existente desde un user que no participa en el chat
        print('test_chat_get_403_user')
        

        credentials = {'username': 'User-0', 'password': 'Pass-0'}

        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('chat', args=(1,)), follow=True)    

        self.assertEqual(response.status_code, 403)
    
    def test_chat_get_404(self):

        #Probamos que NO se puede acceder a un chat NO existente

        print('test_chat_get_404')

        credentials = {'username': 'User-0', 'password': 'Pass-0'}

        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('chat', args=(12345,)), follow=True)    

        self.assertEqual(response.status_code, 404)
        
    def test_chat_get_403_admin(self):
        #Probamos que NO se puede acceder a un chat existente con desde un admin
        print('test_chat_get_403_admin')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('chat', args=(1,)), follow=True)    
        self.assertEqual(response.status_code, 403)

    def test_chat_get_403_owner(self):
        #Probamos que NO se puede acceder a un chat existente con desde un owner que no participa en el chat

        print('test_chat_get_403_owner')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('chat', args=(1,)), follow=True)    
        self.assertEqual(response.status_code, 403)



    def test_chat_list_user(self):
        #Probamos que se puede acceder a la lista de chats del user logueado en cuestión
        print('test_chat_list_user')
        
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('chats'), follow=True)    
        self.assertEqual(response.status_code, 200)
        
    def test_chat_list_owner(self):
        #Probamos que se puede acceder a la lista de chats del owner logueado en cuestión
        print('test_chat_list_owner')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('chats'), follow=True)    
        self.assertEqual(response.status_code, 200)
    
    def test_chat_list_403_admin(self):
        #Probamos que NO se puede acceder a la lista de chats estando logueado como admin
        print('test_chat_list_403_admin')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('chats'), follow=True)    
        self.assertEqual(response.status_code, 403)
    
    def test_chat_list_403_no_login(self):
        #Probamos que NO se puede acceder a la lista de chats sin estar logueado 
        print('test_chat_list_403_no_login')

        response = self.client.get(reverse('chats'), follow=True)    
        self.assertEqual(response.status_code, 403)


 #########################################################    TEST DE ADMIN    ####################################################

    def test_users_list(self):
        #Probamos que se puede acceder a la lista de users
        print('test_users_list')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_users'), follow=True)    
        self.assertEqual(response.status_code, 200)

    def test_users_list_post(self):
        #Probamos que se puede acceder a la lista de users filtrando por username
        print('test_users_list_post')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        data = {'username': 'User'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_users'), data=data, follow=True)    
        self.assertEqual(response.status_code, 200)

    def test_users_list_403_user(self):
        #Probamos que NO se puede acceder a la lista de users estando logueado como user
        print('test_users_list_403_user')
        
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_users'), follow=True)    
        self.assertEqual(response.status_code, 403)

    def test_users_list_403_owner(self):
        #Probamos que NO se puede acceder a la lista de users estando logueado como owner
        print('test_users_list_403_owner')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_users'), follow=True)    
        self.assertEqual(response.status_code, 403)
    
    def test_users_list_403_no_login(self):
        #Probamos que NO se puede acceder a la lista de users sin estar logueado 
        print('test_users_list_403_no_login')
        
        response = self.client.get(reverse('list_users'), follow=True)    
        self.assertEqual(response.status_code, 403)


    def test_owners_list(self):
        #Probamos que se puede acceder a la lista de owners
        print('test_owners_list')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_owners'), follow=True)    
        self.assertEqual(response.status_code, 200)

    def test_owners_list_post(self):
        #Probamos que se puede acceder a la lista de owners filtrando por username
        print('test_owners_list_post')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        data = {'username': 'micu'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_owners'), data=data, follow=True)    
        self.assertEqual(response.status_code, 200)

    def test_owners_list_403_user(self):
        #Probamos que NO se puede acceder a la lista de owners estando logueado como user
        print('test_owners_list_403_user')
        
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_owners'), follow=True)    
        self.assertEqual(response.status_code, 403)

    def test_owners_list_403_owner(self):
        #Probamos que NO se puede acceder a la lista de owners estando logueado como owner
        print('test_owners_list_403_owner')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_owners'), follow=True)    
        self.assertEqual(response.status_code, 403)
    
    def test_owners_list_403_no_login(self):
        #Probamos que NO se puede acceder a la lista de owners sin estar logueado 
        print('test_owners_list_403_no_login')
        
        response = self.client.get(reverse('list_owners'), follow=True)    
        self.assertEqual(response.status_code, 403)


    def test_get_user(self):
        #Probamos que se puede acceder al perfil de un user
        print('test_get_user')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_users', args=(1,)), follow=True)    
        self.assertEqual(response.status_code, 200)
    
    def test_post_user_false(self):
        #Probamos que se puede banear el perfil de un user
        print('test_post_user_false')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        data = {'isBanned':False}
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('list_users', args=(1,)), data=data, follow=True)    
        self.assertEqual(response.status_code, 200)
    
    def test_post_user_true(self):
        #Probamos que se puede acceder habilitar el perfil de un user
        print('test_post_user_true')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        data = {'isBanned':True}
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('list_users', args=(1,)), data=data, follow=True)    
        self.assertEqual(response.status_code, 200)

    def test_get_user_403_user(self):
        #Probamos que se puede acceder al perfil de un user estando logueado como user
        print('test_get_user_403_user')
        
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_users', args=(1,)), follow=True)    
        self.assertEqual(response.status_code, 403)

    def test_get_user_403_owner(self):
        #Probamos que se puede acceder al perfil de un user estando logueado como owner
        print('test_get_user_403_owner')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_users', args=(1,)), follow=True)    
        self.assertEqual(response.status_code, 403)
    
    def test_get_user_403_no_login(self):
        #Probamos que se puede acceder al perfil de un user sin estar logueado
        print('test_get_user_403_no_login')
        
        response = self.client.get(reverse('list_users', args=(1,)), follow=True)    
        self.assertEqual(response.status_code, 403)


    def test_get_owner(self):
        #Probamos que se puede acceder al perfil de un owner
        print('test_get_owner')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_owners', args=(6,)), follow=True)    
        self.assertEqual(response.status_code, 200)

    def test_post_owner_false(self):
        #Probamos que se puede banear el perfil de un owner
        print('test_post_owner_false')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        data = {'isBanned':False}
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('list_owners', args=(6,)), data=data, follow=True)    
        self.assertEqual(response.status_code, 200)
    
    def test_post_owner_true(self):
        #Probamos que se puede acceder habilitar el perfil de un owner
        print('test_post_owner_true')
        
        credentials = {'username': 'laubezque', 'password': 'laubezque'}
        data = {'isBanned':True}
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('list_owners', args=(6,)), data=data, follow=True)    
        self.assertEqual(response.status_code, 200)

    def test_get_owner_403_user(self):
        #Probamos que se puede acceder al perfil de un owner estando logueado como user
        print('test_get_owner_403_user')
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        
        response = self.client.get(reverse('list_owners',args=(1,)), follow=True)    
        self.assertEqual(response.status_code, 403)

    def test_get_owner_403_owner(self):
        #Probamos que se puede acceder al perfil de un owner estando logueado como owner
        print('test_get_owner_403_owner')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('list_owners',args=(1,)), follow=True)    
        self.assertEqual(response.status_code, 403)
    
    def test_get_owner_403_no_login(self):
        #Probamos que se puede acceder al perfil de un owner sin estar logueado
        print('test_get_owner_403_no_login')
        
        response = self.client.get(reverse('list_owners',args=(1,)), follow=True)    
        self.assertEqual(response.status_code, 403)
#Test de tienda
    def test_shop_get_200(self):
        # Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_shop_get_200')

        credentials = {'username': 'User-0', 'password': 'Pass-0'}

        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(
            reverse('shop', args=(1,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 200)

    def test_shop_get_200_without_login(self):
        # Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_shop_get_200_without_login')

        response = self.client.get(
            reverse('shop', args=(1,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 200)

    def test_shop_get_404(self):
        # Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_shop_get_404')
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(
            reverse('shop', args=(12345,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 404)

    def test_list_shop_get_200(self):
        # Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_list_shop_get_200')

        credentials = {'username': 'User-0', 'password': 'Pass-0'}

        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(
            reverse('shops'), follow=True)    # for second object
        self.assertEqual(response.status_code, 200)

    def test_edit_shop_get_200(self):
        # Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_edit_shop_get_200')

        credentials = {'username': 'micum', 'password': 'Contraseña-3'}

        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        data = {'name': 'Nombre nuevo', 'schedule': 'Todos los dias de 12-7',
                'description': 'Buena calidad la ropa de niños', 'address': 'Calle plaza 33', 'durationBooking': '22'}
        form = FormShop(data=data)
        # print(form)
        response = self.client.post(
            reverse('update_shop', args=(4,)), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.is_valid())

    def test_edit_shop_get_403(self):
        # Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_edit_shop_get_403')

        credentials = {'username': 'Anlope', 'password': 'Contraseña-1'}

        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        data = {'name': 'Nombre nuevo', 'schedule': 'Todos los dias de 12-7',
                'description': 'Buena calidad la ropa de niños', 'address': 'Calle plaza 33', 'durationBooking': '22'}
        form = FormShop(data=data)
        response = self.client.post(
            reverse('update_shop', args=(4,)), data=data, follow=True)
        self.assertEqual(response.status_code, 403)

        #TESTS DE PRODUCTOS

    def test_new_product_get(self):
        #Probamos que se puede acceder a la vista de crear un producto
        print('test_new_product_get')

        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('product_create', args=(4,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_new_product_get_403_owner(self):
        #Probamos que no se puede acceder a la vista de crear un producto de otra tienda
        print('test_new_product_get_403_owner')

        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        response = self.client.get(reverse('product_create', args=(1,)), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_new_product_get_403_user(self):
        #Probamos que no se puede acceder a la vista de crear un producto de otra tienda
        print('test_new_product_get_403_user')

        credentials = {'username': 'josruialb', 'password': 'josruialb'}
        
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('product_create', args=(1,)), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_new_product_get_403_admin(self):
        #Probamos que no se puede acceder a la vista de crear un producto de otra tienda
        print('test_new_product_get_403_admin')

        credentials = {'username': 'viclopvaz1', 'password': 'viclopvaz1'}
        
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('product_create', args=(1,)), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_product_details_get(self):
        #Probamos que se puede acceder a los detalles de un producto
        print('test_product_details_get')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('products', args=(28,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_product_details_get_404(self):
        #Probamos que se puede acceder a los detalles de un producto
        print('test_product_details_get')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('products', args=(12345,)), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_product_details_get_user(self):
        #Probamos que se puede acceder a los detalles de un producto
        print('test_product_details_get_user')
        
        credentials = {'username': 'josruialb', 'password': 'josruialb'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('products', args=(28,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_product_details_get_admin(self):
        #Probamos que se puede acceder a los detalles de un producto
        print('test_product_details_get_admin')
        
        credentials = {'username': 'viclopvaz1', 'password': 'viclopvaz1'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('products', args=(28,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_product_edit_post(self):
        #Probamos que se puede editar los detalles de un producto
        print('test_product_edit_post')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        data={'name': 'Camiseta', 'description': 'Buena calidad', 'price': '1', 'select': 'Ropa'}
        form = ProductForm(data=data)
        # print(form)
        response = self.client.post(reverse('products', args=(28,)), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.is_valid())

    def test_product_edit_post_owner(self):
        #Probamos que no se puede editar los detalles de un producto de otra tienda
        print('test_product_edit_post_owner')
        
        credentials = {'username': 'Anlope', 'password': 'Contraseña-1'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        data={'name': 'Camiseta', 'description': 'Buena calidad', 'price': '2', 'select': 'Ropa'}
        response = self.client.post(reverse('products', args=(28,)), data=data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_product_edit_post_user(self):
        #Probamos que no se puede editar los detalles de un producto si eres usuario
        print('test_product_edit_post_user')
        
        credentials = {'username': 'josruialb', 'password': 'josruialb'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        data={'name': 'Camiseta', 'description': 'Buena calidad', 'price': '3', 'select': 'Ropa'}
        response = self.client.post(reverse('products', args=(28,)), data=data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_product_edit_post_admin(self):
        #Probamos que no se puede editar los detalles de un producto si eres administrador
        print('test_product_edit_post_admin')
        
        credentials = {'username': 'viclopvaz1', 'password': 'viclopvaz1'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        data={'name': 'Camiseta', 'description': 'Buena calidad', 'price': '4', 'select': 'Ropa'}
        form = ProductForm(data=data)
        response = self.client.post(reverse('products', args=(28,)), data=data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_product_post_delete_owner_t(self):
        #Probamos que se puede eliminar un producto
        print('test_product_delete')
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.post(reverse('product_delete', args=(28,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_product_post_delete_owner(self):
        #Probamos que no se puede eliminar un producto de otra tienda
        print('test_product_post_delete_owner')
        
        credentials = {'username': 'Anlope', 'password': 'Contraseña-1'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.post(reverse('product_delete', args=(28,)), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_product_post_delete_auser(self):
        #Probamos que no se puede eliminar un producto de una tienda si eres user
        print('test_product_post_delete_user')
        
        credentials = {'username': 'josruialb', 'password': 'josruialb'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.post(reverse('product_delete', args=(28,)), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_product_post_delete_admin(self):
        #Probamos que no se puede eliminar un producto de una tienda si eres admin
        print('test_product_post_delete_admin')
        
        credentials = {'username': 'viclopvaz1', 'password': 'viclopvaz1'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.post(reverse('product_delete', args=(28,)), follow=True)
        self.assertEqual(response.status_code, 403)