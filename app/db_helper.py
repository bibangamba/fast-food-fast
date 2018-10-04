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

    def __init__(self):
        db_url = APP.config['DATABASE_URI']
        self.db_url = db_url
        self.connection = psycopg2.connect(self.db_url)
        self.cursor = self.connection.cursor()

    def create_all_tables(self):
        #create users table
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY,
            email VARCHAR,
            phone VARCHAR(15),
            admin BOOLEAN,
            password VARCHAR)
        """
        )

        # create menu table
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS menu(
            id serial PRIMARY KEY,
            food_name VARCHAR,
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
            order_date_utc timestamp)
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
                order_date_utc) VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """
        self.cursor.execute(query, (order.get('customer_name'),
                                    order.get('customer_phone'),
                                    Json(order.get('customer_order')),
                                    order.get('order_status'),
                                    order.get('order_date')))
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
            return order_organized
        else:
            return None

    def update_order_status_in_db(self, order_id, order_status_update):
            self.cursor.execute(
                "UPDATE orders SET order_status = %s WHERE id = %s;", (order_status_update, order_id))
            return self.get_order_from_db(order_id)

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
