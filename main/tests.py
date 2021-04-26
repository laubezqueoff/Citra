from django.test import TestCase,Client
import unittest
import requests
import json
import sys
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from main.forms import ProductForm


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

    def test_new_chat_get(self):
        #Probamos que se puede acceder a un chat con una tienda con la que todavia no ha hablado
        print('test_new_chat_get')

        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('newChat', args=(1,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 200)


    def test_chat_post(self):
        #Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_chat_post')
        
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        data={'text': 'Hola'}
        response = self.client.post(reverse('chat', args=(0,)), data=data, follow=True)    # for second object
        self.assertEqual(response.status_code, 200)


    def test_chat_get(self):
        #Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_chat_get')
        
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('chat', args=(0,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 200)

    def test_chat_get_403(self):
        #Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_chat_get_403')
        
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('chat', args=(1,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 403)

    # def test_chat_get_404(self):
    #     #Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
    #     print('test_chat_get_404')
        
    #     credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
    #     r = self.client.post(reverse('login'), data=credentials, follow=True)
    #     self.assertEqual(r.status_code, 200)
    #     response = self.client.get(reverse('chat', args=(12345,)), follow=True)    # for second object
    #     self.assertEqual(response.status_code, 404)

    def test_new_product_get(self):
        #Probamos que se puede acceder a la vista de crear un producto

        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('product_create', args=(4,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_new_product_get_403_owner(self):
        #Probamos que no se puede acceder a la vista de crear un producto de otra tienda

        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('product_create', args=(1,)), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_new_product_get_403_user(self):
        #Probamos que no se puede acceder a la vista de crear un producto de otra tienda

        credentials = {'username': 'josruialb', 'password': 'josruialb'}
        
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('product_create', args=(1,)), follow=True)
        self.assertEqual(response.status_code, 403)

    def test_new_product_get_403_admin(self):
        #Probamos que no se puede acceder a la vista de crear un producto de otra tienda

        credentials = {'username': 'viclopvaz1', 'password': 'viclopvaz1'}
        
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('product_create', args=(1,)), follow=True)
        self.assertEqual(response.status_code, 403)

    # def test_new_product_post(self):
    #     #Probamos que se puede acceder crear un producto
        
    #     credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
    #     r = self.client.post(reverse('login'), data=credentials, follow=True)
    #     self.assertEqual(r.status_code, 200)

    #     with open('media\products\pantalon.jpg', 'rb') as fp:
    #         file = SimpleUploadedFile('pantalon', fp.read())
    #         data={'name': 'Pantalon', 'type': '1', 'price': '15', 'description': 'Pantalon de buena calidad', 'image': file}
    #         response = self.client.post(reverse('product_create', args=(4,)), data=data, follow=True)
    #         self.assertEqual(response.status_code, 200)

    # def test_new_product_post(self):
    #     #Probamos que se puede acceder crear un producto
        
    #     credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
    #     r = self.client.post(reverse('login'), data=credentials, follow=True)
    #     self.assertEqual(r.status_code, 200)

    #     # with open('wishlist.doc', 'rb') as fp:
    #     #     c.post('/customers/wishes/', {'name': 'fred', 'attachment': fp})
    #     with open('media\products\pantalon.jpg', 'rb') as fp:
    #         fp.name = 'pantalon'
    #         data={'name': 'Pantalon', 'type': '1', 'price': '15', 'description': 'Pantalon de buena calidad', 'image': fp}
    #         response = self.client.post(reverse('product_create', args=(4,)), data=data, follow=True)
    #         self.assertEqual(response.status_code, 200)

    def test_product_details_get(self):
        #Probamos que se puede acceder a los detalles de un producto
        
        credentials = {'username': 'micum', 'password': 'Contraseña-3'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('products', args=(28,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_product_details_get_user(self):
        #Probamos que se puede acceder a los detalles de un producto
        
        credentials = {'username': 'josruialb', 'password': 'josruialb'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('products', args=(28,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_product_details_get_admin(self):
        #Probamos que se puede acceder a los detalles de un producto
        
        credentials = {'username': 'viclopvaz1', 'password': 'viclopvaz1'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        response = self.client.get(reverse('products', args=(28,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_product_edit_post(self):
        #Probamos que se puede editar los detalles de un producto
        
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
        
        credentials = {'username': 'Anlope', 'password': 'Contraseña-1'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        data={'name': 'Camiseta', 'description': 'Buena calidad', 'price': '2', 'select': 'Ropa'}
        response = self.client.post(reverse('products', args=(28,)), data=data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_product_edit_post_user(self):
        #Probamos que no se puede editar los detalles de un producto
        
        credentials = {'username': 'josruialb', 'password': 'josruialb'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        data={'name': 'Camiseta', 'description': 'Buena calidad', 'price': '3', 'select': 'Ropa'}
        response = self.client.post(reverse('products', args=(28,)), data=data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_product_edit_post_admin(self):
        #Probamos que no se puede editar los detalles de un producto
        
        credentials = {'username': 'viclopvaz1', 'password': 'viclopvaz1'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)

        data={'name': 'Camiseta', 'description': 'Buena calidad', 'price': '4', 'select': 'Ropa'}
        form = ProductForm(data=data)
        response = self.client.post(reverse('products', args=(28,)), data=data, follow=True)
        self.assertEqual(response.status_code, 403)
