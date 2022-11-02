import string
import re

def valid_username(username):
    if not (len(username) >=3 and len(username) <=25):
        return False

    match= string.ascii_letters + string.digits + '-'
    if not all([x in match for x in username]):
        return False
    
    return True

def valid_message(message):
    if not (len(message) >=0 and len(message) <= 160):
        return False
    return message.isprintable()

def valid_recipient(recipient):
    return valid_username(recipient)

def valid_sender(sender):
    return valid_username(sender)

def valid_reply_to(reply_to):
    return reply_to.isdigit() or reply_to == ''

def valid_recipients(recipients):
    recipients_list = recipients.split(' ')
    for recipient in recipients_list:
        if not valid_recipient(recipient):
            return False
    return True

def valid_password(password):
    # At least: 8 characters, one uppercase letter, one lowercase letter, one number
    return re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password)
