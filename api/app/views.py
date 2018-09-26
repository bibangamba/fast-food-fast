#app/views.py

from flask import request, json, jsonify, Response, Blueprint
from .models import OrderModel

import ast

#create blueprint app
order_api = Blueprint('order_api', __name__,)


@order_api.route('/', methods=['POST'])
def place_new_order():
    """
    place new  order function
    """
    request_data = request.values

    if not request_data.get('customer_name'):
        return custom_response({"error": "Missing customer_name parameter. List of required: customer_name, customer_phone, customer_order"}, 400)
    if not request_data.get('customer_phone'):
        return custom_response({"error": "Missing customer_phone parameter. List of required: customer_name, customer_phone, customer_order"}, 400)
    if not request_data.get('customer_order'):
        return custom_response({"error": "Missing customer_order parameter. List of required: customer_name, customer_phone, customer_order"}, 400)

    #validate that param values are not empty
    customer_name = request_data.get('customer_name')
    if customer_name.strip() == '':
        return custom_response({"error": "customer_name must be a non empty string"}, 400)
    customer_phone = request_data.get('customer_phone')
    if customer_phone.strip() == '':
        return custom_response({"error": "customer_phone must not be empty"}, 400)
    customer_order = request_data.get('customer_order')
    if customer_order.strip() == '':
        return custom_response({"error": "customer_order cannot be empty"}, 400)

    # convert stringified array back into a literal
    customer_orders = ast.literal_eval(request_data.get('customer_order'))


    customer_order_format = "[{'food': 'grasshopper pizza', 'price': 20000, 'quantity': 2}, {'food': 'rice and beans pizza', 'price': 12000, 'quantity': 1}]"

    #validate customer order has food, price, and quantity fields
    for order_cust in customer_orders:
        if 'food' not in order_cust:
            return custom_response({"error": "Badly foramtted customer_order. Missing 'food' field in {}. correct format example for 'customer_order' is: {}".format(order_cust, customer_order_format)}, 400)
        if 'price' not in order_cust:
            return custom_response({"error": "Badly foramtted customer_order. Missing 'price' field in {}. correct format example for 'customer_order' is: {}".format(order_cust, customer_order_format)}, 400)
        if 'quantity' not in order_cust:
            return custom_response({"error": "Badly foramtted customer_order. Missing 'quantity' field in {}.. correct format example for 'customer_order' is: {}".format(order_cust, customer_order_format)}, 400)

    #validate customer order values
    for customer_order in customer_orders:
        #food
        if isinstance(customer_order.get('food'), str):
            if str(customer_order.get('food')).strip() == '':
                return custom_response({"error": "customer_order['food'] value must be a non empty string"}, 400)
        else:
                return custom_response({"error": "customer_order['food'] value must be a string, found in {}".format(customer_order)}, 400)

        #quantity
        if isinstance(customer_order.get('quantity'), int):
            if customer_order.get('quantity') < 1:
                return custom_response({"error": "customer_order['quantity'] value must be greater than 1. found in {}".format(customer_order)}, 400)
        else:
                return custom_response({"error": "customer_order['quantity'] value must an integer. found in {}".format(customer_order)}, 400)

        #price
        if isinstance(customer_order.get('price'), int):
            if customer_order.get('price') < 1:
                return custom_response({"error": "customer_order['price'] value must be greater than 1. found in {}".format(customer_order)}, 400)
        else:
                return custom_response({"error": "customer_order['price'] value must an integer. found in {}".format(customer_order)}, 400)


    # created new data object because request_data is immutable (couldn't change customer_order from string to array )
    data = {}
    data['customer_name'] = customer_name
    data['customer_phone'] = customer_phone
    # literal array from string version passed in
    data['customer_order'] = customer_orders
    order = OrderModel(data).to_dictionary()
    # order = OrderModel(request_data).to_dictionary()

    if not order:
        return custom_response({"error": "Failed to save order. Conversion to dict returned None"}, 500)

    OrderModel.place_order(order)
    return custom_response({"success": "Order placed successfully!", "saved_order": order}, 201)
    # return Response(mimetype='application/json', response=json.dumps({"success": "Order placed successfully!"}), status=201)


@order_api.route('/', methods=['GET'])
def get_all_orders():
    """
    get all orders function
    """
    orders = OrderModel.get_all_orders()
    if len(orders) == 0:
        return custom_response({"info": "No orders placed yet"}, 200)
    return custom_response(orders, 200)


@order_api.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    get specific order function
    """
    order = OrderModel.get_specific_order(order_id)

    if not order:
        return custom_response({"error": "No order found with id: %d" % order_id}, 404)
    return custom_response(order, 200)


@order_api.route('/<int:order_id>', methods=['PUT'])
def change_order_status(order_id):
    """
    get specific order function
    """
    new_order_status = request.values.get('status')
    if not new_order_status:
        return custom_response({"error": "'status' parameter not supplied"}, 400)
    if not isinstance(new_order_status, str):
        return custom_response({"error": "status parameter should be a string"}, 400)

    order = OrderModel.update_order_status(order_id, new_order_status)
    if not order:
        return custom_response({"error": "No order found with id: {}".format(order_id)}, 404)
    return custom_response({"success": "Order status was changed successfully!", "order": order}, 201)


def custom_response(res, status_code):
    """
    custom response function
    """
    # return Response(
    #     mimetype='application/json',
    #     response=json.dumps(res),
    #     status=status_code
    # )

    #use jsonify for pretty print in browser too
    return jsonify(res), status_code
