const getToken = () => localStorage.getItem('jwt_token');

const parseJWT = (token) => {
    var base64Url = token.split('.')[1];
    //base64 has + instead of - and / instead of _ so we convert base64Url 
    //to base64 by replacing (regular expression) all occurences
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    //atob() inbuilt function to decode base64. bota() does the opposite
    return JSON.parse(window.atob(base64));
};

const redirect = url => window.location.replace(url);

const getDateFromDateObject = date =>{
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const month = months[date.getMonth()];
    const day = date.getDate();
    const year = date.getFullYear();
    return `${day} ${month} ${year}`; 
}

const isAdmin = (token) => {
    return parseJWT(token)['identity']['admin']
};

const postData = (url = ``, data = {}) => {
    return fetch(url, {
        method: "POST",
        // mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json; charset=utf-8"
        },
        redirect: "follow",
        referrer: "no-referrer",
        body: JSON.stringify(data),

    }).then(response => response.json())
};

const postDataWithAuthHeader = (url = ``, data = {}, token = null) => {
    return fetch(url, {
        method: "POST",
        // mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": `Bearer ${token}`
        },
        redirect: "follow",
        referrer: "no-referrer",
        body: JSON.stringify(data),

    }).then(response => response.json())
};

const putDataWithAuthHeader = (url = ``, data = {}, token = null) => {
    return fetch(url, {
        method: "PUT",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": `Bearer ${token}`
        },
        redirect: "follow",
        referrer: "no-referrer",
        body: JSON.stringify(data),

    }).then(response => response.json())
};

const getData = (url = ``, token = null) => {
    return fetch(url, {
        method: "GET",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": `Bearer ${token}`
        },
        redirect: "follow",
        referrer: "no-referrer",

    }).then(response => response.json())
};

const hideElement = (element) => element.classList.add('hide');
const showElement = (element) => element.classList.remove('hide');
const errorFeedback = document.getElementById("errorFeedback");
const successFeedback = document.getElementById("successFeedback");

//SIGNIN {login}
const signinPageLogic = () => {
    const signInButton = document.getElementById("signinBtn");
    signInButton.onclick = (event) => {
        event.preventDefault();
        signInButton.value = "Loading...";
        hideElement(errorFeedback);

        let loginEmail = document.getElementById("signinEmail").value;
        let loginPassword = document.getElementById("signinPassword").value;

        postData("/api/v2/auth/login", { email: loginEmail, password: loginPassword })
            .then(data => {
                signInButton.value = "Signin"

                const response = data;
                if ('error' in response) {
                    showElement(errorFeedback);
                    errorFeedback.innerHTML = response['error'];
                } else if ('success' in response) {
                    localStorage.setItem('jwt_token', response['jwt_token'])
                    redirect('/menu');
                }
            })
            .catch(error => console.error(error));
    }
}

//SIGNOUT
const signoutPageLogic = () => {
    localStorage.removeItem('jwt_token');
    redirect('/signin');  
}

//SIGNUP {signup}
const signupPageLogic = () => {
    const signupButton = document.getElementById("signupBtn");
    const signupForm = document.getElementById("signupFormActual");

    signupButton.onclick = (event) => {
        event.preventDefault();
        console.log("signup form: ", signupForm);
        signupButton.value = "Saving...";
        // disable(signupButton);
        hideElement(errorFeedback);
        hideElement(successFeedback);

        let name = document.getElementById("userName").value;
        let email = document.getElementById("userEmail").value;
        let phone = document.getElementById("userPhone").value;
        let password = document.getElementById("userPassword").value;
        let confirmPassword = document.getElementById("confirmPassword").value;

        data = {name:name, email:email, phone:phone, password:password, confirm_password:confirmPassword};
        url = "/api/v2/auth/signup";
        postData(url, data)
            .then(response => {
                signupButton.value = "Signup"

                if ('error' in response) {
                    showElement(errorFeedback);
                    errorFeedback.innerHTML = response['error'];
                } else if ('success' in response) {
                    console.log("response on success: ", response);
                    signupForm.reset();
                    successFeedback.innerHTML = `${name} has been registered as a user. Please <a href="/signin">signin</a>.`;
                    showElement(successFeedback);
                }
            })
            .catch(error => console.error(error));
    }
}

//MENU {view menu, add menu item, place order}
const menuPageLogic = () => {
    const errorFeedbackModal = document.getElementById("errorFeedbackModal");
    const successFeedbackModal = document.getElementById("successFeedbackModal");
    const addFoodItemModal = document.getElementById('addMenuItemModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    closeModalBtn.onclick = () => hideElement(addFoodItemModal);
    window.onclick = (event) => {
        if (event.target == addFoodItemModal) {
            hideElement(addFoodItemModal);
        }
    };

    //TODO: add place order logic
    const previewOrder = document.getElementById('previewOrder');
    const submitOrderButton = document.getElementById('submitOrderBtn');
    const menuTable = document.getElementById('menuTable');
    const menuMainContent = document.getElementById('mainContent');
    const noFoodItemsInfo = document.getElementById('emptyMenuText');
    const addFoodItemBtn = document.getElementById('addMenuItemLink');
    const saveFoodItemBtn = document.getElementById('saveFoodItem');

    const updateOrderPreviewBeforeSubmit = orders =>{
        previewOrder.innerHTML = '';
        const unorderedList = document.createElement('ul');
        Object.keys(orders).forEach(key=>{
            const food = orders[key]['food'];
            const quantity = orders[key]['quantity'];
            const price = orders[key]['price'];
            const orderText = `${food}(${quantity}) for ${price}`;
            const listItem = document.createElement('li');
            const listItemContent = document.createTextNode(orderText);
            listItem.appendChild(listItemContent);
            unorderedList.appendChild(listItem);
        });
        previewOrder.appendChild(unorderedList);
    }

    let placeOrderObjectForSubmitting = {};

    const handleCheckboxStateChange = event => {
        hideElement(errorFeedback);
        hideElement(successFeedback);
        const menuItemId = event.target.id;
        const foodName = document.getElementById(`food-${menuItemId}`).innerText;
        const foodPrice = document.getElementById(`price-${menuItemId}`).innerText;
        const quantity = document.getElementById(`select-${menuItemId}`).value;
        const calculatedPrice = parseInt(foodPrice) * parseInt(quantity);
        if(event.target.checked){
            placeOrderObjectForSubmitting[menuItemId] = {food: foodName, quantity: parseInt(quantity), price: calculatedPrice};
            updateOrderPreviewBeforeSubmit(placeOrderObjectForSubmitting);
        }else{
            delete placeOrderObjectForSubmitting[menuItemId];
            updateOrderPreviewBeforeSubmit(placeOrderObjectForSubmitting);
        }
    }

    const handleQuantitySelectTagStateChange = event => {
        hideElement(errorFeedback);
        hideElement(successFeedback);
        const menuItemId = event.target.id.split('-')[1];
        const foodPrice = document.getElementById(`price-${menuItemId}`).innerText;
        const quantity = event.target.value;
        const calculatedPrice = parseInt(foodPrice) * parseInt(quantity);
        if(menuItemId in placeOrderObjectForSubmitting){
            placeOrderObjectForSubmitting[menuItemId]['quantity'] = parseInt(quantity);
            placeOrderObjectForSubmitting[menuItemId]['price'] = calculatedPrice;
            updateOrderPreviewBeforeSubmit(placeOrderObjectForSubmitting);
        }
    }

    submitOrderButton.onclick = () => {
        hideElement(errorFeedback);
        hideElement(successFeedback);
        if(Object.keys(placeOrderObjectForSubmitting).length === 0){
            errorFeedback.innerText = "You need to select at least one (1) food item to be able to submit an order."
            showElement(errorFeedback);
        }else{
            let customerOrder = [];
            Object.keys(placeOrderObjectForSubmitting).forEach(key=>{
                customerOrder.push(placeOrderObjectForSubmitting[key]);
            });

            const data = {customer_order: customerOrder};
            const url = '/api/v2/users/orders/';

            postDataWithAuthHeader(url, data, getToken())
            .then(response=>{
                if ('msg' in response) {
                    showElement(errorFeedback);
                    errorFeedback.innerHTML = response['msg'];
                } else if ('error' in response) {
                    showElement(errorFeedback);
                    errorFeedback.innerHTML = response['error'];
                } else if ('success' in response) {
                    successFeedback.innerText = response['success'];
                    showElement(successFeedback);
                    window.setTimeout(redirect('/orders'), 1000)
                } else {
                    showElement(errorFeedback);
                    errorFeedback.innerHTML = response;
                }
            })
            .catch(error=> console.error(error));
        }
    };

    if (isAdmin(getToken())) {
        showElement(addFoodItemBtn);
        addFoodItemBtn.onclick = (event) => {
            event.preventDefault();
            showElement(addFoodItemModal);

            saveFoodItemBtn.onclick = (event) => {
                event.preventDefault();
                saveFoodItemBtn.value = "Saving...";
                hideElement(errorFeedbackModal);
                hideElement(successFeedbackModal);

                let foodName = document.getElementById("foodName").value;
                let description = document.getElementById("description").value;
                let price = document.getElementById("price").value;
                const url = "/api/v2/menu";
                const data = { food_name: foodName, food_description: description, price: parseInt(price, 10) }
                postDataWithAuthHeader(url, data, getToken())
                    .then(response => {
                        saveFoodItemBtn.value = "Save";

                        if ('error' in response) {
                            showElement(errorFeedbackModal);
                            errorFeedbackModal.innerHTML = response['error'];
                        } else if ('success' in response) {
                            showElement(successFeedbackModal);
                            successFeedbackModal.innerHTML = `'${response['saved_food_item']['food_name']}' has been added to the menu. Feel free to add some more food items`
                        }
                    })
                    .catch(error => {
                        console.error(error);
                        errorFeedbackModal.innerHTML = error;
                        showElement(errorFeedbackModal);
                    });
            }
        }
    } else {
        hideElement(addFoodItemBtn);
    }

    const appendMenuItemToTable = (element, index) => {
        let row = document.createElement('tr');
        let cell1 = document.createElement('td');
        let cell2 = document.createElement('td');
        let cell3 = document.createElement('td');
        let cell4 = document.createElement('td');
        let checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = element['id'];
        checkbox.addEventListener('change', handleCheckboxStateChange, false);
        cell1.appendChild(checkbox);

        let label = document.createElement('label');
        label.id = `food-${element['id']}`;
        label.setAttribute('for', element['id']);
        let labelValue = document.createTextNode(element['food_name']);
        label.appendChild(labelValue);
        cell2.appendChild(label);


        let selectTag = document.createElement('select');
        selectTag.id = `select-${element['id']}`;
        [...Array(10).keys()].forEach(element => {
            let option = document.createElement('option');
            option.value = element + 1;
            option.text = element + 1;
            selectTag.appendChild(option);
        });
        selectTag.addEventListener('change', handleQuantitySelectTagStateChange, false);
        cell3.appendChild(selectTag);

        let priceLabel = document.createElement('label');
        priceLabel.id = `price-${element['id']}`;
        let priceLabelValue = document.createTextNode(element['price']);
        priceLabel.appendChild(priceLabelValue);
        cell4.appendChild(priceLabel);

        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        row.appendChild(cell4);
        menuTable.appendChild(row);
    }

    getData("/api/v2/menu", getToken())
        .then(data => {
            const response = data;
            // console.debug(response);
            if ('msg' in response) {
                console.log("Found a message instead: ", response['msg']);
                showElement(errorFeedback);
                errorFeedback.innerHTML = response['msg'];
            } else if ('error' in response) {
                console.debug("Error loading MENU", response['error']);
                showElement(errorFeedback);
                errorFeedback.innerHTML = response['error'];
            } else if ('info' in response) {
                if(isAdmin(getToken())){
                    document.getElementById('menuTableAndOrderPreview').innerHTML = "<h5>The menu is empty. Please add some food items using the link above.</h5>"
                }else{
                    menuMainContent.innerHTML = '<h3 class="centered-text">We currently do not have anything on the menu. Please check back later.</h3>'
                }
                console.debug("non-success info while loading MENU: ", response['info']);
            } else {
                let menuArray = response;
                // console.log("menuArray check: ", menuArray);
                menuArray.forEach(appendMenuItemToTable);
            }
        })
        .catch(error => console.error(error));

}

//ORDERS{view all orders, view order history, view specific order, update order status}
const ordersPageLogic = () => {
    const ordersTable = document.getElementById('ordersTable');
    const userOrderHistoryTable = document.getElementById('userOrderHistoryTable');
    const errorFeedbackModal = document.getElementById("errorFeedbackModal");
    const successFeedbackModal = document.getElementById("successFeedbackModal");

    const ordersMainContent = document.getElementById('mainContent');
    const viewSpecificOrderModal = document.getElementById('viewSpecificOrderModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    closeModalBtn.onclick = () => hideElement(viewSpecificOrderModal);
    window.onclick = (event) => {
        if (event.target == viewSpecificOrderModal) {
            hideElement(viewSpecificOrderModal);
        }
    };

    const generateCustomerOrderText = (customerOrder) => {
        if (customerOrder.length > 1) {
            let order = "";
            customerOrder.forEach((e, i) => {
                order += `${e['food']}(${e['quantity']}), `
            });
            return order.slice(0, -2); //remove trailing ', '
        } else {
            return `${customerOrder[0]['food']}(${customerOrder[0]['quantity']})`
        }
    }
    
    const generateCustomerOrderPrice = (customerOrder) => {
        if (customerOrder.length > 1) {
            let totalPrice = 0;
            customerOrder.forEach((e, i) => {
                totalPrice += e['price'] /* * e['quantity']*/;
            });
            return totalPrice;
        } else {
            return customerOrder[0]['price'] /* * customerOrder[0]['quantity']*/;
        }
    }

    const showSpecificOrder = event => {
        showElement(viewSpecificOrderModal)
        const customerName = document.getElementById('soCustomerName');
        const customerPhone = document.getElementById('soCustomerPhone');
        const customerOrder = document.getElementById('soCustomerOrder');
        const customerOrderPrice = document.getElementById('soCustomerOrderPrice');
        const orderStatus = document.getElementById('soCustomerOrderStatus');
        const orderDate = document.getElementById('soCustomerOrderDate');
        
        const orderId = event.target.id;
        const url = `/api/v2/orders/${orderId}`;
        
        getData(url, getToken())
        .then(response => {
            if ('msg' in response) {
                showElement(errorFeedbackModal);
                errorFeedbackModal.innerHTML = response['msg'];
            } else if ('error' in response) {
                showElement(errorFeedbackModal);
                errorFeedbackModal.innerHTML = response['error'];
            } else {
                let order = response;
                customerName.innerHTML = order['customer_name'];
                customerPhone.innerHTML = order['customer_phone'];
                customerOrder.innerHTML = generateCustomerOrderText(order['customer_order']);
                customerOrderPrice.innerHTML = generateCustomerOrderPrice(order['customer_order']);
                orderStatus.innerHTML = order['order_status'];
                orderDate.innerHTML = new Date(order['order_date']);
            }
        })
        .catch(error => console.error(error));
    }

    const handleChangeOrderStatus = event =>{
        const selectTagId = event.target.id;
        const orderId = event.target.id.split('-')[1];
        const statusUpdate = document.getElementById(selectTagId).value;

        //call fetch api to change status them refresh the page
        const url = `/api/v2/orders/${orderId}`;
        const data = {status:statusUpdate};
        putDataWithAuthHeader(url, data, getToken())
        .then(response => {
            if ('msg' in response) {
                showElement(errorFeedback);
                errorFeedback.innerHTML = response['msg'];
            } else if ('error' in response) {
                showElement(errorFeedback);
                errorFeedback.innerHTML = response['error'];
            } else if ('success' in response){
                showElement(successFeedback);
                successFeedback.innerHTML = response['success'];
                window.setTimeout(() => window.location.reload(false), 2000)
            }  
        })
        .catch(error => console.error(error));

    }

    const buildUserHistoryTable = (element, index) => {
        let row = document.createElement('tr');
        let cell1 = document.createElement('td');
        let cell2 = document.createElement('td');
        let cell3 = document.createElement('td');
        let cell4 = document.createElement('td');
        let cell5 = document.createElement('td');

        let cell1Value = document.createTextNode(index + 1);
        cell1.appendChild(cell1Value);

        let cell2Value = document.createTextNode(generateCustomerOrderText(element['customer_order']));
        cell2.appendChild(cell2Value);

        let cell3Value = document.createTextNode(generateCustomerOrderPrice(element['customer_order']));
        cell3.appendChild(cell3Value);

        let cell4Value = document.createTextNode(element['order_status']);
        cell4.appendChild(cell4Value);

        let cell5Value = document.createTextNode(getDateFromDateObject(new Date(element['order_date'])));
        cell5.appendChild(cell5Value);

        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        row.appendChild(cell4);
        row.appendChild(cell5);
        userOrderHistoryTable.appendChild(row)
    };
    
    const buildAdminOrdersTable = (element, index) => {
        let row = document.createElement('tr');
        let cell1 = document.createElement('td');
        let cell2 = document.createElement('td');
        let cell3 = document.createElement('td');
        let cell4 = document.createElement('td');
        let cell5 = document.createElement('td');

        let cell1Value = document.createTextNode(index + 1);
        cell1.appendChild(cell1Value);

        let orderLink = document.createElement('a');
        orderLink.href = '#';
        orderLink.id = element['customer_order'];
        orderLink.setAttribute('class', 'order-link');
        let cell2ValueLabel = document.createElement('label');
        cell2ValueLabel.id = element['id'];
        let cell2Value = document.createTextNode(generateCustomerOrderText(element['customer_order']));
        cell2ValueLabel.appendChild(cell2Value);
        orderLink.appendChild(cell2ValueLabel);
        orderLink.addEventListener('click', showSpecificOrder, false);
        cell2.appendChild(orderLink);

        let cell3Value = document.createTextNode(element['order_status']);
        cell3.appendChild(cell3Value);

        let cell4Value = document.createTextNode(element['customer_name']);
        cell4.appendChild(cell4Value);

        let selectTag = document.createElement('select');
        selectTag.id = `select-${element['id']}`;
        selectTag.setAttribute('class', 'change-status-select');
        ['new', 'processing','cancelled', 'complete'].forEach(e=>{
            let option = document.createElement('option');
            option.value = e;
            option.text = e;
            if(element['order_status'] == e){
                option.selected = true;
            }
            selectTag.appendChild(option);
        });
        selectTag.addEventListener('change', handleChangeOrderStatus, false);
        cell5.appendChild(selectTag);

        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        row.appendChild(cell4);
        row.appendChild(cell5);
        ordersTable.appendChild(row)

    }

    let url ="";
    if(isAdmin(getToken())){
        url = "/api/v2/orders"; 
    }else{
        url = "/api/v2/users/orders"; 
    }
    getData(url, getToken())
    .then(response => {
        if ('msg' in response) {
            console.log("Found a message instead: ", response['msg']);
            showElement(errorFeedback);
            errorFeedback.innerHTML = response['msg'];
        } else if ('error' in response) {
            console.debug("Error loading ORDERS", response['error']);
            showElement(errorFeedback);
            errorFeedback.innerHTML = response['error'];
        } else if ('info' in response) {
            ordersMainContent.innerHTML = '<h3 class="centered-text">Unfortunatley, no orders have been placed yet.</h3>'
            console.debug("non-success info while loading ORDERS: ", response['info']);
        } else {
            let ordersArray = response;
            if(isAdmin(getToken())){
                showElement(ordersTable);
                hideElement(userOrderHistoryTable);
                ordersArray.forEach(buildAdminOrdersTable);
            }else{
                showElement(userOrderHistoryTable);
                hideElement(ordersTable);
                ordersArray.forEach(buildUserHistoryTable);
            }
        }
    })
    .catch(error => console.error(error));
}

switch (document.body.classList[0]) {
    case 'signin-page':
        signinPageLogic();
        break;
    case 'signup-page':
        signupPageLogic();
        break;
    case 'menu-page':
        menuPageLogic();
        break;
    case 'orders-page':
        ordersPageLogic();
        break;
    case 'signout-page':
        console.log('ask to run signout logic')
        signoutPageLogic();
        break;

    default:
        break;
}