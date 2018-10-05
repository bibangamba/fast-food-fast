from app import config

import psycopg2
from psycopg2.extras import Json 
from app import APP


class DatabaseConnectionHelper():
    """
    This class has all the queries needed by the different model classes
    and enables re-use of the connection and the cursor
    """
    #initialise  connection helper with default db_url set to import from run.app (result of create_app())

    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = psycopg2.connect(self.db_url)
        self.cursor = self.connection.cursor()

    def create_all_tables(self):
        #create users table
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY,
            name VARCHAR,
            email VARCHAR UNIQUE,
            phone VARCHAR(15),
            admin BOOLEAN NOT NULL DEFAULT FALSE,
            password VARCHAR)
        """
        )

        # create menu table
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS menu(
            id serial PRIMARY KEY,
            food_name VARCHAR UNIQUE,
            price NUMERIC,
            food_description VARCHAR)
        """
        )

        #create orders table
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS orders(
            id serial PRIMARY KEY,
            customer_name varchar,
            customer_phone varchar(15),
            customer_order jsonb,
            order_status varchar(20),
            order_date_utc timestamp,
            user_id int)
        """
        )

        self.connection.commit()

    def insert_order_into_db(self, order):
        query = """
            INSERT INTO orders (
                customer_name,
                customer_phone,
                customer_order,
                order_status,
                order_date_utc,
                user_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """
        self.cursor.execute(query, (order.get('customer_name'),
                                    order.get('customer_phone'),
                                    Json(order.get('customer_order')),
                                    order.get('order_status'),
                                    order.get('order_date'), 
                                    order.get('user_id')))
        self.connection.commit()
        #set id field to the id returned from insert query
        order['id'] = self.cursor.fetchone()[0]
        return order

    def get_all_orders_from_db(self):
        list_of_orders = []
        self.cursor.execute("SELECT * FROM orders")
        orders = self.cursor.fetchall()
        self.connection.commit()

        for order in orders:
            organized_order = {}
            organized_order['id'] = order[0]
            organized_order['customer_name'] = order[1]
            organized_order['customer_phone'] = order[2]
            organized_order['customer_order'] = order[3]
            organized_order['order_status'] = order[4]
            organized_order['order_date'] = order[5]
            organized_order['user_id'] = order[5]
            list_of_orders.append(organized_order)
        return list_of_orders
    
    def get_all_orders_belonging_to_user_from_db(self, user_id):
        list_of_orders = []
        self.cursor.execute("SELECT * FROM orders WHERE user_id = {}".format(user_id))
        orders = self.cursor.fetchall()
        self.connection.commit()

        for order in orders:
            organized_order = {}
            organized_order['id'] = order[0]
            organized_order['customer_name'] = order[1]
            organized_order['customer_phone'] = order[2]
            organized_order['customer_order'] = order[3]
            organized_order['order_status'] = order[4]
            organized_order['order_date'] = order[5]
            organized_order['user_id'] = order[5]
            list_of_orders.append(organized_order)
        return list_of_orders

    def get_order_from_db(self, order_id):
        self.cursor.execute(
            "SELECT * FROM orders WHERE id = {}".format(order_id))
        order = self.cursor.fetchone()
        if order is not None:
            order_organized = {}
            order_organized['id'] = order[0]
            order_organized['customer_name'] = order[1]
            order_organized['customer_phone'] = order[2]
            order_organized['customer_order'] = order[3]
            order_organized['order_status'] = order[4]
            order_organized['order_date'] = order[5]
            order_organized['user_id'] = order[5]
            return order_organized
        else:
            return order

    def update_order_status_in_db(self, order_id, order_status_update):
            self.cursor.execute(
                "UPDATE orders SET order_status = '{}' WHERE id = {};".format(order_status_update, order_id))
            return self.get_order_from_db(order_id)

    #USER RELATED
    def insert_user_into_db(self, user):
        query = """
            INSERT INTO users (
                name,
                email,
                phone,
                password) VALUES ( %s, %s, %s, %s) RETURNING id;
        """
        self.cursor.execute(query, (user.get('name'),
                                    user.get('email'),
                                    user.get('phone'),
                                    user.get('password')))
        self.connection.commit()
        #set id field to the id returned from insert query
        user['id'] = self.cursor.fetchone()[0]
        return user

    def find_user_in_db_using_id(self, id):
        self.cursor.execute(
            "SELECT * FROM users WHERE id = {}".format(id))
        user = self.cursor.fetchone()
        if user is not None:
            organized_user = {}
            organized_user['id'] = user[0]
            organized_user['name'] = user[1]
            organized_user['email'] = user[2]
            organized_user['phone'] = user[3]
            organized_user['admin'] = user[4]
            organized_user['password'] = user[5]
            return organized_user
        else:
            return user

    def find_user_in_db_using_email(self, email):
        #todo: refactor to remove duplication
        self.cursor.execute(
            "SELECT * FROM users WHERE email = '{}'".format(email))
        user = self.cursor.fetchone()
        if user is not None:
            organized_user = {}
            organized_user['id'] = user[0]
            organized_user['name'] = user[1]
            organized_user['email'] = user[2]
            organized_user['phone'] = user[3]
            organized_user['admin'] = user[4]
            organized_user['password'] = user[5]
            return organized_user
        else:
            return user

    def update_user_role_in_db(self, user_id, user_is_admin):
            self.cursor.execute(
                "UPDATE users SET admin = {} WHERE id = {};".format(user_is_admin, user_id))
            return self.find_user_in_db_using_id(user_id)

    #MENU RELATED
    def insert_menu_item_into_db(self, menu_item):
        query = """
            INSERT INTO menu (
                food_name,
                food_description,
                price) VALUES (%s, %s, %s) RETURNING id;
        """
        self.cursor.execute(query, (menu_item.get('food_name'),
                                    menu_item.get('food_description'),
                                    menu_item.get('price')))
        self.connection.commit()
        menu_item['id'] = self.cursor.fetchone()[0]
        return menu_item

    def get_all_menu_items_from_db(self):
        list_of_menu_items = []
        self.cursor.execute("SELECT * FROM menu")
        menu_items = self.cursor.fetchall()
        self.connection.commit()

        if menu_items is not None:
            for menu_item in menu_items:
                organized_menu_item = {}
                organized_menu_item['id'] = menu_item[0]
                organized_menu_item['food_name'] = menu_item[1]
                if menu_item[2] is not None:
                    organized_menu_item['price'] = int(menu_item[2]) #convert Decimal to int since Decimal is not JSON serializable
                organized_menu_item['food_description'] = menu_item[3]
                list_of_menu_items.append(organized_menu_item)
        return list_of_menu_items

    def find_menu_item_in_db_using_id(self, menu_item_id):
        self.cursor.execute(
            "SELECT * FROM menu WHERE id = {}".format(menu_item_id))
        menu_item = self.cursor.fetchone()
        if menu_item is not None:
            organized_menu_item = {}
            organized_menu_item['id'] = menu_item[0]
            organized_menu_item['food_name'] = menu_item[1]
            organized_menu_item['price'] = menu_item[2]
            organized_menu_item['food_description'] = menu_item[3]
            return organized_menu_item
        else:
            return menu_item
        pass
    
    def find_menu_item_in_db_using_food_name(self, food_name):
        self.cursor.execute(
            "SELECT * FROM menu WHERE food_name = '{}'".format(food_name))
        menu_item = self.cursor.fetchone()
        if menu_item is not None:
            organized_menu_item = {}
            organized_menu_item['id'] = menu_item[0]
            organized_menu_item['food_name'] = menu_item[1]
            organized_menu_item['price'] = menu_item[2]
            organized_menu_item['food_description'] = menu_item[3]
            return organized_menu_item
        else:
            return menu_item
        pass

    def update_menu_item_price_in_db(self, menu_item_id, price):
        self.cursor.execute(
            "UPDATE menu SET price = {} WHERE id = {};".format(price, menu_item_id))
        return self.find_menu_item_in_db_using_id(menu_item_id)

    def delete_data_from_all_tables(self):
        #'restart identity' resets id column in 'serial' columns
        self.cursor.execute("TRUNCATE TABLE users RESTART IDENTITY")
        self.cursor.execute("TRUNCATE TABLE menu RESTART IDENTITY")
        self.cursor.execute("TRUNCATE TABLE orders RESTART IDENTITY")
        # cursor.execute("TRUNCATE TABLE orders CASCADE")
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
