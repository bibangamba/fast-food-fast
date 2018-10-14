# fast-food-fast

[![Build Status](https://travis-ci.org/bibangamba/fast-food-fast.svg?branch=ft-place-order-endpoint-160908874)](https://travis-ci.org/bibangamba/fast-food-fast)
[![Coverage Status](https://coveralls.io/repos/github/bibangamba/fast-food-fast/badge.svg?branch=ft-place-order-endpoint-160908874)](https://coveralls.io/github/bibangamba/fast-food-fast?branch=ft-place-order-endpoint-160908874)
[![Maintainability](https://api.codeclimate.com/v1/badges/5c4fade3616fe64f7994/maintainability)](https://codeclimate.com/github/bibangamba/fast-food-fast/maintainability)

Fast-Food-Fast is a food delivery service app for a restaurant

## Relevant Links

### UI Demo Link

The ui demo for fast-food-fast can be found on [gh-pages](http://deliver4me.net/fast-food-fast/)

### Heroku Link

To test the api endpoints with Postman, please use this [link](https://bibangamba-fast-food-fast-v2.herokuapp.com/api/v2/menu)

## Setup

### Running the app locally

If however, you'd like to run the app on your local machine:

1. clone the repo
2. cd into the app directory
3. create a virtual environment and activate it

    - to create: `python -m venv env-name` (windows) or `python3 -m venv env-name` (macOS)
    - to activate: `env-name\Scripts\activate.bat` (windows cmd. repalce `.bat` with `.ps1` for windows powershell) or `source env-name/bin/activate`
    - to deactivate: `env-name\Scripts\deactivate.bat` (windows)
4. set environment variable FLASK_ENV to development, PORT to 5000, DATABASE_URI to postgres development database, and TEST_DATABASE_URI to postgres test database

    - `set FLASK_ENV="development"` on windows cmd (`$env:FLASK_ENV="development"` in powershell) or `export FLASK_ENV="development"`
    - `set PORT=5000` on windows cmd (`$env:PORT=5000` in powershell) or `export PORT=5000` on macOS
5. run `pip install -r requirements.txt` to install all the required packages
6. run `python run.py` to start the app. you can then navigate to `localhost:5000/api/v2/orders/`

### Working with the endpoints

|Endpoint                       |Method |Action                                     |JSON                                          |
|:---                           |:---   |:---                                       |:--                                           |
|/api/v2/auth/signup            |POST   |sign up as a user                          |email, password, confirm_password, name, phone|
|/api/v2/auth/login             |POST   |login so as to get an auth token           |email, password                               |
|/api/v2/orders/                |GET    |get a list of all orders                   |N/A                                           |
|/api/v2/orders/int:order_id    |GET    |get a specific order whose id = order_id   |order_id                                      |
|/api/v2/orders/int:order_id    |PUT    |update an order's status                   |order_id, status                              |
|/api/v2/menu/                  |POST   |add food item to the menu                  |food_name, price, food_description            |
|/api/v2/menu/                  |GET    |get all food items on the menu             |N/A            |
|/api/v2/users/orders/          |POST   |place an order                             |customer_order                                |
|/api/v2/users/orders/          |GET    |get current user's order history           |N/A                                |

Excluding the login and signup  endpoints, all other endpoints require an Authorizaion header e.g.

`{"Authorization": "Bearer jwt-token"}`

And some routes can only be accessed by admin level users.

### Users

|Email          |Name       |Password   |Admin  |
|:---           |:---       |:---       |:---   |
|andrew@a.com   |Andrew.T   |yurizahard |YES    |
|joseph@a.com   |Joseph.H   |password   |NO     |

### Parameters description

1. order_id is an `int`
2. customer_name is a `string`. it could be made unique (or be just an email) and used to identify a user on signin and getting their history of orders.
3. customer_order is a `string` with a json arrya. A JSON array formatted as a string. The sample format is:

    ```js
    [
        {
            "food":"beans and rice pizza",
            "quantity":2,
            "price":32000
        },
        {
            "food":"grasshoppers pizza",
            "quantity":1,
            "price":17000
        }
    ]
    ```
4. cusomer_contact is a 10-digit phone number saved as a `string`