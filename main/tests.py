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

    def test_chat_get_404(self):
        #Probamos que se puede acceder enviar un mensaje a un chat con una tienda con la que ha hablado antes
        print('test_chat_get_404')
        
        credentials = {'username': 'User-0', 'password': 'Pass-0'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.get(reverse('chat', args=(12345,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 404)

