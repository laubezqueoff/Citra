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

    print("=========activar-tienda")
    def test_sus_post_existe(self):
        print('test_sus_post_existe')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('activate_shop', args=(0,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 403)

    def test_sus_post_404(self):
        print('test_sus_post_existe')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('activate_shop', args=(4239823457,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 404)
    print("=========promocion-mensual")

    def test_sus_post_mon_existe(self):
        print('test_sus_post_mon_existe')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('promotion_month_shop', args=(0,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 403)

    def test_sus_post_mon_404(self):
        print('test_sus_post_mon_404')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('promotion_month_shop', args=(4239823457,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 404)

    print("=========suscripcion-trimestral")
    def test_sus_post_3mon_existe(self):
        print('test_sus_post_3mon_existe')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('activate_shop_three_months', args=(0,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 403)

    def test_sus_post_3mon_404(self):
        print('test_sus_post_3mon_404')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('activate_shop_three_months', args=(4239823457,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 404)
    
    print("=========promocion-shop-semanal")

    def test_promotion_week_shop_existe(self):
        print('test_promotion_week_shop_existe')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('promotion_week_shop', args=(0,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 403)

    def test_promotion_week_shop_404(self):
        print('test_promotion_week_shop_404')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('promotion_week_shop', args=(4239823457,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 404)

    def test_activate_shop_one_year_existe(self):
        print('test_activate_shop_one_year_existe')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('activate_shop_one_year', args=(0,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 403)

    def test_activate_shop_one_year_404(self):
        print('test_activate_shop_one_year_404')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('activate_shop_one_year', args=(4239823457,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 404)

    def test_promotion_month_product_existe(self):
        print('test_promotion_month_product_existe')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('promotion_month_product', args=(0,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 403)

    def test_promotion_month_product_404(self):
        print('test_promotion_month_product_404')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('promotion_month_product', args=(4239823457,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 404)

    def test_promotion_week_product_existe(self):
        print('test_promotion_week_product_existe')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('promotion_week_product', args=(0,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 403)

    def test_promotion_week_product_404(self):
        print('test_promotion_week_product_404')
        
        credentials = {'username': 'Magarcia', 'password': 'Magarcia'}
        
        r = self.client.post(reverse('login'), data=credentials, follow=True)
        self.assertEqual(r.status_code, 200)
        response = self.client.post(reverse('promotion_week_product', args=(4239823457,)), follow=True)    # for second object
        self.assertEqual(response.status_code, 404)



