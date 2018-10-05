# app/model.py
import os

import psycopg2
from psycopg2.extras import Json, DictCursor
import datetime
from flask import json
from .db_helper import DatabaseConnectionHelper
from app import APP


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
        if cls.get_specific_order(id) is not None:
            db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
            updated_order = db.update_order_status_in_db(id, order_status)
            del db
            return updated_order
        else:
            return None

    def to_dictionary(self):
        """
        convert order object to dictionary
        """
        #this will the order a dictionary which is JSON serializable
        return self.__dict__


class UserModel():
    """
    User Model
    """

    def __init__(self, data):
        """
        user example ->
            id: int
            name: andrew bibangamba
            email: andrew@g.com
            phone: 0782930481
            password: hash
        """

        self.name = data.get('name')
        self.email = data.get('email')
        self.phone = data.get('phone')
        self.admin = False
        self.password = data.get('password')

    @classmethod
    def add_user(cls, user):
        """
        insert user into the database
        """
        db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        user = db.insert_user_into_db(user)
        del db
        return user

    @classmethod
    def get_user_by_id(cls, id):
        """
        search for user with matching id
        """
        db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        user = db.find_user_in_db_using_id(id)
        return user

    @classmethod
    def get_user_by_email(cls, email):
        """
        search for user with matching email
        """
        db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        user = db.find_user_in_db_using_email(email)
        return user

    @classmethod
    def update_user_role(cls, email, role):
        """
        update the user's role
        """
        if cls.get_user_by_email(email) is not None:
            db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
            updated_order = db.update_user_role_in_db(email, role)
            del db
            return updated_order
        else:
            return None

    def to_dictionary(self):
        """
        convert order object to dictionary
        """
        #this will the order a dictionary which is JSON serializable
        return self.__dict__


class MenuModel():
    """
    Menu Model
    """

    def __init__(self, data):
        """
        user example ->
            id: int
            food_name: "grasshoppers pizza"
            price: 12000
            food_description: "grasshoppers pizza is amazing. just imagine it, how can it not be awesome"
        """
        self.food_name = data.get('food_name')
        self.food_description = data.get('food_description')
        self.price = data.get('price')

    @classmethod
    def add_menu_item(cls, menu_item):
        """
        insert user into the database
        """
        db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        menu_item = db.insert_menu_item_into_db(menu_item)
        del db
        return menu_item

    @classmethod
    def get_menu_item_by_id(cls, menu_item_id):
        """
        search for user with matching id
        """
        db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        menu_item = db.find_menu_item_in_db_using_id(menu_item_id)
        return menu_item
    
    @classmethod
    def get_menu_item_by_food_name(cls, food_name):
        """
        search for user with matching id
        """
        db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        menu_item = db.find_menu_item_in_db_using_food_name(food_name)
        return menu_item

    @classmethod
    def get_all_menu_items(cls):
        """
        search for user with matching id
        """
        db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
        all_menu_items = db.get_all_menu_items_from_db()
        return all_menu_items

    @classmethod
    def update_menu_item_price_from_id(cls, price, menu_item_id):
        """
        update the menu_item's price
        """
        if cls.get_menu_item_by_id(menu_item_id) is not None:
            #check
            db = DatabaseConnectionHelper(APP.config['DATABASE_URI'])
            updated_order = db.update_menu_item_price_in_db(
                menu_item_id, price)
            del db
            return updated_order
        else:
            return None

    def to_dictionary(self):
        """
        convert order object to dictionary
        """
        #this will the order a dictionary which is JSON serializable
        return self.__dict__
