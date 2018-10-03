#app/views.py

from flask import request, json, jsonify, Response, Blueprint
from .models import OrderModel

# import ast

#create blueprint app
order_api = Blueprint('order_api', __name__,)


@order_api.route('/', methods=['POST'])
def place_new_order():
    """
    place new  order function
    """
    request_data = request.json
    json_response_message = {}

    def validate_request_data_contains_valid_parameters(parameter_key):
        if(parameter_key == 'customer_order'):
            if not request_data.get(parameter_key):
                json_response_message['message'] = {
                    "error": parameter_key + " is missing or empty. List of required: customer_name, customer_phone, customer_order"}
                json_response_message['status_code'] = 400
        else:
            if not request_data.get(parameter_key):
                json_response_message['message'] = {
                    "error": "Missing " + parameter_key + " parameter. List of required: customer_name, customer_phone, customer_order"}
                json_response_message['status_code'] = 400

            else:
                parameter = request_data.get(parameter_key)
                if parameter.strip() == '':
                    json_response_message['message'] = {
                        "error": "{} cannot be empty".format(parameter_key)}
                    json_response_message['status_code'] = 400

    def validate_customer_order_content_and_values(order, content_key, content_type):
        json_response_message = {}
        if content_key not in order:
            json_response_message['message'] = {"error": "Badly foramtted customer_order. Missing "+content_key +
                                                " field in {}. correct format example for 'customer_order' is: {}".format(order, customer_order_format)}
            json_response_message['status_code'] = 400
        else:
            if content_type == 'str':
                if isinstance(order.get(content_key), str):
                    if str(order.get(content_key)).strip() == '':
                        json_response_message['message'] = {
                            "error": "customer_order["+content_key+"] value must be a non empty string"}
                        json_response_message['status_code'] = 400
                else:
                    json_response_message['message'] = {
                        "error": "customer_order["+content_key+"] value must be a string, found in {}".format(order)}
                    json_response_message['status_code'] = 400
            elif content_type == 'int':
                if isinstance(order.get(content_key), int):
                    if order.get(content_key) < 1:
                        json_response_message['message'] = {
                            "error": "customer_order[{}] value must be greater than 1, found in {}".format(content_key, order)}
                        json_response_message['status_code'] = 400
                else:
                        json_response_message['message'] = {
                            "error": "customer_order[{}] value must be an integer. found in {}".format(content_key, order)}
                        json_response_message['status_code'] = 400

        if len(json_response_message) > 0:
            return custom_response(json_response_message.get('message'), json_response_message.get('status_code'))

    validate_request_data_contains_valid_parameters('customer_name')
    validate_request_data_contains_valid_parameters('customer_phone')
    validate_request_data_contains_valid_parameters('customer_order')
    if len(json_response_message) > 0:
        return custom_response(json_response_message.get('message'), json_response_message.get('status_code'))

    # customer_name = request_data.get('customer_name')
    # customer_phone = request_data.get('customer_phone')
    # convert stringified array back into a literal
    # customer_orders = ast.literal_eval(request_data.get('customer_order'))
    customer_orders = request_data.get('customer_order')
    customer_order_format = "[{'food': 'grasshopper pizza', 'price': 20000, 'quantity': 2}, {'food': 'rice and beans pizza', 'price': 12000, 'quantity': 1}]"

    #validate customer order has food, price, and quantity fields
    for order in customer_orders:
        validate_customer_order_content_and_values(order, 'food', 'str')
        validate_customer_order_content_and_values(order, 'quantity', 'int')
        validate_customer_order_content_and_values(order, 'price', 'int')

    order = OrderModel(request_data).to_dictionary()
    OrderModel.place_order(order)
    return custom_response({"success": "Order placed successfully!", "saved_order": order}, 201)


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
    elif order is None:
        return custom_response({"error": "No order found with id: %d" % order_id}, 404)

    return custom_response(order, 200)


@order_api.route('/<int:order_id>', methods=['PUT'])
def change_order_status(order_id):
    """
    get specific order function
    """
    new_order_status = request.json.get('status')
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
    #use jsonify for pretty print in browser too
    return jsonify(res), status_code
