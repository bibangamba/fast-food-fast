class Validator:
    @classmethod
    def validate_request_data_contains_valid_parameters(cls, request_data, json_response_message, parameter_key):
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
        return json_response_message

    @classmethod
    def validate_register_user_data(cls, request_data):
        message = {}
        if request_data is None:
            message['error'] = 'Missing JSON request data.'
            message['status_code'] = 400
            return message

        email = request_data.get('email')
        name = request_data.get('name')
        password = request_data.get('password')
        confirm_password = request_data.get(
            'confirm_password')  # can be done on the client
        phone = request_data.get('phone')

        #email validation
        if email is None:
            message['error'] = 'Missing email parameter. It is required.'
            message['status_code'] = 400
        elif not isinstance(email, str):
            message['error'] = 'Email parameter must be a string.'
            message['status_code'] = 400
        elif len(email.strip()) == 0:
            message['error'] = 'Email parameter cannot be empty.'
            message['status_code'] = 400
        elif "@" not in email:
            message['error'] = 'Supplied email parameter is not a valid email format. Must contain an @'
            message['status_code'] = 400
        else:
            #name validation
            if name is None:
                message['error'] = 'Missing name parameter. It is required.'
                message['status_code'] = 400
            elif not isinstance(name, str):
                message['error'] = 'Name parameter must be a string.'
                message['status_code'] = 400
            elif len(name.strip()) == 0:
                message['error'] = 'Name parameter must be a string.'
                message['status_code'] = 400
            else:
                #password validation
                if password is None:
                    message['error'] = 'Missing password parameter. It is required.'
                    message['status_code'] = 400
                elif not isinstance(password, str):
                    message['error'] = 'Password parameter must be a string.'
                    message['status_code'] = 400
                elif password != confirm_password:
                    message['error'] = 'Confirm Password does not match Password. They must match'
                    message['status_code'] = 400
                elif len(password) < 8:
                    message['error'] = 'Password must be 8 characters or more'
                    message['status_code'] = 400
                else:
                    #phone validation
                    if phone is None:
                        message['error'] = 'Missing phone parameter. It is required.'
                        message['status_code'] = 400
                    elif not isinstance(phone, str):
                        message['error'] = 'Phone parameter must be a string.'
                        message['status_code'] = 400
                    elif len(phone) != 10:
                        message['error'] = 'Phone parameter must have a length of 10 (ten numbers).'
                        message['status_code'] = 400
                    elif not phone.isdigit():
                        message['error'] = 'Phone parameter must be a digits only string.'
                        message['status_code'] = 400
        return message

    @classmethod
    def validate_login_request_data(cls, request_data):
        message = {}
        if request_data is None:
            message['error'] = 'Missing JSON request data.'
            message['status_code'] = 400
            return message

        email = request_data.get('email')
        password = request_data.get('password')

        if email is None:
            message['error'] = 'Missing email parameter.'
            message['status_code'] = 400
        elif not isinstance(email, str):
            message['error'] = 'Email parameter must be a string.'
            message['status_code'] = 400
        elif len(email.strip()) == 0:
            message['error'] = 'Email parameter cannot be empty.'
            message['status_code'] = 400
        elif "@" not in email:
            message['error'] = 'Supplied email parameter is not a valid email format. Must contain an @'
            message['status_code'] = 400
        else:
            if password is None:
                    message['error'] = 'Missing password parameter. It is required.'
                    message['status_code'] = 400
            elif not isinstance(password, str):
                message['error'] = 'Password parameter must be a string.'
                message['status_code'] = 400
            elif len(password) < 8:
                message['error'] = 'Password must be 8 characters or more'
                message['status_code'] = 400

        return message

    @classmethod
    def validate_new_menu_item_request_data(cls, request_data):
        message = {}
        if request_data is None:
            message['error'] = 'Missing JSON request data.'
            message['status_code'] = 400
            return message

        food_name = request_data.get('food_name')
        price = request_data.get('price')
        food_description = request_data.get('food_description')

        #food_name validation
        if food_name is None:
            message['error'] = 'Missing food_name parameter. It is required.'
            message['status_code'] = 400
        elif not isinstance(food_name, str):
            message['error'] = 'food_name parameter must be a string.'
            message['status_code'] = 400
        elif len(food_name.strip()) == 0:
            message['error'] = 'food_name parameter cannot be empty.'
            message['status_code'] = 400
        elif len(food_name.strip()) > 50:
            message['error'] = 'food_name parameter should be a short name (less than 50 characters).'
            message['status_code'] = 400
        else:
            #price validation
            if price is None:
                message['error'] = 'Missing price parameter. It is required.'
                message['status_code'] = 400
            elif not isinstance(price, int):
                message['error'] = 'price parameter must be an integer.'
                message['status_code'] = 400
            else:
                #food_description validation
                if food_description is None:
                    message['error'] = 'Missing food_description parameter. It is required.'
                    message['status_code'] = 400
                elif not isinstance(food_description, str):
                    message['error'] = 'food_description parameter must be a string.'
                    message['status_code'] = 400
                elif len(food_name.strip()) == 0:
                    message['error'] = 'food_name parameter cannot be empty.'
                    message['status_code'] = 400
        return message
