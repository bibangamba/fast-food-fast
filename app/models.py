# app/model.py
import os

import psycopg2
from psycopg2.extras import Json, DictCursor
import datetime
from flask import json
from .db_helper import DatabaseConnectionHelper
from app import APP


#create the multiple tables needed
"""
USERS
- email
- name
- phone
- password
- id
"""


class OrderModel():
    """
    Order Model
    """

    def __init__(self, data):
        """
        order example ->
            id: int
            order_status: status
            customer_name: andrew
            customer_phone: 0782930481
            customer_order: [
                {'food':'grasshopper pizza', 
                    'quantity':'2', 
                    'price':'20000'},
                {'food':'rice and beans pizza', 
                    'quantity':'1', 
                    'price':'13000'}

                ]
        """

        self.customer_name = data.get('customer_name')
        self.customer_phone = data.get('customer_phone')
        self.customer_order = data.get('customer_order')
        self.order_status = 'new'
        self.order_date = datetime.datetime.utcnow()

    @classmethod
    def place_order(cls, order):
        """
        insert order into database
        """
        db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        order = db.insert_order_into_db(order)
        del db 
        return order

    @classmethod
    def get_all_orders(cls):
        """
        return the orders list
        """
        db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        orders = db.get_all_orders_from_db()
        del db
        return orders

    @classmethod
    def get_specific_order(cls, id):
        """
        search for order with matching id in orders list
        return the order if one is found
        return None if no order matched the id passed in as a parameter
        """
        db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        order = db.get_order_from_db(id)
        return order
        

    @classmethod
    def update_order_status(cls, id, order_status):
        """
        search for order with matching id in orders list
        replace the order_status with supplied order_status from params
        """
        order = {}
        if cls.get_specific_order(id) is not None:
            db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
            updated_order = db.update_order_status_in_db(id, order_status)
            del db
            order = updated_order
        else:
            order = None
        return order

    def to_dictionary(self):
        """
        convert order object to dictionary
        """
        #this will the order a dictionary which is JSON serializable
        return self.__dict__
