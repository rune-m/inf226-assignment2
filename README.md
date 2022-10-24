# INF226 - Assignment 2+3

## Refactoring

Security issues:

- Secret key should be random. Alternatively be in a seperate environment file.
  - Generated random key
- Users should not be in the source code. Passwords/tokens should be encrypted anyways.
- Easy to perform SQL injections.
  - Fixed with prepared statements
- Navigating via a "next" parameter -> XSS?
  - Value is checked to be safe url
  - User can access all endpoints without being logged in
    - We added message without being logged in
    - Fixed by enforcing that users has to be logged in to use endpoints
  - Cross site request forgery
    - Rune can send Anders a link with parameters for a message and if Anders is authenticated and clicks the link the message will be posted from Anders account
    - Removed next parameter to avoid CSRF
    - Next will remain in the URL, but wont do anything

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
