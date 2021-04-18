from django.test import TestCase,Client
import unittest
import requests
import json
import sys

class TestMethods(unittest.TestCase):

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
        #Probamos que el usuario se puede registrar de forma correcta.
        
        credentials = {"username": 'USER-0', "password": 'PASS-0'}
        
        url = "http://127.0.0.1:9000/login/"
        # url = "https://citra-ispp.herokuapp.com/login/"
        
        c = Client()
        r = c.post(url, credentials)

        self.assertEqual(r.status_code, 200)

