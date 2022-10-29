import string

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
    return valid_username(reply_to)

#TODO: Should validate that the string is legal list of recipients (should call "valid_recipient")
def valid_recipients(recipients):
    return True