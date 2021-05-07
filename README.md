# Delivery

## About the application
This is a supermarket delivery system which starts from website on the internet that allows any person on the internet to view the supermarket products in a beautiful card view that contains all the required information about the product (product name, category, description, price, and a picture for the product), also he can make search in the products with many criteria (product category, price, name or title). However no one can make purchase request until he get logged in or of course register first if he didn't have an acount on the website 'in case of registeration user must include his address and phone for it's a crucial information in the home delivery part'. As soon as the user logged in to the web application he has the capability to add the viewed products into his cart in the quantity that he needs, the user or the customer can add different products as many as he likes in the same cart defining the required quantity of each product.
The system will automaticaly calculate the total price of each product multipling the quantity the customer entered by the price of the item for each product separately showing it in detail through a well organized table which shows in its last record the total cost of all chosen items in USD.
Then the customer has the choice to continue the purshase or roll back. if the user decided to continue, all that he needs is to click a button that will take all the selected items with its quantities and create a new purchase ORDER. Once an order has been created the user can follow it's status which can be either "Preparing" or "Submitted" from a user friendly view board. Also in the same moment the supermarket operator received the order in the operator's dashboard. So he can now manage to prepare the order, and as soon as the order is ready he can asign it to one of the three delivery men registred in the market and this will change the order status from "Preparing" into "Submitted". The delivery man also has access to the application to see only the orders assigned to him and change these orders status to "delivered" after he deliver it and recieve the cash from the customer.
By these steps we have offered our supermarket products though the internet and handled the workflow supported by web technology to give the customer easy and comfortable purchase service until delivering his orders to his home or work or whatever address he was used in the registeration. And because of we use the information the user entered in the regiseration especially phone and address in the delivery process, the application designed to give every user the capiblity to change his profile information including (phone, address) so customer shouldn't worry losing our services if they changed their residency, work place or phone numbers. Also every user can change his password if he wanted and the system save all passwords encrypted in a database, so no one even the administrator of the system can know it.
One last thing I want to mention in this section that all this works starts from the data entry function which I added to allow a user with data entry permissions to insert and register items and new products to the store, also he can edit the product attributes like (name, description, price, picture, or even the product's availability on the supermarket store), for example if the data entry acquainted that some product is been out of stock, he can update this product record that it's not available, so it will be removed from the offered products in the website. Once the supermarket receive shipment of this product the data entry can update it's value to be available again and this will reinsert it the products preview section in the website.

## New features I found in this application
* User permission managment through groups and builtin features introduced by Django Framework.
* Deep define for many to many relationship between two models through third model which was explained well in Django Documentation.
* Using Templatetags to identify new filter to use it in the templates which also mentioned in Django Documentation.

## Application Groups

### customer
Users in this group are able to preview Products and add items to their cart. And amke orders.

### operator
Users in this group are able to deal with the operator's dashboard, view all orders in all it's stages, starting from being received from the customers to the order fulfillment by delivering it to the registered address to the user. Also users in this group is resposible for redirecting the received orders to the delivery men.

### dataentry
Users in this group are able to access the data entry page where they can register new items in the supermarket and also update the items values if needed.

### deliveryman
Users in this group  are able to access delivery request panel which include orders redirected to him, note that every member in this group has access only to the orders that redirected to him, as soon as he deliver the orders items to the customer, he can update the status of the order into "delivered".

## Application Main Files

### urls.py
Include 12 paths for each end point function in the application. And 2 paths for JavaScript API calls by fetch functions ("PUT", "POST).

### models.py
Include 4 modules: User, Item, Order, and OrderItem which define the manay to many relationship between Item model and Order model.

### admin.py
Include 4 modules [User, Item, Order, and OrderItem] registered in the admin site, to be accessable to the project superuser.

### db.sqlite3
The database file which include 14 tables:
1. delivery_item
2. delivery_order
3. delivery_orderitem
4. delivery_user
5. delivery_user_groups
6. delivery_user_user_permissions
7. django_admin_log
8. django_content_type
9. django_migrations
10. django_session
11. auth_group
12. auth_group_permissions
13. auth_permission
14. sqlite_sequence
the first 4 was created based on the models I added in the models.py file.

### .gitignore
I added this file to untrack unnecessary tracks from being pushed to the project repository in github.com

### Templates
I have put all templates in one folder "templates/delivery", and i will mention every template and it's task

#### layout.html
This is the HTML template that wraps all the project content, mainly it include the definition of the unchangable parts through all the workflow in the application like: The Navigation bar, Header, Footer. also every other page stated below wraped inside it in the main section.
Moreover all links for external libraries or files (Cascading Style Sheets, JavaScript) defined in the head of this page.

#### index.html
The page show all products available in the supermarket, and it is accessible whether customers signed in or not, however they can't make purchase until they sign in. Also all the market staff (Operator, Data Entry, Delivery) lose the privlidge to access this page as soon as they login with their accounts. This has been made for purpose, to keep then focused in their tasks in the workflow and they can make another custmer accounts to access the application as customers in their free times.

#### register.html
Registeration form that contains fields to register new client user (Username, Password, Address, Phone). Note that the market staff don't register from this page, but the admin register them from the admin site, giving them the suffecient previlidge to fulfill their tasks.

#### login.html
Login page which available for everyone to enters his username / password to have additional access features according to his account group.

#### orders.html
This page is available only for the clients, where they can monitor their orders and follow it's current state until it delivered to them, once the order is delivered it being removed from the orders view. for example if a user made 3 orders and none of them delivered to him this page will show 3 orders, an as soon as one of the 3 orders delivered the page will contains only two orders until all orders delivered and it will be empty from orders.

#### dataentry.html
This page available only for accounts with dataentry group, so they can register new Products and Edit it's values (name, description, price, picture, or even the product's availability on the supermarket store), and here I will remention the example in the about section, if the data entry acquainted that some product is been out of stock, he can update this product record that it's not available, so it will be removed from the offered products in the website. Once the supermarket receive shipment of this product the data entry can update it's value to be available again and this will reinsert it the products preview section in the website.
Also it's good to mention that i used JavaScript and CSS together to handel the Edit Function by creating a custom Modal for items edit.

#### operator.html
This page available only for accounts with operator group, The Operator is the engine of this application He manages the orders from his dashboard which preview all the orders in all status (Preparing, Submitted, Delivered), he monitor his dashboard and as soon as he receive a new order request from customer, he use this page to redirect the order to one of the registered delivery men. and continue follow the order until it is delivered. The Order will never removed from this page but it will be placed in appropriate section.

#### deliveryman.html
This page available only for accounts with deliveryman group, where the delivery man monitor this page for any new delivery requests redirected to him, so he take the order for delivery and as soon as he delivered it and get the cash from the customer he can change the order state to "Delivered". Note that the application is mobile-responsive so he can use his mobile to update the status from out without a computer.

#### edit_profile.html
This page allow users to update their profiles information (username, address, phone).

#### reset_password.html
This page allow users to reset their passwords by providing their old passwords first.


### views.py
I have separated views.py into two parts. The first contains all end point functions for the application, the other part include the functions resposable for handling the http requests sent by JavaScript code in the Frontend.
### First Part
#### index Function:
Renders the index page with the appropriate items according to filters provided by the user.

#### register Function:
Create a new user with add customer group to it, and redirect to the index page.

#### login_user Function:
Receive the user's Username and Password authenticate the user from the database, if matches redirect the user to the index page.

#### logout_user Function:
Log the user out using logout function available in Django library "django.contrib.auth", then redirect to the index page.

#### data_entry Function:
Receives new item data (name, description, category, price, photoUrl, availability). If the values is valid, insert the new item into the database.

#### show_orders Function:
Receive the orders from the database and render it into the orders page.

#### show_all_orders Function:
Return the orders categorized (preparing, submitted, delivered) to the operator dashboard.

#### show_delivery_orders Function:
Return the active submitted orders to its appropriate delivery man.

#### assign_deliveryman Function:
Assign a delivery man for a specific order.

#### finish_order Function:
Update the Order status to "delivered".

#### edit_profile Function:
Receive values for user's username, address, phone from post request, and update the user's record according to the provided values.


#### reset_pwd Function:
Compare old password provided by the user with his password in the database, and if it was matched continue to update the password if the value of the new password and it's confirmation are the same.

### Second Part: Functions To Handle http requests sent from the JavaScript Code in the Frontend
#### edit_item Function:
Receive new values to update the item record in the database (name, description, category, price, photoUrl, availability).

#### make_order Function:
create a new order.

### Login Information
In case you needed, here is the Usernames / Passwords to Access the Application from different users with different permissions according to their groups. moreover you can create new accounts as much as you like from the registeration form for account with client permission, or from the admin site for the rest group acounts.

#### As Client
* username: emad
* Password: emad

* username: rami
* Password: rami

* username: sarah
* Password: sara

* username: nancy
* Password: emad

#### As Operator
* username: operator
* Password: emad

#### As Data Entry
* username: dataentry
* Password: emad

#### As Delivery Man
* username: deliveryman-1
* Password: emad

* username: deliveryman-2
* Password: emad

* username: deliveryman-3
* Password: emad

#### Software Versions:
* Python (3.9.2)
* Django (3.1.7)
* bootstrap (5.0.0-beta3)
***To run the application, just change directory to the main project folder called "capstone", then run the command "python manage.py runserver".***

#### Contact Informantion
* Name:   Emad N. Younan
* E-Mail: emadunan@gmail.com
* Phone:  +201003379933

***Thanks for CS50 Team!***