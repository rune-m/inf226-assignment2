# INF226 - Assignment 2

## Design considerations

### Improvments of Structure

- First thing we saw was that the project was badly structured. Code that is badly structured are harder to maintain and is vulnerable to bugs which could negatively impact the security of the application and its users. We therefore started with restructuring the application to make it easier to maintain and improve

#### Main Components of New Structure

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
- templates folder
  - All HTML templates
- static/js folder
  - All JavaScript logic for the templates

app.py now only contains functionality for initializing the application. There are some additional files that are used as utilities for other files but the main components are covered above.

### Initial Security Issues

- Another problem that we found was that the secret key was not random and was stored directly in the source code. That made it so that everyone that could see the source code, would know the secret key. This left the application vulnerable to session hijacking by making the session cookies easier to guess

- The next big security flaw was that users was stored directly in the source code. The result being that everyone that had access to the source code would be able to see all of the user information. This problem was very critical since password was not even encrypted and was stored as plain text inside of the user object

- There was no Authentication implemented and a user could type whatever username they wanted and log in to said account without the password being considered. This might be a result of the insecure and messy design of the application leading to small bugs like this.

- There was clear SQL injection vulnerabilites as data which originated from user input was concatanated directly into SQL statement strings

- We found severel authorization vulneraibilites. Firstly, users could access some critical endpoints without being logged in. Users could add messages and read messages without logging in which breaks the confidentiality of our application

- The 'next' URL-parameter can potentially be dangerous as an attacker may be able to make an URL which changes the state on behalf of other user. We checked that the url is escaped, but it can still be dangerous. As an example did we manage to construct a URL that posted a new message when clicked on by authorized user. It basically made it very easy to perform cross site request forgeries

- The application had no access controll which is very problematic as private messages could be viewed by all users in the system. Another problem was that a user can be sent from anybody as the users wrote who the message was from

- A common vulnerabilty is that the cookies are not correctly configured and therefore becomes a security vulnerabilty. The application did not specify anything other than the secret key which could be problematic if the default values does not match the application context

- A Csrf token was sent on login form, but not on form inside of the index.html. This may lead to successful cross site request forgery attacks on our website

- The search function fetches user supplied messages from the database and adds them to the DOM. If this data is not escaped, the applicaton is vulnerable to persistent XSS attacks

- Some variables was used directly inside of the HTML leaving the application vulnerable to XSS attacks. Another problem was that "innerHtml" was used despite being notoriusly problematic when it comes to XSS

- No validation on input and invariants are not enforced

- No logging which makes it very hard to trace attacks that may occur

### Refactoring to Address the Inital Security Issues

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

- To address the XSS vulnerability we got rid of all "innerHtml" calls and replaced them with "setHTML" which automatically sanitizes the data. Instanses of setting "textContent" was ignored as it ignores all markup and is therefore safe. The variables that was used directly in the HTML was also sanitized to avoid them being interpreted as anything more than data.

- We have made some inputvalidation logic, to enforce some invariants. The problem is that the task is very open so defining these constraints were quite difficult. In another setting one would ask a lot of questions to some domain expert to get a comprehensive understanding of the domain which the system represents but this was not possible for the given context. We have therefore only made some primitive validation logic. In a real setting we should have defined domain primitives and added the constraints to the constructors. This would ensure that all objects conformed to the given constraints.

- Added some logging. The logs are stored seperately in its own file. The logs contains no sensitive information. In a real world setting, more thought and work must go into logging

### Comments

We also found that the implementation of the bearer token was quite problematic. The token was not encrypted and could therefore be picked up by some packet sniffer. In this application we use session cookies and have not focused on the bearer token implementation. When looking into it we realized it was quite hard to test as the application always used session cookies and never used the bearer token logic. Another thing which is not addresses is logic to handle DDOS like IP based rate limiting. This is quite complicated and therefore not implemented. We have not implemented anything https-related (except setting secure on cookie), as this is complicated and we were told that we could assume https was configured.

## Features of our application

We have kept the original message page (with updated logic to address security concerns) and have made a new page to contain the logic for the new messaging API.

The old message page is at /oldMessages and /index.html. The new is at / and /message.

- Users can add an account
  - Passwords will be stored securely (hashed with salt)
  - Passwords must contain at least: 8 characters, one uppercase letter, one lowercase letter, one number
- Users can log in and out of accounts
  - Log in enforces correct email and password
- Users are stored in a database
  - Passwords not stored as plaintext

### Old messaging page

- Users can send messages to everyone or specific people (can be multiple)
  - The sent messages are stored in a database
  - Users are automatically set as sender of a sent message
- Users can show all messages that are sent by them, to them or to all
- Users can search messages and will se messages that are sent by them, to them or to all that also matches the provided pattern

### New messaging page

- Users can send messages to everyone or one or multiple persons
  - The sent messages are stored in a database
  - Users are automatically set as sender of a sent message
- Users can reply to messages
- Users can show all messages that are sent by them, to them or to all
- Can logout via button

## Instructions on how to test and demo

- To run application, do "flask run"
- Go to <http://127.0.0.1:5000/> with Chrome or Edge (Santizer not compatible with other browsers)
- Valid usernames and passwords:
  - alice : password123
  - bob : banana

## Techincal details of implementation

- Uses the Flask framework
  - Manages sessions
  - Used flask forms for our forms because they make it easy to send CSRF tokens
- Passwords are encrypted using bcrypt with salting
- Users, messages and announcements are stored in an SQL lite database
  - Application inserts some users on initialization
- The application logs security events into logging.txt file
- Application does some basic input validation
- Application can be ran through docker

## Answers to Questions

### Who might attack the application?

- Attackers might be interested in seeing the messages that the attacker is not authorized to see
  - Originally there was no access control or no authorization in place
  - Attackers could do whatever they wanted
- Attackers might want to get hold of the users passwords
  - Originally, passwords was stored in the source code in plain text
  - Problematic as users often use same passwords for multiple purposes
  - Attackers could perform some clever SQL injection attacks to see the passwords in plaintext from db
- An attacker might want to trick the system into acting on behalf of another user
  - No validation of passwords. Attacker could simply choose what username to be logged in as
    - Did not even have to log in to send requests to some of the endpoints
  - Originally, user sets the sender (NO INTEGRITY!). An attacker could simply put another username as sender
  - The original application had minimal protection against CSRF. Attacker could use this to trick people into sending unintended messages.
  - Attacker could do session hijacking as the secret key was not secure
- At attacker might want to crash or make the application inaccessible
  - Could perform SQL injection as there was no measures for stopping this
  - Could perform XSS attacks as there was no measures for stopping this
  - Could perform DDOS attakcs as there was no measures for stopping this

#### What damage could be done?

Confidentiality:

- Reading private messages and passwords.

Integrity:

- Sending a message from another users account.
- Tricking a user into sending a message through CSRF

Availability:

- DDOS attack
- Deleting content using injection (SQL or XSS).

### Limits

Originally there was very few limits and and an attacker could do a lot of damage without too much work. Some XSS would have been avoided due to some of the methods that was used to interact with the DOM was safe in terms of XSS. The implementation had a vast amount of security problems which resulted in a very insecure application. In this application there is a lot of input coming from the user, which makes it hard to ensure security across the entire application. We are also limited to protecting against the vulnerarbilities which we have identified, but there might be more that has been overlooked.

### Attack vectors

The original application had several attack vectors

- Injections (SQL, XSS)
- CSRF
- DDOS
- Cryptgraphic failures (No encryption)
- Breaking access control
- Identification and Authentication Failures (Almost no authenticaiton in place)
- Session hijacking
- Insecure design (Messy design with may lead to security flaws like not checking passwords)
- Security misconfiguration (bad secret key, cookie header not set, etc)
- Security Logging and Monitoring Failures (no logging implemented)

### What have you done to protect against attacks?

See [Refactoring to Address the Inital Security Issues](#refactoring-to-address-the-inital-security-issues)

### Access control

Relationship-Based Access Control (ReBAC)

- Users can only view public messages or their own messages (messages from/to the user).

### How can you know that you security is good enough?

It is hard to know if the application is secure enough before deploying it on the internet. We have tried to fix most security issues we know about but there is a high chance that people will find security holes in the application at some point, and possibly exploit them.

We have added some logging (should be a lot more logging in a real-life application). This can be a way of tracing potential security issues that occur.
