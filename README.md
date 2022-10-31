# INF226 - Assignment 2+3

# TODO for security stuff:

HTML and JS check to see if there are more XSS stuff
Make sure user initiates all requests: CSRF
Look at cookies. Are all the correct flags set?

## Refactoring

Security issues:

- Secret key should be random. Alternatively be in a seperate environment file.
  - Generated random key
- Users should not be in the source code. Passwords/tokens should be encrypted anyways.
  - Initially, passwords was not even checked and you could log in to whatever account withouth giving any password
- Easy to perform SQL injections.
  - Fixed with prepared statements
- Navigating via a "next" parameter -> XSS?
  - Value is checked to be safe url
  - User can access all endpoints without being logged in
    - We added message without being logged in
    - Fixed by enforcing that users has to be logged in to use endpoints
    - Not necessairy for coffe, favicon and CSS (CSS already available when inspecting the page)
  - Cross site request forgery
    - Rune can send Anders a link with parameters for a message and if Anders is authenticated and clicks the link the message will be posted from Anders account
    - Removed next parameter to avoid CSRF
    - Next will remain in the URL, but wont do anything
- Search function fetches users supplied messages and senders and is added to DOM
  - Could be vulnerable to persistent XSS attack
  - After checking, the output is automatically escaped -> no work done
- When making new endpoints, we have to escape the output to avoid stored XSS

- Some variables are used directly in html

  - Sanitized messages in message.html (must check if there are more
  - Must check all HTML and JS code to see if there are more XSS faults

- Bearer token is not secure as it is not encrypted. A packet sniffer can take token and be authorized on server.

  - Not mentioned in text and hard to test, so this is not fixed

- We have tried to validate all input to enforce the invariants of the domain.
  - Should have made domain primitives but not enough time

Access control:

- Can send messages as anybody
  - Removed "From" input and rather used the currently logged in user id
- No check when fetching messages from db -> everyone can see everything
  - Fixed so that user only sees messages that are sent by the user or to the user
- No check on announcements as they should be seen by all

Improvments of structure:

- Create new files:
  - controller.py
    - This files includes all endpoints for the application.
  - login_manager.py
    - Contains login_manager functions like user_loader() and request_loader()
  - password_utils.py
    - Methods for hashing and verifying passwords
  - utils.py
    - Extra util methods.

app.py now only contains functionality for initializing the application.
