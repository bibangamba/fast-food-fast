#tests/test_order_api

import unittest
import os
import json

import psycopg2

from app.app import create_app
from app.models import OrderModel
from app import APP
from app.db_helper import DatabaseConnectionHelper
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)


class OrderTest(unittest.TestCase):
    """
    order api endpoints TestCase
    """
    # APP.config['TESTING'] = True

    def setUp(self):
        """
        Test setup
        """
        self.app = create_app("testing")
        APP.config = self.app.config
        self.db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        self.db.create_all_tables()
        #insert non-admin user into db
        self.db.insert_user_into_db(
            {'name': 'Joseph.H', 'phone': '0785222293', 'email': 'joseph@g.com', 'password': 'blablabla'})
        with self.app.app_context():
            #we need the app context to access JWTManager app settings (so we can call create_access_token())
            self.admin_auth_token = create_access_token(
                identity={'name': "Andrew.T", 'phone': '0785222293', 'email': "andrew@g.com", 'id': "1", 'admin': True})
            self.non_admin_auth_token = create_access_token(
                identity={'name': "Joseph.H", 'phone': '0785222293', 'email': "joseph@g.com", 'id': "2", 'admin': False})
            self.headers = {'Authorization': 'Bearer {}'.format(
                self.admin_auth_token)}
            self.non_admin_headers = {'Authorization': 'Bearer {}'.format(
                self.non_admin_auth_token)}
        self.client = self.app.test_client

        self.URL = '/api/v2/'

    def post_users_orders(self, data):
        return self.client().post(self.URL+"users/orders/", json=data, headers=self.non_admin_headers)

    def post_auth_login(self, data):
        return self.client().post(self.URL + "auth/login", json=data)

    def post_auth_signup(self, data):
        return self.client().post(self.URL + "auth/signup", json=data)

    def post_sample_orders(self):
        self.client().post(self.URL+"users/orders/", json=dict(dict(customer_order=[{'food': 'grasshopper pizza', 'price': 23000, 'quantity': 1}])), headers=self.non_admin_headers)
        self.client().post(self.URL+"users/orders/", json=dict(dict(customer_order=[{'food': 'rice and beans pizza', 'price': 13000, 'quantity': 1}])), headers=self.headers)
        self.client().post(self.URL+"users/orders/", json=dict(dict(customer_order=[{'food': 'sweet potatoe flavored icecream', 'price': 6000, 'quantity': 1}])), headers=self.non_admin_headers)

    #LOGIN
    def test_user_login(self):
        res = self.post_auth_login(
            {'email': 'andrew@a.com', 'password': 'yurizahard'})
        self.assertIsNotNone(res.json.get('jwt_token'))
        self.assertEqual(res.json.get('success'),
                         'Successfully logged in as Andrew.T')
        self.assertEqual(res.status_code, 200)

    def test_user_login_invalid_password(self):
        res = self.post_auth_login(
            {'email': 'andrew@a.com', 'password': 'yurizahard2222'})

        self.assertIsNone(res.json.get('jwt_token'))
        self.assertEqual(res.json.get('error'),
                         'Email/Password authntication failed')
        self.assertEqual(res.status_code, 401)
        # "error": "

    def test_user_login_email_not_registered(self):
        res = self.post_auth_login(
            {'email': 'andrea@a.com', 'password': 'yurizahard'})

        self.assertIsNone(res.json.get('jwt_token'))
        self.assertEqual(res.json.get('error'),
                         'User with email: andrea@a.com is not registered')
        self.assertEqual(res.status_code, 401)

    def test_user_login_email_invalid(self):
        res = self.post_auth_login(
            {'email': 'andrea at a dot com', 'password': 'yurizahard'})

        self.assertIsNone(res.json.get('jwt_token'))
        self.assertEqual(res.json.get(
            'error'), 'Supplied email parameter is not a valid email format. Must contain an @')
        self.assertEqual(res.status_code, 400)

    def test_user_login_empty_email(self):
        res = self.post_auth_login(
            {'email': '', 'password': 'yurizahard'})
        self.assertIsNone(res.json.get('jwt_token'))
        self.assertEqual(res.json.get('error'),
                         'Email parameter cannot be empty')
        self.assertEqual(res.status_code, 400)

    def test_user_login_empty_password(self):
        res = self.post_auth_login(
            {'email': 'andrew@a.com', 'password': ''})
        self.assertIsNone(res.json.get('jwt_token'))
        self.assertEqual(res.json.get('error'),
                         'Password cannot be an empty string')
        self.assertEqual(res.status_code, 400)

    def test_user_login_missing_email_param(self):
        res = self.post_auth_login(
            {'password': 'yurizahard'})
        self.assertIsNone(res.json.get('jwt_token'))
        self.assertEqual(res.json.get('error'), 'Missing email parameter')
        self.assertEqual(res.status_code, 400)

    def test_user_login_missing_password_param(self):
        res = self.post_auth_login(
            {'email': 'andrew@a.com'})
        self.assertIsNone(res.json.get('jwt_token'))
        self.assertEqual(res.json.get('error'),
                         'Missing password parameter is required')
        self.assertEqual(res.status_code, 400)

    #SIGNUP
    def test_user_signup(self):
        """
        test user signup with all parameters correct
        """
        res = self.post_auth_signup({"name": "Joel.T", "email": "joel@a.com",
                                     "phone": "0312910481", "password": "blablabla", "confirm_password": "blablabla"})
        self.assertEqual(res.json.get('saved_user').get('email'), 'joel@a.com')
        self.assertEqual(res.json.get('success'),'User was successfully created')
        self.assertEqual(res.status_code, 201)

    def test_user_signup_missing_name_param(self):
        """
        test user signup  with missing name parameter
        """
        res = self.post_auth_signup({"email": "joel@a.com",
                                     "phone": "0312910481", "password": "blablabla", "confirm_password": "blablabla"})
        self.assertEqual(res.json.get('error'),'Missing name parameter. It is required.')
        self.assertEqual(res.status_code, 400)
        
    def test_user_signup_missing_email_param(self):
        """
        test user signup  with missing email parameter
        """
        res = self.post_auth_signup({"name": "Joel.T", "phone": "0312910481", "password": "blablabla", "confirm_password": "blablabla"})
        self.assertEqual(res.json.get('error'),'Missing email parameter. It is required.')
        self.assertEqual(res.status_code, 400)
    
    def test_user_signup_missing_phone_param(self):
        """
        test user signup  with missing phone parameter
        """
        res = self.post_auth_signup({"name": "Joel.T", "email": "joel@a.com",
                                     "password": "blablabla", "confirm_password": "blablabla"})
        self.assertEqual(res.json.get('error'),'Missing phone parameter. It is required.')
        self.assertEqual(res.status_code, 400)
    
    def test_user_signup_missing_password_param(self):
        """
        test user signup  with missing password parameter
        """
        res = self.post_auth_signup({"name": "Joel.T", "email": "joel@a.com",
                                     "phone": "0312910481", "confirm_password": "blablabla"})
        self.assertEqual(res.json.get('error'),'Missing password parameter. It is required.')
        self.assertEqual(res.status_code, 400)

    def test_user_signup_missing_confirm_password_param(self):
        """
        test user signup  with missing confirm_password parameter
        """
        res = self.post_auth_signup({"name": "Joel.T", "email": "joel@a.com",
                                     "phone": "0312910481", "password": "blablabla"})
        self.assertEqual(res.json.get('error'),'Missing confirm_password parameter. It is required.')
        self.assertEqual(res.status_code, 400)
    # TODO: add more validation tests once other endpoints later (after all endpoints have some coverage)

    #ORDER SAVING
    def test_place_order(self):
        """
        test saving an order with valid data
        """
        # res = self.post_users_orders(dict(customer_order=self.cust_order))
        res = self.post_users_orders(dict(customer_order=[{'food': 'grasshopper pizza', 'price': 20000, 'quantity': 2}]))
        self.assertIsNotNone(res.json.get('saved_order'))
        self.assertEqual(res.json.get('success'),
                         "Order placed successfully!")
        self.assertEqual(res.status_code, 201)
    
    def test_place_order_missing_customer_order(self):
        """
        test saving an order with missing customer order
        """
        res = self.post_users_orders(dict(customer5_order5=[{'food': 'grasshopper pizza', 'price': 20000, 'quantity': 2}]))
        self.assertEqual(res.json.get('error'),
                         "Missing customer_order parameter. It is required.")
        self.assertEqual(res.status_code, 400)
    
    def test_place_order_missing_food_param_in_customer_order(self):
        """
        test saving an order with missing food param in customer order
        """
        res = self.post_users_orders(dict(customer_order=[{'fo222od': 'grasshopper pizza', 'price': 20000, 'quantity': 2}]))
        self.assertEqual(res.json.get('error'),
                         "Missing food parameter in {'fo222od': 'grasshopper pizza', 'price': 20000, 'quantity': 2}. It is required")
        self.assertEqual(res.status_code, 400)
    
    def test_place_order_missing_price_param_in_customer_order(self):
        """
        test saving an order with missing price param in customer order
        """
        res = self.post_users_orders(dict(customer_order=[{'food': 'grasshopper pizza', 'pryyice': 20000, 'quantity': 2}]))
        self.assertEqual(res.json.get('error'),
                         "Missing price parameter in {'food': 'grasshopper pizza', 'pryyice': 20000, 'quantity': 2}. It is required")
        self.assertEqual(res.status_code, 400)
    
    def test_place_order_missing_quantity_param_in_customer_order(self):
        """
        test saving an order with missing quantity param in customer order
        """
        res = self.post_users_orders(dict(customer_order=[{'food': 'grasshopper pizza', 'price': 20000, 'quwwwantity': 2}]))
        self.assertEqual(res.json.get('error'),
                         "Missing quantity parameter in {'food': 'grasshopper pizza', 'price': 20000, 'quwwwantity': 2}. It is required")
        self.assertEqual(res.status_code, 400)
    # TODO: add more validation tests to check for empty or zero values


    #GET ALL ORDERS
    def test_get_all_orders(self):
        """
        test getting all orders
        """
        self.post_sample_orders()

        res = self.client().get(self.URL+"orders/", headers=self.headers)

        self.assertEqual(res.status_code, 200)
    
    def test_get_all_orders_not_admin(self):
        """
        test getting all orders when not an admin user
        """
        self.post_sample_orders()
        res = self.client().get(self.URL+"orders/", headers=self.non_admin_headers)

        self.assertEqual(res.json.get('error'), 'You do not have enough permissions to access this endpoint')
        self.assertEqual(res.status_code, 401)

    def test_get_all_orders_no_orders_saved(self):
        """
        test get all orders but no orders placed yet
        """
        res = self.client().get(self.URL+"orders/", headers=self.headers)

        self.assertEqual(res.json.get('info'), "No orders placed yet")
        self.assertEqual(res.status_code, 200)


    #FIND SPECIFIC ORDER
    def test_get_specific_order(self):
        """
        test get specific order using order id
        """
        self.post_sample_orders()

        res = self.client().get(self.URL+"orders/1", headers=self.headers)
        self.assertEqual(res.status_code, 200)
    
    def test_get_specific_order_that_does_not_exist(self):
        """
        test get specific order that doesn't exist
        """
        self.post_sample_orders()

        res = self.client().get(self.URL+"orders/5", headers=self.headers)
        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'),
                         "No order found with id: 5")
        self.assertEqual(res.status_code, 404)
    
    def test_get_specific_order_but_not_admin(self):
        """
        test get specific order but not admin
        """
        self.post_sample_orders()

        res = self.client().get(self.URL+"orders/1", headers=self.non_admin_headers)
        
        self.assertEqual(res.json.get('error'),
                         'You do not have enough permissions to access this endpoint')
        self.assertEqual(res.status_code, 401)

     #USER ORDER HISTORY
    def test_get_current_user_order_history(self):
        """
        test get order history
        """
        self.post_sample_orders()

        res = self.client().get(self.URL+"users/orders/", headers=self.headers)
        self.assertEqual(res.status_code, 200)

    #ORDER STATUS UPDATE
    def test_update_order_status(self):
        """
        test update order_status successfully
        """
        self.post_sample_orders()

        res = self.client().put(self.URL+"orders/1",
                                json=dict(status='complete'), headers=self.headers)
        
        self.assertEqual(res.json.get('success'),
                         "Order status was changed successfully!")
        self.assertEqual(res.status_code, 200)
    
    def test_update_order_status_order_does_not_exist(self):
        """
        test update order_status successfully
        """
        self.post_sample_orders()

        res = self.client().put(self.URL+"orders/5",
                                json=dict(status='complete'), headers=self.headers)
        
        self.assertEqual(res.json.get('error'),
                         'No order found with id: 5')
        self.assertEqual(res.status_code, 404)

    def test_invalid_order_status_update(self):
        """
        test feedback when supplied status is invalid (not one of: new, processing, cancelled, or complete)
        """
        self.post_sample_orders()

        res = self.client().put(self.URL+"orders/2",
                                json=dict(status='blah'), headers=self.headers)
        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'),
                         "'status' can only be one of these options: new, processing, cancelled, or complete")
        self.assertEqual(res.status_code, 400)

    def test_status_update_no_status(self):
        """
        test correct feedback when status update is not supplied
        """
        self.post_sample_orders()

        res = self.client().put(self.URL+"orders/2", json=dict(), headers=self.headers)
        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'),
                         "'status' parameter not supplied")
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        """
        Tear Down method used to reset orders variable
        """
        with self.app.app_context():
            self.db.delete_data_from_all_tables()
            del self.db
