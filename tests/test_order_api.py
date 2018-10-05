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
        with self.app.app_context():
            self.auth_token = create_access_token(
                identity={'name': "Andrew.T", 'phone':'0785222293', 'email': "andrew@g.com", 'id': "1", 'admin': True})
            self.auth_token2 = create_access_token(
                identity={'name': "Joseph.H", 'phone':'0785222293', 'email': "joseph@g.com", 'id': "1", 'admin': False})
            self.headers = {'Authorization': 'Bearer {}'.format(self.auth_token)}
            self.headers2 = {'Authorization': 'Bearer {}'.format(self.auth_token2)}
        self.client = self.app.test_client

        self.URL = '/api/v2/'

        self.order_no_customer_order = {
            'customer_name': 'andrew',
            'customer_phone': '0782930481'
        }

        self.cust_order = [{'food': 'grasshopper pizza',
                            'price': 20000,
                            'quantity': 2},
                           {'food': 'rice&beans pizza',
                            'price': 12000,
                            'quantity': 1}]
        self.cust_order_food_missing = [{'price': 20000,
                                         'quantity': 2},
                                        {'food': 'rice&beans pizza',
                                         'price': 12000,
                                         'quantity': 1}]
        self.cust_order_price_missing = [{'food': 'grasshopper pizza',
                                          'price': 20000,
                                          'quantity': 2},
                                         {'food': 'rice&beans pizza',
                                          'price': 12000,
                                          'quantity': 1}]
        self.cust_order_quantity_missing = [{'food': 'grasshopper pizza',
                                             'price': 20000},
                                            {'food': 'rice&beans pizza',
                                             'price': 12000,
                                             'quantity': 1}]

    def post(self, data):
        # response from post request
        return self.client().post(self.URL+"orders/", json=data, headers=self.headers2)

    #ORDER SAVING
    def test_place_order_with_correct_data(self):
        """
        test saving an order with correct data
        """
        res = self.post(dict(customer_name='andrew',
                             customer_phone='0782930481', customer_order=self.cust_order))

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('success'),
                         "Order placed successfully!")
        self.assertEqual(res.status_code, 201)

    def test_place_order_with_missing_customer_name(self):
        """
        test saving an order with missing customer_name param
        """
        res = self.post(dict(customer_phone='0782930481',
                             customer_order=self.cust_order))

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get(
            'error'), "Missing customer_name parameter. List of required: customer_name, customer_phone, customer_order")
        self.assertEqual(res.status_code, 400)

    def test_place_order_with_missing_customer_phone(self):
        """
        test saving an order with missing customer_phone param
        """
        res = self.post(dict(customer_name='andrew',
                             customer_order=self.cust_order))

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get(
            'error'), "Missing customer_phone parameter. List of required: customer_name, customer_phone, customer_order")
        self.assertEqual(res.status_code, 400)

    def test_place_order_with_missing_customer_order(self):
        """
        test saving an order with missing customer_order param
        """
        res = self.post(dict(customer_name='andrew',
                             customer_phone='0782930481'))

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get(
            'error'), "customer_order is missing or empty. List of required: customer_name, customer_phone, customer_order")
        self.assertEqual(res.status_code, 400)

    # def test_place_order_with_empty_customer_name(self):
    #     """
    #     test saving an order with empty customer_name param
    #     """
    #     res = self.client().post(self.URL+"orders/",
    #                              json=dict(customer_name='  ', customer_phone='0782930481',
    #                                        customer_order=self.cust_order))

    #     json_res_data = json.loads(res.data)
    #     self.assertEqual(json_res_data.get('error'),
    #                      "customer_name cannot be empty")
    #     self.assertEqual(res.status_code, 400)

    # def test_place_order_with_empty_customer_phone(self):
    #     """
    #     test saving an order with empty customer_phone param
    #     """
    #     res = self.client().post(self.URL+"orders/",
    #                              json=dict(customer_name='andrew', customer_phone='    ',
    #                                        customer_order=self.cust_order))

    #     json_res_data = json.loads(res.data)
    #     self.assertEqual(json_res_data.get('error'),
    #                      "customer_phone cannot be empty")
    #     self.assertEqual(res.status_code, 400)

    def test_place_order_with_empty_customer_order(self):
        """
        test saving an order with empty customer_order param
        """
        res = self.client().post(self.URL+"orders/",
                                 json=dict(customer_name='andrew', customer_phone='0782930481', customer_order=[]), headers=self.headers2)

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'),
                         "customer_order is missing or empty. List of required: customer_name, customer_phone, customer_order")
        self.assertEqual(res.status_code, 400)

    #GET ALL ORDERS
    def test_get_all_orders_no_orders_saved(self):
        """
        test saving an order with empty customer_order param
        """
        res = self.client().get(self.URL+"orders/", headers=self.headers)
        json_res_data = json.loads(res.data)

        self.assertEqual(json_res_data.get('info'), "No orders placed yet")
        self.assertEqual(res.status_code, 200)

    def test_get_all_orders(self):
        """
        test getting all orders
        """
        self.post_sample_orders()

        res = self.client().get(self.URL+"orders/", headers=self.headers)
        self.assertEqual(res.status_code, 200)

    #FIND SPECIFIC ORDER
    def test_get_specific_order(self):
        """
        test get specific order using order id
        """
        self.post_sample_orders()

        res = self.client().get(self.URL+"orders/1", headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_get_specific_order_failed(self):
        """
        test get specific order fail using order id
        """
        self.post_sample_orders()

        res = self.client().get(self.URL+"orders/5", headers=self.headers)
        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'),
                         "No order found with id: 5")
        self.assertEqual(res.status_code, 404)

    #STATUS UPDATE
    def test_successful_update_order_status(self):
        """
        test update order_status successfully
        """
        self.post_sample_orders()

        res = self.client().put(self.URL+"orders/1",
                                json=dict(status='complete'), headers=self.headers)
        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('success'),
                         "Order status was changed successfully!")
        self.assertEqual(res.status_code, 201)

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

    def test_empty_or_no_order_status_update_supplied(self):
        """
        test correct feedback when status update is not supplied
        """
        self.post_sample_orders()

        res = self.client().put(self.URL+"orders/2", json=dict(), headers=self.headers)
        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'),
                         "'status' parameter not supplied")
        self.assertEqual(res.status_code, 400)

    def post_sample_orders(self):
        self.client().post(self.URL+"orders/",
                           json=dict(customer_name='andrew',
                                     customer_phone='0782930481',
                                     customer_order=self.cust_order),
                           headers=self.headers)
        self.client().post(self.URL+"orders/",
                           json=dict(customer_name='jospeh',
                                     customer_phone='0782930481',
                                     customer_order=self.cust_order),
                           headers=self.headers)
        self.client().post(self.URL+"orders/",
                           json=dict(customer_name='karungi',
                                     customer_phone='0782930481',
                                     customer_order=self.cust_order),
                           headers=self.headers)

    def tearDown(self):
        """
        Tear Down method used to reset orders variable
        """
        with self.app.app_context():
            self.db.delete_data_from_all_tables()
            del self.db
