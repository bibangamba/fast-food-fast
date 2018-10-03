# app/model.py
import os

import psycopg2
from psycopg2.extras import Json, DictCursor
import datetime
from flask import json


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
    print("######################### flask_env: ", os.getenv('FLASK_ENV'))
    if (os.getenv('FLASK_ENV')=="testing"):
        connection = psycopg2.connect(os.getenv('TEST_DATABASE_URI'))
    else:
        connection = psycopg2.connect(os.getenv('DATABASE_URI'))

    cursor = connection.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS orders(
        id serial PRIMARY KEY,
        customer_name varchar,
        customer_phone varchar(15),
        customer_order jsonb,
        order_status varchar(20),
        order_date_utc timestamp)
    """
    )
    connection.commit()
    cursor.close()
    connection.close()

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
        append order from passed in parameter to the orders list
        """
        print("######################### flask_env: ", os.getenv('FLASK_ENV'))
        if (os.getenv('FLASK_ENV')=="testing"):
            connection = psycopg2.connect(os.getenv('TEST_DATABASE_URI'))
        else:
            connection = psycopg2.connect(os.getenv('DATABASE_URI'))
        cursor = connection.cursor()
        query = """
            INSERT INTO orders (
                customer_name,
                customer_phone,
                customer_order,
                order_status,
                order_date_utc) VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """
        cursor.execute(query, (order.get('customer_name'),
                               order.get('customer_phone'),
                               Json(order.get('customer_order')),
                               order.get('order_status'),
                               order.get('order_date')))
        connection.commit()

        #get the id for just the inserted/placed order
        order['id'] =  cursor.fetchone()[0]

        cursor.close()
        connection.close()
        
        return order

    @classmethod
    def get_all_orders(cls):
        """
        return the orders list
        """
        organized_order_list = []
        print("######################### flask_env: ", os.getenv('FLASK_ENV'))
        if (os.getenv('FLASK_ENV')=="testing"):
            connection = psycopg2.connect(os.getenv('TEST_DATABASE_URI'))
        else:
            connection = psycopg2.connect(os.getenv('DATABASE_URI'))
        # connection=psycopg2.connect(os.getenv('DATABASE_URI'))

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders")

        orders = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

        for order in orders:
            organized_order = {}
            organized_order['id'] = order[0]
            organized_order['customer_name'] = order[1]
            organized_order['customer_phone'] = order[2]
            organized_order['customer_order'] = order[3]
            organized_order['order_status'] = order[4]
            organized_order['order_date'] = order[5]
            organized_order_list.append(organized_order)
        return organized_order_list

    @classmethod
    def get_specific_order(cls, id):
        """
        search for order with matching id in orders list
        return the order if one is found
        return None if no order matched the id passed in as a parameter
        """
        # connection = psycopg2.connect(os.getenv('DATABASE_URI'))
        print("######################### flask_env: ", os.getenv('FLASK_ENV'))
        if (os.getenv('FLASK_ENV')=="testing"):
            connection = psycopg2.connect(os.getenv('TEST_DATABASE_URI'))
        else:
            connection = psycopg2.connect(os.getenv('DATABASE_URI'))

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = {}".format(id))

        order = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        if order is not None:
            order_organized = {}
            order_organized['id'] = order[0]
            order_organized['customer_name'] = order[1]
            order_organized['customer_phone'] = order[2]
            order_organized['customer_order'] = order[3]
            order_organized['order_status'] = order[4]
            order_organized['order_date'] = order[5]
            return order_organized
        else:
            return order

    @classmethod
    def update_order_status(cls, id, order_status):
        """
        search for order with matching id in orders list
        replace the order_status with supplied order_status from params
        """

        if cls.get_specific_order(id) is not None:
            connection = psycopg2.connect(os.getenv('DATABASE_URI'))

            cursor = connection.cursor()
            cursor.execute("UPDATE orders SET order_status = %s WHERE id = %s;", (order_status, id))
            connection.commit()
            cursor.close()
            connection.close()

            order = cls.get_specific_order(id)
            return order
        else:
            return None

    def to_dictionary(self):
        """
        convert order object to dictionary
        """
        #this will the order a dictionary which is JSON serializable
        return self.__dict__
