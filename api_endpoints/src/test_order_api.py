import unittest
import os
import json

from .app import create_app


class OrderTest(unittest.TestCase):
    """
    order api endpoints TestCase
    """

    def setUp(self):
        """
        Test setup
        """
        self.app = create_app("testing")
        self.client = self.app.test_client

        self.URL = '/api/v1/orders/'

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

    #ORDER SAVING
    def test_place_order_with_correct_data(self):
        """
        test saving an order with correct data
        """
        res = self.client().post(self.URL,
                                 data=dict(customer_name='andrew',
                                           customer_phone='0782930481',
                                           customer_order=str(self.cust_order)))

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('success'),
                         "Order placed successfully!")
        self.assertEqual(res.status_code, 201)

    def test_place_order_with_missing_customer_name(self):
        """
        test saving an order with missing customer_name param
        """
        res = self.client().post(self.URL,
                                 data=dict(customer_phone='0782930481',
                                           customer_order=str(self.cust_order)
                                           ))

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get(
            'error'), "Missing customer_name parameter. List of required: customer_name, customer_phone, customer_order")
        self.assertEqual(res.status_code, 400)

    def test_place_order_with_missing_customer_phone(self):
        """
        test saving an order with missing customer_phone param
        """
        res = self.client().post(self.URL,
                                 data=dict(customer_name='andrew',
                                           customer_order=str(self.cust_order)))

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get(
            'error'), "Missing customer_phone parameter. List of required: customer_name, customer_phone, customer_order")
        self.assertEqual(res.status_code, 400)

    def test_place_order_with_missing_customer_order(self):
        """
        test saving an order with missing customer_order param
        """
        res = self.client().post(self.URL,\
                                 #  headers={'Content-Type': 'application/json'},\
                                 data=dict(customer_name='andrew', customer_phone='0782930481'))
        #  data=json.dumps(self.order_no_customer_order))
        # print("############self.order_no_customer_order ",self.order_no_customer_order," #############")
        # print("############json.dumps ",json.dumps(self.order_no_customer_order)," #############")

        # json_data=json.loads(res.data)
        print("############res ", res, " #############")
        print("############res data ", res.data, " #############")
        print("############json_res_data ",
              json.loads(res.data), " #############")
        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get(
            'error'), "Missing customer_order parameter. List of required: customer_name, customer_phone, customer_order")
        self.assertEqual(res.status_code, 400)

    def test_place_order_with_empty_customer_name(self):
        """
        test saving an order with empty customer_name param
        """
        res = self.client().post(self.URL,
                                 data=dict(customer_name='  ', customer_phone='0782930481',
                                           customer_order=str(self.cust_order)))

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'),
                         "customer_name must be a non empty string")
        self.assertEqual(res.status_code, 400)

    def test_place_order_with_empty_customer_phone(self):
        """
        test saving an order with empty customer_phone param
        """
        res = self.client().post(self.URL,
                                 data=dict(customer_name='andrew', customer_phone='    ',
                                           customer_order=str(self.cust_order)))

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'),
                         "customer_phone must not be empty")
        self.assertEqual(res.status_code, 400)

    def test_place_order_with_empty_customer_order(self):
        """
        test saving an order with empty customer_order param
        """
        res = self.client().post(self.URL,
                                 data=dict(customer_name='andrew', customer_phone='0782930481', customer_order='  '))

        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'),
                         "customer_order cannot be empty")
        self.assertEqual(res.status_code, 400)

    #GET ALL ORDERS
    # def test_get_all_orders_no_orders_saved(self):
    #     """
    #     test saving an order with empty customer_order param
    #     """
    #     res = self.client().get(self.URL)
    #     json_res_data = json.loads(res.data)
    #     print("############# ", json_res_data)
    #     self.assertEquals(json_res_data.get('info'), "No orders placed yet")
    #     self.assertEqual(res.status_code, 200)

    def test_get_all_orders(self):
        """
        test getting all orders
        """
        self.client().post(self.URL,
                           data=dict(customer_name='andrew',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))
        self.client().post(self.URL,
                           data=dict(customer_name='jospeh',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))
        self.client().post(self.URL,
                           data=dict(customer_name='karungi',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))
        res = self.client().get(self.URL)
        self.assertEqual(res.status_code, 200)

    #FIND SPECIFIC ORDER
    def test_get_specific_order(self):
        """
        test get specific order using order id
        """
        self.client().post(self.URL,
                           data=dict(customer_name='andrew',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))
        self.client().post(self.URL,
                           data=dict(customer_name='jospeh',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))
        self.client().post(self.URL,
                           data=dict(customer_name='karungi',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))

        # res = self.client().get('{}{}'.format(self.URL, 3))
        res = self.client().get(self.URL+'3')
        self.assertEqual(res.status_code, 200)

    def test_get_specific_order_failed(self):
        """
        test get specific order fail using order id
        """
        self.client().post(self.URL,
                           data=dict(customer_name='andrew',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))
        self.client().post(self.URL,
                           data=dict(customer_name='jospeh',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))
        self.client().post(self.URL,
                           data=dict(customer_name='karungi',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))

        res = self.client().get(self.URL+'23')
        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'), "No order found with id: 23")
        self.assertEqual(res.status_code, 404)

    #STATUS UPDATE
    def test_successful_update_order_status(self):
        """
        test update order_status successfully
        """
        self.client().post(self.URL,
                           data=dict(customer_name='andrew',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))
        self.client().post(self.URL,
                           data=dict(customer_name='jospeh',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))
        self.client().post(self.URL,
                           data=dict(customer_name='karungi',
                                     customer_phone='0782930481',
                                     customer_order=str(self.cust_order)))

        res = self.client().put(self.URL+'2', data=dict(status='accepted'))
        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('success'), "Order status was changed successfully!")
        self.assertEqual(res.status_code, 201)
    
    def test_fail_update_order_status(self):
        """
        test update order_status rejection
        """
        res = self.client().put(self.URL+'55', data=dict(status='accepted'))
        json_res_data = json.loads(res.data)
        self.assertEqual(json_res_data.get('error'), "No order found with id: 55")
        self.assertEqual(res.status_code, 404)
