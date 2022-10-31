from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField

class MessageForm(FlaskForm):
    recipients = StringField('Recipients')
    message = StringField('Message')
    replyto = HiddenField('Replyto')
