#app/views.py
import os
import datetime

from flask import Flask, request, json, jsonify, Response, Blueprint
from .models import UserModel, OrderModel, MenuModel
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)
from app import APP
from .validations import Validator

#create blueprint app
order_api = Blueprint('order_api', __name__,)


@order_api.route('users/orders/', methods=['POST'])
@jwt_required
def place_new_order():
    """
    place new  order function
    """
    current_user = get_jwt_identity()

    request_data = request.json

    #set user details from token encoded data
    request_data['customer_name'] = current_user.get('name')
    request_data['customer_phone'] = current_user.get('phone')
    request_data['user_id'] = current_user.get('id')

    message = Validator.validate_place_order(request_data)
    if len(message) > 0:
        return custom_response({'error': message.get('error')}, message.get('status_code'))

    order = OrderModel(request_data).to_dictionary()
    OrderModel.place_order(order)
    return custom_response({"success": "Order placed successfully!", "saved_order": order}, 201)

@order_api.route('users/orders/', methods=['GET'])
@jwt_required
def get_user_order_history():
    """
    get all orders belonging to user function
    """
    current_user = get_jwt_identity()
    user_id = current_user.get('id')

    orders = OrderModel.get_user_order_history(user_id)
    return custom_response(orders, 200)

@order_api.route('orders/', methods=['GET'])
@jwt_required #- ADMIN
def get_all_orders():
    """
    get all orders function
    """
    current_user = get_jwt_identity()
    if not current_user.get('admin'):
        return custom_response({'error':'You do not have enough permissions to access this endpoint'}, 401)

    orders = OrderModel.get_all_orders()
    if len(orders) == 0:
        return custom_response({"info": "No orders placed yet"}, 200)
    return custom_response(orders, 200)


@order_api.route('orders/<int:order_id>', methods=['GET'])
@jwt_required #- ADMIN
def get_order(order_id):
    """
    get specific order function
    """
    current_user = get_jwt_identity()
    if not current_user.get('admin'):
        return custom_response({'error':'You do not have enough permissions to access this endpoint'}, 401)

    order = OrderModel.get_specific_order(order_id)

    if not order:
        return custom_response({"error": "No order found with id: %d" % order_id}, 404)

    return custom_response(order, 200)


@order_api.route('orders/<int:order_id>', methods=['PUT'])
@jwt_required
def change_order_status(order_id):
    """
    get specific order function
    """
    new_order_status = request.json.get('status')
    if not new_order_status:
        return custom_response({"error": "'status' parameter not supplied"}, 400)
    if new_order_status not in ['new', 'processing', 'cancelled', 'complete']:
        return custom_response({"error": "'status' can only be one of these options: new, processing, cancelled, or complete"}, 400)

    order = OrderModel.update_order_status(order_id, new_order_status)
    if not order:
        return custom_response({"error": "No order found with id: {}".format(order_id)}, 404)
    return custom_response({"success": "Order status was changed successfully!", "order": order}, 200)


#LOGIN AND SIGNUP
@order_api.route('auth/signup', methods=['POST'])
def register_user():
    request_data = request.json

    message = Validator.validate_register_user_data(request_data)

    if len(message) > 0:
        return custom_response({'error': message.get('error')}, message.get('status_code'))

    email = request_data.get('email')

    user_exists = UserModel.get_user_by_email(email)
    if user_exists is not None:
        user_exists.pop('password')
        return custom_response({"error": "User with email:'{}' already exists in the database".format(email), "fail": user_exists}, 409)

    user = UserModel(request_data).to_dictionary()
    #pop() removes password from returned user data

    #todo: hash password with bcrypt before saving to db
    saved_user = UserModel.add_user(user)
    saved_user.pop('password')
    return custom_response({"success": "User was successfully created", "saved_user": saved_user}, 201)


@order_api.route('auth/login', methods=['POST'])
def log_user_in():
    request_data = request.json

    message = Validator.validate_login_request_data(request_data)
    if len(message) > 0:
        return custom_response({'error': message.get('error')}, message.get('status_code'))

    email = request_data.get('email')
    password = request_data.get('password')
    user_from_db = UserModel.get_user_by_email(email)

    if user_from_db is None:
        return custom_response({"error": "User with email: {} is not registered".format(email)}, 401)

    #todo add bcrypt to unhash password when given hash salt
    db_user_password = user_from_db.get('password')
    user_id = user_from_db.get('id')
    is_admin = user_from_db.get('admin')
    name = user_from_db.get('name')
    phone = user_from_db.get('phone')

    if(db_user_password != password):
        return custom_response({"error": "Email/Password authentication failed"}, 401)
    expires = datetime.timedelta(days=7)
    auth_token = create_access_token(
        identity={'name': name, 'phone': phone, 'email': email, 'id': user_id, 'admin': is_admin}, expires_delta=expires)
    return custom_response({'success': 'Successfully logged in as {}'.format(name), 'jwt_token': auth_token}, 200)

#MENU
@order_api.route('menu', methods=['POST'])
@jwt_required # - ADMIN 
def add_food_to_menu():
    #Admin user filter
    current_user = get_jwt_identity()
    if not current_user.get('admin'):
        return custom_response({'error':'You do not have enough permissions to access this endpoint'}, 401)


    request_data = request.json

    message = Validator.validate_new_menu_item_request_data(request_data)

    if len(message) > 0:
        return custom_response({'error': message.get('error')}, message.get('status_code'))

    food_name = request_data.get('food_name')

    food_already_saved = MenuModel.get_menu_item_by_food_name(food_name)
    if food_already_saved is not None:
        price = food_already_saved['price']
        food_already_saved['price'] = int(price)
        return custom_response({"error": "Food name: {} is already on the menu. Please supply a different food_name".format(food_name), "failed_save": food_already_saved}, 409)

    food_item = MenuModel(request_data).to_dictionary()

    #todo: hash password with bcrypt before saving to db
    saved_food_item = MenuModel.add_menu_item(food_item)

    return custom_response({"success": "Menu was updated with {}".format(food_name), "saved_food_item": saved_food_item}, 200)

@order_api.route('menu', methods=['GET'])
@jwt_required
def get_menu():
    """
    get menu items function
    """
    menu_items = MenuModel.get_all_menu_items()
    if len(menu_items) == 0:
        return custom_response({"info": "Menu is currently empty. Please try again some other time, we'll have more to offer."}, 200)
    return custom_response(menu_items, 200)

def custom_response(res, status_code):
    """
    custom response function
    """
    #use jsonify for pretty print in browser too
    return jsonify(res), status_code
