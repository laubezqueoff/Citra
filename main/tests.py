from django.test import TestCase,Client
import unittest
import requests
import json
import sys
from django.urls import reverse


class TestMethods(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()


    #Es importante que se ejecute primero este test. Los test se ejecutan por orden alfabéico.
    
    def test_login(self):
        #Probamos que el usuario se puede registrar de forma correcta.
        
        credentials = {"username": 'USER-0', "password": 'PASS-0'}
        
        url = "http://127.0.0.1:9000/login/"
        # url = "https://citra-ispp.herokuapp.com/login/"
        
        c = Client()
        r = c.post(url, credentials)

        self.assertEqual(r.status_code, 200)


    
    def test_logout(self):
        #Probamos que el usuario puede hacer logout de forma correcta.
        
        credentials = {"username": 'USER-0', "password": 'PASS-0'}
        
        url = "http://127.0.0.1:9000/login/"
        
        c = Client()
        r = c.post(url, credentials)

        self.assertEqual(r.status_code, 200)


 ########################################################    TEST DE CHATS    ####################################################
    def test_new_chat_get(self):
        #Probamos que se puede acceder a un chat con una tienda con la que todavia no ha hablado
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
        
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
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