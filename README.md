# INF226 - Assignment 2+3

## Improvments of Structure

- First thing we saw was that the project was badly structured. Code that is badly structured are harder to maintain and is vulnerable to bugs which could negatively impact the safety of the application and its users. We therefore started with restructuring the application to make it easier to maintain and improve

### Main Components of New Structure

- controller.py
  - This files includes all endpoints for the application
- db_init.py
  - Initiaties the database
- db_service.py
  - Methods for communication with database
- login_manager.py
  - Contains login_manager functions like user_loader() and request_loader()
- password_utils.py
  - Methods for hashing and verifying passwords
- input_validator.py
  - Methods for validating user input
- utils.py

  - Extra util methods

app.py now only contains functionality for initializing the application. There are some additional files that are used as utilities for other files but the main components are covered above.

## Initial Security Issues

- First thing we found was that the secret key was not random and was stored directly in the source code. That made it so that everyone that could see the source code, would know the secret key. This left the application vulnerable to session hijacking by making the session cookies easier to guess

- The next big security flaw was that users was stored directly in the source code. The result being that everyone that had access to the source code would be able to see all of the user information. This problem was very critical since password was not even encrypted and was stored as plain text inside of the user object

- There was no Authentication implemented and a user could type whatever username they wanted and log in to said account

- There was clear SQL injection vulnerabilites as data which originated from user input was concatanated directly into SQL statement strings

- We found severel authorization vulneraibilites. Firstly, users could access some critical endpoints without being logged in. Users could add messages and read messages without logging in which breaks the confidentiality of our application

- The next parameter can potentially be dangerous as an attacker may be able to make an URL which changes the state on behalf of other user. We checked that the url is escaped, but it can still be dangerous. As an example did we manage to construct a URL that posted a new message when clicked on by authorized user. It basically made it very easy to perform cross site request forgeries

- The application had no access controll which is very problematic as private messages could be viewed by all users in the system. Another problem was that a user can be sent from anybody as the users wrote who the message was from

- A common vulnerabilty is that the cookies are not correctly configured and therefore becomes a security vulnerabilty. The application did not specify anything other than the secret key which could be problematic if the default values does not match the application context

- A Csrf token was sent on login form, but not on form inside of the index.html. This may lead to successful cross site request forgery attacks on our website

- The search function fetches user supplied messages from the database and adds them to the DOM. If this data is not escaped, the applicaton is vulnerable to persistent XSS attacks

## Refactoring to Address the Inital Security Issues

- One option would be to store the key in some environment file that makes it somewhat more hidden. The problem with this approach is that
  the key would still be vulnerable to brute force attacks and if an attacker gets the key, all sesions would be vulnerable. Therefore we made the key random

- We removed the user objects from the source code and stored them in a database. We still had the problem that if an attacker got access to the database, the attacker would see all of the passwords. We fixed this by encrypting passwords using bcrypt. We also salted the passwords to make to be resilient against rainbow table attacks

- We fixed authentication by enforcing that the provided password matched the password in the database for the user with given username

- SQL injection vulnerabilites was fixed my removing concatanation and replacing it with prepared statements that lets the database distinguish between SQL statements and the data

- We solved authorization problems on endpoints by enforcing that users has to be logged in to make new messages and read existing messages. Some endpoints was left available for unauthenticated users, namely coffee, favicon and CSS. Coffee and favicon can not change state or return confidential information and CSS simply returns information that is already available when inspecting the page

- The next parameter is still in the URL as it is part of Flask default configuration, but all logic to support the next parameter is removed to make it useless. We did this as we thought that it was unnecessairy in this application and may be the root of several vulnerabilites. We also addressed the general csrf concern using csrf tokens on all forms

- Some basic access control was implemented. Firstly, the user can no longer write who the message is from. We used Flask to check what user was currently logged in and set the from-field to the logged in user. The application therefore ensures that the message is sent from the username given in the sender-field. We also fixed the problem of all users being able to see all messages by enforcing that users should only see messages that are sent to everybody, to the user or from the user

- We made sure the cookies had the correct flags by setting them ourselves. We set the secure flag ensuring that only the cookies are only sent over HTTPS, the HTTPOnly flag was set to ensure that the cookies cannot be read with JavaScript and we set sameSite to Strict to ensure that cookies are only sent with requests originating from the same origin

- To further address the csrf issues, we implemented csrf tokens on all of the forms. We also validated the form using form.validate_on_submit inside of our controller methods that recieved inputs from forms. If the form was not validated, the request is denied

- We investagated whether results from searching messages are automatically escaped and we found that they are. As the data is escaped, we did not do any more to avoid persistent XSS as Flask seemingly does it for us

## Refactoring (NOT written nicely yet)

Security issues:

- When making new endpoints, we have to escape the output to avoid stored XSS

- Some variables are used directly in html

  - Sanitized messages in message.html (must check if there are more
  - Must check all HTML and JS code to see if there are more XSS faults
  - Removed innerHTML and replaces with setHTML which does not render complete markup
    - setHtml parses and sanitizes input
    - All user input that is present in the DOM is santized or set via textcontent which is safe

- Bearer token is not secure as it is not encrypted. A packet sniffer can take token and be authorized on server.

  - Not mentioned in text and hard to test, so this is not fixed

- We have tried to validate all input to enforce the invariants of the domain.
  - Should have made domain primitives but not enough time
