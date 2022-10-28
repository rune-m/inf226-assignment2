from flask import abort, request, send_from_directory, make_response, render_template, Blueprint
import flask
from requests import session
from db_init import initialize_database
from login_form import LoginForm
from apsw import Error
from login_manager import user_loader
from password_utils import check_password
from flask_login import current_user, login_required, login_user, logout_user
from apsw import Error
from pygments.formatters import HtmlFormatter
from db_service import get_all_messages, get_announcements, get_credentials, search_messages, send_message, get_message
from input_validator import valid_username

conn = initialize_database()
cssData = HtmlFormatter(nowrap=True).get_style_defs('.highlight')
endpoints = Blueprint('endpoints', __name__)

@endpoints.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(endpoints.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@endpoints.route('/favicon.png')
def favicon_png():
    return send_from_directory(endpoints.root_path, 'favicon.png', mimetype='image/png')


@endpoints.route('/oldMessages')
@endpoints.route('/index.html')
@login_required
def index_html():
    return send_from_directory(endpoints.root_path,
                        'index.html', mimetype='text/html')

@endpoints.route('/')
@endpoints.route('/message')
@endpoints.route('/message.html')
@login_required
def message_html():
    return send_from_directory(endpoints.root_path,
                        'message.html', mimetype='text/html')

@endpoints.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)
    if form.validate_on_submit():
        username = form.username.data
        if not valid_username(username):
            return render_template('./login.html', form=form)
        password = form.password.data
        u = get_credentials(username)
        if u and check_password(u["password"], password, u["salt"]):
            user = user_loader(username)
            
            # automatically sets logged in session cookie
            login_user(user)

            flask.flash('Logged in successfully.')
            
            return flask.redirect(flask.url_for('endpoints.message_html'))
    return render_template('./login.html', form=form)

@endpoints.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect('/')

@endpoints.get('/search')
@login_required
def search():
    query = request.args.get('q') or request.form.get('q') or '*'
    try:
        result = search_messages(query)
        return result
    except Error as e:
        return (f'{result}ERROR: {e}', 500)

@endpoints.route('/send', methods=['POST','GET'])
@login_required
def send():
    try:
        sender = request.args.get('sender') or request.form.get('sender')
        message = request.args.get('message') or request.args.get('message')
        if not sender or not message:
            return f'ERROR: missing sender or message'
        result = send_message(sender, message, '*', None)
        return f'{result}ok'
    except Error as e:
        return f'{result}ERROR: {e}'

@endpoints.route('/new', methods=['POST'])
@login_required
def new_message():
    try:
        sender = request.args.get('sender') or request.form.get('sender')
        message = request.args.get('message') or request.form.get('message')

        if not sender or not message:
            return f'ERROR: missing sender or message'

        recipient = (request.args.get('recipients') or request.form.get('recipients')) or '*'
        reply_to = request.args.get('reply_to') or request.form.get('reply_to')
        
        # TODO: Split recipients and send one message to each

        result = send_message(sender, message, recipient, reply_to)
        return f'{result}ok'
    except Error as e:
        return f'{result}ERROR: {e}'

@endpoints.route('/messages', methods=['GET'])
@login_required
def all_messages():
    try:
        user_id = current_user.id
        result = get_all_messages(user_id)
        return result
    except Error as e:
        return f'{result}ERROR: {e}'

@endpoints.route('/messages/<int:message_id>', methods=['GET'])
@login_required
def message(message_id):
    id = message_id
    user_id = current_user.id
    message = get_message(id, user_id)
    return message

@endpoints.get('/announcements')
@login_required
def announcements():
    try:
        return get_announcements()
    except Error as e:
        return {'error': f'{e}'}

@endpoints.get('/coffee/')
def nocoffee():
    abort(418)

@endpoints.route('/coffee/', methods=['POST','PUT'])
def gotcoffee():
    return "Thanks!"

@endpoints.get('/highlight.css')
def highlightStyle():
    resp = make_response(cssData)
    resp.content_type = 'text/css'
    return resp