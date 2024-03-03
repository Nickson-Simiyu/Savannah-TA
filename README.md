A simple python (flask) service that has a design of (PSQL)database.
    Customer_order
    User
Implemented authentication and authorization via OpenID Connect using third party Auth0. It takes in the email and password (Username-Password-Authentication) also allows google-oauth2.

The app  is designed to navigate to the login page to start a session so you can make an order and a button that sends you to the home("/")page.

The home page has a "/logout"(button) that clears the users session in return navigates you back to the "/login" to start the process again.

The "/order" consists of a form rendered from the order.html entailing:
    ID
    Full Name
    Phone Number
    Item
    Amount
    Time
Once an order is placed the customer receives an SMS alerting them on their order using the Africa's Talking SMS gateway(delivery reports).