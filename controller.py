from flask import abort, request, send_from_directory, make_response, render_template, Blueprint
import flask
from db_init import initialize_database
from login_form import LoginForm
from apsw import Error
from login_manager import user_loader
from password_utils import check_password
from flask_login import login_required, login_user, logout_user
from apsw import Error
from pygments.formatters import HtmlFormatter
from db_service import get_announcements, get_credentials, search_messages, send_message

conn = initialize_database()
cssData = HtmlFormatter(nowrap=True).get_style_defs('.highlight')
endpoints = Blueprint('endpoints', __name__)

@endpoints.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(endpoints.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@endpoints.route('/favicon.png')
def favicon_png():
    return send_from_directory(endpoints.root_path, 'favicon.png', mimetype='image/png')


@endpoints.route('/')
@endpoints.route('/index.html')
@login_required
def index_html():
    return send_from_directory(endpoints.root_path,
                        'index.html', mimetype='text/html')

@endpoints.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        print(f'Received form: {"invalid" if not form.validate() else "valid"} {form.form_errors} {form.errors}')
        print(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = get_credentials(username)
        if u and check_password(u["password"], password, u["salt"]):
            user = user_loader(username)
            
            # automatically sets logged in session cookie
            login_user(user)

            flask.flash('Logged in successfully.')
            
            return flask.redirect(flask.url_for('endpoints.index_html'))
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
        result = send_message(sender, message)
        return f'{result}ok'
    except Error as e:
        return f'{result}ERROR: {e}'

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