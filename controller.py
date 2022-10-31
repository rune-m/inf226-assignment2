from flask import abort, redirect, request, send_from_directory, make_response, render_template, Blueprint
import flask
from requests import session
from db_init import initialize_database
from flmessage_form import MessageForm
from login_form import LoginForm
from apsw import Error
from login_manager import user_loader
from password_utils import check_password
from flask_login import current_user, login_required, login_user, logout_user
from apsw import Error
from pygments.formatters import HtmlFormatter
from db_service import create_user, get_all_messages, get_announcements, get_credentials, search_messages, send_message, get_message
from input_validator import valid_username, valid_message, valid_recipients, valid_reply_to, valid_sender

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


@endpoints.route('/message')
@endpoints.route('/message.html')
@login_required
def message_html():
    return send_from_directory(endpoints.root_path,
                        'message.html', mimetype='text/html')

@endpoints.route('/', methods=['GET', 'POST'])
@endpoints.route('/flmessage', methods=['GET', 'POST'])
@login_required
def flmessage_html():
    form = MessageForm()
    if form.validate_on_submit():
        try:
            sender = current_user.id
            print("sender", sender)
            message = request.form.get('message')
            print("message", message)
            reply_to = request.form.get('replyto')
            print("reply to", reply_to)

            if not message:
                # return f'ERROR: missing message'
                # return render_template("./flmessage.html", form=form), 400
                # abort(400, 'bad req')
                print('missing message')
                return redirect(request.url)

            if not valid_sender(sender) or not valid_message(message) or not valid_reply_to(reply_to):
                # return f'ERROR: invalid sender, message or reply'
                print(f'ERROR: invalid sender, message or reply')
                return redirect(request.url)
            
            recipients = request.form.get('recipients')
            if recipients == None or recipients.strip() == '':
                send_message(sender, message, '*', reply_to)
                return redirect(request.url)
            if not valid_recipients(recipients):
                # return f'ERROR: Not valid recipients'
                print('No valid recipients')
                return redirect(request.url)
            else:
                recipients_list = dict.fromkeys(recipients.split(' '))
                for recipient in recipients_list:
                    send_message(sender, message, recipient, reply_to)
                return redirect(request.url)
        except Error as e:
            return f'ERROR: {e}'
    return render_template('./flmessage.html', form=form)

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
            
            # TODO: Endre url til ny page
            return flask.redirect(flask.url_for('endpoints.message_html'))
    return render_template('./login.html', form=form)

@endpoints.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)
    if form.validate_on_submit():
        username = form.username.data
        if not valid_username(username):
            return render_template('./register.html', form=form)
        password = form.password.data
        u = get_credentials(username)
        if u == None:
            try:
                create_user(username, password)
            except:
                return render_template('./register.html', form=form)

            user = user_loader(username)
            
            # automatically sets logged in session cookie
            login_user(user)

            flask.flash('Registered successfully.')
            
            return flask.redirect(flask.url_for('endpoints.message_html'))
    return render_template('./register.html', form=form)

@endpoints.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect('/')

@endpoints.get('/search')
@login_required
def search():
    query = request.args.get('q') or request.form.get('q') or '*'
    user_id = current_user.id
    try:
        result = search_messages(query, user_id)
        return result
    except Error as e:
        return (f'{result}ERROR: {e}', 500)

@endpoints.route('/send', methods=['POST','GET'])
@login_required
def send():
    try:
        sender = current_user.id
        message = request.args.get('message') or request.args.get('message')
        if not sender or not message:
            return f'ERROR: missing sender or message'
        if not valid_sender(sender) or not valid_message(message):
            return f'ERROR: invalid sender or message'
        result = send_message(sender, message, '*', None)
        return f'{result}ok'
    except Error as e:
        return f'{result}ERROR: {e}'

@endpoints.route('/new', methods=['POST'])
@login_required
def new_message():
    try:
        sender = current_user.id
        message = request.args.get('message') or request.form.get('message')
        reply_to = request.args.get('reply_to') or request.form.get('reply_to')

        if not message:
            return f'ERROR: missing message'

        if not valid_sender(sender) or not valid_message(message) or not valid_reply_to(reply_to):
            return f'ERROR: invalid sender, message or reply'
        
        recipients = request.args.get('recipients') or request.form.get('recipients')
        if recipients == None or recipients.strip() == '':
            send_message(sender, message, '*', reply_to)
            return 'ok'
        if not valid_recipients(recipients):
            return f'ERROR: Not valid recipients'
        else:
            recipients_list = dict.fromkeys(recipients.split(' '))
            for recipient in recipients_list:
                send_message(sender, message, recipient, reply_to)
        return f'ok'
    except Error as e:
        return f'ERROR: {e}'

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