# app/model.py
import datetime
from flask import json


class OrderModel():
    """
    Order Model
    """
    orders = []
    #testing orders list
    # orders = [
    #     {
    #         "id": 2,
    #         "customer_name": "andrew",
    #         "customer_phone": "0782930481",
    #         "customer_order": [
    #             {"food": "grasshopper pizza",
    #              "quantity": 2, "price": 20000},
    #             {"food": "rice and beans pizza",
    #              "quantity": 1, "price": 12000}
    #         ],
    #         "order_status": "pending"
    #     }
    # ]

    def __init__(self, data):
        """
        constructor
        data consists of ->
        id: int
        order_status: status
        customer_name: andrew
        customer_phone: 0782930481
        customer_order: [{
                'food':'grasshopper pizza', 
                'quantity':'2', 
                'price':'20000'
            }]
        """

        self.id = len(self.orders)+1
        self.customer_name = data.get('customer_name')
        self.customer_phone = data.get('customer_phone')
        self.customer_order = data.get('customer_order')
        self.order_status = 'pending'
        self.order_date = datetime.datetime.utcnow()

    @classmethod
    def place_order(cls, order):
        """
        append order from passed in parameter to the orders list
        """
        cls.orders.append(order)
        return order

    @classmethod
    def get_all_orders(cls):
        """
        return the orders list
        """
        return cls.orders

    @classmethod
    def get_specific_order(cls, id):
        """
        search for order with matching id in orders list
        return the order if one is found
        return None if no order matched the id passed in as a parameter
        """
        for order in cls.orders:
            if order['id'] == id:
                return order
        return None

    @classmethod
    def update_order_status(cls, id, order_status):
        """
        search for order with matching id in orders list
        replace the order_status with supplied order_status from params
        """
        for order in cls.orders:
            if order['id'] == id:
                order['order_status'] = order_status
                return order
        return None

    def to_dictionary(self):
        """
        convert order object to dictionary
        """
        #this will stop the TypeError: Object of type 'OrderModel' is not JSON serializable
        return self.__dict__
