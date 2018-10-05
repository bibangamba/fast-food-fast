# fast-food-fast

[![Build Status](https://travis-ci.org/bibangamba/fast-food-fast.svg?branch=api_v2)](https://travis-ci.org/bibangamba/fast-food-fast)
[![Coverage Status](https://coveralls.io/repos/github/bibangamba/fast-food-fast/badge.svg?branch=api_v2)](https://coveralls.io/github/bibangamba/fast-food-fast?branch=api_v2)
[![Maintainability](https://api.codeclimate.com/v1/badges/5c4fade3616fe64f7994/maintainability)](https://codeclimate.com/github/bibangamba/fast-food-fast/maintainability)

Fast-Food-Fast is a food delivery service app for a restaurant

## Relevant Links

### UI Demo Link

The ui demo for fast-food-fast can be found on [gh-pages](http://deliver4me.net/fast-food-fast/)

### Heroku Link

To test the api endpoints with Postman, please use this [link](https://bibangamba-fast-food-fast-api.herokuapp.com/api/v1/orders/)

## Setup

### Running the app locally

If however, you'd like to run the app on your local machine:

1. clone the repo
2. cd into the app directory
3. create a virtual environment and activate it

    - to create: `python -m venv env-name` (windows) or `python3 -m venv env-name` (macOS)
    - to activate: `env-name\Scripts\activate.bat` (windows cmd. repalce `.bat` with `.ps1` for windows powershell) or `source env-name/bin/activate`
    - to deactivate: `env-name\Scripts\deactivate.bat` (windows)
4. set FLASK_ENV to development and PORT to 5000

    - `set FLASK_ENV="development"` on windows cmd (`$env:FLASK_ENV="development"` in powershell) or `export FLASK_ENV="development"`
    - `set PORT=5000` on windows cmd (`$env:PORT=5000` in powershell) or `export PORT=5000` on macOS
5. run `pip install -r requirements.txt` to install all the required packages
6. run `python run.py` to start the app. you can then navigate to `localhost:5000/api/v2/orders/`

### Working with the endpoints

|Endpoint                       |Method |Action                                     |Parameters                                     |
|:---                           |:---   |:---                                       |:--                                            |
|/api/v2/orders/                |GET    |get a list of all orders                   |N/A                                            |
|/api/v2/orders/int:order_id    |GET    |get a specific order whose id = order_id   |order_id                                       |
|/api/v2/orders/                |POST   |place an order                             |customer_name, customer_order, customer_contact|
|/api/v2/orders/int:order_id    |PUT    |update an order's status                   |order_id, status                               |

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